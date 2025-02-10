import json
import os


class ConfigReader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.config = self._load_config()

    def _load_config(self):
        assert os.path.exists(self.file_path), f"The configuration file {self.file_path} was not found."
        with open(self.file_path, "r") as file:
            return json.load(file)

    def get(self, key):
        return self.config[key]

    def update(self, key, value):
        self.config[key] = value
        self.save()

    def save(self):
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.config, file, indent=4)
        except PermissionError:
            raise
        except IOError as e:
            raise
