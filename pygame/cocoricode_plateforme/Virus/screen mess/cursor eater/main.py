"""Root le mangeur de curseur.

Root se balade par-dessus ton bureau et marche vers ta souris. S'il l'attrape,
il mange le curseur bouchée par bouchée jusqu'à ce qu'il n'existe plus, savoure
sa victoire 5 secondes, disparaît... et tout recommence 15 secondes plus tard.

Lancer :  py main.py      —  Échap pour quitter (Windows uniquement)
Si le curseur restait mangé après un crash :  py restaure_curseur.py
"""

import math
import os
import random
import sys
from pathlib import Path

import wincursor as wc

wc.activer_dpi()  # avant pygame, sinon la souris et la fenêtre divergent en 125/150 %
os.environ.setdefault("SDL_VIDEO_WINDOW_POS", "0,0")

import pygame

DOSSIER = Path(__file__).resolve().parent
COULEUR_CLE = (255, 0, 255)

TEST = os.environ.get("ROOT_TEST") == "1"
if TEST:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DOSSIER_TEST = Path(os.environ.get("ROOT_TEST_DIR", str(DOSSIER / "captures_test")))

VITESSE = 240.0
PORTEE_MORSURE = 70.0
INTERVALLE_MORSURE = 0.25 if TEST else 0.8
DUREE_VICTOIRE = 1.5 if TEST else 5.0
DUREE_DISPARITION = 0.45
DUREE_ABSENT = 2.5 if TEST else 15.0

# ---------------------------------------------------------------------------
# Le curseur mangeable : réplique pixel-art de la flèche Windows, modélisée en
# cellules ; chaque morsure retire un paquet de cellules du bas vers la pointe.
# ---------------------------------------------------------------------------

FLECHE = [
    "X..........",
    "XX.........",
    "XoX........",
    "XooX.......",
    "XoooX......",
    "XooooX.....",
    "XoooooX....",
    "XooooooX...",
    "XoooooooX..",
    "XooooooooX.",
    "XoooooXXXXX",
    "XooXooX....",
    "XoX.XooX...",
    "XX..XooX...",
    "X....XooX..",
    ".....XooX..",
    "......XX...",
]
ECHELLE_CURSEUR = 2  # chaque cellule = 2x2 px
CANEVAS_CURSEUR = 48


class CurseurMangeable:
    def __init__(self):
        self.cellules = {}
        self.visible = True
        self.reinitialiser()

    def reinitialiser(self):
        self.cellules = {
            (x, y): c
            for y, ligne in enumerate(FLECHE)
            for x, c in enumerate(ligne)
            if c != "."
        }
        self.visible = True
        self._appliquer()

    def _appliquer(self):
        t = CANEVAS_CURSEUR
        buf = bytearray(t * t * 4)
        for (cx, cy), c in self.cellules.items():
            bgra = bytes((0, 0, 0, 255)) if c == "X" else bytes((255, 255, 255, 255))
            for dy in range(ECHELLE_CURSEUR):
                for dx in range(ECHELLE_CURSEUR):
                    i = ((cy * ECHELLE_CURSEUR + dy) * t + cx * ECHELLE_CURSEUR + dx) * 4
                    buf[i:i + 4] = bgra
        wc.appliquer_curseur_pixels(bytes(buf), t, t, (0, 0))

    def croquer(self):
        """Retire une bouchée (bord ébréché aléatoire). Renvoie (nb cellules, fini)."""
        if not self.cellules:
            return 0, True
        centre = max(self.cellules, key=lambda c: (c[1], c[0]))  # la plus basse
        mordues = [
            c for c in self.cellules
            if (c[0] - centre[0]) ** 2 + (c[1] - centre[1]) ** 2
            <= (3.0 + random.uniform(-0.5, 0.7)) ** 2
        ]
        for c in mordues:
            del self.cellules[c]
        if self.cellules:
            self._appliquer()
            return len(mordues), False
        self.visible = False
        wc.appliquer_curseur_invisible()
        return len(mordues), True


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------

