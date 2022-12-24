# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from CLI           import konsol
from flet.page     import Page, ControlEvent
from flet          import UserControl, Container, Column, Row, Text, Dropdown, TextField, FloatingActionButton, icons, ProgressRing, Markdown, MarkdownExtensionSet, colors
from flet.dropdown import Option as DropdownOption
from Libs          import TCDD, bildirim

from datetime import datetime
bugun = lambda: datetime.now().strftime("%d.%m.%Y")

from tabulate import tabulate
from regex    import findall

class Panel(UserControl):
    def __init__(self, sayfa:Page):
        super().__init__()
        self.sayfa = sayfa

        self.tcdd = TCDD()
        def kapanirken(e):
            if e.data == "close":
                self.tcdd.tarayici.quit()
                self.sayfa.window_destroy()

        self.sayfa.window_prevent_close = True
        self.sayfa.on_window_event      = kapanirken
        self.sayfa.update()

        self.baslik      = Text("TCDD Bilet Kontrol Etme Arayüzü", size=25, weight="bold", color="#EF7F1A")
        self.nerden      = Dropdown(label="Nereden?", hint_text="Nereden?", options=[DropdownOption(durak) for durak in self.tcdd.duraklar], autofocus=True)
        self.nereye      = Dropdown(label="Nereye?",  hint_text="Nereye?",  options=[DropdownOption(durak) for durak in self.tcdd.duraklar])
        self.tarih       = TextField(label="Tarih",   hint_text=bugun(), value=bugun(), on_submit=lambda e: self.bilet_ara(e))
        self.ara_buton   = FloatingActionButton(text="Bilet Ara", icon=icons.SEARCH, on_click=self.bilet_ara)
        self.araniyor    = ProgressRing(visible=False)
        self.cikti_alani = Text("Aramaya Hazır..", size=23, weight="bold", color=colors.CYAN_700, visible=True)

    def build(self):
        return Container(
            Column(
                [
                    Row([self.baslik], alignment="center"),
                    Row([], alignment="center", height=25),
                    Row([self.nerden, self.nereye], alignment="center"),
                    Row([self.tarih], alignment="center"),
                    Row([self.ara_buton], alignment="center"),
                    Row([self.araniyor], alignment="center"),
                    Row([self.cikti_alani], alignment="center")
                ]
            )
        )

    def arama_gizle(self, gorunum:bool):
        if isinstance(self.sayfa.controls[-1], Markdown):
            self.sayfa.controls.pop(-1)
            self.sayfa.update()

        self.ara_buton.visible   = not gorunum
        self.araniyor.visible    = gorunum
        self.cikti_alani.visible = not gorunum
        self.update()

    def __sorgu_kontrol(self):
        self.cikti_alani.visible = True

        if not self.nerden.value or not self.nereye.value or not self.tarih.value:
            return self.__bilgi_metni("Lütfen tüm alanları doldurunuz..")

        if self.nerden.value == self.nereye.value:
            return self.__bilgi_metni("Bilete ihtiyacınız oluğunu düşünmüyorum..")

        try:
            if datetime.strptime(bugun(), "%d.%m.%Y") > datetime.strptime(self.tarih.value, "%d.%m.%Y"):
                return self.__bilgi_metni("Geçmişe gidebilmeniz henüz mümkün değil..")
        except Exception:
            return self.__bilgi_metni("Muhtemelen tarih formatını hatalı kullandınız..")

        self.cikti_alani.visible = False
        self.update()
        return True

    def __bilgi_metni(self, hata:str, renk:str=colors.RED_700):
        self.cikti_alani.value = hata
        self.cikti_alani.color = renk
        self.update()
        return False

    def bilet_ara(self, _:ControlEvent):
        konsol.log(self.nerden.value, self.nereye.value, self.tarih.value)

        if not self.__sorgu_kontrol():
            return None

        self.arama_gizle(True)
        bilet_json = self.tcdd.bilet_ara(self.nerden.value, self.nereye.value, self.tarih.value)
        self.arama_gizle(False)

        if not bilet_json:
            self.__bilgi_metni("Bilet Bulunamadı..", renk=colors.PURPLE_700)
            bildirim(
                baslik = f"{self.nerden.value} - {self.nereye.value}",
                icerik = f"Bilet Bulunamadı. ~ {self.tarih.value}"
            )
            return None

        konsol.print(bilet_json)

        self.sayfa.add(
            Markdown(
                value         = tabulate(bilet_json, headers="keys", tablefmt="github"),
                selectable    = True,
                extension_set = MarkdownExtensionSet.GITHUB_WEB
            )
        )

        tren_sayisi  = len(bilet_json)
        bilet_sayisi = sum(
            sum(int(sayi) for sayi in findall(r"-([0-9]*)-", tren["Vagon Tipi"]))
                for tren in bilet_json
        )

        bildirim(
            baslik = f"{self.nerden.value} - {self.nereye.value}",
            icerik = f"{tren_sayisi} trende, {bilet_sayisi} adet bilet bulundu. ~ {self.tarih.value}"
        )
        self.__bilgi_metni(f"{tren_sayisi} trende, {bilet_sayisi} adet bilet bulundu..", renk=colors.GREEN_700)
        self.update()