import json
import socket
import subprocess

LOCALHOST = socket.gethostbyname(socket.gethostname())


def create_update(update_dic: dict | None = {}):
    update_dic["type"] = "update"
    return json.dumps(update_dic)


def find_powershell_path():
    try:
        result = subprocess.run(
            ["where", "powershell"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        if result.returncode == 0:
            return result.stdout.strip().splitlines()[0]
        else:
            print("Error: PowerShell executable not found.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_localhost():
    return LOCALHOST
