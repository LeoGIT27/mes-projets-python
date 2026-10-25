import platform
import subprocess
import psutil


def get_system_info():
    info = {}

    info["Nom"] = platform.node()
    info["Système"] = platform.system()
    info["Version"] = platform.release()
    info["Architecture"] = platform.machine()

    info["CPU"] = platform.processor()

    info["Cœurs physiques"] = psutil.cpu_count(False)
    info["Cœurs logiques"] = psutil.cpu_count(True)

    info["RAM"] = round(psutil.virtual_memory().total / (1024**3), 2)

    try:
        gpu = subprocess.check_output(
            ["system_profiler", "SPDisplaysDataType"],
            text=True
        )

        for ligne in gpu.split("\n"):

            if "Chipset Model" in ligne:
                info["GPU"] = ligne.split(":")[1].strip()

            if "Metal Support" in ligne:
                info["Metal"] = ligne.split(":")[1].strip()

    except Exception:
        info["GPU"] = "Inconnu"

    return info