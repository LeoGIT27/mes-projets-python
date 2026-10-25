import multiprocessing
import torch
import time


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

if __name__ == "__main__":
    print("Démarrage du stress CPU...")
    cpu_stress(duration=999999999999999999),
    print("Stress CPU terminé.")