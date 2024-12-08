from plugins import BasePlugin

class Plugin(BasePlugin):
    PLUGIN_NAME = "SimpleEchoPlugin"
    PLUGIN_DIR = None # replace on f"plugins/{PLUGIN_NAME}" to creating plugin folder

    def __init__(self):
        super().__init__()

    def server_inited(self):
        pass

    def server_started(self):
        pass

    def process_client_pkg(self, data):
        if data.startswith("ECHO "):
            return data[5:]

        return None
