# Mehmet Çağrı Aksoy UPDATE!

- Aralık 2022
- GUI Düzenlendi, loglama mekanizması eklendi, stdout loglara yazdırıldı.
- Yeni durak isimleri eklendi.
- Mekanizmalar yeniden düzenlendi.

Ekran görüntüsü:
![python_k81455g7zP](https://user-images.githubusercontent.com/56798318/179353750-31305c49-e25e-4e58-ad02-2429b2680ad6.png)

- Ocak 2023 Güncellemeler
- .exe sürümü yayımlanacak
- logo eklenecek.
- Bildirim sistemi güncellenecek, sms ya da e posta eklenecek.
- tcdd chapta koruması tespiti yapılacak.

# TCDD Bilet Kontrol

- Chrome driver indirme https://chromedriver.storage.googleapis.com/index.html

- Uygulama TCDD sitesine özel tasarlanmıştır.

- Uygulama 30 saniye aralıklarla sorgu yapmaktadır `main.py -> mainLoop()`fonksiyonu yerinden istediğiniz gibi ayarlayabilirsiniz.

### Paket Kurulumu 
`$ pip install -r requirements.txt`

### Çalıştırılabilir .exe oluşturma

```sh
$ pyinstaller --onefile --noconsole main.py
```

### Kullanımı
```sh
$ py main.py
```
