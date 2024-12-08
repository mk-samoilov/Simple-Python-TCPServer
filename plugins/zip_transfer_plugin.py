from plugins import BasePlugin
import os, base64

class Plugin(BasePlugin):
    PLUGIN_NAME = "ZipTransferPlugin"
    PLUGIN_DIR = f"plugins/{PLUGIN_NAME}"

    def __init__(self):
        super().__init__()

    def process_client_pkg(self, data):
        if data.startswith("zt_LIST"):
            return str(os.listdir(self.PLUGIN_DIR))

        if data.split(" ")[0] == "zt_UPLOAD":
            filename = data.split(" ")[1]
            content_base64 = data.split(" ")[2]
            content = base64.b64decode(content_base64)

            with open(file=f"{self.PLUGIN_DIR}/{filename}", mode="wb") as file:
                file.write(content)

            return "OK"

        if data.split(" ")[0] == "zt_DOWNLOAD":
            filename = data.split(" ")[1]
            with open(file=f"{self.PLUGIN_DIR}/{filename}", mode="rb") as file:
                content = file.read()

            content_base64 = base64.b64encode(content).decode("utf-8")
            return content_base64

        return None
