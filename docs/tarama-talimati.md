# Kampanya tarama talimatı (zamanlanmış görevler için)

Bu dosya, kullanıcının (İbrahim Samet Gündüz) Finans uygulamasını besleyen zamanlanmış tarama görevlerinin ortak talimatıdır. Her görev kendine verilen **ALAN** için bu adımları uygular. Görev sırasında kimse soru cevaplamaz; belirsizlikte makul varsayım yap ve kayda not düş. Tüm metinler Türkçe.

Amaç: Türkiye'de geçerli, kullanıcının yararlanabileceği **tüm** kampanya ve ek gelir fırsatlarını kaçırmadan yakalamak. Az ama emin olmak yerine **kapsamlı + doğru etiketli** olmak esastır: teyit edilemeyen ama makul fırsat da eklenir, `teyitsiz: true` işaretlenir.

## 1. Hazırlık
1. `mcp__claude-code-remote__add_repo` ile `samyeli-max/finans-veri` deposunu `access: "push"` ile ekle, verdiği komutla klonla.
2. `kaynaklar.json`, `parcalar/<ALAN>.json` (varsa, bir önceki taramanın sonucu) ve `kapsama/<ALAN>.json` (varsa) dosyalarını oku. Önceki kapsamada `durum` değeri `taranmadi` ya da `ulasilamadi` olan kaynakları not et: bu taramada **önce** onlar ele alınır (bkz. §4 bütçe kuralı).

## 2. Uygunluk etiketleri
- Kredi kartı gerektirenler → `kredi-karti`. Belirli bir operatör hattı gerektirenler (ör. Vodafone) → `kontrol`.
- Yeni müşteri kampanyalarını her kurum için eksiksiz topla ve `uygunluk: "yeni-musteri"` yaz. "Hesabın var mı / yeni müşteri mi" kararını sen verme ve herhangi bir hesap listesi arama: bu karar uygulamada, kullanıcının telefonunda verilir. Sen yalnız kampanyayı doğru etiketle. Birleştirme betiği her kampanyaya kurumun bilinen adlarını (`ka`) ekler.

## 3. Kapsam dışı (hiç ekleme)
- **Geleneksel (mevduat) bankalarının faizli fırsatları:** hoş geldin faizi, yüksek/vadeli mevduat faizi, günlük kazandıran hesap faizi, faizli/düşük faizli kredi ve ek hesap. (Katılım bankalarının kâr payı fırsatları ve **faizsiz** kredi/taksit/nakit avans kampanyaları kapsam içindedir.) Birleştirme betiği de bunları süzer ama baştan ekleme.
- Bitmiş kampanyalar, kişisel davet/referans kodları, kumar/bahis, kesinliği olmayan söylentiler, kişisel veri.

## 4. Araştırma yöntemi (ALAN'a göre)
- `kaynaklar.json` → `alanlar.<ALAN>` listesindeki **her** kurumu gez: resmi kampanya sayfası (url), kurumun "kampanyalar / fırsatlar / arkadaşını getir / yeni müşteri" sayfaları, mobil uygulama mağaza açıklamaları. URL çalışmıyorsa doğrusunu bul ve `kaynaklar.json`'da düzelt; listede olmayan ama bu alana giren yeni bir kurum/platform bulursan ekle.
- Derleme siteleri (`kaynaklar.json` → `derleme`) ve haber siteleri bu alana ait yeni kampanyaları bulmak için taranır; bulunan bilgi mümkünse resmi sayfadan teyit edilir.
- ALAN = `sosyal`: forumlar (`forum`), sosyal medya (`sosyal.aramalar` kalıplarıyla arama motoru üzerinden X/Instagram/Telegram/YouTube içerikleri), derleme siteleri ve "son gün", "yeni kampanya", "arkadaşını getir", "bedava", "nakit iade" gibi aramalar. Tüm alanlardan **yeni çıkan** ve **son günü yaklaşan** fırsatları yakala. Giriş gerektiren içerik okunamaz; arama sonuçlarındaki bilgi resmi sayfadan teyit edilmezse `teyitsiz`.
  - **Forumlarda yalnız arama motoruna güvenme** (arama dizini Türkçe forumların son günlerini çoğu zaman kapsamaz; `site:` araması boş dönebilir). Her forumun kampanya bölümünü ya da ilgili başlığını sayfa okuma aracıyla **doğrudan aç** ve en yeni konulara/mesajlara bak: DonanımHaber "Banka-Kredi Kartı Fırsatları" (f2119) ve "Sıcak Fırsatlar" (f2118) bölümleri ile banka ana konuları; Technopat Sosyal ve ShiftDelete forumunun kampanya/fırsat bölümleri; R10 ve DonanımArşivi'nin kampanya bölümleri; Ekşi Sözlük'te kampanya başlıkları (ör. "banka kampanyaları", "<kurum> kampanyası"); Reddit'te ilgili alt forumların (r/Turkey, r/KGBTR, r/TurkeyJerky, r/BorsaIstanbul vb.) en yeni gönderileri. Ana sayfa açılmazsa bölüm ya da başlık adresini dene.
  - Bir kaynağı `ulasilamadi` saymadan önce hem aramayı hem doğrudan açmayı dene; ikisi de olmazsa sebebini kapsamaya yaz (bkz. §5).
