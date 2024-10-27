class BasePlugin:
    def server_inited(self):
        pass

    def server_started(self):
        pass

    def process_client_pkg(self, data):
        raise NotImplementedError("Subclasses must implement process method")
