import tkinter as tk
import random
import time

# ---------------- SETTINGS ---------------- #

WINDOW_WIDTH = 250
WINDOW_HEIGHT = 100
SPAWN_DELAY = 1      # milliseconds
DURATION = 30          # seconds

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
start_time = None


def close_all(event=None):
    """Close every popup and exit."""
    for w in windows[:]:
        try:
            w.destroy()
        except tk.TclError:
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
    global start_time

    warning.destroy()

    start_time = time.time()

    spawn_window()


def cancel_program():
    close_all()


# ---------------- Warning Window ---------------- #

warning = tk.Toplevel(root)
warning.title("⚠️ WARNING")
warning.geometry("520x280")
warning.resizable(False, False)

tk.Label(
    warning,
    text=(
        "WARNING!"
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
    command=start_program
).pack(side="left", padx=10)

tk.Button(
    buttons,
    text="Close the program",
    width=12,
    command=cancel_program
).pack(side="right", padx=10)

root.mainloop()