import subprocess
import xml.etree.ElementTree as ET
import time
import os


# ============================================================
# CONFIGURATION
# ============================================================

# Dossier que l'on veut surveiller.
# Modifie cette ligne selon ton ordinateur.
DOSSIER_A_SURVEILLER = os.path.expanduser("~/Desktop")

# Extensions que l'on souhaite surveiller.
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
    """
    Retourne True si le fichier se trouve dans le dossier
    surveillé et possède une extension intéressante.
    """

    chemin = os.path.abspath(chemin)
    dossier = os.path.abspath(DOSSIER_A_SURVEILLER)

    # Vérifie que le fichier se trouve dans le dossier surveillé.
    try:
        if not os.path.commonpath([chemin, dossier]) == dossier:
            return False
    except ValueError:
        return False

    # Récupère l'extension du fichier.
    extension = os.path.splitext(chemin)[1].lower()

    return extension in EXTENSIONS


# ============================================================
# LECTURE DES EVENEMENTS WINDOWS
# ============================================================

def recuperer_evenements():
    """
    Demande à Windows les derniers événements 4663
    du journal Security.
    """

    commande = [
        "powershell",
        "-NoProfile",
        "-Command",
        """
        Get-WinEvent -FilterHashtable @{
            LogName='Security'
            Id=4663
        } -MaxEvents 50 |
        ForEach-Object {
            $_.ToXml()
        }
        """
    ]

    try:
        resultat = subprocess.run(
            commande,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if resultat.returncode != 0:
            print("Impossible de lire le journal Security.")
            print(resultat.stderr)
            return []

        # Chaque événement XML est séparé.
        texte = resultat.stdout

        evenements = []
        debut = 0

        while True:
            debut_event = texte.find("<Event", debut)

            if debut_event == -1:
                break

            fin_event = texte.find("</Event>", debut_event)

            if fin_event == -1:
                break

            fin_event += len("</Event>")

            xml_event = texte[debut_event:fin_event]
            evenements.append(xml_event)

            debut = fin_event

        return evenements

    except Exception as erreur:
        print("Erreur :", erreur)
        return []


# ============================================================
# EXTRACTION DES INFORMATIONS
# ============================================================

def extraire_informations(xml_event):
    """
    Extrait le nom du fichier, le type d'accès et le processus
    depuis un événement Windows 4663.
    """

    try:
        racine = ET.fromstring(xml_event)

    except ET.ParseError:
        return None

    donnees = {}

    # Windows utilise un namespace XML.
    namespace = {
        "event": "http://schemas.microsoft.com/win/2004/08/events/event"
    }

    for data in racine.findall(".//event:EventData/event:Data", namespace):
        nom = data.attrib.get("Name")
        valeur = data.text

        if nom:
            donnees[nom] = valeur

    chemin = donnees.get("ObjectName")
    processus = donnees.get("ProcessName")
    access = donnees.get("AccessMask")

    if not chemin:
        return None

    return {
        "fichier": chemin,
        "processus": processus,
        "access": access
    }


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
    print("Extensions surveillées :")
    print(", ".join(sorted(EXTENSIONS)))
    print()
    print("Surveillance démarrée...")
    print("Appuie sur Ctrl+C pour arrêter.")
    print()

    evenements_deja_vus = set()

    while True:

        evenements = recuperer_evenements()

        for xml_event in evenements:

            # On crée une empreinte du XML pour éviter
            # d'afficher plusieurs fois le même événement.
            identifiant = hash(xml_event)

            if identifiant in evenements_deja_vus:
                continue

            evenements_deja_vus.add(identifiant)

            informations = extraire_informations(xml_event)

            if informations is None:
                continue

            fichier = informations["fichier"]
            processus = informations["processus"]
            access = informations["access"]

            # 0x1 correspond à ReadData pour un fichier.
            if access != "0x1":
                continue

            if not fichier_interessant(fichier):
                continue

            print("------------------------------------------")
            print("LECTURE DETECTEE")
            print()
            print("Fichier :")
            print(fichier)
            print()
            print("Programme :")
            print(processus)
            print()
            print("AccessMask :")
            print(access)
            print("------------------------------------------")
            print()

        # Petite pause pour éviter de solliciter
        # constamment Windows.
        time.sleep(1)


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
        print("Surveillance arrêtée.")
