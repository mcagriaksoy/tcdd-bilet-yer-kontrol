# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from flet.page import Page
from flet      import UserControl, Container, Column, Row, Text, Dropdown
from flet.dropdown import Option as DropdownOption
from Libs      import TCDD

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

        self.baslik = Text("TCDD Bilet Arama Botu", size=25, weight="bold", color="#EF7F1A")
        self.nerden = Dropdown(label="Nereden?", hint_text="Nereden?", options=[DropdownOption(durak) for durak in self.tcdd.duraklar], autofocus=True)
        self.nereye = Dropdown(label="Nereye?",  hint_text="Nereye?",  options=[DropdownOption(durak) for durak in self.tcdd.duraklar])

    def build(self):
        return Container(
            Column(
                [
                    Row([self.baslik], alignment="center"),
                    Row([], alignment="center", height=25),
                    Row([self.nerden, self.nereye], alignment="center")
                ]
            )
        )