class Root:
    def __init__(self, frames_droite, frames_gauche, zone):
        self.frames_d = frames_droite
        self.frames_g = frames_gauche
        self.zone = zone
        self.largeur = frames_droite[0].get_width()
        self.hauteur = frames_droite[0].get_height()
        self.ombre = self._creer_ombre()
        self.pos = pygame.Vector2(zone.centerx, zone.centery)
        self.vers_la_droite = True
        self.phase_anim = 0.0
        self.echelle = 1.0
        self.impulsion = 0.0  # coup de mâchoire après une morsure
        self.saut = 0.0
        self.cible_errance = pygame.Vector2(self.pos)
        self.chrono_errance = 0.0
        self.apparaitre_au_bord()

    def _creer_ombre(self):
        # Alpha impossible sur fond colorkey : ombre opaque en damier, façon rétro
        l, h = int(self.largeur * 0.8), 16
        s = pygame.Surface((l, h))
        s.fill(COULEUR_CLE)
        s.set_colorkey(COULEUR_CLE)
        for y in range(h):
            for x in range(l):
                nx, ny = (x - l / 2) / (l / 2), (y - h / 2) / (h / 2)
                if nx * nx + ny * ny <= 1.0 and (x + y) % 2 == 0:
                    s.set_at((x, y), (40, 28, 28))
        return s

    def apparaitre_au_bord(self):
        marge = self.hauteur
        bord = random.choice(("gauche", "droite", "haut", "bas"))
        if bord == "gauche":
            self.pos.update(-marge / 2, random.uniform(marge, self.zone.height - marge))
        elif bord == "droite":
            self.pos.update(self.zone.width + marge / 2, random.uniform(marge, self.zone.height - marge))
        elif bord == "haut":
            self.pos.update(random.uniform(marge, self.zone.width - marge), -marge / 2)
        else:
            self.pos.update(random.uniform(marge, self.zone.width - marge), self.zone.height + marge / 2)
        self.echelle = 1.0
        self.saut = 0.0

    def bouche(self):
        dx = self.largeur * 0.38 * (1 if self.vers_la_droite else -1)
        return self.pos + pygame.Vector2(dx, -self.hauteur * 0.12)

    def regarder(self, point):
        if abs(point.x - self.pos.x) > 4:
            self.vers_la_droite = point.x > self.pos.x

    def marcher_vers(self, cible, dt, vitesse=VITESSE):
        direction = cible - self.pos
        if direction.length() > 4:
            direction.scale_to_length(min(vitesse * dt, direction.length()))
            self.pos += direction
            self.regarder(cible)
        self.phase_anim += dt * 12
        # Root peut dépasser un peu des bords à l'apparition, mais pas s'échapper
        self.pos.x = max(-self.largeur, min(self.zone.width + self.largeur, self.pos.x))
        self.pos.y = max(-self.hauteur, min(self.zone.height + self.hauteur, self.pos.y))

    def errer(self, dt):
        self.chrono_errance -= dt
        if self.chrono_errance <= 0 or self.pos.distance_to(self.cible_errance) < 12:
            self.chrono_errance = random.uniform(0.8, 1.6)
            marge = self.hauteur
            self.cible_errance = pygame.Vector2(
                random.uniform(marge, self.zone.width - marge),
                random.uniform(marge, self.zone.height - marge),
            )
        self.marcher_vers(self.cible_errance, dt, vitesse=VITESSE * 0.6)

    def machouiller(self, dt):
        self.phase_anim += dt * 6
        self.impulsion = 1.0

    def maj(self, dt):
        self.impulsion = max(0.0, self.impulsion - dt * 5)

    def dessiner(self, ecran):
        if self.echelle <= 0:
            return
        frames = self.frames_d if self.vers_la_droite else self.frames_g
        frame = frames[int(self.phase_anim) % len(frames)]
        w = max(1, int(self.largeur * self.echelle * (1 + 0.12 * self.impulsion)))
        h = max(1, int(self.hauteur * self.echelle * (1 - 0.10 * self.impulsion)))
        img = pygame.transform.scale(frame, (w, h))
        pied_y = self.pos.y + self.hauteur / 2
        ombre = self.ombre
        if self.echelle < 1.0:
            ombre = pygame.transform.scale(
                self.ombre,
                (max(1, int(self.ombre.get_width() * self.echelle)),
                 max(1, int(self.ombre.get_height() * self.echelle))),
            )
            ombre.set_colorkey(COULEUR_CLE)
        ecran.blit(ombre, ombre.get_rect(center=(self.pos.x, pied_y - 4)))
        ecran.blit(img, img.get_rect(midbottom=(self.pos.x, pied_y - self.saut)))


# ---------------------------------------------------------------------------
# Miettes de curseur
# ---------------------------------------------------------------------------

class Miettes:
    def __init__(self):
        self.particules = []

    def eclat(self, pos, n):
        for _ in range(n):
            angle = random.uniform(-math.pi, 0)  # vers le haut
            v = random.uniform(90, 260)
            self.particules.append({
                "pos": pygame.Vector2(pos),
                "vel": pygame.Vector2(math.cos(angle) * v, math.sin(angle) * v),
                "vie": random.uniform(0.4, 0.9),
                "couleur": random.choice(((255, 255, 255), (230, 230, 230), (30, 30, 30))),
                "taille": random.choice((3, 4, 5)),
            })

    def maj(self, dt):
        for p in self.particules:
            p["vel"].y += 900 * dt
            p["pos"] += p["vel"] * dt
            p["vie"] -= dt
        self.particules = [p for p in self.particules if p["vie"] > 0]

    def dessiner(self, ecran):
        for p in self.particules:
            t = p["taille"]
            ecran.fill(p["couleur"], (p["pos"].x - t / 2, p["pos"].y - t / 2, t, t))


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------

