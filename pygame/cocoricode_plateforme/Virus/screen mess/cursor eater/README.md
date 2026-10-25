# Root le mangeur de curseur 🍊

Root est un petit personnage orange qui se balade **par-dessus ton bureau Windows**
et marche en permanence vers ta souris. S'il l'attrape, il mange ton curseur
bouchée par bouchée — le vrai curseur système change d'apparence à chaque morsure —
jusqu'à ce qu'il n'en reste rien. Root savoure sa victoire 5 secondes, disparaît,
puis le curseur et lui réapparaissent 15 secondes plus tard. Et ça recommence.

## Installation

Windows uniquement. Il faut Python 3.10+ ([python.org](https://www.python.org/downloads/)).

```
py -m pip install -r requirements.txt
py main.py
```

## Contrôles

- **Échap** — quitter (le curseur est restauré automatiquement)

## Comment ça marche

- Une fenêtre pygame plein écran invisible et *click-through* (layered window
  Windows) dessine Root par-dessus toutes tes fenêtres : tu peux continuer à
  utiliser ton PC pendant qu'il te course.
- Le curseur est réellement remplacé au niveau système (`SetSystemCursor`) par
  une flèche pixel-art recalculée à chaque morsure, pour toutes les formes
  courantes (flèche, texte, main, croix).

## Si le curseur reste mangé

Le programme restaure toujours le curseur en quittant (même sur une erreur).
Si jamais le process est tué brutalement au mauvais moment :

```
py restaure_curseur.py
```

(ou Paramètres Windows > Souris > Paramètres souris supplémentaires > Pointeurs > OK.)

## Dossiers

- `assets/` — les 8 frames de marche de Root utilisées par le jeu
- `art_src/` — les PNG sources en 2000×2000
- `tools/prepare_assets.py` — régénère `assets/` depuis `art_src/` (nécessite Pillow)
