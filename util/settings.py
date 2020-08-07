import configparser

class AppSettings():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("bb_ball.ini")

    def read_settings(self, section):
        if section == 'Settings':
            varDebug = self.config.get("Settings", "Debug")
            varVerbose = self.config.get("Settings", "Verbose")
            setting = {"Debug" : varDebug, "Verbose" : varVerbose}
        elif section == 'Bluetooth':
            varDevice = self.config.get("Bluetooth", "device")
            setting = {"device": varDevice}
        return setting

    def save_settings(self, section, settings):
        self.config[section] = settings

        with open("bb_ball.ini",'w') as f:
            self.config.write(f)

