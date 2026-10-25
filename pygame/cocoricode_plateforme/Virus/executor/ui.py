import threading
from benchmark_cpu import run_cpu_benchmark
import customtkinter as ctk
from system_info import get_system_info

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MacBenchmark")
        self.geometry("800x500")

        # Layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.title_label = ctk.CTkLabel(
            self.sidebar,
            text="MacBenchmark",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=20)

        self.btn_info = ctk.CTkButton(
            self.sidebar,
            text="Infos système",
            command=self.show_system_info
        )
        self.btn_info.pack(pady=10)

        self.btn_cpu = ctk.CTkButton(
            self.sidebar,
            text="CPU Benchmark",
            command=self.cpu_placeholder
        )
        self.btn_cpu.pack(pady=10)

        self.btn_gpu = ctk.CTkButton(
            self.sidebar,
            text="GPU Benchmark",
            command=self.gpu_placeholder
        )
        self.btn_gpu.pack(pady=10)

        # Zone principale
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.output = ctk.CTkTextbox(self.main_frame, width=500, height=400)
        self.output.pack(padx=10, pady=10)

        self.show_system_info()

    # ------------------------

    def show_system_info(self):
        self.output.delete("1.0", "end")

        info = get_system_info()

        for k, v in info.items():
            self.output.insert("end", f"{k} : {v}\n")

    def cpu_benchmark(self):
        self.output.delete("1.0", "end")
        self.output.insert("end", "CPU Benchmark en cours...\n")

        def task():
            result = run_cpu_benchmark(duration=5)

            self.output.delete("1.0", "end")
            self.output.insert("end", "🧠 CPU BENCHMARK TERMINÉ\n\n")
            self.output.insert("end", f"Temps : {result['temps']} s\n")
            self.output.insert("end", f"Iterations : {result['iterations']}\n")
            self.output.insert("end", f"Score CPU : {result['score_cpu']}\n")

        threading.Thread(target=task, daemon=True).start()

    def gpu_placeholder(self):
        self.output.delete("1.0", "end")
        self.output.insert("end", "GPU Benchmark à venir...\n")


# ------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()