from app.window import Window
from base.actions import Actions
from base.reremote_base import ReremoteBase
from event.event_listener import EventListener
from helper.helper import create_update
from servers.actions_websocket import ActionsWebsocket
from servers.settings_websocket import SettingsWebsocket
from servers.static_server import StaticServer
import threading


class Main(EventListener):
    def __init__(self):
        super().__init__()

        self.__base = ReremoteBase()
        self.app = Window(self.stop_event_loop, self.__base)
        self.frontend_http = StaticServer(
            7373, "frontend", self._emit_event_to_listener, self.__base
        )
        self.settings_ws = SettingsWebsocket(
            7272, "settings", self._emit_event_to_listener, self._get_logs, self.__base
        )
        self.actions_ws = ActionsWebsocket(
            7171, "actions", self._emit_event_to_listener, self.__base, False
        )

        threading.Thread(target=self.app.start_app, daemon=True).start()
        threading.Thread(target=self.frontend_http.initiate_server, daemon=True).start()
        threading.Thread(target=self.settings_ws.initiate_server, daemon=True).start()
        threading.Thread(target=self.actions_ws.initiate_server, daemon=True).start()

        self.start_event_loop()

    def _process_event(self, event: dict):
        self._add_log(event["log"])

        self.settings_ws.send_message_to_all_clients(
            create_update({"log": event["log"]})
        )

        if event["update_buttons_on_clients"]:
            self.settings_ws.send_message_to_all_clients(
                create_update(
                    {"custom_buttons": self.__base._get_options()["custom_buttons"]}
                )
            )
            self.actions_ws.send_message_to_all_clients(
                create_update(
                    {"custom_buttons": self.__base._get_options()["custom_buttons"]}
                )
            )

        if event["update_ports_on_clients"]:
            self.settings_ws.send_message_to_all_clients(
                create_update({"ports": self.__base._get_ports()})
            )


if __name__ == "__main__":
    Main()
