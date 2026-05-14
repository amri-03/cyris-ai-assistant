import json
from pathlib import Path


class StorageService:

    def __init__(self):
        self.storage_path = Path("data/memory.json")

        if not self.storage_path.exists():
            self.storage_path.write_text("{}")

    def _load_storage(self):
        with open(self.storage_path, "r") as file:
            return json.load(file)

    def _save_storage(self, data):
        with open(self.storage_path, "w") as file:
            json.dump(data, file, indent=4)

    def save(
            self,
            key: str,
            value
    ):
        data = self._load_storage()

        data[key] = value.model_dump()

        self._save_storage(data)

        return {
            "status": "saved",
            "key": key
        }

    def retrieve(
            self,
            key: str
    ):
        data = self._load_storage()

        return data.get(key)

    def list_keys(self):
        data = self._load_storage()

        return list(data.keys())