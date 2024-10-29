
# Plugin Creation Guide

This guide explains how to create plugins for our system using the `BasePlugin` class.

## Table of Contents

1. [Plugin Structure](#plugin-structure)
2. [Creating a New Plugin](#creating-a-new-plugin)
3. [Plugin Methods](#plugin-methods)
4. [Handling Client Packages](#handling-client-packages)
5. [Example: ZipTransferPlugin](#example-ziptransferplugin)

## Plugin Structure

Each plugin should be a Python class that inherits from the `BasePlugin` class. The basic structure of a plugin is as follows:

```python
from plugins import BasePlugin

class Plugin(BasePlugin):
    PLUGIN_NAME = "YourPluginName"
    PLUGIN_DIR = f"plugins/{PLUGIN_NAME}" # Or None for not creating directory

    def __init__(self):
        super().__init__()

    def server_inited(self):
        pass

    def server_started(self):
        pass

    def process_client_pkg(self, data):
        # Handle client packages here
        pass
```

## Creating a New Plugin

1. Create a new Python file in the `plugins` server directory.
2. Import the `BasePlugin` class.
3. Define your `Plugin` class, inheriting from `BasePlugin`.
4. Set the `PLUGIN_NAME` and `PLUGIN_DIR` class variables.
5. Implement the required methods.

## Plugin Methods

### `__init__(self)`

The constructor for your plugin. Always call the superclass constructor using `super().__init__()`.

### `server_inited(self)`

This method is called when the server is initialized. Use it for any setup tasks that need to be performed before the server starts.

### `server_started(self)`

This method is called when the server has started. Use it for any tasks that should be performed once the server is running.

### `process_client_pkg(self, data)`

This method is called to process packages received from clients. It should return a response or `None` if no response is needed.

## Handling Client Packages

The `process_client_pkg` method is where you'll implement the main functionality of your plugin. This method receives data from the client and should return a response.

- Parse the incoming data to determine what action to take.
- Perform the requested action.
- Return a response to the client, or `None` if no response is needed.

## Example: ZipTransferPlugin

Here's an example of a plugin that handles file transfers:

```python
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
```

This plugin demonstrates how to handle different types of client requests:

- Listing files in the plugin directory
- Uploading files to the plugin directory
- Downloading files from the plugin directory

Remember to handle exceptions and validate input data in your actual implementation to ensure robustness and security.
