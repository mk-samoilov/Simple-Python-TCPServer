import socket, threading, importlib, os, logging
from typing import List, Tuple

from plugins import BasePlugin
from config import *


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PersonalClientHandler:
    def __init__(self, client_socket, client_address, server):
        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server
        self.running = True

    def handle(self):
        while self.running:
            data = self.client_socket.recv(1024).decode()
            if not data:
                break

            logging.info(f"Client {self.client_address[0]} sent package")
            self.process_data(data)

        self.client_socket.close()
        logging.info(f"Client {self.client_address[0]} disconnected")

    def process_data(self, data):
        for plugin in self.server.plugins:
            response = str(plugin.process_client_pkg(data))
            if response:
                self.client_socket.send(response.encode('utf-8'))
                break
        else:
            self.client_socket.send("None".encode('utf-8'))

    def stop(self):
        self.running = False

class TCPServer:
    def __init__(self):
        self.handling = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))

        self.clients: List[Tuple[PersonalClientHandler, threading.Thread]] = []
        self.plugins: List[BasePlugin] = []

        if LOADING_PLUGINS:
            self.load_plugins()

        for plugin in self.plugins:
            plugin.server_inited()

    def main(self):
        self.socket.listen(MAX_CLIENTS)
        logging.info(f"Server started on {HOST.replace(
            '0.0.0.0', 
            socket.gethostbyname(
                socket.gethostname()
            ))}:{PORT}")

        for plugin in self.plugins:
            plugin.server_started()

        while self.handling:
            self.handle_client_connect()

    def handle_client_connect(self):
        client_socket, client_address = self.socket.accept()
        logging.info(f"Connected client from {client_address[0]}")
        c_handler = PersonalClientHandler(client_socket, client_address, self)
        client_thread = threading.Thread(target=c_handler.handle)
        client_thread.start()
        self.clients.append((c_handler, client_thread))

    def load_plugins(self):
        for filename in os.listdir(PLUGINS_DIR):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module = importlib.import_module(f"{PLUGINS_DIR}.{module_name}")
                if hasattr(module, "Plugin"):
                    plugin = module.Plugin()
                    self.plugins.append(plugin)
                    logging.info(f"Loaded plugin: {module_name}")

    def stop(self):
        self.handling = False
        for handler, thread in self.clients:
            handler.stop()
        self.socket.close()


if __name__ == "__main__":
    srv = TCPServer()
    try:
        srv.main()
    except KeyboardInterrupt:
        logging.info("Server shutting down...")
        srv.stop()
        input("Press enter to exit.")
