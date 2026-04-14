import sys
import os

from webapp import create_app

app = create_app()


def _force_utf8_stdio():
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def main():
    _force_utf8_stdio()
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    web_port = int(os.environ.get("TCDD_WEB_PORT", "5001"))
    app.run(
        debug=debug_mode,
        use_reloader=False,
        host="127.0.0.1",
        port=web_port,
    )


if __name__ == "__main__":
    main()
