# Bu Araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from SelSik import SelSik

class TCDD:
    def __init__(self):
        self.duraklar = [
            "İstanbul(Söğütlü Ç.)",
            "İstanbul(Bakırköy)",
            "İstanbul(Halkalı)",
            "İstanbul(Pendik)",
            "Gebze",
            "Bilecik YHT",
            "Eskişehir",
            "Ankara Gar",
            "Konya",
        ]

        self.selsik   = SelSik("https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf")
        self.tarayici = self.selsik.tarayici
