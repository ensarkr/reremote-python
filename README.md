# reremote-python

## About

reremote-python is a Python backend server application designed to enable users to remotely control their Windows PCs using an Android mobile application.         
The main project comprises three primary components: 
1. [reremote-react-native](https://github.com/ensarkr/reremote-react-native) - app with various controls 
2. [reremote-vue](https://github.com/ensarkr/reremote-vue) - settings served by windows app
3. `reremote-python` - windows backend app 


## Features

- Windows controls using pywin32 or subprocesses
    - Main controls
        - mouse 
        - media 
        - type 
        - numpad
    - Custom buttons can be added from settings 
        - to open apps
        - to run cmd or powershell commands

- Uses websocket to increase communication speed

## Servers

- `WEBSOCKET ACTIONS` Listens android app to run actions, served to local network
- `WEBSOCKET SETTINGS` Listens settings website to add new buttons, served only to local machine
- `HTTP FRONTEND` Serves settings website, served only to local machine

## How to Use

⚠️ app does not use any encryption or password system ⚠️        
⚠️ do not use it on unsafe networks ⚠️

#### Installing app
1. Download the reremote.exe from release.
2. Double-click to open.
3. Firewall will ask for access, `allow it`. It wont work otherwise.

#### Installing android app
1. Download the reremote.apk from [this repo's](https://github.com/ensarkr/reremote-react-native) release.
2. Install it to your android.


#### Connecting
1. Connect both your pc and android to same local network
2. On pc right click to apps tray icon to open settings
3. On the opened website check bottom right for websocket address of the app 
4. Open the setting on your android app
5. Write the address we found to there and click connect
6. On the next sessions app will automatically connect

#### Open app on startup
1. Add shortcut of reremote.exe to 
`C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`  

#### Adding custom buttons
1. On pc right click to apps tray icon to open settings
2. Go to buttons tab
3. Test and add new buttons


## To Run Dev Locally

```
$ pip install -r requirements.txt
$ python src/main.py
```

After this servers will try to serve until they find open ports.      
Check cli logs to see where they started.      

Default starting ports:
- `WEBSOCKET ACTIONS` 7171
- `WEBSOCKET SETTINGS` 7272
- `HTTP FRONTEND` 7373

## To Build

```
$  pyinstaller --clean --uac-admin --onefile --add-data "frontend/index.html:." --windowed --icon assets/app.ico  --name reremote  src/main.py  
```

## Technologies

- Python
- PyQt6
- pywin32
- websockets
- pyinstaller


## App Process

When app starts it creates 5 class instance.

1. `ReremoteBase` does actions and saves or reads options, injected to all classes below
2. `Window` pyqt app
3. `StaticServer` serves settings to local machine
4. `SettingsWebsocket` websocket that connects to setting, adds new buttons 
5. `ActionsWebsocket` websocket that connects to android app, listens and does requested actions

After creation, it starts event loop of last four instances, on different threads.   

Next, main thread starts main event loop which listens for custom events that other threads emitted.

#### asyncio
All threads uses asyncio to manage their events.         
asyncio lets rest of the code continue to run when its waiting for something like I/O-bound tasks which normally blocks the thread.
For example servers can answer other clients while waiting for one clients IO operation to finish.

#### threading in python
This app uses 5 different threads to run.    
Normally threading can achieve parallelism. But in CPython, because of GIL only one thread can run at a time.          
Because of this threading in python works kinda similar to asyncio.




