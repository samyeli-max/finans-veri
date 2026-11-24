# finans-veri

Finans uygulamasının internetten okuduğu veri dosyaları. Kişisel veri içermez; yalnızca herkese açık kampanya bilgileri.

- `kampanyalar.json` — uygulamanın okuduğu birleşik liste (6 saatte bir çekilir). Elle düzenleme; `scripts/birlestir.py` üretir.
- `parcalar/<alan>.json` — alan taramalarının sonuçları (bankalar, fintech, yatirim, alisveris, ekgelir, sosyal).
- `kapsama/<alan>.json` — hangi kaynakların tarandığı / ulaşılamadığı.
- `kaynaklar.json` — taranacak kurumlar, resmi kampanya sayfaları, derleme siteleri, forumlar, sosyal medya aramaları.
- `docs/tarama-talimati.md` — zamanlanmış tarama görevlerinin ortak talimatı ve takvimi.

Birleştirme kuralları (scripts/birlestir.py): biten kampanyalar ve 21 günden eski belirsiz tarihliler çıkar, geleneksel bankaların faizli fırsatları süzülür, aynı kampanya birleştirilir, ilk görülme günü (`eklenme`) korunur.
