[![mcagriaksoy - tcdd-bilet-yer-kontrol](https://img.shields.io/static/v1?label=mcagriaksoy&message=tcdd-bilet-yer-kontrol&color=red&logo=github)](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol "Go to GitHub repo")
[![stars - tcdd-bilet-yer-kontrol](https://img.shields.io/github/stars/mcagriaksoy/tcdd-bilet-yer-kontrol?style=social)](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol)
[![forks - tcdd-bilet-yer-kontrol](https://img.shields.io/github/forks/mcagriaksoy/tcdd-bilet-yer-kontrol?style=social)](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol)
[![GitHub release](https://img.shields.io/github/release/mcagriaksoy/tcdd-bilet-yer-kontrol?include_prereleases=&sort=semver&color=red)](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/releases/)
[![License](https://img.shields.io/badge/License-GPL--3.0--1-red)](#license)
[![issues - tcdd-bilet-yer-kontrol](https://img.shields.io/github/issues/mcagriaksoy/tcdd-bilet-yer-kontrol)](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/issues)


TCDD bilet yer kontrol programi sayesinde tcdd sitesine surekli girmek zorunda kalmadan, ayarlayacaginiz periyotlarla websitesinden bilet yer durumunu ogrenebilmeniz saglanmistir. Uygulama kullanıcıların bilet arama işlemlerini kolaylaştırmak ve otomatize etmek amacıyla tasarlanmış bir uygulamadır. Bu uygulama, Türkiye Cumhuriyeti Devlet Demiryolları (TCDD) tarafından sunulan biletlerin doğruluğunu ve geçerliliğini hızlı ve güvenli bir şekilde kontrol etmeyi sağlar.


Basitçe: bu program TCDD bilet sitesini belirtilen aralıklarla kontrol ederek seçtiğiniz seferde boş koltuk olup olmadığını size bildirir. Otomasyon, sesli/görsel uyarı ve (isteğe bağlı) Telegram bildirimleri sağlar.

Bana aşağıdaki buton ile destekte bulunabilirsin...

<a href="https://www.buymeacoffee.com/mcagriaksoy" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-green.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;"></a>

## Öne çıkan özellikler

- Kolay arama: tarih, saat, kalkış ve varış bilgileri ile arama.
- Otomatik periyodik kontrol: belirlediğiniz aralıklarla bilet kontrolü.
- Sesli ve görsel uyarılar.
- Telegram ile (isteğe bağlı) bildirim gönderme desteği.
- Windows/Linux/macOS üzerinde çalışacak şekilde tasarlandı (Selenium/Edge kullanımı).

## Uyarı / Sorumluluk Reddi

⚠️ UYARI: Bu yazılım "olduğu gibi" sağlanmaktadır. Yazılımın kullanımı sonucu ortaya çıkabilecek her türlü zarardan, hesabınızın kısıtlanması, TCDD sitesinin erişim engeli, veri kaybı, hizmet kesintisi veya benzeri olumsuz durumlardan proje sahipleri, katkıda bulunanlar veya dağıtıcısı sorumlu tutulamaz. Bu aracı kullanmadan önce TCDD'nin kullanım şartlarını ve ilgili mevzuatı kontrol edin. Herhangi bir otomasyon işlemine başlamadan önce kendi risk değerlendirmesini yapınız.

Bu proje TCDD veya onun bağlı kuruluşları tarafından desteklenmemektedir. Tamamen açık kaynak kodlu gönüllü bir projedir.

## İndir

[![Download - v4.0](https://img.shields.io/static/v1?label=Download&message=v4_0&color=2ea44f)](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/releases/tag/v4.0)

## Ekran Görüntüsü

![Screenshot](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/blob/master/img/Screenshot.jpg)

## Kurulum

1. Python 3.8+ yüklü olduğundan emin olun.
2. Gerekli paketleri yükleyin:

```powershell
pip install -r requirements.txt
```

3. Chrome yerine Edge (Chromium) kullanılması önerilir; sisteminizde uygun webdriver (msedgedriver) olduğundan emin olun.

## Kullanım

Programı başlatmak için:

```powershell
python main.py
```

UI üzerinden arama parametrelerini girin (kalkış, varış, tarih, saat) ve otomatik kontrolü başlatın.

Not: Eğer "session not created: probably user data directory is already in use" gibi bir hata alırsanız, açık Chromium tablarını kapatıp tekrar deneyin.


## Sürüm Notları (kısa)

Projedeki ana değişiklikler ve geçmiş sürümler için GitHub sürümler sayfasına bakabilirsiniz. Öne çıkanlar:
- v4.0
	- UI: Arayüz yenilenip kullanıcı deneyimi geliştirildi (yeni tasarım, daha stabil pencere yönetimi).
	- Tarayıcı desteği: Selenium/Edge yapılandırmaları güncellendi; msedgedriver ile daha uyumlu hale getirildi.
	- Otomasyon: Arama ve tekrar mekanizmaları optimize edildi; periyot ve zaman aşımı davranışları iyileştirildi.
	- Hata yönetimi: Webdriver bağlantı sorunları ve oturum çakışmalarına karşı daha iyi hata yakalama ve yönlendirme eklendi.
	- Bildirimler: Sesli uyarı ve Telegram bildirimleri kararlılık açısından güncellendi.
	- Bağımlılıklar: requirements ve paket yönetimi güncellendi; PySimpleGUI tamamen çıkarıldı ve bağımlılıklar sadeleştirildi.
	- Düzeltmeler: Bilinen birkaç çökme ve performans sorunu giderildi.
- v3.2: PySimpleGUI kaldırıldı, UI Tkinter ile yeniden yazıldı, timeout ve site erişim sorunları giderildi.
- v3: Kod büyük oranda yenilendi, arama algoritması güncellendi.

Detaylı değişiklik geçmişi orijinal README içeriğinde bulunmaktadır.

## Katkıda Bulunanlar & Teşekkür

Teşekkürler: @alporak ve katkıda bulunanlar.

## Lisans

Bu proje GNU GENERAL PUBLIC LICENSE Version 3 lisansı ile lisanslanmıştır. Daha fazla detay için `LICENSE` dosyasına bakınız.
