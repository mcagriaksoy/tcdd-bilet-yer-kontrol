# Mehmet Çağrı Aksoy UPDATE!

- Aralık 2022
v2.1
- Slider eklendi.
- Bilet bulunca ortaya çıkan popup eklendi!
- Bulunan kişi sayısındaki hata giderildi.

SS:
![python_k81455g7zP](https://github.com/mcagriaksoy/tcdd-bilet-yer-kontrol/blob/master/ss2.png)

v2
- GUI Düzenlendi, loglama mekanizması eklendi, stdout loglara yazdırıldı.
- Yeni durak isimleri eklendi.
- Mekanizmalar yeniden düzenlendi.


- Ocak 2023 Güncellemeler
- .exe sürümü yayımlanacak - DONE!
- logo eklenecek.
- hatalar giderilecek.
- Bildirim sistemi güncellenecek, sms ya da e posta eklenecek.
- tcdd chapta koruması tespiti yapılacak.

# TCDD Bilet Kontrol

- Chrome driver indirme https://chromedriver.storage.googleapis.com/index.html

- Uygulama TCDD sitesine özel tasarlanmıştır.

- Uygulama seçilen dakika aralıklarında (1 - 10 dk) sorgu yapmaktadır 

`main.py -> mainLoop()`fonksiyonu yerinden istediğiniz gibi ayarlayabilirsiniz.

### Paket Kurulumu 
`$ pip install -r requirements.txt`

### Çalıştırılabilir .exe oluşturma

```sh
$ pyinstaller --onefile --noconsole main.py
```

### Kullanımı
```sh
$ python main.py
```
