# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Libs.TCDD_Selenium import TCDD
from notifypy           import Notify

def bildirim(baslik:str, icerik:str):

    _bildirim = Notify()
    _bildirim._notification_application_name = baslik
    _bildirim._notification_icon             = "Resimler/TCDD.png"

    _bildirim.title   = baslik
    _bildirim.message = icerik

    _bildirim.send(block=False)