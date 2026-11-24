#!/usr/bin/env python3
"""Alan taramalarının parçalarını (parcalar/*.json) tek kampanyalar.json'da birleştirir.

Kurallar
- Bitiş tarihi geçmiş kampanyalar çıkar.
- Bitiş tarihi belirsiz kampanya, parçası 21 günden eskiyse çıkar (kimse yeniden görmemiş demek).
- Geleneksel (mevduat) bankalarının faizli fırsatları çıkar: hoş geldin faizi, yüksek mevduat faizi, faizli kredi.
  Katılım bankaları ve faizsiz fırsatlar kalır. Banka türü kaynaklar.json'dan okunur.
- Aynı kampanya birden fazla parçada varsa birleşir (id → aynı kurum+link → aynı kurum+bitiş+benzer başlık).
  En yeni parçadaki kayıt esas alınır, boş alanları diğerinden tamamlanır.
- "eklenme": kampanyanın ilk görüldüğü gün; önceki kampanyalar.json'dan korunur.

Kullanım: python3 scripts/birlestir.py [--bugun YYYY-MM-DD]   (depo kökünde çalıştır)
Çıkış kodu 0 değilse doğrulama hatası vardır; kampanyalar.json yazılmaz.
"""
import hashlib
import json
import re
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UYGUNLUK = {"uygun", "kontrol", "yeni-musteri", "kredi-karti", "maas-emekli"}
UYGUNLUK_METNI = {"uygun": "Uygun", "kontrol": "Kontrol et", "yeni-musteri": "Yeni müşteri şartı",
                  "kredi-karti": "Kredi kartı gerekir", "maas-emekli": "Maaş/emekli şartı"}
FAIZLI_TUR = {"hoş geldin faizi", "yüksek mevduat faizi", "mevduat faizi", "düşük faizli kredi", "faizli kredi"}
FAIZ_KELIME = re.compile(r"(hoş ?geldin faiz|mevduat faiz|yüksek faiz|faiz oranı|%\s*\d+[.,]?\d*\s*faiz|vadeli mevduat|günlük kazandıran|gecelik faiz)", re.I)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
GENEL_LINK = re.compile(r"/(kampanyalar|campaigns|firsatlar|kampanya)/?$", re.I)


def fold(s: str) -> str:
    s = (s or "").replace("ı", "i").replace("İ", "I")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def kid(kurum: str, kampanya: str) -> str:
    return hashlib.sha1(f"{kurum}|{kampanya}".encode()).hexdigest()[:10]


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def banka_turleri() -> dict:
    """kurum adı (katlanmış) → tip (katilim / mevduat / ...)"""
    out = {}
    p = ROOT / "kaynaklar.json"
    if not p.exists():
        return out
    for alan in load(p).get("alanlar", {}).values():
        for k in alan:
            for ad in [k["kurum"], *k.get("diger_adlar", [])]:
                out[fold(ad)] = k.get("tip", "")
    return out


def alias_gruplari() -> list:
    """kaynaklar.json'daki kurum + diğer adları (katlanmış) gruplar halinde. Kişisel bilgi içermez."""
    k = ROOT / "kaynaklar.json"
    out = []
    if k.exists():
        for alan in load(k).get("alanlar", {}).values():
            for x in alan:
                out.append({fold(a) for a in [x["kurum"], *x.get("diger_adlar", [])] if fold(a)})
    return out


def kurum_anahtarlari(kurum: str, gruplar: list) -> list:
    """Kampanyanın kurumunu tanıyan katlanmış adlar. Uygulama bunları kullanıcının kendi (telefondaki)
    hesap listesiyle karşılaştırır; 'hesabın var mı / yeni müşteri mi' kararı telefonda verilir, burada değil."""
    parcalar = {fold(p) for p in re.split(r"[/(),]", kurum) if fold(p)} | {fold(kurum)}
    out = set(parcalar)
    for g in gruplar:
        if g & parcalar:
            out |= g
    return sorted(out)


def geleneksel_banka(kurum: str, tipler: dict) -> bool:
    f = fold(kurum)
    tip = tipler.get(f)
    if tip is None:  # "Ziraat Bankası / Bankkart" gibi
        tip = next((t for ad, t in tipler.items() if ad and (f.startswith(ad) or ad.startswith(f))), "")
    return tip == "mevduat"


def faizli(c: dict, tipler: dict) -> bool:
    if not geleneksel_banka(c["kurum"], tipler):
        return False
    if "faizsiz" in fold(c.get("tur", "")) or "faizsiz" in fold(c.get("kampanya", "")):
        return False
    if c.get("tur", "").lower() in FAIZLI_TUR:
        return True
    return bool(FAIZ_KELIME.search(f"{c.get('kampanya', '')} {c.get('fayda', '')}"))


