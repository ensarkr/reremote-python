import json

import websockets


class WebsocketCommunication:
    def __init__(
        self, websocket: websockets.WebSocketServerProtocol, request_json_string: str
    ):
        request_json = json.loads(request_json_string)
        if ("con_id" not in request_json):
            raise Exception("connection identifier not found")
        self.__websocket = websocket
        self.__response = {"type": "response", "con_id": request_json["con_id"]}
        self.request_name = request_json["name"]
        self.request = request_json

    async def send_ok(self):
        res = self.__response.copy()
        res["status"] = True
        await self.__websocket.send(json.dumps(res))

    async def send_error(self, error_message: str):
        res = self.__response.copy()
        res["status"] = False
        res["error_message"] = error_message
        await self.__websocket.send(json.dumps(res))

    async def send_response(self, status: bool, res_dict: dict):
        res = self.__response.copy()
        res["status"] = status
        res["value"] = res_dict
        await self.__websocket.send(json.dumps(res))


def create_parse_error_response():
    res = {"type": "response", "status": False, "error_message": "parsing error"}
    return json.dumps(res)
