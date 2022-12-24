# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from CLI import cikis_yap, hata_yakala

from flet      import FLET_APP, WEB_BROWSER
from flet      import app as flet
from flet.page import Page

from Layouts import KekikFlet, Panel
from os      import name as sistem

def ana_sayfa(sayfa:Page):
    KekikFlet(sayfa, "TCDD | @KekikAkademi")

    sayfa.add(Panel(sayfa))

if __name__ == "__main__":
    try:
        flet(target=ana_sayfa, view=FLET_APP if sistem != "nt" else WEB_BROWSER, port=1927, assets_dir="Assets")
        cikis_yap(False)
    except Exception as hata:
        hata_yakala(hata)