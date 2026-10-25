import ctypes
from ctypes import wintypes
import psutil
import time

user32 = ctypes.windll.user32

WM_CLOSE = 0x0010

# Processus qui ne seront JAMAIS fermés
IGNORED_PROCESSES = {
    "pycharm.exe",
    "code.exe",
    "python.exe",
    "pythonw.exe",
}


def get_window_title(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)

    if length == 0:
        return ""

    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)

    return buffer.value


def get_process_name(hwnd):
    process_id = wintypes.DWORD()

    user32.GetWindowThreadProcessId(
        hwnd,
        ctypes.byref(process_id)
    )

    try:
        process = psutil.Process(process_id.value)
        return process.name().lower()

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return ""


def close_window(hwnd):
    user32.PostMessageW(
        hwnd,
        WM_CLOSE,
        0,
        0
    )


def find_windows():
    windows = []

    def callback(hwnd, lparam):
        if not user32.IsWindowVisible(hwnd):
            return True

        title = get_window_title(hwnd)

        if not title:
            return True

        process_name = get_process_name(hwnd)

        if not process_name:
            return True

        if process_name in IGNORED_PROCESSES:
            return True

        windows.append((hwnd, process_name, title))

        return True

    callback_type = ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HWND,
        wintypes.LPARAM
    )

    callback_func = callback_type(callback)

    user32.EnumWindows(callback_func, 0)

    return windows


def fermeture_normale():
    windows = find_windows()

    print("=== FERMETURE NORMALE ===")

    for hwnd, process_name, title in windows:
        print("[FERMETURE]", process_name, "|", title)
        close_window(hwnd)


def fermeture_forcee():
    print()
    print("=== FERMETURE FORCÉE ===")

    processes = {}

    for process in psutil.process_iter(["pid", "name"]):
        try:
            name = process.info["name"]

            if not name:
                continue

            name = name.lower()

            if name in IGNORED_PROCESSES:
                continue

            processes[name] = process

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    for name, process in processes.items():

        try:
            print("[FORCÉ]", name)

            process.kill()

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


if __name__ == "__main__":

    print("=" * 60)
    print(" MODE TRÈS AGRESSIF")
    print("=" * 60)
    print()
    print("PyCharm, VS Code, Python et Windows sont protégés.")
    print("Les autres applications peuvent être forcées à se fermer.")
    print()

    input("Appuyez sur Entrée pour commencer...")

    fermeture_normale()

    print()
    print("Attente de 3 secondes...")
    time.sleep(3)

    fermeture_forcee()

    print()
    print("Terminé.")
    input("Appuyez sur Entrée pour quitter...")