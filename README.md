# TCDD Bilet Kontrol

- Chrome driver indirme https://chromedriver.storage.googleapis.com/index.html

- Uygulama TCDD sitesine özel tasarlanmıştır.

- Uygulama 30 saniye aralıklarla sorgu yapmaktadır `main.py -> mainLoop()`fonksiyonu yerinden istediğiniz gibi ayarlayabilirsiniz.


### Paket Kurulumu 
`$ pip install -r requirements.txt`

### PushSafer Kurulumu 
`main.py -> PushSafer().sendNotification()` fonksiyonunun key kısmına https://www.pushsafer.com 'dan üye olup aldığınız private key'inizi giriniz

![chrome_oGIz4AlFYP](https://user-images.githubusercontent.com/56798318/179354186-a0115ad5-f725-4ff9-8d9a-e0793369acea.png)

### Arayüz
![python_k81455g7zP](https://user-images.githubusercontent.com/56798318/179353750-31305c49-e25e-4e58-ad02-2429b2680ad6.png)

### Çalıştırılabilir .exe oluşturma

```sh
$ pyinstaller --onefile --noconsole main.py
```

### Kullanımı
```sh
$ py main.py
```
