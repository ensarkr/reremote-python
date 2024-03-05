import subprocess
import time
from base.options import Options
import win32api
import win32con
from helper.helper import find_powershell_path


class Actions(Options):
    def __init__(self):
        super().__init__()
        self.__powershell_path = find_powershell_path()

    def doAction(self, dict: dict):
        actions_params = {} if "button_params" not in dict else dict["button_params"]

        match dict["button_name"]:
            case "move_mouse":
                self.__move_mouse(**actions_params)
            case "mouse_click":
                self.__mouse_click(**actions_params)
            case "mouse_hold":
                self.__mouse_hold(**actions_params)
            case "increase_volume":
                self.__increase_volume()
            case "decrease_volume":
                self.__decrease_volume()
            case "mute_volume":
                self.__mute_volume()
            case "next_track":
                self.__next_track()
            case "previous_track":
                self.__previous_track()
            case "play_pause_track":
                self.__play_pause_track()
            case "stop_track":
                self.__stop_track()
            case "open_home_browser":
                self.__open_home_browser()
            case "type_string":
                self.__type_string(**actions_params)
            case "keyboard_click":
                self.__keyboard_click(**actions_params)
            case "custom_button":
                return self.__custom_button(dict["custom_button_id"])
            case _:
                raise Exception("button not found")

        return True

    def __custom_button(self, button_id: str):
        button_data = self._get_custom_button(button_id)
        if button_data is None:
            return False
        match button_data["custom_button_type"]:
            case "run_app":
                subprocess.Popen(
                    [button_data["app_path"]],
                    shell=True,
                )

            case "run_command":
                if button_data["cli"] == "cmd":
                    subprocess.Popen(
                        [button_data["command"]],
                        shell=True,
                    )
                elif button_data["cli"] == "powershell":
                    if self.__powershell_path is None:
                        return False
                    subprocess.Popen(
                        [self.__powershell_path, button_data["command"]],
                        shell=True,
                    )
        return True

    # main buttons

    def __move_mouse(self, x: float, y: float):
        old_x, old_y = win32api.GetCursorPos()
        win32api.SetCursorPos((int(old_x + x), int(old_y + y)))

    def __mouse_click(self, button: str):
        x, y = win32api.GetCursorPos()

        match button:
            case "left":
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y)
            case "right":
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y)
            case "middle":
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, x, y)
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, x, y)
            case _:
                raise Exception("button not found")

    def __mouse_hold(self, button: str):
        x, y = win32api.GetCursorPos()

        match button:
            case "left":
                if win32api.GetKeyState(win32con.VK_LBUTTON) > -1:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)
                else:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y)
            case "right":
                if win32api.GetKeyState(win32con.VK_RBUTTON) > -1:
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y)
                else:
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y)
            case _:
                raise Exception("button not found")

    def __click_key(self, key: int):
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        win32api.keybd_event(
            key, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0
        )

    def __increase_volume(self):
        VK_VOLUME_UP = 0xAF
        self.__click_key(VK_VOLUME_UP)

    def __decrease_volume(self):
        VK_VOLUME_DOWN = 0xAE
        self.__click_key(VK_VOLUME_DOWN)

    def __mute_volume(self):
        VK_MUTE_VOLUME = 0xAD
        self.__click_key(VK_MUTE_VOLUME)

    def __play_pause_track(self):
        VK_MEDIA_PLAY_PAUSE = 0xB3
        self.__click_key(VK_MEDIA_PLAY_PAUSE)

    def __previous_track(self):
        VK_MEDIA_PREV_TRACK = 0xB1
        self.__click_key(VK_MEDIA_PREV_TRACK)

    def __next_track(self):
        VK_MEDIA_NEXT_TRACK = 0xB0
        self.__click_key(VK_MEDIA_NEXT_TRACK)

    def __stop_track(self):
        VK_MEDIA_STOP = 0xB2
        self.__click_key(VK_MEDIA_STOP)

    def __type_string(self, string: str):
        VK_LSHIFT = 0xA0
        VK_CONTROL = 0x11
        VK_ALT = 0x12

        for char in string:
            scan = win32api.VkKeyScan(char)

            low, high = scan & 0xFF, (scan >> 8) & 0xFF

            if low == -1 or high == -1:
                continue

            if (high >> 2 & 1) == 1:
                win32api.keybd_event(VK_ALT, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)

            if (high >> 1 & 1) == 1:
                win32api.keybd_event(VK_CONTROL, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)

            if (high & 1) == 1:
                win32api.keybd_event(VK_LSHIFT, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)

            self.__click_key(low)

            if (high >> 2 & 1) == 1:
                win32api.keybd_event(
                    VK_ALT,
                    0,
                    win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP,
                    0,
                )

            if (high >> 1 & 1) == 1:
                win32api.keybd_event(
                    VK_CONTROL,
                    0,
                    win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP,
                    0,
                )

            if (high & 1) == 1:
                win32api.keybd_event(
                    VK_LSHIFT,
                    0,
                    win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP,
                    0,
                )

    def __keyboard_click(self, key: str):
        VK_TAB = 0x09
        VK_CAPITAL = 0x14
        VK_BACK = 0x08
        VK_ESCAPE = 0x1B
        VK_LWIN = 0x5B
        VK_NUMLOCK = 0x90
        VK_SNAPSHOT = 0x2C
        VK_SCROLL = 0x91
        VK_PAUSE = 0x13
        VK_INSERT = 0x2D
        VK_HOME = 0x24
        VK_PRIOR = 0x21
        VK_DELETE = 0x2E
        VK_END = 0x23
        VK_NEXT = 0x22
        VK_RETURN = 0x0D
        VK_SPACE = 0x20
        VK_LEFT = 0x25
        VK_UP = 0x26
        VK_RIGHT = 0x27
        VK_DOWN = 0x28

        VK_NUMPAD0 = 0x60
        VK_NUMPAD1 = 0x61
        VK_NUMPAD2 = 0x62
        VK_NUMPAD3 = 0x63
        VK_NUMPAD4 = 0x64
        VK_NUMPAD5 = 0x65
        VK_NUMPAD6 = 0x66
        VK_NUMPAD7 = 0x67
        VK_NUMPAD8 = 0x68
        VK_NUMPAD9 = 0x69
        VK_MULTIPLY = 0x6A
        VK_ADD = 0x6B
        VK_SUBTRACT = 0x6D
        VK_DECIMAL = 0x6E
        VK_DIVIDE = 0x6F

        match key:
            case "tab":
                self.__click_key(VK_TAB)
            case "caps_lock":
                self.__click_key(VK_CAPITAL)
            case "backspace":
                self.__click_key(VK_BACK)
            case "esc":
                self.__click_key(VK_ESCAPE)
            case "windows":
                self.__click_key(VK_LWIN)
            case "num_lock":
                self.__click_key(VK_NUMLOCK)
            case "PS":
                self.__click_key(VK_SNAPSHOT)
            case "SL":
                self.__click_key(VK_SCROLL)
            case "PB":
                self.__click_key(VK_PAUSE)
            case "insert":
                self.__click_key(VK_INSERT)
            case "home":
                self.__click_key(VK_HOME)
            case "page_up":
                self.__click_key(VK_PRIOR)
            case "delete":
                self.__click_key(VK_DELETE)
            case "end":
                self.__click_key(VK_END)
            case "page_down":
                self.__click_key(VK_NEXT)
            case "enter":
                self.__click_key(VK_RETURN)
            case "space":
                self.__click_key(VK_SPACE)
            case "left_arrow":
                self.__click_key(VK_LEFT)
            case "down_arrow":
                self.__click_key(VK_DOWN)
            case "up_arrow":
                self.__click_key(VK_UP)
            case "right_arrow":
                self.__click_key(VK_RIGHT)
            case "divide":
                self.__click_key(VK_DIVIDE)
            case "multiply":
                self.__click_key(VK_MULTIPLY)
            case "subtract":
                self.__click_key(VK_SUBTRACT)
            case "add":
                self.__click_key(VK_ADD)
            case "decimal":
                self.__click_key(VK_DECIMAL)
            case "numpad_0":
                self.__click_key(VK_NUMPAD0)
            case "numpad_1":
                self.__click_key(VK_NUMPAD1)
            case "numpad_2":
                self.__click_key(VK_NUMPAD2)
            case "numpad_3":
                self.__click_key(VK_NUMPAD3)
            case "numpad_4":
                self.__click_key(VK_NUMPAD4)
            case "numpad_5":
                self.__click_key(VK_NUMPAD5)
            case "numpad_6":
                self.__click_key(VK_NUMPAD6)
            case "numpad_7":
                self.__click_key(VK_NUMPAD7)
            case "numpad_8":
                self.__click_key(VK_NUMPAD8)
            case "numpad_9":
                self.__click_key(VK_NUMPAD9)
            case _:
                raise Exception("key not found")
