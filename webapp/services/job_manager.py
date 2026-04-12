from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from threading import Event, Lock, Thread

from backend.error_codes import BASARILI, GUZERGAH_HATASI, SAAT_HATASI
from backend.selenium_runner import PayloadValidationError, run_check_loop


@dataclass
class JobState:
    running: bool = False
    status: str = "Hazır"
    attempt: int = 0
    found: bool = False
    started_at: str | None = None
    finished_at: str | None = None
    active_payload: dict = field(default_factory=dict)
    last_result_code: int | None = None


class JobManager:
    def __init__(self):
        self._lock = Lock()
        self._state = JobState()
        self._logs = []
        self._log_seq = 0
        self._worker = None
        self._stop_event = Event()

    def _append_log(self, message):
        with self._lock:
            self._log_seq += 1
            self._logs.append(
                {
                    "id": self._log_seq,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "message": message,
                }
            )
            self._logs = self._logs[-400:]

    def get_logs(self, after=0):
        with self._lock:
            items = [entry for entry in self._logs if entry["id"] > after]
            return {"items": items, "last_id": self._log_seq}

    def get_status(self):
        with self._lock:
            return {
                "running": self._state.running,
                "status": self._state.status,
                "attempt": self._state.attempt,
                "found": self._state.found,
                "started_at": self._state.started_at,
                "finished_at": self._state.finished_at,
                "active_payload": self._state.active_payload,
                "last_result_code": self._state.last_result_code,
            }

    def _set_status(self, **kwargs):
        with self._lock:
            for key, value in kwargs.items():
                setattr(self._state, key, value)

    def start(self, payload):
        with self._lock:
            if self._state.running:
                raise ValueError("Halihazirda calisan bir kontrol var.")
            self._state = JobState(
                running=True,
                status="Baslatiliyor",
                attempt=0,
                found=False,
                started_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                finished_at=None,
                active_payload=payload,
                last_result_code=None,
            )
        self._stop_event = Event()
        self._append_log("Yeni kontrol istegi alindi.")
        self._worker = Thread(
            target=self._run_worker,
            args=(payload,),
            daemon=True,
        )
        self._worker.start()

    def stop(self):
        self._stop_event.set()
        self._append_log("Durdurma istegi alindi.")
        self._set_status(status="Durduruluyor")

    def _run_worker(self, payload):
        try:
            result = run_check_loop(
                payload=payload,
                stop_event=self._stop_event,
                log=self._append_log,
                update=self._set_status,
            )
            final_status = "Bilet bulundu" if result == BASARILI else "Tamamlandi"
            if result == GUZERGAH_HATASI:
                final_status = "Guzergah hatasi"
            if result == SAAT_HATASI:
                final_status = "Sefer saati bulunamadi"
            if self._stop_event.is_set():
                final_status = "Kullanici tarafindan durduruldu"
            self._set_status(
                running=False,
                status=final_status,
                found=result == BASARILI,
                finished_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                last_result_code=result,
            )
        except PayloadValidationError as exc:
            self._append_log(f"Form hatasi: {exc}")
            self._set_status(
                running=False,
                status="Form hatasi",
                finished_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        except Exception as exc:
            self._append_log(f"Beklenmeyen hata: {exc}")
            self._set_status(
                running=False,
                status="Beklenmeyen hata",
                finished_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
