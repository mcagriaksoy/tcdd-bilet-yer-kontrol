TCDD bilet yer kontrol programi sayesinde tcdd sitesine surekli girmek zorunda kalmadan, ayarlayacaginiz periyotlarla websitesinden bilet yer durumunu ogrenebilmeniz saglanmistir.

<a href="https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=mcagriaksoy&message=tcdd-bilet-yer-kontrol&color=blue&logo=github" alt="mcagriaksoy - tcdd-bilet-yer-kontrol"></a>
<a href="https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/releases/"><img src="https://img.shields.io/github/tag/mcagriaksoy/tcdd-bilet-yer-kontrol?include_prereleases=&sort=semver&color=blue" alt="GitHub tag"></a>
<a href="#license"><img src="https://img.shields.io/badge/License-MIT-blue" alt="License"></a>
<a href="https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/issues"><img src="https://img.shields.io/github/issues/mcagriaksoy/tcdd-bilet-yer-kontrol" alt="issues - tcdd-bilet-yer-kontrol"></a>
[![OS - Linux](https://img.shields.io/badge/OS-Linux-blue?logo=linux&logoColor=white)](https://www.linux.org/ "Go to Linux homepage")
[![Hosted with GH Pages](https://img.shields.io/badge/Hosted_with-GitHub_Pages-blue?logo=github&logoColor=white)](https://pages.github.com/ "Go to GitHub Pages homepage")
[![OS - Windows](https://img.shields.io/badge/OS-Windows-blue?logo=windows&logoColor=white)](https://www.microsoft.com/ "Go to Microsoft homepage")

<a href="https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol"><img src="https://img.shields.io/github/stars/mcagriaksoy/tcdd-bilet-yer-kontrol?style=social" alt="stars - tcdd-bilet-yer-kontrol"></a>
<a href="https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol"><img src="https://img.shields.io/github/forks/mcagriaksoy/tcdd-bilet-yer-kontrol?style=social" alt="forks - tcdd-bilet-yer-kontrol"></a>

## Indir

[![Download - v2.3](https://img.shields.io/static/v1?label=Download&message=v2.2.1&color=2ea44f)](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/releases/download/v2.2.1/TCDD.Bilet.Bulma.Botu.v2.2.1.zip)

## Versionlar
v2.3
Bir Edge webdriver sorunu cozuldu.
Webdriver artik sayfanin yuklenmesini daha cok bekliyor.
Koltuk sayisini bulan regex algoritmasi yeniden yazildi.
UI tarafi:
    - Artik kullanici saati 17,30 17.30 veya 17:30 cinsinde girebiliyor.
    - Ayni sekilde tarihler -, ., / cinsinden de yazilabiliyor.
    - Hata durumlari icin mekanizma eklendi.

v2.2.1
Chrome kaldirildi. Artik Edge ile tarama yapiliyor.
Seleniumdan kaynaklanan bir hata sebebiyle .exe surumu bozuldu. Gecici sureyle GUI arkasinda konsol cikacak.

v2.2
- [25.03.2024] Hata cikaran telegram modulu suan icin kaldirildi.
- Daha kucuk executable icin pygame kutuphanesi kucultuldu.
- Icon kaldirildi, iconu avast virus olarak tanimliyordu. :D

v2.1
- Eksik olan Eskisehir ili eklendi!

v2.0

- Bilet bulunca ortaya cikan bir hata giderildi.
- Bilet arama algoritmasi optimize edildi.
- Koltuk sayisi hesaplama algoritmasi bastan tasarlandi.
- Ses kutuphanesi duzenlendi. Artik her denemede bir uyari sesi cikiyor.
- Bilet bulununca ortaya cikan ses calamama sorunu cozuldu.
- Eksik olan tum sehirler eklendi. 100+ durak eklendi.

v1.7

- Windows destegi genisletildi!
- Calistirilabilir icerik (.exe) Eklendi!
- Telegram mesaj botu destegi eklendi. Artik bilet bulundugunda telegram uzerinden telefonuna mesaj gonderilebilecek!
- Sesli uyari butonu eklendi.
- Kod optimizasyonu yapildi. Uygulama artik daha hizli calisiyor!

v1.6

- Linux, macOS destegi eklendi.
- PyLint sorunlari cozuldu.
- Dizinleme yapildi.

v1.5

- Yorucu bir release
- Tüm tcdd arayüzü değiştiği için selenium tekrar configure edildi.
- tcdd sitesi bloklamasına karşı, gizli chrome araması kapatıldı, artık chrome program ile birlikte açılıyor.
- selenium hata ayarları güncellendi.
- return mekanizması eklendi, hata kodları ve butonlar güncellendi.
- durak isimleri güncellendi.
- birden fazla aramanın önüne geçebilmek için buton kilitleme işlevi eklendi.

v1.4

- sesli uyarı eklendi.

v1.3

- icon eklendi
- .exe düzeltildi.
- selenium performansı arttırıldı.
- loglama mekanizması düzeltildi.
- bilinen çökme sorunları çözüldü.
- yeni rotalar eklendi.

SS:
![python_k81455g7zP](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/blob/master/img/screenshot.png)

v1.1

- Slider eklendi.
- Bilet bulunca ortaya çıkan popup eklendi!
- Bulunan kişi sayısındaki hata giderildi.

v1.0

- GUI Düzenlendi, loglama mekanizması eklendi, stdout loglara yazdırıldı.
- Yeni durak isimleri eklendi.
- Mekanizmalar yeniden düzenlendi.

- Ocak 2023 Gelecek Güncellemeler
- .exe sürümü yayımlanacak - DONE!
- logo eklenecek.
- hatalar giderilecek.
- Bildirim sistemi güncellenecek, sms ya da e posta eklenecek.
- tcdd chapta koruması tespiti yapılacak.

# TCDD Bilet Kontrol

- Uygulama TCDD sitesine özel tasarlanmıştır.

- Uygulama seçilen dakika aralıklarında (1 - 10 dk) sorgu yapmaktadır

- Bilet bulunursa telegram uzerinden mesaj gonderebilmektedir.

- Bilet bulunursa sesli uyari ve popup uyarisinda bulunabilmektedir.

### Kullanımı

```sh
$ python main.py
```

ya da .exe dosyasini calistirabilirsiniz.

Buradan indirebilirsiniz: [tcddBiletYerKontrol_v2.0.zip](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/releases/download/v2.0/TCDD.Bilet.Bulma.Botu.v2.0.zip)
