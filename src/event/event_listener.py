from abc import ABC, abstractmethod
import asyncio


class EventListener(ABC):
    def __init__(self):
        pass

    __is_event_running = True
    __event_stack = []
    __logs = []

    def _emit_event_to_listener(self, event_with_id: dict):
        self.__event_stack.append(event_with_id)

    async def __event_loop(self):
        while self.__is_event_running:
            if self.__event_stack.__len__() > 0:
                self._process_event(self.__event_stack.pop(0))
            await asyncio.sleep(0.001)

    def start_event_loop(self):
        print("event loop starting")
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.__event_loop())
        except KeyboardInterrupt:
            loop.close()
        finally:
            loop.close()

    def stop_event_loop(self):
        print("event loop stopping")
        self.__is_event_running = False

    def _add_log(self, log: str):
        print(log)
        self.__logs.append(log)

    def _get_logs(self):
        return self.__logs

    @abstractmethod
    def _process_event(self, event_with_id):
        pass
