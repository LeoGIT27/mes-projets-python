import tkinter as tk
from tkinter import ttk

from system_info import get_system_info

root = tk.Tk()
root.title("MacBenchmark")
root.geometry("650x500")

title = ttk.Label(
    root,
    text="MacBenchmark",
    font=("Arial", 22, "bold")
)
title.pack(pady=20)

info = get_system_info()

for cle, valeur in info.items():

    ttk.Label(
        root,
        text=f"{cle} : {valeur}",
        font=("Arial", 11)
    ).pack(anchor="w", padx=25)

root.mainloop()