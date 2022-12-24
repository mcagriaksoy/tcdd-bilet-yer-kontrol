# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from CLI           import konsol
from flet.page     import Page, ControlEvent
from flet          import UserControl, Container, Column, Row, Text, Dropdown, TextField, FloatingActionButton, icons, ProgressRing, Markdown, MarkdownExtensionSet
from flet.dropdown import Option as DropdownOption
from Libs          import TCDD

from datetime import datetime
bugun = datetime.now().strftime("%d.%m.%Y")

from tabulate import tabulate

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

        self.baslik      = Text("TCDD Bilet Arama Botu", size=25, weight="bold", color="#EF7F1A")
        self.nerden      = Dropdown(label="Nereden?", hint_text="Nereden?", options=[DropdownOption(durak) for durak in self.tcdd.duraklar], autofocus=True)
        self.nereye      = Dropdown(label="Nereye?",  hint_text="Nereye?",  options=[DropdownOption(durak) for durak in self.tcdd.duraklar])
        self.tarih       = TextField(label="Tarih",   hint_text=bugun, value=bugun, on_submit=lambda e: self.bilet_ara(e))
        self.ara_buton   = FloatingActionButton(text="Bilet Ara", icon=icons.SEARCH, on_click=self.bilet_ara)
        self.araniyor    = ProgressRing(visible=False)

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
                ]
            )
        )

    def arama_gizle(self, gorunum:bool):
        if isinstance(self.sayfa.controls[-1], Markdown):
            self.sayfa.controls.pop(-1)
            self.sayfa.update()

        self.ara_buton.visible = not gorunum
        self.araniyor.visible  = gorunum
        self.update()

    def bilet_ara(self, _:ControlEvent):

        self.arama_gizle(True)
        konsol.log(self.nerden.value, self.nereye.value, self.tarih.value)
        bilet_json  = self.tcdd.bilet_ara(self.nerden.value, self.nereye.value, self.tarih.value)
        bilet_tablo = tabulate(bilet_json, headers="keys", tablefmt="github")
        konsol.print(bilet_tablo)
        self.arama_gizle(False)

        self.sayfa.add(
            Markdown(
                value         = bilet_tablo,
                selectable    = True,
                extension_set = MarkdownExtensionSet.GITHUB_WEB
            )
        )

        self.update()