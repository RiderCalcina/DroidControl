import json
import os

class HistoryManager:
    def __init__(self, filename="settings.json"):
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.filepath = os.path.join(self.base_path, filename)
        self.settings = self.load()

    def load(self):
        defaults = {
            "output_dir": os.path.join(self.base_path, "captures"),
            "last_ip": "",
            "last_port": "5555"
        }
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    for key, val in defaults.items():
                        if key not in data: data[key] = val
                    return data
            except Exception:
                return defaults
        return defaults

    def save(self):
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception:
            pass

    def get_output_dir(self):
        path = self.settings.get("output_dir")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path

    def set_output_dir(self, path):
        self.settings["output_dir"] = path
        self.save()

    def get_wifi_settings(self):
        return self.settings.get("last_ip", ""), self.settings.get("last_port", "5555")

    def set_wifi_settings(self, ip, port):
        self.settings["last_ip"] = ip
        self.settings["last_port"] = port
        self.save()
