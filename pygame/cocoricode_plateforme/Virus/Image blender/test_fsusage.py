import subprocess

print("Démarrage de fs_usage...")
print("Appuie sur Ctrl+C pour arrêter.")
print()

processus = subprocess.Popen(
    ["fs_usage", "-w", "-f", "filesys"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

try:
    for ligne in processus.stdout:
        print(ligne, end="")

except KeyboardInterrupt:
    print("\nArrêt...")
    processus.terminate()