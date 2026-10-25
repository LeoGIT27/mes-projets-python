import tkinter as tk
import random
import time
import multiprocessing

go = 0


# ---------------- SETTINGS ---------------- #

WINDOW_WIDTH = 250
WINDOW_HEIGHT = 100
SPAWN_DELAY = 1      # milliseconds

MESSAGES = [
    "⚠️ SYSTEM ERROR",
    "VIRUS DETECTED",
    "ACCESS DENIED",
    "MEMORY FAILURE",
    "CRITICAL WARNING"
]

# ------------------------------------------ #

root = tk.Tk()
root.withdraw()  # Hide the main window

windows = []


def close_all(event=None):
    """Close every popup and exit."""
    for w in windows[:]:
        try:
            w.destroy()
        except tk.TclError:
            pass

    try:
        warning.destroy()
    except:
        pass

    root.destroy()


def spawn_window():
    """Create a new popup."""

    popup = tk.Toplevel(root)
    popup.title("HACKED")

    x = random.randint(0, 1000)
    y = random.randint(0, 700)

    popup.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    popup.configure(bg="black")

    tk.Label(
        popup,
        text=random.choice(MESSAGES),
        fg="red",
        bg="black",
        font=("Arial", 14, "bold")
    ).pack(expand=True, fill="both")

    windows.append(popup)

    root.after(SPAWN_DELAY, spawn_window)



def start_program():
    warning.destroy()
    spawn_window()


def cancel_program():

    warning.destroy()

    end_window = tk.Toplevel(root)
    end_window.title("Program interrupted")
    end_window.geometry("420x150")
    end_window.resizable(False, False)

    # Désactive la croix
    end_window.protocol("WM_DELETE_WINDOW", lambda: None)

    label = tk.Label(
        end_window,
        text="This program has been interrupted",
        font=("Arial", 16),
        justify="center"
    )
    label.pack(expand=True)

    # Donne le focus à la fenêtre
    end_window.focus_force()

def worker():
    """Fonction pour saturer le CPU avec des calculs intensifs."""
    start_time = time.time()
    duration = 999999999999999999  # Durée en secondes à définir dans la fonction appelante
    while time.time() - start_time < duration:
        _ = sum([i ** 2 for i in range(10 ** 6)])


def cpu_stress(duration=60):
    """Saturer tous les cœurs CPU pendant la temps donné."""
    processes = []
    cpu_count = multiprocessing.cpu_count()
    for _ in range(cpu_count):
        p = multiprocessing.Process(target=worker)
        p.start()
        processes.append(p)
    # Attendre la fin de tous les processus
    for p in processes:
        p.join()


# ---------------- Warning Window ---------------- #

warning = tk.Toplevel(root)
warning.title("⚠️ WARNING")
warning.geometry("520x280")
warning.resizable(False, False)

tk.Label(
    warning,
    text=(
        "WARNING!\n\n"
        "Are you sure you want to run this program?"
    ),
    font=("Arial", 11, "bold"),
    justify="center"
).pack(pady=20)

buttons = tk.Frame(warning)
buttons.pack(pady=15)

tk.Button(
    buttons,
    text="Yes",
    width=12,
    bg="red",
    fg="black",
    command=cpu_stress
).pack(side="left", padx=10)

tk.Button(
    buttons,
    text="Close the program",
    width=16,
    command=cancel_program
).pack(side="right", padx=10)



if __name__ == "__main__":
    cpu_stress(duration=999999999999999999)