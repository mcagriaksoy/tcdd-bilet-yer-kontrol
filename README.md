# Mehmet Çağrı Aksoy 2023 geliştirme ve önerilere açığım :=)
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
![python_k81455g7zP](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/blob/master/ss2.png)


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

- Chrome driver indirme https://chromedriver.storage.googleapis.com/index.html

- Uygulama TCDD sitesine özel tasarlanmıştır.

- Uygulama seçilen dakika aralıklarında (1 - 10 dk) sorgu yapmaktadır 

### Paket Kurulumu 
`$ pip install -r requirements.txt`

### Çalıştırılabilir .exe oluşturma

```sh
$ pyinstaller --onefile --noconsole --icon=icon.ico -F main.py
```

Ayrıca linkten: https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/blob/master/tcddBiletYerKontrol_v1.4.zip
.exe sürümünü indirebilirsiniz.

### Kullanımı
```sh
$ python main.py
```