def journal(t, message):
    if TEST:
        print(f"[{t:6.2f}] {message}", flush=True)


def principal():
    pygame.init()
    info = pygame.display.Info()
    largeur, hauteur = info.current_w, info.current_h
    ecran = pygame.display.set_mode((largeur, hauteur), pygame.NOFRAME)
    pygame.display.set_caption("Root")
    wc.rendre_overlay(pygame.display.get_wm_info()["window"], COULEUR_CLE)

    frames_d = [
        pygame.image.load(DOSSIER / "assets" / f"root_{i}.png").convert_alpha()
        for i in range(1, 9)
    ]
    frames_g = [pygame.transform.flip(f, True, False) for f in frames_d]

    zone = ecran.get_rect()
    root = Root(frames_d, frames_g, zone)
    curseur = CurseurMangeable()
    miettes = Miettes()
    horloge = pygame.time.Clock()

    etat = "CHASSE"
    chrono = 0.0
    prochaine_morsure = 0.0
    morsures = 0
    cycles = 0
    t = 0.0
    fin_test = None

    if TEST:
        DOSSIER_TEST.mkdir(parents=True, exist_ok=True)
        wc.capturer_curseur(DOSSIER_TEST / "00_entier.png")
        journal(t, "état → CHASSE")

    wc.echap_presse()  # purge un appui Échap antérieur au lancement
    en_route = True
    while en_route:
        dt = min(horloge.tick(60) / 1000.0, 0.05)
        t += dt

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_route = False
        if wc.echap_presse():
            en_route = False

        if TEST:
            # La souris est pilotée : cercle 1 s pour tester la poursuite, puis immobile
            if t < 1.0:
                wc.fixer_position_souris(
                    zone.centerx + math.cos(t * 5) * 300,
                    zone.centery + math.sin(t * 5) * 180,
                )
            elif etat in ("CHASSE", "MANGE"):
                wc.fixer_position_souris(zone.centerx + 200, zone.centery)

        souris = pygame.Vector2(wc.position_souris())
        souris.x = max(0, min(zone.width, souris.x))
        souris.y = max(0, min(zone.height, souris.y))

        if etat == "CHASSE":
            if curseur.visible and root.bouche().distance_to(souris) <= PORTEE_MORSURE:
                etat = "MANGE"
                prochaine_morsure = 0.3
                journal(t, "état → MANGE")
            else:
                # vise avec la bouche, pas le ventre
                root.marcher_vers(souris - (root.bouche() - root.pos), dt)

        elif etat == "MANGE":
            root.regarder(souris)
            if root.bouche().distance_to(souris) > PORTEE_MORSURE * 1.5:
                etat = "CHASSE"
                journal(t, "le curseur s'échappe → CHASSE")
            else:
                root.machouiller(dt)
                prochaine_morsure -= dt
                if prochaine_morsure <= 0:
                    n, fini = curseur.croquer()
                    morsures += 1
                    miettes.eclat(souris, 4 + n // 2)
                    prochaine_morsure = INTERVALLE_MORSURE
                    journal(t, f"morsure n°{morsures} ({n} cellules){' — curseur englouti !' if fini else ''}")
                    if TEST:
                        wc.capturer_curseur(DOSSIER_TEST / f"{morsures:02d}_morsure.png")
                    if fini:
                        etat = "VICTOIRE"
                        chrono = 0.0
                        journal(t, "état → VICTOIRE")

        elif etat == "VICTOIRE":
            chrono += dt
            root.errer(dt)
            root.saut = abs(math.sin(t * 9)) * 12
            if chrono >= DUREE_VICTOIRE:
                etat = "DISPARITION"
                chrono = 0.0
                journal(t, "état → DISPARITION")

        elif etat == "DISPARITION":
            chrono += dt
            root.saut = 0.0
            root.echelle = max(0.0, 1.0 - chrono / DUREE_DISPARITION)
            if root.echelle <= 0:
                etat = "ABSENT"
                chrono = 0.0
                journal(t, "état → ABSENT (écran vide)")

        elif etat == "ABSENT":
            chrono += dt
            if chrono >= DUREE_ABSENT:
                cycles += 1
                curseur.reinitialiser()
                root.apparaitre_au_bord()
                morsures = 0
                etat = "CHASSE"
                journal(t, f"réapparition (cycle {cycles}) → CHASSE")
                if TEST:
                    wc.capturer_curseur(DOSSIER_TEST / "99_restaure.png")
                    fin_test = t + 1.0

        root.maj(dt)
        miettes.maj(dt)

        ecran.fill(COULEUR_CLE)
        if etat not in ("ABSENT",):
            root.dessiner(ecran)
        miettes.dessiner(ecran)
        pygame.display.flip()

        if TEST and fin_test is not None and t >= fin_test:
            journal(t, "TEST TERMINÉ — cycle complet OK")
            en_route = False

    pygame.quit()


if __name__ == "__main__":
    try:
        principal()
    finally:
        wc.restaurer_curseurs()
