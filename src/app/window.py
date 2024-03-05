
from PyQt6.QtGui import QIcon,QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
)
from PyQt6.QtCore import QByteArray
import webbrowser
from base.reremote_base import ReremoteBase





class Window:
    def __init__(self, stop_event_loop, base:ReremoteBase):
        super().__init__()
        self.__stop_event_loop = stop_event_loop
        self.__base = base

    def start_app(self):
        app = QApplication([])
        app.aboutToQuit.connect(self.__stop_event_loop)
        base64_icon = b"iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAnNJREFUSEt9VluWmzAMlehpwTCLYFZSspIhKwlZSTIrmXQlYRGDHdozqEd+gIyd8RcxSFf36hUEcRAAyP7entZf8dX2TXIfW/Nrf4OAQB4ghk3urdNnnv29/0YArDjWODidp8+BAAER3wCwBaDRElzoVhTFn59KXWU47GULiJ+fHGNMVxBdAKCVLIOIwmwEWt7L5mXYKevMcmznaRoI8RTQOS8R1VziiM5l0wwxg50dO3l8TgMUeMoTy+gui2IF2ayjwLwsH4zL6Xb0nonoXu01RsRjqdQ11IDwgfDQ0x295sG4rOsExxjTFstXD1icUt1xLGv1GsJajf8a05NLasSvVDGAJMW5AnRySjZfiIdaqZvLhz/zNF0Isd9TDgweWpOUjoG1Me0PoPteRgK4VXV9CC1mIWat7wTQ7vWIAXw0CMAAVqoEwHIcy7p+jRnYCNMT5yDO+mOaBrQS+aLwFUVAY2UBRBHMAUD68JHmiul5r7h8VE2NdiIEY5Zo7dpQGh7AS8h2ljpLg0QXBOhSzlKi0MncYFp/5Az2SQZazuVLMxht2oKIg0qmLxFdq6Y5RhIZozskYJDoJABA44J4VErdZGnLMuVm+1WrK2u1+ltpI3T8QjaakCiA76TCzna+e+sraOO2boh/xvQL0CU767cKyY6QENCCeGB2IRKhiJvjXHp2BHw3hJLM+lJZyOZHjoJkH7g5s/RhBOxrXAJL3YnoXNlxvTVjlIN9UFYuIm4i3mKZFly7Y016rlGjaSodsbmfNR0t9BsQueZ5u4WV+c4O3ZKRx6/MaCfnoHNcfdnl9n0Msf07ebIJZRTfqZMVRWwphP/dB2AxOW6SzwAAAABJRU5ErkJggg=="
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray.fromBase64(base64_icon))
        icon = QIcon(pixmap)
        tray_icon = QSystemTrayIcon(icon)
        tray_icon.setToolTip("REREMOTE")
        menu = QMenu()
        action_settings = menu.addAction("Settings")
        menu.addSeparator()
        action_quit = menu.addAction("Quit")
        action_settings.triggered.connect(self.__open_settings)
        action_quit.triggered.connect(app.quit)
        
        tray_icon.setContextMenu(menu)
        tray_icon.show()
        app.exec()

    
    def __get_current_settings_url(self):
        options = self.__base._get_options()
        if "frontend" not in options["ports"]:
            raise Exception("url not set")
        
        return f"http://localhost:{options["ports"]["frontend"]}"
        
    def __open_settings(self):
        try:
            url = self.__get_current_settings_url()
            webbrowser.open(url)
        except Exception as e:
            print(str(e))

            

