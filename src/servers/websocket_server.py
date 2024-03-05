from abc import ABC, abstractmethod
import asyncio
import websockets
import json
from base.reremote_base import ReremoteBase
from event.event_emitter import EventEmitter


class WebsocketServer(ABC, EventEmitter):
    def __init__(
        self,
        starting_port: int,
        id: str,
        _emit_event_to_listener,
        base: ReremoteBase,
        serve_to_only_local_machine=True,
    ):
        super().__init__(_emit_event_to_listener, id)
        self.__starting_port = starting_port
        self.__serve_to_only_local_machine = serve_to_only_local_machine
        self.__clients = []
        self._base = base

    def initiate_server(self):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.main())

    async def main(self):
        current_port = self.__starting_port

        while current_port < self.__starting_port + 20:
            try:
                self.emit_event("trying to serve websocket at " + str(current_port))
                self.server = await websockets.serve(
                    self.process_client,
                    "localhost" if self.__serve_to_only_local_machine else "0.0.0.0",
                    current_port,
                )
                self.emit_event(
                    "successfully serving websocket at " + str(current_port),
                    update_ports_on_clients=True,
                )
                self._base._update_port(self.id, current_port)
                await self.server.wait_closed()
            except OSError as e:
                self.emit_event("error occurred \n" + str(e))
                current_port += 1
                continue
            except Exception as e:
                self.emit_event("error occurred \n" + str(e))
                self.emit_event("try restarting app")
                break

    @abstractmethod
    async def process_client(self, websocket: websockets.WebSocketServerProtocol):
        pass

    def _append_client(self, client):
        self.__clients.append(client)

    def send_message_to_all_clients(self, message: str):
        # if hasattr(self, "loop"):
        #     self.loop.create_task(self.__send_message_to_all_clients(message))

        # it uses main loop while sending it to clients
        asyncio.get_running_loop().create_task(
            self.__send_message_to_all_clients(message)
        )

    async def __send_message_to_all_clients(self, message: str):
        for client in self.__clients:
            try:
                await client.send(message)
            except Exception as e:
                print(str(e))
                if str(e).find("1001") is not -1:
                    self.__clients.remove(client)
