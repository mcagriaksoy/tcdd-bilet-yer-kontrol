from pathlib import Path

from flask import (
    Blueprint,
    Response,
    current_app,
    jsonify,
    render_template,
    request,
    send_file,
    url_for,
)

from backend.stations import STATIONS

bp = Blueprint("main", __name__)

LEGAL_PAGES = {
    "iletisim": {
        "title": "İletişim",
        "summary": "Sorularınız, önerileriniz ve iş birlikleri için bizimle iletişime geçebilirsiniz.",
        "items": [
            "E-posta: destek@tcddbiletalarmi.com",
            "Çalışma saatleri: Hafta içi 09:00 - 18:00",
            "Teknik destek taleplerinde kullandığınız rota ve saat bilgisini belirtmeniz süreci hızlandırır.",
        ],
    },
    "gizlilik": {
        "title": "Gizlilik Politikası",
        "summary": "Kullanıcı verilerinin korunması, saklanması ve işlenmesi süreçlerini şeffaf şekilde açıklarız.",
        "items": [
            "Formda girdiğiniz rota ve sefer bilgileri yalnızca arama işlemi için kullanılır.",
            "Telegram bildirim bilgileri (bot token ve chat id) üçüncü taraflarla paylaşılmaz.",
            "Hizmet güvenliği için sınırlı teknik loglar tutulabilir.",
        ],
    },
    "kullanim-kosullari": {
        "title": "Kullanım Koşulları",
        "summary": "Platformu kullanırken geçerli olan temel kurallar ve sorumluluk çerçevesi.",
        "items": [
            "Sistem TCDD eBilet sitesini düzenli aralıklarla otomatik kontrol eder.",
            "Bilet bulunması, satın alma işleminin tamamlandığı anlamına gelmez.",
            "Kullanıcı, hizmeti yürürlükteki mevzuata ve TCDD kullanım şartlarına uygun kullanmalıdır.",
        ],
    },
}


@bp.get("/")
def index():
    return render_template("index.html", stations=STATIONS)


@bp.get("/favicon.ico")
def favicon():
    ico_path = Path(current_app.root_path).parent / "icon.ico"
    return send_file(ico_path, mimetype="image/x-icon")


@bp.get("/<slug>")
def legal_page(slug):
    data = LEGAL_PAGES.get(slug)
    if not data:
        return ("Sayfa bulunamadı", 404)
    return render_template("legal_page.html", slug=slug, **data)


@bp.get("/sitemap.xml")
def sitemap():
    urls = [
        request.url_root.rstrip("/") + url_for("main.index"),
        request.url_root.rstrip("/") + url_for("main.legal_page", slug="iletisim"),
        request.url_root.rstrip("/") + url_for("main.legal_page", slug="gizlilik"),
        request.url_root.rstrip("/") + url_for("main.legal_page", slug="kullanim-kosullari"),
    ]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        body.append(f"  <url><loc>{url}</loc></url>")
    body.append("</urlset>")
    return Response("\n".join(body), mimetype="application/xml")


@bp.get("/robots.txt")
def robots():
    content = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.url_root.rstrip('/')}{url_for('main.sitemap')}",
    ]
    return Response("\n".join(content), mimetype="text/plain")


@bp.get("/api/status")
def status():
    return jsonify(current_app.job_manager.get_status())


@bp.get("/api/logs")
def logs():
    after = request.args.get("after", default=0, type=int)
    return jsonify(current_app.job_manager.get_logs(after))


@bp.post("/api/start")
def start():
    payload = request.get_json(force=True, silent=False)
    try:
        current_app.job_manager.start(payload)
        return jsonify(current_app.job_manager.get_status())
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@bp.post("/api/stop")
def stop():
    current_app.job_manager.stop()
    return jsonify(current_app.job_manager.get_status())
