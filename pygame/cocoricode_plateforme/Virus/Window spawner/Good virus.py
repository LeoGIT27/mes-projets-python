import tkinter as tk
import random
import time
from tkinter import messagebox

# =====================
# CONFIGURATION
# =====================
DURATION = 20          # Durée totale du prank (secondes)
MAX_WINDOWS = 60       # Nombre max de fenêtres
AFTER_DELAY = 0       # PLUS PETIT = PLUS RAPIDE (ms)

messages = [
    "⚠️ SYSTEM ERROR",
    "VIRUS DETECTED",
    "ACCESS DENIED",
    "MEMORY FAILURE",
    "CRITICAL WARNING"
]

# =====================
# FENÊTRE PRINCIPALE
# =====================
root = tk.Tk()
root.title("Warning")
root.geometry("300x120")
root.resizable(False, False)

windows = []
start_time = None

# =====================
# FONCTIONS
# =====================
def close_all():
    for w in windows:
        try:
            w.destroy()
        except:
            pass
    try:
        root.destroy()
    except:
        pass

def spawn_window():
    if time.time() - start_time >= DURATION or len(windows) >= MAX_WINDOWS:
        close_all()
        return

    w = tk.Toplevel()
    w.title("WARNING")
    w.geometry(
        f"260x110+{random.randint(0, 1000)}+{random.randint(0, 600)}"
    )
    w.configure(bg="black")

    tk.Label(
        w,
        text=random.choice(messages),
        fg="red",
        bg="black",
        font=("Arial", 14, "bold")
    ).pack(expand=True, fill="both")

    windows.append(w)

    # Apparition RAPIDE
    root.after(AFTER_DELAY, spawn_window)

def run_program():
    demo = tk.Toplevel()
    demo.title("Program")
    demo.geometry("300x150")
    tk.Label(
        demo,
        text="Program is running.\n(Warning accepted)",
        font=("Arial", 12),
        pady=20
    ).pack()

def execute():
    global start_time
    start_time = time.time()
    root.withdraw()   # cache la fenêtre principale
    spawn_window()
    run_program()

def do_not_execute():
    messagebox.showinfo("Information", "The program will not run")
    close_all()

# =====================
# INTERFACE
# =====================
tk.Label(
    root,
    text="Voulez-vous exécuter le programme ?",
    font=("Arial", 12),
    pady=10
).pack()

frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Exécuter", width=12, command=execute).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Ne pas exécuter", width=12, command=do_not_execute).grid(row=0, column=1, padx=5)

root.mainloop()