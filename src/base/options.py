import json
import os
import socket
import threading
import uuid


OPTIONS_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "reremote")
OPTIONS_JSON = os.path.join(OPTIONS_PATH, "options.json")
LOCALHOST = socket.gethostbyname(socket.gethostname())


class Options:
    def __init__(self):
        self.__lock = threading.Lock()
        self.__options = {}
        self._setup_options_json()

    def _setup_options_json(self):
        with self.__lock:
            if not (os.path.isfile(OPTIONS_JSON)):
                if not (os.path.isdir(OPTIONS_PATH)):
                    os.mkdir(OPTIONS_PATH)
                with open(OPTIONS_JSON, "w", encoding="utf-8") as json_file:
                    default_options = {"custom_buttons": [], "ports": {}}
                    self.__options = default_options
                    json.dump(default_options, json_file, ensure_ascii=False, indent=4)
            else:
                with open(OPTIONS_JSON, "r", encoding="utf-8") as json_file:
                    options = json.load(json_file)

                    for key in ["port_frontend", "port_settings", "port_actions"]:
                        if key in options:
                            del options[key]

                    self.__options = options

    def _read_options_json(self):
        with self.__lock:
            with open(OPTIONS_JSON, "r", encoding="utf-8") as json_file:
                self.__options = json.load(json_file)
            return self.__options

    def _save_options(self):
        with self.__lock:
            with open(OPTIONS_JSON, "w", encoding="utf-8") as json_file:
                json.dump(self.__options, json_file, ensure_ascii=False, indent=4)

    def _add_key_value(self, key, value):
        with self.__lock:
            self.__options[key] = value

    def _get_options(self):
        with self.__lock:
            return self.__options

    # ports
    def _get_ports(self):
        with self.__lock:
            res = {"ip": LOCALHOST}
            for id in ["frontend", "settings", "actions"]:
                if id in self.__options["ports"]:
                    res[id] = self.__options["ports"][id]
                else:
                    res[id] = "loading"
            return res

    def _update_port(self, key, value):
        with self.__lock:
            self.__options["ports"][key] = value

    # custom button
    def _add_new_custom_button(self, button_data):
        self._remove_custom_button(button_data["custom_button_id"])
        with self.__lock:
            self.__options["custom_buttons"].append(button_data)

        self._save_options()

    def _remove_custom_button(self, custom_button_id):
        with self.__lock:
            for item in self.__options["custom_buttons"]:
                if (
                    "custom_button_id" in item
                    and item["custom_button_id"] == custom_button_id
                ):
                    self.__options["custom_buttons"].remove(item)
                    break
        self._save_options()

    def _get_custom_button(self, custom_button_id):
        with self.__lock:
            for item in self.__options["custom_buttons"]:
                if item["custom_button_id"] == custom_button_id:
                    return item
            return None

    def _get_custom_buttons(self):
        with self.__lock:
            return self.__options["custom_buttons"]

    def _get_simplified_custom_buttons(self):
        with self.__lock:
            res = []
            for button in self.__options["custom_buttons"]:
                res.append(
                    {
                        "custom_button_name": button["custom_button_name"],
                        "custom_button_id": button["custom_button_id"],
                        "button_name": "custom_button",
                    }
                )
            return res
