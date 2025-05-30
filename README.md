# TCDD Bilet Kontrol Etme Programi
TCDD bilet yer kontrol programi sayesinde tcdd sitesine surekli girmek zorunda kalmadan, ayarlayacaginiz periyotlarla websitesinden bilet yer durumunu ogrenebilmeniz saglanmistir. Uygulama kullanıcıların bilet arama işlemlerini kolaylaştırmak ve otomatize etmek amacıyla tasarlanmış bir uygulamadır. Bu uygulama, Türkiye Cumhuriyeti Devlet Demiryolları (TCDD) tarafından sunulan biletlerin doğruluğunu ve geçerliliğini hızlı ve güvenli bir şekilde kontrol etmeyi sağlar.

Bana asagidaki buton ile destek olabilirsiniz :)

<a href="https://www.buymeacoffee.com/mcagriaksoy" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-green.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
## Özellikler:

Kolay Bilet Arama: Verilen saat, tarih, kalkis ve varis bilgileri ile.

Otomatik Kontrol: Bilet bilgilerini otomatik olarak kontrol etme ve doğrulama.

Kullanıcı Dostu Arayüz: Basit ve anlaşılır tasarım ile kolay kullanım. Bilet bulunmasi, veya biletin bosa cikmasi durumunda, sesli ve gorsel uyari.

Hızlı İşlem: Bilet bilgilerini anında kontrol etme imkanı. 10 Saniye icerisinde bilet yer durumu kontrolu.

Güvenli: Kullanıcı bilgilerini güvenli bir şekilde işleme. Hic bir kisisel bilginiz tutulmaz, bilgiler tamamen TCDD sitesine aktarilir.


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

[![Download - v3.2](https://img.shields.io/static/v1?label=Download&message=v3&color=2ea44f)](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/releases/download/v3.2/TCDD.Bilet.Bulma.Botu.v3.2.zip)

## Ekran Goruntusu

![Screenshot](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/blob/master/img/Screenshot.jpg)

## Version Degisimleri
v3.2
- PySimpleGUI tamamen kaldirildi.
- UI Tkinker ile yeniden yazildi.
- Timeout sorunu cozuldu.
- Guncellenen tcdd websitesine erisim sorunu cozuldu.
- Yeni browser ozellikleri eklendi.

v3

NOT: Eger su hatayi aliyorsaniz: "Driver ayarlarında hata oluştu: Message: session not created: probably user data directory is already in use, please specify a unique value for --user-data-dir argument, or don't use --user-data-dir" Arkada acik olan tum chromium tabanli tarayicilari kapatip tekrar deneyiniz.

-Yenilenen tcdd websitesi icin uyum saglandi.

-Kod tamamen yenilendi!

-Arama algoritmasi yeni siteye uyum saglandi.

-Donate butonu eklendi.

-Pyinstaller paketi 6.surumune guncellendi.

-Selenium webdriver buffer sorunu cozuldu.

v2.4

- Takvimden kaynaklanan bir sorun cozuldu.

v2.3

Bircok Edge webdriver sorunu cozuldu.
    - webdriver kapanamama sorunu cozuldu.
- Webdriver artik sayfanin yuklenmesini daha cok bekliyor.
- Koltuk sayisini bulan regex algoritmasi yeniden yazildi.
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


### Kullanımı

Oncelikle gerekli kutuphaneleri yuklemek icin asagidaki komutu cagirin:
```
pip install -r requirements.txt
```
Sonrasinda main.py yi cagirabilirsiniz:
```
python main.py
```
### Tesekkur

@alporak yardimlarin icin tesekkurler :)
