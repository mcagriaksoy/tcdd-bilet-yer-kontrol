# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from flet.page import Page

class KekikFlet:
    def __init__(self, sayfa:Page, baslik:str):
        sayfa.title                = baslik
        sayfa.horizontal_alignment = "center"
        sayfa.vertical_alignment   = "center"
        sayfa.theme_mode           = "dark"
        sayfa.scroll               = "adaptive"
        sayfa.auto_scroll          = True

        self.sayfa = sayfa