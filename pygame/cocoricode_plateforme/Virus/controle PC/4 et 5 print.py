import ctypes
from ctypes import wintypes
import psutil
import time

user32 = ctypes.windll.user32

WM_CLOSE = 0x0010

# Processus que le programme ne doit JAMAIS fermer
IGNORED_PROCESSES = {
    "pycharm.exe",
    "code.exe",
    "python.exe",
    "pythonw.exe",

    # Windows
    "explorer.exe",
    "dwm.exe",
    "winlogon.exe",
    "csrss.exe",
    "services.exe",
    "lsass.exe",
    "svchost.exe",
    "System",
    "System Idle Process",
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


def enum_windows_callback(hwnd, lparam):

    if not user32.IsWindowVisible(hwnd):
        return True

    title = get_window_title(hwnd)

    if not title:
        return True

    process_name = get_process_name(hwnd)

    if not process_name:
        return True

    # Protection
    if process_name in IGNORED_PROCESSES:
        print("[PROTEGE]   {} | {}".format(
            process_name,
            title
        ))
        return True

    print("[FERMETURE] {} | {}".format(
        process_name,
        title
    ))

    # Demande de fermeture normale
    user32.PostMessageW(
        hwnd,
        WM_CLOSE,
        0,
        0
    )

    return True


EnumWindowsProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM
)


def fermer_fenetres():

    callback = EnumWindowsProc(
        enum_windows_callback
    )

    user32.EnumWindows(callback, 0)


if __name__ == "__main__":

    print("=" * 70)
    print("FERMETURE DES FENETRES")
    print("=" * 70)
    print()

    fermer_fenetres()

    print()
    print("Fermeture demandee.")
    print("Attente de quelques secondes...")

    time.sleep(3)

    print("Termine.")