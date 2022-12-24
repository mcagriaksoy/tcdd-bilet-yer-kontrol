# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Libs.TCDD_Selenium import TCDD
from notifypy           import Notify
from os                 import name as sistem

def bildirim(baslik:str, icerik:str):

    _bildirim = Notify()
    _bildirim._notification_application_name = "TCDD | @KekikAkademi"
    _bildirim._notification_icon             = "Resimler/TCDD.png"
    if sistem == "nt":
        _bildirim.icon = "Resimler/TCDD.png"

    _bildirim.title   = baslik
    _bildirim.message = icerik

    _bildirim.send(block=False)