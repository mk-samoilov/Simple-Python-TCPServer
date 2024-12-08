# TCP Server with Plugin Support

#### plugins creating instruction: https://github.com/mk-samoilov/Simple-Python-TCPServer/blob/main/creating_plugins.md

> [!WARNING]
> By default, you can transfer data in a volume of no more than 1gb (1024mb), but you can increase this volume, since the server and client are open source.
> (You can change the value of the server's incoming data in the "config.py" file and of client in "client.py" file)

This Python script implements a TCP server that can handle multiple clients concurrently and supports plugins for processing client data. Here's a breakdown of the main components and their functionality:

## 1. Imports and Configuration

The script imports necessary modules and assumes there's a `config.py` file with configuration variables like `HOST`, `PORT`, `MAX_CLIENTS`, `LOADING_PLUGINS`, and `PLUGIN_DIR`.

## 2. PersonalClientHandler Class

This class handles individual client connections:

- Initialized with a client socket, address, and server reference.
- `handle()` method runs in a loop, receiving data from the client.
- `process_data()` method passes received data through loaded plugins.
- `stop()` method allows for graceful shutdown of the client handler.

## 3. TCPServer Class

This is the main server class:

- Initializes a TCP socket and binds it to the specified HOST and PORT.
- Loads plugins if `LOADING_PLUGINS` is True.
- `main()` method starts the server and listens for incoming connections.
- `handle_client_connect()` creates a new `PersonalClientHandler` for each client connection.
- `load_plugins()` dynamically loads Python modules from the `PLUGIN_DIR`.
- `stop()` method for graceful server shutdown.

## 4. Plugin System

- Plugins are loaded from a specified directory.
- Each plugin module should have a `Plugin` class.
- Plugins can implement a `process_client_pkg()` method to handle client data.
- Plugins can also implement a `server_started()` method that's called when the server starts.

## 5. Main Execution

- Creates a `TCPServer` instance.
- Runs the server's `main()` method.
- Handles KeyboardInterrupt for graceful shutdown.

## Key Features

1. **Concurrent Client Handling**: Uses threading to handle multiple clients simultaneously.
2. **Plugin Support**: Dynamically loads and uses plugins for processing client data.
3. **Graceful Shutdown**: Implements methods to stop the server and client handlers cleanly.
4. **Logging**: Prints timestamped log messages for server events.
