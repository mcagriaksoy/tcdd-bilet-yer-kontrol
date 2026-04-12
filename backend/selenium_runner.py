from __future__ import annotations

import logging
import os
from datetime import datetime
from time import sleep

from .control import Control
from .driver_get import DriverGet
from .driver_setting import DriverSetting, cleanup_webdriver_runtime
from .error_codes import BASARILI, GUZERGAH_HATASI, SAAT_HATASI, TEKRAR_DENE
from .route import Rota
from .stations import STATIONS
from .telegram_msg import TelegramMsg


class PayloadValidationError(ValueError):
    pass


def _build_logger():
    logger = logging.getLogger("tcdd_web_app")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        os.path.join(os.getcwd(), "tcdd_web_debug.log"),
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    logger.addHandler(handler)
    return logger


def normalize_date_text(raw_text):
    raw_text = (raw_text or "").strip()
    if not raw_text:
        return raw_text
    if "-" in raw_text and len(raw_text.split("-")[0]) == 4:
        year, month, day = raw_text.split("-")
        return f"{day}.{month}.{year}"
    return raw_text.replace("/", ".").replace("-", ".")


def normalize_time_text(raw_text):
    return (raw_text or "").replace(".", ":").replace(",", ":").strip()


def validate_payload(payload):
    nereden = (payload.get("nereden") or "").strip()
    nereye = (payload.get("nereye") or "").strip()
    tarih = normalize_date_text(payload.get("tarih"))
    saat = normalize_time_text(payload.get("saat"))
    allow_economy = bool(payload.get("allow_economy"))
    allow_business = bool(payload.get("allow_business"))
    delay_time = int(payload.get("delay_time") or 1)
    telegram_msg = bool(payload.get("telegram_msg"))
    bot_token = (payload.get("bot_token") or "").strip()
    chat_id = (payload.get("chat_id") or "").strip()

    if not nereden or not nereye:
        raise PayloadValidationError("Kalkis ve varis istasyonlari secilmeli.")
    if nereden == nereye:
        raise PayloadValidationError("Kalkis ve varis ayni olamaz.")
    if nereden not in STATIONS or nereye not in STATIONS:
        raise PayloadValidationError("Istasyon secimleri listeden yapilmali.")
    if not tarih:
        raise PayloadValidationError("Tarih gerekli.")
    if not saat:
        raise PayloadValidationError("Saat gerekli.")
    if not (allow_economy or allow_business):
        raise PayloadValidationError("En az bir bilet tipi secilmeli.")

    datetime.strptime(tarih, "%d.%m.%Y")
    datetime.strptime(saat, "%H:%M")

    if telegram_msg:
        if not bot_token or not chat_id:
            raise PayloadValidationError("Telegram icin bot token ve chat id gerekli.")
        if not TelegramMsg().check_telegram_bot_status(bot_token):
            raise PayloadValidationError("Telegram bot token dogrulanamadi.")

    return {
        "nereden": nereden,
        "nereye": nereye,
        "tarih": tarih,
        "saat": saat,
        "delay_time": max(1, delay_time),
        "telegram_msg": telegram_msg,
        "bot_token": bot_token,
        "chat_id": chat_id,
        "allow_business": allow_business,
        "allow_economy": allow_economy,
    }


def run_check_loop(payload, stop_event, log, update):
    payload = validate_payload(payload)
    logger = _build_logger()
    attempt = 0

    while not stop_event.is_set():
        attempt += 1
        update(status=f"Deneme {attempt} calisiyor", attempt=attempt)
        log(f"Deneme #{attempt} baslatildi.")

        driver = DriverSetting(logger=logger).driver_init()
        if driver is None:
            log("Tarayici baslatilamadi. Edge ve msedgedriver kurulumunu kontrol edin.")
            return None

        try:
            log("TCDD sayfasi yukleniyor...")
            DriverGet(driver, logger=logger).driver_get()
            if stop_event.is_set():
                return None

            log("Rota bilgileri giriliyor...")
            route_ok = Rota(
                driver,
                payload["nereden"],
                payload["nereye"],
                payload["tarih"],
            ).dataInput()
            if route_ok == -1:
                log("Rota bilgileri girilemedi.")
                return GUZERGAH_HATASI

            log("Sefer uygunluk kontrolu yapiliyor...")
            result = Control(
                driver,
                payload["saat"],
                allow_economy=payload["allow_economy"],
                allow_business=payload["allow_business"],
                logger=logger,
            ).sayfa_kontrol()

            if result == BASARILI:
                log("Uygun bilet bulundu.")
                if payload["telegram_msg"]:
                    sent = TelegramMsg().send_telegram_message(
                        payload["bot_token"],
                        payload["chat_id"],
                    )
                    log(
                        "Telegram bildirimi gonderildi."
                        if sent
                        else "Telegram bildirimi gonderilemedi."
                    )
                return BASARILI

            if result == GUZERGAH_HATASI:
                log("Guzergah bilgileri TCDD tarafinda kabul edilmedi.")
                return result
            if result == SAAT_HATASI:
                log(
                    "Girilen saatte uygun sefer bulunamadi. "
                    "Lutfen saat bilgisini kontrol edip tekrar deneyin."
                )
                return result

            if result == TEKRAR_DENE:
                log(f"{payload['delay_time']} dakika sonra tekrar denenecek.")
            else:
                log(
                    f"Kontrol sonucu kodu: {result}. "
                    f"{payload['delay_time']} dakika sonra yeni deneme baslayacak."
                )
        finally:
            cleanup_webdriver_runtime(driver, logger)

        wait_seconds = payload["delay_time"] * 60
        update(status=f"Bekleme modunda ({wait_seconds}s)")
        for second in range(wait_seconds, 0, -1):
            if stop_event.is_set():
                log("Bekleme dongusu kullanici tarafindan durduruldu.")
                return None
            if second in (60, 30, 10, 5, 4, 3, 2, 1):
                update(status=f"Bekleme modunda ({second}s)")
            sleep(1)

        log("Bekleme tamamlandi, yeni deneme baslatiliyor.")

    return None
