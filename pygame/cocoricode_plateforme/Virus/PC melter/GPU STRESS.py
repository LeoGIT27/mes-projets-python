import multiprocessing
import torch
import time


def worker():
    """Fonction pour saturer le CPU avec des calculs intensifs."""
    start_time = time.time()
    duration = 999999999999999999  # Durée en secondes à définir dans la fonction appelante
    while time.time() - start_time < duration:
        _ = sum([i ** 2 for i in range(10 ** 6)])

def gpu_stress(duration=999999999999999999):
    """Saturer le GPU pendant la durée donnée."""
    if torch.cuda.is_available():
        start_time = time.time()
        device = torch.device("cuda")
        while time.time() - start_time < duration:
            a = torch.randn(1000000000, 1000000000, device=device)
            b = torch.randn(1000000000, 1000000000, device=device)
            torch.matmul(a, b)
    else:
        print("GPU non disponible.")


if __name__ == "__main__":
    print("Démarrage du stress GPU...")
    gpu_stress(duration=999999999999999999)
    print("Stress GPU terminé.")