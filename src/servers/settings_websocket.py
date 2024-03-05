import json
import subprocess
from websockets import WebSocketServerProtocol
from communication.response import WebsocketCommunication, create_parse_error_response
from helper.helper import  find_powershell_path
from servers.websocket_server import WebsocketServer


class SettingsWebsocket(WebsocketServer):
    def __init__(
        self,
        starting_port: int,
        id: str,
        _emit_event_to_listener,
        get_logs,
        base,
        serve_to_only_local_machine=True,
    ):
        super().__init__(
            starting_port,
            id,
            _emit_event_to_listener,
            base,
            serve_to_only_local_machine,
        )
        self.__powershell_path = find_powershell_path()
        self.__get_logs = get_logs

    async def process_client(self, websocket: WebSocketServerProtocol):
        self._append_client(websocket)
        self.emit_event(
            "client connected for action: " + str(websocket.remote_address[1])
        )
        self.emit_event("listening for action")

        while True:
            json_string = await websocket.recv()

            try:
                com = WebsocketCommunication(websocket, json_string)
            except Exception as e:
                self.emit_event("error occurred while parsing: \n" + str(e))
                await websocket.send(create_parse_error_response())
                continue

            try:
                self.emit_event("action requested: " + com.request_name)
                await self.__process_request(com)

            except Exception as e:
                self.emit_event("error occurred while processing request: \n" + str(e))
                await websocket.send(com.send_error(str(e)))

    async def __process_request(self, websocket_communication: WebsocketCommunication):
        match websocket_communication.request_name:
            case "get_logs":
                await websocket_communication.send_response(
                    True, {"logs": self.__get_logs()}
                )

            case "get_custom_buttons":
                await websocket_communication.send_response(
                    True,
                    {
                        "custom_buttons": self._base._get_custom_buttons(),
                    },
                )

            case "run_app":
                subprocess.Popen(
                    [websocket_communication.request["app_path"]],
                    shell=True,
                )
                await websocket_communication.send_ok()

            case "run_command":
                if websocket_communication.request["cli"] == "cmd":
                    subprocess.Popen(
                        [websocket_communication.request["command"]],
                        shell=True,
                    )
                elif websocket_communication.request["cli"] == "powershell":
                    if self.__powershell_path is None:
                        await websocket_communication.send_error("powershell not found")
                        return

                    subprocess.Popen(
                        [
                            self.__powershell_path,
                            websocket_communication.request["command"],
                        ],
                        shell=True,
                    )

                await websocket_communication.send_ok()

            case "add_custom_button":
                self._base._add_new_custom_button(
                    websocket_communication.request["custom_button_data"]
                )
                self.emit_event(
                    f"new custom button added: {websocket_communication.request["custom_button_data"]["custom_button_name"]}", update_buttons_on_clients=True
                )
                await websocket_communication.send_ok()

            case "remove_custom_button":
                self._base._remove_custom_button(
                    websocket_communication.request["custom_button_id"]
                )
                self.emit_event("removed custom button", update_buttons_on_clients=True)
                await websocket_communication.send_ok()

            case "get_ports":
                await websocket_communication.send_response(
                    True, {"ports": self._base._get_ports()}
                )
