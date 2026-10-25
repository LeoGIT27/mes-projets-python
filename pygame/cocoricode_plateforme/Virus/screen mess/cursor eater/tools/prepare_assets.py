"""Prépare les frames de Root : alpha binarisé, recadrage commun, réduction NEAREST.

À rejouer uniquement si les PNG sources de art_src/ changent :
    py tools/prepare_assets.py
Nécessite Pillow.
"""

from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
SRC = RACINE / "art_src"
DEST = RACINE / "assets"
HAUTEUR_CIBLE = 140


def main() -> None:
    DEST.mkdir(exist_ok=True)
    frames = []
    for i in range(1, 9):
        img = Image.open(SRC / f"Copie de Root{i}.png").convert("RGBA")
        # Alpha binaire : indispensable pour le colorkey de l'overlay (pas de halo)
        r, g, b, a = img.split()
        a = a.point(lambda v: 255 if v >= 128 else 0)
        img.putalpha(a)
        frames.append(img)

    # Bounding box commune à toutes les frames pour ne pas faire sauter l'animation
    boxes = [f.getbbox() for f in frames]
    gauche = min(b[0] for b in boxes)
    haut = min(b[1] for b in boxes)
    droite = max(b[2] for b in boxes)
    bas = max(b[3] for b in boxes)

    largeur = droite - gauche
    hauteur = bas - haut
    echelle = HAUTEUR_CIBLE / hauteur
    taille = (round(largeur * echelle), HAUTEUR_CIBLE)

    for i, img in enumerate(frames, start=1):
        petit = img.crop((gauche, haut, droite, bas)).resize(taille, Image.NEAREST)
        petit.save(DEST / f"root_{i}.png")
        print(f"root_{i}.png {petit.size}")


if __name__ == "__main__":
    main()
