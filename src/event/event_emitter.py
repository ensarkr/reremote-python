class EventEmitter:
    def __init__(self, _emit_event_to_listener, id: str):
        self.id = id
        self.__emit_event_to_listener = _emit_event_to_listener

    def emit_event(
        self,
        log: str,
        update_buttons_on_clients: bool | None = False,
        update_ports_on_clients: bool | None = False,
    ):
        event = {}
        event["log"] = f"[{self.get_ui_name(self.id)}] " + log
        event["update_buttons_on_clients"] = update_buttons_on_clients
        event["update_ports_on_clients"] = update_ports_on_clients
        self.__emit_event_to_listener(event)

    def get_ui_name(self, str):
        match str:
            case "frontend":
                return "HTTP SETTINGS"
            case "settings":
                return "WEBSOCKET SETTINGS"
            case "actions":
                return "WEBSOCKET ACTIONS"
