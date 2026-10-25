import tkinter as tk
import threading
import math
import time
import random

DURATION = 60          # Durée du test (secondes)
NUM_WINDOWS = 10       # Nombre de fenêtres
THREADS_PER_WINDOW = 10 # Calculs par fenêtre

running = True

def heavy_calculation():
    x = random.random() + 1
    while running:
        for _ in range(200000):
            x = math.sin(x) * math.cos(x)
            x += math.sqrt(abs(x) + 1)

root = tk.Tk()
root.title("Stress Test")
root.geometry("350x120")

tk.Label(
    root,
    text="Stress test CPU en cours...",
    font=("Arial", 14)
).pack(pady=15)

countdown = tk.Label(root, font=("Arial", 12))
countdown.pack()

# Création des fenêtres
for i in range(NUM_WINDOWS):
    w = tk.Toplevel(root)
    w.title(f"Calcul {i+1}")
    w.geometry(f"240x90+{100+i*40}+{100+i*40}")
    tk.Label(
        w,
        text=f"Threads actifs : {THREADS_PER_WINDOW}",
        font=("Arial", 11)
    ).pack(expand=True)

    for _ in range(THREADS_PER_WINDOW):
        threading.Thread(target=heavy_calculation, daemon=True).start()

start = time.time()

def update():
    remaining = max(0, int(DURATION - (time.time() - start)))
    countdown.config(text=f"Temps restant : {remaining} s")

    if remaining == 0:
        stop()
    else:
        root.after(1000, update)

update()
root.mainloop()