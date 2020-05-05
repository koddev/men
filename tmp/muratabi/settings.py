import json

class Settings:
    def __init__(self):
        try:
            f = open("settings", "r")
            content = f.read()
            f.close()
            self.settings = json.loads(str(content))
        except:
            self.settings = {
                "fps": 5,
                "resolution": ""
            }
    
    def write_settings(self):
        f = open("settings", "w")
        content = json.dumps(self.settings)
        f.write(content)
        f.close()

    def change_setting(self, setting, value):
        self.settings[setting] = value
        self.write_settings()