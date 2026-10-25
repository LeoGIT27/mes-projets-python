import math
import pygame

# --------------------------------------------------
# Initialisation
# --------------------------------------------------

pygame.init()

LARGEUR = 800
HAUTEUR = 600
FPS = 60

screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Personnage pixelisé qui suit le curseur")

clock = pygame.time.Clock()


# --------------------------------------------------
# Chargement du sprite
# --------------------------------------------------

SPRITE_PATH = "ton_image.png"
TAILLE_SPRITE = (64, 64)

try:
    personnage_img = pygame.image.load(SPRITE_PATH).convert_alpha()
    personnage_img = pygame.transform.scale(personnage_img, TAILLE_SPRITE)

except (pygame.error, FileNotFoundError):
    print(f"Impossible de charger l'image : {SPRITE_PATH}")

    # Placeholder
    personnage_img = pygame.Surface(TAILLE_SPRITE, pygame.SRCALPHA)
    pygame.draw.rect(
        personnage_img,
        (50, 100, 255),
        personnage_img.get_rect()
    )
    pygame.draw.rect(
        personnage_img,
        (255, 255, 255),
        personnage_img.get_rect(),
        2
    )


# --------------------------------------------------
# Joueur
# --------------------------------------------------

position = pygame.Vector2(LARGEUR / 2, HAUTEUR / 2)

# Vitesse en pixels par seconde
VITESSE = 240

# Dernière direction connue
direction = pygame.Vector2(1, 0)


# --------------------------------------------------
# Fonctions
# --------------------------------------------------

def wrap_position(pos):
    """Fait réapparaître le personnage de l'autre côté de l'écran."""

    if pos.x < 0:
        pos.x = LARGEUR

    elif pos.x > LARGEUR:
        pos.x = 0

    if pos.y < 0:
        pos.y = HAUTEUR

    elif pos.y > HAUTEUR:
        pos.y = 0


def get_rotation(direction):
    """Retourne l'angle du sprite en fonction de sa direction."""

    return math.degrees(math.atan2(-direction.y, direction.x))


# --------------------------------------------------
# Boucle principale
# --------------------------------------------------

running = True

while running:

    # --------------------------------------------------
    # Gestion des événements
    # --------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            # Échap pour quitter
            if event.key == pygame.K_ESCAPE:
                running = False


    # --------------------------------------------------
    # Delta time
    # --------------------------------------------------

    dt = clock.tick(FPS) / 1000.0

    # Évite les énormes déplacements si la fenêtre
    # est bloquée pendant un moment.
    dt = min(dt, 0.05)


    # --------------------------------------------------
    # Position de la souris
    # --------------------------------------------------

    souris = pygame.Vector2(pygame.mouse.get_pos())


    # --------------------------------------------------
    # Direction vers la souris
    # --------------------------------------------------

    direction_souris = souris - position
    distance = direction_souris.length()

    # Seuil minimum pour éviter les tremblements
    if distance > 2:

        direction = direction_souris.normalize()

        # Déplacement indépendant du nombre de FPS
        position += direction * VITESSE * dt


    # --------------------------------------------------
    # Wrap-around
    # --------------------------------------------------

    wrap_position(position)


    # --------------------------------------------------
    # Rotation du sprite
    # --------------------------------------------------

    angle = get_rotation(direction)

    rotated_sprite = pygame.transform.rotate(
        personnage_img,
        angle
    )

    sprite_rect = rotated_sprite.get_rect(
        center=position
    )


    # --------------------------------------------------
    # Affichage
    # --------------------------------------------------

    screen.fill((30, 30, 30))

    screen.blit(
        rotated_sprite,
        sprite_rect
    )

    pygame.display.flip()


# --------------------------------------------------
# Fermeture
# --------------------------------------------------

pygame.quit()