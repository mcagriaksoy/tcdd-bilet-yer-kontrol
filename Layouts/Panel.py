# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from CLI           import konsol
from flet.page     import Page, ControlEvent
from flet          import UserControl, Container, Column, Row, Text, Dropdown, TextField, FloatingActionButton, icons
from flet.dropdown import Option as DropdownOption
from Libs          import TCDD
from datetime      import datetime

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
        bugun = datetime.now().strftime("%d.%m.%Y")
        self.tarih       = TextField(label="Tarih",   hint_text=bugun, value=bugun, on_submit=lambda e: self.bilet_ara(e))
        self.ara_buton   = FloatingActionButton(text="Bilet Ara", icon=icons.SEARCH, on_click=self.bilet_ara)
        self.cikti_alani = Column(auto_scroll=True)

    def build(self):
        return Container(
            Column(
                [
                    Row([self.baslik], alignment="center"),
                    Row([], alignment="center", height=25),
                    Row([self.nerden, self.nereye], alignment="center"),
                    Row([self.tarih], alignment="center"),
                    Row([self.ara_buton], alignment="center"),
                    Row([], alignment="center", height=25),
                    Row([self.cikti_alani], alignment="center", height=25)
                ]
            )
        )

    def bilet_ara(self, _:ControlEvent):
        konsol.log(self.nerden.value, self.nereye.value, self.tarih.value)
        biletler = self.tcdd.bilet_ara(self.nerden.value, self.nereye.value, self.tarih.value)
        konsol.log(biletler)

        self.update()