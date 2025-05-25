import matplotlib.pyplot as plt
import numpy as np

# Verileri oluştur
x = np.linspace(1, 10, 100)
y = 10 / x  # Azalan bir fonksiyon (ters orantı)

# Grafik çizimi (eksen sayıları gizlenmiş halde)
plt.figure(figsize=(6, 6))
plt.plot(x, y, label='Matematik-Müzik İlişkisi', color='blue')

# Noktalar ve etiketler
plt.scatter([1.5, 9], [10 / 1.5, 10 / 9], color='purple', s=100)
plt.axvline(x=1.5, linestyle='dashed', color='gray')
plt.axvline(x=9, linestyle='dashed', color='gray')
plt.text(1.5, 10 / 1.5 + 0.5, 'Antik Yunan', ha='center')
plt.text(9, 10 / 9 + 0.5, 'Günümüz', ha='center')

# Eksen etiketleri ve başlık
plt.xlabel('Zaman (Antik Yunan → Günümüz)')
plt.ylabel('İlişki Düzeyi')
plt.title('Tarihte Matematik-Müzik İlişkisi')

# Eksen sayıları gizleniyor
plt.xticks([])
plt.yticks([])

plt.grid(True)
plt.show()

