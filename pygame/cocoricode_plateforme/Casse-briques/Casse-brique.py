import pygame
import sys
import random

# Initialisation
pygame.init()
LARGEUR, HAUTEUR = 850, 600
ECRAN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Casse-Briques")
FPS = 60
HORLOGE = pygame.time.Clock()

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
COULEURS_BRIQUES = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]

# Raquette
RAQUETTE_LARGEUR = 100
RAQUETTE_HAUTEUR = 20
raquette_x = LARGEUR // 2 - RAQUETTE_LARGEUR // 2
raquette_y = HAUTEUR - 50
VITESSE_RAQUETTE = 8

# Balle
BALLE_TAILLE = 15
balle_x = LARGEUR // 2
balle_y = HAUTEUR // 2
balle_vitesse_x = 4 * random.choice([-1, 1])
balle_vitesse_y = -4
balle_rect = pygame.Rect(balle_x, balle_y, BALLE_TAILLE, BALLE_TAILLE)

# Briques
BRIQUE_LARGEUR = 75
BRIQUE_HAUTEUR = 30
briques = []

def initialiser_briques():
    briques.clear()
    for ligne in range(3):
        for colonne in range(10):
            brique_x = colonne * (BRIQUE_LARGEUR + 5) + 30
            brique_y = ligne * (BRIQUE_HAUTEUR + 5) + 50
            briques.append(pygame.Rect(brique_x, brique_y, BRIQUE_LARGEUR, BRIQUE_HAUTEUR))

initialiser_briques()

# Score et vies
score = 0
vies = 3
game_over = False
victoire = False
font = pygame.font.SysFont(None, 36)

def afficher_infos():
    score_texte = font.render(f"Score: {score}", True, BLANC)
    vies_texte = font.render(f"Vies: {vies}", True, BLANC)
    ECRAN.blit(score_texte, (10, 10))
    ECRAN.blit(vies_texte, (LARGEUR - 100, 10))

def reinitialiser_balle():
    global balle_x, balle_y, balle_vitesse_x, balle_vitesse_y
    balle_x = LARGEUR // 2
    balle_y = HAUTEUR // 2
    balle_vitesse_x = 4 * random.choice([-1, 1])
    balle_vitesse_y = -4
    balle_rect.update(balle_x, balle_y, BALLE_TAILLE, BALLE_TAILLE)

def reinitialiser_jeu():
    global score, vies, game_over, victoire
    initialiser_briques()
    score = 0
    vies = 3
    game_over = False
    victoire = False
    reinitialiser_balle()

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or victoire):
                reinitialiser_jeu()

    if not game_over and not victoire:
        # Déplacement de la raquette
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and raquette_x > 0:
            raquette_x -= VITESSE_RAQUETTE
        if keys[pygame.K_RIGHT] and raquette_x < LARGEUR - RAQUETTE_LARGEUR:
            raquette_x += VITESSE_RAQUETTE

        # Mouvement de la balle
        balle_x += balle_vitesse_x
        balle_y += balle_vitesse_y
        balle_rect.update(balle_x, balle_y, BALLE_TAILLE, BALLE_TAILLE)

        # Collisions avec les bords
        if balle_x <= 0 or balle_x >= LARGEUR - BALLE_TAILLE:
            balle_vitesse_x *= -1
        if balle_y <= 0:
            balle_vitesse_y *= -1

        # Perte d'une vie si la balle tombe
        if balle_y >= HAUTEUR:
            vies -= 1
            if vies > 0:
                reinitialiser_balle()
            else:
                game_over = True

        # Collision avec la raquette
        raquette_rect = pygame.Rect(raquette_x, raquette_y, RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)
        if balle_rect.colliderect(raquette_rect):
            balle_vitesse_y *= -1
            balle_vitesse_x = (balle_x - (raquette_x + RAQUETTE_LARGEUR // 2)) // 10

        # Collision avec les briques
        for brique in briques[:]:
            if balle_rect.colliderect(brique):
                balle_vitesse_y *= -1
                briques.remove(brique)
                score += 10
                break

        # Vérifier la victoire
        if not briques:
            victoire = True

    # Affichage
    ECRAN.fill(NOIR)
    pygame.draw.rect(ECRAN, VERT, (raquette_x, raquette_y, RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR))
    pygame.draw.ellipse(ECRAN, BLANC, balle_rect)

    for i, brique in enumerate(briques):
        couleur = COULEURS_BRIQUES[i % len(COULEURS_BRIQUES)]
        pygame.draw.rect(ECRAN, couleur, brique)

    afficher_infos()

    # Messages de fin
    if game_over:
        defaite_texte = font.render("GAME OVER! Appuyez sur R pour rejouer", True, ROUGE)
        ECRAN.blit(defaite_texte, (LARGEUR // 2 - 250, HAUTEUR // 2))
    elif victoire:
        victoire_texte = font.render("VICTOIRE! Appuyez sur R pour rejouer", True, VERT)
        ECRAN.blit(victoire_texte, (LARGEUR // 2 - 250, HAUTEUR // 2))

    pygame.display.flip()
    HORLOGE.tick(FPS)

pygame.quit()
sys.exit()