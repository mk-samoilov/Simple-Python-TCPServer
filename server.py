import socket, threading, importlib, os, logging, time
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
            try:
                # self.client_socket.settimeout(TIMEOUT)
                data = self.client_socket.recv(MAX_DATA_VOLUME).decode()
                if not data:
                    break

                logging.info(f"Client {self.client_address[0]} sent package '{data}'")
                self.process_data(data)

            # except socket.timeout:
            #     logging.warning(f"Timeout occurred for client {self.client_address[0]}")

            except Exception as e:
                logging.error(f"Error handling client {self.client_address[0]}: {str(e)}")
                break

        self.close_connection()

    def process_data(self, data):
        try:
            for plugin in self.server.plugins:
                response = plugin.process_client_pkg(data)
                if response:
                    self.send_pkg(str(response))
                    break
            else:
                self.send_pkg("None")

        except Exception as e:
            logging.error(f"Error processing data from client {self.client_address[0]}: {str(e)}")
            self.send_pkg("Error occurred while processing data")

    def send_pkg(self, response):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.client_socket.send(response.encode("utf-8"))
                return

            except Exception as e:
                if attempt < max_retries - 1:
                    logging.warning(f"Failed to send response to client {self.client_address[0]}, retrying... (Attempt {attempt + 1})")
                    time.sleep(1)
                else:
                    logging.error(f"Failed to send response to client {self.client_address[0]} after {max_retries} attempts: {str(e)}")

    def close_connection(self):
        try:
            self.client_socket.close()
            logging.info(f"Client {self.client_address[0]} disconnected")

        except Exception as e:
            logging.error(f"Error closing connection for client {self.client_address[0]}: {str(e)}")

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
            try:
                plugin.server_inited()
                if plugin.PLUGIN_DIR:
                    try:
                        os.mkdir(plugin.PLUGIN_DIR)
                    except FileExistsError:
                        pass
                    except PermissionError:
                        logging.error(f"Not have permissions to create plugin folder '{plugin.PLUGIN_DIR}'")

            except Exception as e:
                logging.error(f"Failed to plugin {plugin.PLUGIN_NAME}: {str(e)}")

    def main(self):
        try:
            self.socket.listen(MAX_CLIENTS)
            logging.info(
                f"Server started on {HOST.replace(
                    '0.0.0.0', 
                    socket.gethostbyname(
                        socket.gethostname()
                    )
                )}:{PORT}"
            )

            for plugin in self.plugins:
                try:
                    plugin.server_started()

                except Exception as e:
                    logging.error(f"Failed to plugin {plugin.PLUGIN_NAME}: {str(e)}")

            while self.handling:
                self.handle_client_connect()

        except Exception as e:
            logging.error(f"Error in main server loop: {str(e)}")

    def handle_client_connect(self):
        try:
            self.socket.settimeout(1)
            client_socket, client_address = self.socket.accept()
            logging.info(f"Connected client from {client_address[0]}")
            c_handler = PersonalClientHandler(client_socket, client_address, self)
            client_thread = threading.Thread(target=c_handler.handle)
            client_thread.start()
            self.clients.append((c_handler, client_thread))

        except socket.timeout:
            pass

        except Exception as e:
            logging.error(f"Error accepting client connection: {str(e)}")

    def load_plugins(self):
        if not os.path.exists(PLUGINS_DIR):
            logging.error(f"Plugins directory not found: {PLUGINS_DIR}")
            return

        for filename in os.listdir(PLUGINS_DIR):
            if filename.endswith(".py") and not filename.startswith("__"):
                try:
                    module_name = filename[:-3]
                    module = importlib.import_module(f"{PLUGINS_DIR}.{module_name}")
                    if hasattr(module, "Plugin"):
                        plugin = module.Plugin()
                        self.plugins.append(plugin)
                        logging.info(f"Loaded plugin: {module_name}")

                except Exception as e:
                    logging.error(f"Error loading plugin {filename}: {str(e)}")

    def stop(self):
        self.handling = False
        for handler, thread in self.clients:
            handler.stop()

        if self.socket:
            try:
                self.socket.close()

            except Exception as e:
                logging.error(f"Error closing server socket: {str(e)}")

        logging.info("Server shut down")

if __name__ == "__main__":
    srv = TCPServer()
    try:
        srv.main()
    except KeyboardInterrupt:
        logging.info("Server shutting down due to keyboard interrupt...")
    finally:
        srv.stop()
