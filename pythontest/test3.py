import os
import subprocess
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def disable_windows_update():
    try:
        # Disable Windows Update service
        subprocess.run(["sc", "config", "wuauserv", "start=disabled"], check=True, shell=True)
        subprocess.run(["sc", "stop", "wuauserv"], check=True, shell=True)
        print("Windows Update service has been disabled.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable Windows Update: {e}")

if __name__ == "__main__":
    if is_admin():
        disable_windows_update()
    else:
        print("This script must be run as an administrator.")
        