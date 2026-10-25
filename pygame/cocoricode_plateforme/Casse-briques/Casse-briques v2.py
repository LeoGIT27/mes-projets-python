
import random
import sys
import pygame
import pygame.freetype
import math

pygame.init()
pygame.freetype.init()

myfont = pygame.freetype.SysFont(None, 20)

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Casse-briques")

clock = pygame.time.Clock()

BLANC = (255, 255, 255)
COULEURS = [(255, 0, 0),(0, 255, 0),(0, 0, 255)]
NOIR = (0, 0, 0)

RAYON_BALLE = 10
XMIN, YMIN = 100, 0
XMAX, YMAX = width, height


class Balle:

    def vitesse_par_angle(self, angle):
        self.vx = self.vitesse * math.cos(math.radians(angle))
        self.vy = -self.vitesse * math.sin(math.radians(angle))

    def __init__(self):
        self.x, self.y = (400, 400)
        self.vitesse = 8
        self.vitesse_par_angle(60)
        self.sur_raquette = True

    def afficher(self):
        pygame.draw.rect(
            screen, BLANC,
            (int(self.x - RAYON_BALLE),
             int(self.y - RAYON_BALLE),
             2 * RAYON_BALLE, 2 * RAYON_BALLE), 0
        )

    def rebond_raquette(self, raquette):
        diff = raquette.x - self.x
        longueur_totale = raquette.longueur / 2 + RAYON_BALLE
        angle = 90 + 80 * diff / longueur_totale
        self.vitesse_par_angle(angle)

    def deplacer(self, raquette, briques):
        if self.sur_raquette:
            self.y = raquette.y - 2 * RAYON_BALLE
            self.x = raquette.x
        else:
            self.x += self.vx
            self.y += self.vy

            if raquette.collision_balle(self) and self.vy > 0:
                self.rebond_raquette(raquette)

            if self.x + RAYON_BALLE > XMAX:
                self.vx = -self.vx

            if self.x - RAYON_BALLE < XMIN:
                self.vx = -self.vx

            if self.y + RAYON_BALLE > YMAX:
                self.sur_raquette = True

            if self.y - RAYON_BALLE < YMIN:
                self.vy = -self.vy

            for brique in briques:
                if brique.en_vie():
                    brique.collision_balle(self)


class Raquette:

    def __init__(self):
        self.x = (XMIN + XMAX) / 2
        self.y = YMAX - RAYON_BALLE
        self.longueur = 10 * RAYON_BALLE

    def afficher(self):
        pygame.draw.rect(
            screen, BLANC,
            (int(self.x - self.longueur / 2),
             int(self.y - RAYON_BALLE),
             self.longueur, 2 * RAYON_BALLE), 0
        )

    def deplacer(self, x):
        if x - self.longueur / 2 < XMIN:
            self.x = XMIN + self.longueur / 2
        elif x + self.longueur / 2 > XMAX:
            self.x = XMAX - self.longueur / 2
        else:
            self.x = x

    def collision_balle(self, balle):
        vertical = abs(self.y - balle.y) < 2 * RAYON_BALLE
        horizontal = abs(self.x - balle.x) < (
            self.longueur / 2 + RAYON_BALLE
        )
        return vertical and horizontal


class Brique:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie = 1
        self.longueur = 5 * RAYON_BALLE
        self.largeur = 3 * RAYON_BALLE
        self.color = random.choice(COULEURS)

    def en_vie(self):
        return self.vie > 0

    def afficher(self):
        pygame.draw.rect(
            screen, self.color,
            (int(self.x - self.longueur / 2),
             int(self.y - self.largeur / 2),
             self.longueur, self.largeur), 0
        )

    def collision_balle(self, balle):
        marge = self.largeur / 2 + RAYON_BALLE
        dy = balle.y - self.y
        touche = False

        if balle.x >= self.x:
            dx = balle.x - (
                self.x + self.longueur / 2 - self.largeur / 2
            )
            if abs(dy) <= marge and dx <= marge:
                touche = True
                if dx <= abs(dy):
                    balle.vy = -balle.vy
                else:
                    balle.vx = -balle.vx
        else:
            dx = balle.x - (
                self.x - self.longueur / 2 + self.largeur / 2
            )
            if abs(dy) <= marge and -dx <= marge:
                touche = True
                if -dx <= abs(dy):
                    balle.vy = -balle.vy
                else:
                    balle.vx = -balle.vx

        if touche:
            self.vie -= 1

        return touche


class Jeu:

    def __init__(self):
        self.initialiser()

    def initialiser(self):
        self.balle = Balle()
        self.raquette = Raquette()
        self.briques = []

        for ligne in range(5):
            for colonne in range(10):
                x = 150 + colonne * 60
                y = 50 + ligne * 35
                self.briques.append(Brique(x, y))

        self.vies = 3
        self.score = 0
        self.niveau = 1
        self.game_over = False

    def gestion_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game_over:
                        self.initialiser()
                    elif self.balle.sur_raquette:
                        self.balle.sur_raquette = False
                        self.balle.vitesse_par_angle(60)

    def mise_a_jour(self):
        if self.game_over:
            return

        x, y = pygame.mouse.get_pos()

        if not self.balle.sur_raquette:
            ancienne_vie = [
                brique.vie for brique in self.briques
            ]

            self.balle.deplacer(self.raquette, self.briques)

            for i, brique in enumerate(self.briques):
                if ancienne_vie[i] > 0 and not brique.en_vie():
                    self.score += 10

            if self.balle.sur_raquette and self.balle.y >= YMAX - RAYON_BALLE:
                self.vies -= 1

                if self.vies <= 0:
                    self.game_over = True

        else:
            self.balle.deplacer(self.raquette, self.briques)

        self.raquette.deplacer(x)

        if all(not brique.en_vie() for brique in self.briques):
            self.niveau += 1
            self.briques = []

            for ligne in range(5):
                for colonne in range(10):
                    x = 150 + colonne * 60
                    y = 50 + ligne * 35
                    self.briques.append(Brique(x, y))

            self.balle = Balle()
            self.raquette = Raquette()

    def affichage(self):
        screen.fill(NOIR)

        pygame.draw.line(
            screen, BLANC, (XMIN, YMIN), (XMIN, YMAX), 2
        )

        for brique in self.briques:
            if brique.en_vie():
                brique.afficher()

        self.balle.afficher()
        self.raquette.afficher()

        texte, rect = myfont.render(
            "Score : " + str(self.score), BLANC
        )
        rect.topleft = (10, 20)
        screen.blit(texte, rect)

        texte, rect = myfont.render(
            "Vies : " + str(self.vies), BLANC
        )
        rect.topleft = (10, 50)
        screen.blit(texte, rect)

        texte, rect = myfont.render(
            "Niveau : " + str(self.niveau), BLANC
        )
        rect.topleft = (10, 80)
        screen.blit(texte, rect)

        if self.game_over:
            texte, rect = myfont.render(
                "Game Over - Cliquez pour recommencer", BLANC
            )
            rect.center = (width // 2, height // 2)
            screen.blit(texte, rect)


jeu = Jeu()

while True:
    jeu.gestion_evenements()
    jeu.mise_a_jour()
    jeu.affichage()

    pygame.display.flip()
    clock.tick(60)