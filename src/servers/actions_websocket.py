import json
from websockets import WebSocketServerProtocol
from communication.response import WebsocketCommunication, create_parse_error_response
from servers.websocket_server import WebsocketServer


class ActionsWebsocket(WebsocketServer):
    def __init__(
        self,
        starting_port: int,
        id: str,
        _emit_event_to_listener,
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

                if com.request_name != "run_button":
                    self.emit_event("action requested: " + com.request_name)
                elif com.request["button_data"]["button_name"] == "custom_button":
                    self.emit_event(
                        "action requested: "
                        + com.request["button_data"]["custom_button_name"]
                    )
                elif com.request["button_data"]["button_name"] != "move_mouse":
                    self.emit_event(
                        "action requested: " + com.request["button_data"]["button_name"]
                    )

                await self.__process_request(com)
            except Exception as e:
                self.emit_event("error occurred while processing request: \n" + str(e))
                await com.send_error(str(e))

    async def __process_request(self, websocket_communication: WebsocketCommunication):
        match websocket_communication.request_name:
            case "get_simplified_custom_buttons":
                await websocket_communication.send_response(
                    True,
                    {
                        "custom_buttons_simplified": self._base._get_simplified_custom_buttons(),
                    },
                )

            case "run_button":
                self._base.doAction(websocket_communication.request["button_data"])
                await websocket_communication.send_ok()

            case _:
                raise Exception("button not found")
