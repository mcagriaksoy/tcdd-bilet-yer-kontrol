"""TCDD sayfasindaki guvenlik dogrulamasi (CAPTCHA) tespiti ve bekleme yardimcilari."""

from __future__ import annotations

from time import monotonic, sleep

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

CAPTCHA_SELECTORS = (
    "iframe[src*='recaptcha']",
    "iframe[src*='hcaptcha']",
    "iframe[src*='turnstile']",
    "iframe[src*='challenges.cloudflare.com']",
    "iframe[title*='Cloudflare']",
    ".g-recaptcha",
    ".h-captcha",
    ".cf-turnstile",
    "#captcha",
    "[id*='captcha']",
    "[class*='captcha']",
)

CAPTCHA_TEXT_MARKERS = (
    "captcha",
    "robot değilsiniz",
    "robot degilsiniz",
    "robot olmadığınızı",
    "robot olmadiginizi",
    "güvenlik doğrulaması",
    "guvenlik dogrulamasi",
    "doğrulama kodu",
    "dogrulama kodu",
)

DEFAULT_CAPTCHA_TIMEOUT = 180


def captcha_present(driver) -> bool:
    """Sayfada gorunen bir CAPTCHA/guvenlik dogrulamasi var mi?"""
    try:
        for selector in CAPTCHA_SELECTORS:
            for element in driver.find_elements(By.CSS_SELECTOR, selector):
                try:
                    if element.is_displayed():
                        return True
                except WebDriverException:
                    continue

        body = driver.find_element(By.TAG_NAME, "body")
        text = (body.text or "").lower()
    except WebDriverException:
        return False

    return any(marker in text for marker in CAPTCHA_TEXT_MARKERS)


def bring_browser_to_front(driver) -> None:
    """CAPTCHA cozulebilsin diye Selenium tarayicisini one getirmeyi dene."""
    try:
        driver.switch_to.window(driver.current_window_handle)
    except WebDriverException:
        pass

    try:
        driver.maximize_window()
    except WebDriverException:
        pass

    try:
        driver.execute_script("window.focus();")
    except WebDriverException:
        pass


def wait_for_captcha(
    driver,
    stop_event,
    log,
    update,
    timeout=DEFAULT_CAPTCHA_TIMEOUT,
) -> bool:
    """Kullanici CAPTCHA'yi cozene kadar bekle. Cozulurse True doner."""
    log(
        "Guvenlik dogrulamasi (CAPTCHA) algilandi. "
        "Acilan Edge penceresinde dogrulamayi tamamlayin; kontrol bekliyor."
    )
    update(status="Guvenlik dogrulamasi bekleniyor", captcha=True)
    bring_browser_to_front(driver)

    started_at = monotonic()
    last_notice = 0.0

    while monotonic() - started_at < timeout:
        if stop_event and stop_event.is_set():
            log("Guvenlik dogrulamasi beklenirken kullanici durdurdu.")
            update(captcha=False)
            return False

        if not captcha_present(driver):
            log("Guvenlik dogrulamasi tamamlandi, kontrole devam ediliyor.")
            update(captcha=False)
            return True

        elapsed = monotonic() - started_at
        if elapsed - last_notice >= 30:
            remaining = max(0, int(timeout - elapsed))
            update(
                status=f"Guvenlik dogrulamasi bekleniyor ({remaining}s)",
                captcha=True,
            )
            last_notice = elapsed

        sleep(2)

    log(
        "Guvenlik dogrulamasi zaman asimina ugradi. "
        "Dogrulama tamamlanmadi; yeni deneme baslatilacak."
    )
    update(captcha=False)
    return False
