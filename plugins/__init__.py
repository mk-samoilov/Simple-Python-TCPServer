class BasePlugin:
    PLUGIN_NAME = "BasePlugin"
    PLUGIN_DIR = f"plugins/{PLUGIN_NAME}"

    def server_inited(self):
        pass

    def server_started(self):
        pass

    def process_client_pkg(self, data: str) -> str:
        return ""