def normalize(c: dict, parca_tarih: str, alan: str) -> dict:
    c = dict(c)
    c["kurum"] = c["kurum"].strip()
    c["kampanya"] = re.sub(r"\s+", " ", c["kampanya"]).strip()
    c["id"] = c.get("id") or kid(c["kurum"], c["kampanya"])
    for k in ("baslangic", "bitis"):
        v = c.get(k)
        c[k] = v if isinstance(v, str) and DATE_RE.match(v) else None
    kosul = (c.get("kosul") or "").strip()
    if kosul.startswith("(teyitsiz)"):
        kosul = kosul[len("(teyitsiz)"):].strip()
        c["teyitsiz"] = True
    c["kosul"] = kosul
    c["teyitsiz"] = bool(c.get("teyitsiz")) or "teyit edilemedi" in kosul.lower()
    if c.get("uygunluk") not in UYGUNLUK:
        c["uygunluk"] = "kontrol"
    c["uygunlukMetni"] = c.get("uygunlukMetni") or UYGUNLUK_METNI[c["uygunluk"]]
    c["link"] = c.get("link") or None
    c["oneCikan"] = bool(c.get("oneCikan"))
    c["fayda"] = (c.get("fayda") or "").strip()
    c["tur"] = (c.get("tur") or "diğer").strip().lower()
    c["alan"] = c.get("alan") or alan
    et = c.get("etiketler")
    if isinstance(et, list):
        et = [str(x).strip().lower() for x in et if str(x).strip()]
        c["etiketler"] = sorted(set(et)) or None
    else:
        c.pop("etiketler", None)
    if not c.get("etiketler"):
        c.pop("etiketler", None)
    c["_parca_tarih"] = parca_tarih
    return c


def baslik_benzer(a: str, b: str) -> bool:
    ta, tb = set(fold(a).split()), set(fold(b).split())
    if not ta or not tb:
        return False
    return len(ta & tb) / min(len(ta), len(tb)) >= 0.7


def birlestir(kayitlar: list) -> list:
    """Aynı kampanyaları birleştir; en yeni parça esas."""
    kayitlar = sorted(kayitlar, key=lambda c: c["_parca_tarih"], reverse=True)
    out: list = []
    for c in kayitlar:
        hit = None
        for o in out:
            if o["id"] == c["id"]:
                hit = o
            elif fold(o["kurum"]) == fold(c["kurum"]):
                if c["link"] and o["link"] == c["link"] and not GENEL_LINK.search(c["link"]):
                    hit = o
                elif o["bitis"] == c["bitis"] and baslik_benzer(o["kampanya"], c["kampanya"]):
                    hit = o
            if hit:
                break
        if hit:
            for k, v in c.items():
                if hit.get(k) in (None, "", False) and v not in (None, ""):
                    hit[k] = v
            hit["oneCikan"] = hit["oneCikan"] or c["oneCikan"]
            hit.setdefault("_ids", set()).add(c["id"])
        else:
            out.append(c)
    return out


def main(argv):
    bugun = date.today().isoformat()
    if "--bugun" in argv:
        bugun = argv[argv.index("--bugun") + 1]
    eski_tarih = (date.fromisoformat(bugun) - timedelta(days=21)).isoformat()
    tipler = banka_turleri()
    gruplar = alias_gruplari()

    onceki = {}
    hedef = ROOT / "kampanyalar.json"
    if hedef.exists():
        for c in load(hedef).get("kampanyalar", []):
            onceki[c["id"]] = c.get("eklenme")

    kayitlar, hatalar, cikan = [], [], {"biten": 0, "eski": 0, "faizli": 0}
    for p in sorted((ROOT / "parcalar").glob("*.json")):
        d = load(p)
        pt = d.get("tarih")
        if not (isinstance(pt, str) and DATE_RE.match(pt)):
            hatalar.append(f"{p.name}: 'tarih' YYYY-MM-DD olmalı")
            continue
        for i, c in enumerate(d.get("kampanyalar", [])):
            if not c.get("kurum") or not c.get("kampanya"):
                hatalar.append(f"{p.name}[{i}]: kurum/kampanya eksik")
                continue
            c = normalize(c, pt, p.stem)
            if c["bitis"] and c["bitis"] < bugun:
                cikan["biten"] += 1
                continue
            if not c["bitis"] and pt < eski_tarih:
                cikan["eski"] += 1
                continue
            if faizli(c, tipler):
                cikan["faizli"] += 1
                continue
            c.pop("musteri", None)
            c.pop("yeniMusteri", None)
            c["ka"] = kurum_anahtarlari(c["kurum"], gruplar)
            kayitlar.append(c)

    if hatalar:
        print("HATA:\n" + "\n".join(hatalar[:30]))
        return 1

    sonuc = birlestir(kayitlar)
    for c in sonuc:
        ilk = [onceki.get(i) for i in {c["id"], *c.pop("_ids", set())} if onceki.get(i)]
        if isinstance(c.get("eklenme"), str) and DATE_RE.match(c["eklenme"]):
            ilk.append(c["eklenme"])
        c["eklenme"] = min(ilk) if ilk else bugun
        c.pop("_parca_tarih", None)
    sonuc.sort(key=lambda c: (not c["oneCikan"], c["bitis"] or "9999", fold(c["kurum"])))
    ids = [c["id"] for c in sonuc]
    if len(ids) != len(set(ids)):
        print("HATA: tekrar eden id")
        return 1
    if not sonuc:
        print("HATA: hiç kampanya yok, yazılmadı")
        return 1

    g, a, y = bugun[8:10], bugun[5:7], bugun[0:4]
    out = {"kaynak": f"Kampanya taraması – {g}.{a}.{y}", "tarih": bugun, "kampanyalar": sonuc}
    hedef.write_text(json.dumps(out, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    yeni = sum(1 for c in sonuc if c["eklenme"] == bugun)
    print(f"OK: {len(sonuc)} kampanya ({yeni} yeni) · çıkarılan: {cikan['biten']} biten, {cikan['eski']} eskimiş, {cikan['faizli']} faizli (geleneksel banka)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