- Her kampanya için başlangıç/bitiş tarihini bulmaya çalış; bulunamazsa null (uydurma). Koşulları (SMS kodu, katıl butonu, min. harcama, kart türü, yeni müşteri şartı) kısa yaz. Forum ipuçlarını ("banka kartıyla da çalışıyor", "ödül gecikiyor") koşula ekle.
- **Abonelik ve fatura iadeleri (her alan kendi kurumlarında arar, özellikle bankalar / fintech / alisveris):** uygulama, kullanıcının aboneliği yaklaşınca "bu ay en çok iade veren ödeme aracı"nı bu kampanyalardan seçer. O yüzden şu türleri eksiksiz topla: Netflix, Spotify, YouTube Premium, Disney+, Amazon Prime, Apple (iCloud/Music/App Store), Google Play/One, Exxen, BluTV/Max, TOD, Gain, Tabii, ChatGPT/OpenAI, Microsoft/Xbox, PlayStation, Steam, Storytel, Duolingo; dijital oyun/uygulama mağazası ödemeleri; elektrik, doğalgaz, su, internet, mobil hat **fatura** ödemeleri ve otomatik ödeme talimatı iadeleri. `kampanya` metninde platform adını **açıkça** yaz (ör. "Netflix ödemelerine %20 iade") ve `fayda`'yı hesaplanabilir yaz ("%20, en fazla 100 TL" / "50 TL iade"). Harcama kampanyalarına (puan, iade, indirim) `etiketler` dizisi ekle; uygulama "bu harcamayı hangi araçla yapayım" önerisini önce bu etiketlerle eşleştirir. **Yalnız şu sözlükten** seç (birden çok olabilir): kategori → `market`, `yeme` (restoran/kafe/yemek siparişi), `akaryakit`, `ulasim` (toplu taşıma, taksi, otopark, HGS), `fatura` (elektrik, doğalgaz, su, internet, GSM), `abonelik` (dijital platform/üyelik), `eticaret`, `elektronik`, `giyim` (giyim/ayakkabı/kozmetik), `saglik` (eczane/hastane/optik), `egitim`, `seyahat` (uçak/otel/otobüs), `eglence` (sinema/konser/oyun), `kira`, `tum-harcamalar` (kategori ayırmayan genel harcama kampanyası); platform/marka → küçük harf tek kelime: `netflix`, `spotify`, `youtube`, `disney`, `amazon`, `apple`, `google`, `exxen`, `blutv`, `tod`, `gain`, `tabii`, `chatgpt`, `migros`, `a101`, `bim`, `sok`, `carrefoursa`, `trendyol`, `hepsiburada`, `getir`, `yemeksepeti`, `opet`, `shell`, `po`, `starbucks` vb. Örnek: `["abonelik","netflix"]`, `["market","migros"]`, `["fatura"]`.
- Hedef sayısı yok; alanı tükenene kadar tara. Arama/okuma bütçesini kaynak listesine dengeli dağıt. Sıra: (1) önceki kapsamada `taranmadi` olanlar, (2) önceki kapsamada `ulasilamadi` olanlar (bir kez daha dene; sebep robots ise ve yine engelliyse geç), (3) resmi sayfalar, (4) derleme, (5) serbest arama. Bütçe ya da zaman biterse hiç denenmemiş kaynakları kapsamaya `taranmadi` yaz ki bir sonraki tarama onlarla başlasın.

## 5. Çıktı biçimi
`parcalar/<ALAN>.json` dosyasını **baştan yaz** (bu alanın güncel tam listesi; önceki dosyadaki hâlâ geçerli kampanyaları yeniden doğrulayıp koru):

