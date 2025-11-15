# utils/history_manager.py
import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path.home() / ".fuzzy_history.json"

class HistoryManager:
    def __init__(self, path: Path = HISTORY_FILE):
        self.path = path
        if not path.exists():
            self._write([])

    def _read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _write(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, disease, inputs: dict, risco: float):
        data = self._read()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "disease": disease,
            "inputs": inputs,
            "risco": float(risco)
        }
        data.insert(0, entry)
        # keep only last 200 entries to limit file size
        data = data[:200]
        self._write(data)
        return entry

    def list(self, limit=50):
        return self._read()[:limit]

    def clear(self):
        self._write([])
