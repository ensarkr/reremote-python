from http.server import HTTPServer, BaseHTTPRequestHandler

import pkg_resources
from base.reremote_base import ReremoteBase
from event.event_emitter import EventEmitter


class StaticServer(EventEmitter):
    def __init__(
        self, starting_port: int, id: str, _emit_event_to_listener, base: ReremoteBase
    ):
        super().__init__(_emit_event_to_listener, id)
        self.__starting_port = starting_port
        self.__base = base

    def initiate_server(self):
        self.main()

    def main(self):
        current_port = self.__starting_port

        while current_port < self.__starting_port + 20:
            try:
                http = HTTPServer(
                    ("localhost", self.__starting_port),
                    lambda *args, **kwargs: Server(
                        emit_event=self.emit_event, *args, **kwargs
                    ),
                )
                self.emit_event(
                    f"starting to serve on port {self.__starting_port}",
                    update_ports_on_clients=True,
                )
                self.__base._update_port(self.id, current_port)
                http.serve_forever()
                http.server_close()
            except OSError as e:
                self.emit_event("error occurred \n" + str(e))
                current_port += 1
                continue
            except Exception as e:
                self.emit_event("error occurred \n" + str(e))
                self.emit_event("try restarting app")
                break


class Server(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.__emit_event = kwargs.pop("emit_event")
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        # Override log_message to do nothing
        pass

    def do_GET(self):
        self.__emit_event("page requested")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        # build path
        html_path = pkg_resources.resource_filename(__name__, "../index.html")

        # dev path
        # html_path = "frontend/index.html"

        with open(html_path, "rb") as file:
            html_content = file.read()

        self.wfile.write(html_content)
