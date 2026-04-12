"""
Enhanced version @author: Mehmet Cagri Aksoy https://github.com/mcagriaksoy
"""

import os
import subprocess
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from desktop_app import ui
except ImportError:
    import ui  # type: ignore

VERSION_DEBUG = False


def _force_utf8_stdio():
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def main():
    """Main function"""
    _force_utf8_stdio()

    if VERSION_DEBUG:

        def install_requirements():
            """Install the requirements from requirements.txt"""
            subprocess.check_call(
                ["python", "-m", "pip", "install", "-r", "requirements.txt"]
            )

        install_requirements()

    ui.__main__()


if __name__ == "__main__":
    main()
