# Bu Araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from CLI    import konsol
from SelSik import SelSik
from pandas import read_html
from json   import loads

class TCDD:
    def __init__(self):
        self.tcdd_sorgu_sayfa = "https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf"
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

        self.selsik   = SelSik(self.tcdd_sorgu_sayfa, pencere="gizli")
        self.tarayici = self.selsik.tarayici

    def bilet_ara(self, nereden:str, nereye:str, tarih:str) -> list[dict] | None:
        self.tarayici.get(self.tcdd_sorgu_sayfa)

        _nereden = self.selsik.eleman_bekle("//input[@id='nereden']")
        _nereden.clear()
        _nereden.send_keys(nereden)

        _nereye = self.selsik.eleman_bekle("//input[@id='nereye']")
        _nereye.clear()
        _nereye.send_keys(nereye)

        _tarih = self.selsik.eleman_bekle("//input[@id='trCalGid_input']")
        _tarih.clear()
        _tarih.send_keys(tarih)

        _sorgula_buton = self.selsik.eleman_bekle("//button[@id='btnSeferSorgula']")
        self.tarayici.execute_script("arguments[0].click();", _sorgula_buton)

        self.selsik.eleman_bekle("//tbody[@id='mainTabView:gidisSeferTablosu_data']")
        sefer_tablo = self.selsik.kaynak_kod("//div[@id='mainTabView:gidisSeferTablosu']//table").get()

        if not sefer_tablo:
            return None

        panda_veri  = read_html(str(sefer_tablo))[0].rename(
            columns = {
                "Unnamed: 1" : "Sefer Süresi",
                "Seçim"      : "sil",
            }
        ).drop(columns="sil").dropna().reset_index(drop=True)

        return loads(panda_veri.to_json(orient="records"))