import tkinter as tk
from tkinter import ttk
import random

messages = [
    "Analyse des processus système...",
    "Vérification des signatures de sécurité...",
    "Scan des fichiers système...",
    "Analyse des connexions réseau...",
    "Vérification des extensions navigateur...",
    "Analyse heuristique en cours...",
    "Recherche d'activités suspectes...",
    "Scan des zones critiques..."
]

results = [
    "Aucune menace détectée.",
    "Système sain, aucune action requise.",
    "Aucun malware identifié.",
    "Analyse terminée sans anomalie."
]

scan_running = False
after_id = None


def start_scan():
    global scan_running

    if scan_running:
        return

    scan_running = True

    progress["value"] = 0
    percent.config(text="0 %")
    status.config(text="Analyse en cours...")
    log_box.delete("1.0", tk.END)

    scan_btn.config(state="disabled")
    stop_btn.config(state="normal")

    add_log("Démarrage du scan complet du système")
    loop()


def loop():
    global after_id, scan_running

    if not scan_running:
        return

    value = progress["value"]

    if value >= 100:
        finish()
        return

    # messages plus rares (réalisme)
    if random.randint(1, 5) == 1:
        msg = random.choice(messages)
        status.config(text=msg)
        add_log(msg)

    # progression plus lente
    progress["value"] = min(
        100,
        value + random.choice([1, 1, 1, 2])
    )

    percent.config(text=f"{int(progress['value'])} %")

    delay = random.randint(250, 900)

    after_id = root.after(delay, loop)


def stop_scan():
    global scan_running, after_id

    scan_running = False

    if after_id:
        root.after_cancel(after_id)
        after_id = None

    status.config(text="Analyse interrompue")
    add_log("Scan interrompu par l'utilisateur")

    result.config(text="❌ Analyse interrompue", fg="#ef4444")

    scan_btn.config(state="normal")
    stop_btn.config(state="disabled")


def finish():
    global scan_running

    scan_running = False

    status.config(text="Analyse terminée")
    percent.config(text="100 %")

    result.config(
        text="✔ " + random.choice(results),
        fg="#22c55e"
    )

    add_log("Analyse terminée avec succès")

    scan_btn.config(state="normal")
    stop_btn.config(state="disabled")

def add_log(text):
    log_box.insert(tk.END, f"• {text}\n")
    log_box.see(tk.END)


def on_enter(btn, color):
    btn.config(bg=color)

def on_leave(btn, color):
    btn.config(bg=color)


root = tk.Tk()
root.title("Security")
root.geometry("560x460")
root.resizable(False, False)
root.configure(bg="#0b0f19")


header = tk.Frame(root, bg="#111827", height=60)
header.pack(fill="x")

title = tk.Label(
    header,
    text="Safe scan",
    font=("Segoe UI", 16, "bold"),
    fg="white",
    bg="#111827"
)
title.pack(pady=15)


status = tk.Label(
    root,
    text="Prêt à analyser le système",
    font=("Segoe UI", 11),
    bg="#0b0f19",
    fg="#e5e7eb"
)
status.pack(pady=10)


percent = tk.Label(
    root,
    text="0 %",
    font=("Segoe UI", 14, "bold"),
    bg="#0b0f19",
    fg="#e5e7eb"
)
percent.pack()

progress = ttk.Progressbar(
    root,
    length=500,
    mode="determinate"
)
progress.pack(pady=10)


scan_btn = tk.Button(
    root,
    text="Lancer l'analyse",
    font=("Segoe UI", 11, "bold"),
    width=22,
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    relief="flat",
    cursor="hand2",
    command=start_scan
)
scan_btn.pack(pady=6)

scan_btn.bind("<Enter>", lambda e: on_enter(scan_btn, "#1d4ed8"))
scan_btn.bind("<Leave>", lambda e: on_leave(scan_btn, "#2563eb"))


stop_btn = tk.Button(
    root,
    text="Arrêter l'analyse",
    font=("Segoe UI", 11, "bold"),
    width=22,
    bg="#ef4444",
    fg="white",
    activebackground="#dc2626",
    relief="flat",
    cursor="hand2",
    state="disabled",
    command=stop_scan
)
stop_btn.pack(pady=6)

stop_btn.bind("<Enter>", lambda e: on_enter(stop_btn, "#dc2626"))
stop_btn.bind("<Leave>", lambda e: on_leave(stop_btn, "#ef4444"))


result = tk.Label(
    root,
    text="",
    font=("Segoe UI", 11, "bold"),
    bg="#0b0f19",
    fg="#e5e7eb"
)
result.pack(pady=10)


panel = tk.Frame(root, bg="#111827")
panel.pack(pady=10, padx=15, fill="both", expand=True)

log_box = tk.Text(
    panel,
    font=("Consolas", 9),
    bg="#0b0f19",
    fg="#d1d5db",
    insertbackground="white",
    relief="flat"
)
log_box.pack(fill="both", expand=True, padx=5, pady=5)


root.mainloop()