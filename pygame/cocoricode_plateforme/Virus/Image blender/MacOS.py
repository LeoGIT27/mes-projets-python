import subprocess
import os
import signal
import sys


# ============================================================
# CONFIGURATION
# ============================================================

# Dossier à surveiller.
DOSSIER_A_SURVEILLER = os.path.expanduser("~/Desktop")

# Extensions à surveiller.
EXTENSIONS = {
    ".txt",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".pdf",
}


# ============================================================
# VERIFICATION DU FICHIER
# ============================================================

def fichier_interessant(chemin):

    chemin = os.path.abspath(chemin)
    dossier = os.path.abspath(DOSSIER_A_SURVEILLER)

    try:
        if os.path.commonpath([chemin, dossier]) != dossier:
            return False
    except ValueError:
        return False

    extension = os.path.splitext(chemin)[1].lower()

    return extension in EXTENSIONS


# ============================================================
# TRAITEMENT DES LIGNES FS_USAGE
# ============================================================

def traiter_ligne(ligne):

    ligne = ligne.strip()

    if not ligne:
        return

    # On recherche les opérations "open".
    morceaux = ligne.split()

    if len(morceaux) < 2:
        return

    operation = morceaux[1]

    if operation != "open":
        return

    # Recherche d'un chemin qui correspond au dossier surveillé.
    dossier = os.path.abspath(DOSSIER_A_SURVEILLER)

    position = ligne.find(dossier)

    if position == -1:
        return

    # Récupère tout ce qui suit le chemin du dossier.
    reste = ligne[position:]

    # Le dernier champ correspond généralement au processus.
    morceaux_reste = reste.split()

    if not morceaux_reste:
        return

    chemin = morceaux_reste[0]

    if not fichier_interessant(chemin):
        return

    processus = morceaux[-1]

    print("------------------------------------------")
    print("OUVERTURE DETECTEE")
    print()
    print("Fichier :")
    print(chemin)
    print()
    print("Processus :")
    print(processus)
    print("------------------------------------------")
    print()


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():

    print("==========================================")
    print("       SURVEILLANCE DES FICHIERS")
    print("==========================================")
    print()
    print("Dossier surveillé :")
    print(DOSSIER_A_SURVEILLER)
    print()
    print("Surveillance démarrée...")
    print("Appuie sur Ctrl+C pour arrêter.")
    print()

    commande = [
        "fs_usage",
        "-w",
        "-f",
        "filesys"
    ]

    try:

        processus = subprocess.Popen(
            commande,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        for ligne in processus.stdout:
            traiter_ligne(ligne)

    except PermissionError:

        print("Permission refusée.")
        print("Lance le programme avec sudo.")

    except KeyboardInterrupt:

        print()
        print("Arrêt de la surveillance.")

        processus.terminate()

        sys.exit(0)


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":
    main()