```json
{"alan": "<ALAN>", "tarih": "YYYY-MM-DD", "kampanyalar": [
  {"kurum": "...", "kampanya": "...", "tur": "...", "fayda": "...",
   "baslangic": "YYYY-MM-DD" | null, "bitis": "YYYY-MM-DD" | null,
   "kosul": "...", "teyitsiz": true/false,
   "uygunluk": "uygun" | "kontrol" | "yeni-musteri" | "kredi-karti" | "maas-emekli",
   "link": "https://..." | null, "oneCikan": true/false, "kaynak": "resmi|derleme|forum|sosyal|haber",
   "etiketler": ["abonelik", "netflix"]  // isteğe bağlı, sözlükten
]}
```
- `tur` değerlerinden biri: puan, cashback, indirim, faizsiz taksit, faizsiz kredi, arkadaşını getir, yeni müşteri bonusu, kripto bonus, çekiliş, BES ek katkı, emekli promosyonu, ücretsiz hizmet, komisyon indirimi, anket/görev, satış platformu, diğer.
- `oneCikan: true`: yüksek değerli (≈500 TL üstü net kazanç), ücretsiz ya da 7 gün içinde biten ve `uygun`/`yeni-musteri` olanlar.
- `id` yazma; betik `kurum|kampanya`'dan üretir. Aynı kampanyayı farklı adla tekrar yazma; kurum adını `kaynaklar.json`'daki gibi yaz.

`kapsama/<ALAN>.json`: `{"alan": "...", "tarih": "YYYY-MM-DD", "kaynaklar": [{"ad": "...", "url": "...", "durum": "ok|ulasilamadi|kampanya-yok|taranmadi", "sebep": "...", "bulunan": 0}], "not": "..."}`
- `ok`: tarandı, kampanya bulundu. `kampanya-yok`: tarandı, yeni/uygun kampanya yok.
- `ulasilamadi`: denendi ama okunamadı (arama da doğrudan açma da sonuçsuz). `sebep` zorunlu, şunlardan biri: `robots` (site botları engelliyor), `site-hatasi`, `onay-zaman-asimi` (alan adı onay bekledi, kimse onaylamadı), `giris-gerekli`, `arama-sonucsuz`.
- `taranmadi`: bütçe/zaman yetmediği için hiç denenmedi. Bir sonraki taramada önce bunlara bakılır.

## 6. Birleştir ve gönder
1. Depo kökünde `python3 scripts/birlestir.py` çalıştır. "OK" yazmalı; hata verirse parça dosyasını düzelt ve tekrarla.
2. `git add -A && git commit -m "Tarama: <ALAN> GG.AA.YYYY (+N yeni)"`.
3. `git pull --rebase` → çakışma `kampanyalar.json`'daysa betiği yeniden çalıştırıp çakışmayı onun çıktısıyla çöz → `git push`. Push 3 denemede olmazsa `parcalar/<ALAN>.json`'u `/mnt/user-data/outputs/` altına kaydedip SendUserFile ile gönder.
4. Kısa bitiş mesajı: alan, kaç kampanya (kaç yeni), kapsama özeti (kaç kaynak ok / ulaşılamadı (sebepleriyle) / taranmadı), en önemli 3 yeni fırsat (son tarihleriyle), push durumu.

## 7. Yalnız `yatirim` alanı: TÜFE serisini güncel tut
Uygulama reel getiriyi `tufe.json`'daki aylık TÜFE değişimleriyle hesaplar. Her `yatirim` taramasında:
1. `tufe.json`'daki `son_ay`'dan sonra TÜİK'in açıkladığı ay var mı bak (TÜİK her ayın 3'ünde saat 10:00'da açıklar). Kaynak: TCMB "Tüketici Fiyatları" tablosu (tcmb.gov.tr › İstatistikler › Enflasyon Verileri) ya da TÜİK bülteni; en az iki kaynakta aynı rakamı gör.
2. Yeni ay varsa `aylik["YYYY-AA"]` = aylık % değişim, `yillik["YYYY-AA"]` = yıllık % değişim (ondalık nokta ile, ör. 2.58) ekle; `son_ay` ve `guncelleme`yi yaz. Eski değerlere dokunma.
3. Kontrol: son 12 aylık değerin bileşiği ((1+a1/100)×…×(1+a12/100)−1)×100 ile yeni yıllık değer arasındaki fark 0,6 puandan büyükse ekleme yapma, raporda belirt.
4. Kampanya dosyalarıyla aynı commit'te gönder.

## Görev takvimi
| ALAN | İçerik | Ne zaman |
|---|---|---|
| bankalar | katılım + mevduat + dijital bankalar, kart programları (faizli fırsatlar hariç) | Pzt, Per |
| fintech | e-cüzdan, ödeme kuruluşları, dijital cüzdanlar | Sal, Cum |
| yatirim | kripto platformları, BES/sigorta, aracı kurumlar | Çar, Cmt |
| alisveris | sadakat/fiş/cashback uygulamaları, e-ticaret, telekom, seyahat ortak kampanyaları | Pzt, Per |
| ekgelir | arkadaşını getir, yeni müşteri bonusları, anket/görev uygulamaları, satış ve freelance platformları | Sal, Cum, Paz |
| sosyal | forum + sosyal medya + derleme siteleri: tüm alanlarda yeni ve son günü yaklaşanlar | Her gün |
| (rapor) | kampanyalar.json + kapsama'dan haftalık Doküman + Excel | Pzt |
