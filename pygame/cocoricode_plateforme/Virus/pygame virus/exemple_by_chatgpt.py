import pygame

# ============================================================
# INITIALISATION
# ============================================================

pygame.init()

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bienvenue")

clock = pygame.time.Clock()


# ============================================================
# COULEURS
# ============================================================

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 120, 220)
BLUE_HOVER = (70, 140, 240)


# ============================================================
# POLICES
# ============================================================

title_font = pygame.font.SysFont(
    "Arial",
    32,
    bold=True
)

question_font = pygame.font.SysFont(
    "Arial",
    24
)

button_font = pygame.font.SysFont(
    "Arial",
    20,
    bold=True
)

input_font = pygame.font.SysFont(
    "Arial",
    22
)


# ============================================================
# CHAMP DE TEXTE
# ============================================================

name = ""

input_box = pygame.Rect(
    250,
    220,
    300,
    50
)

input_active = True


# ============================================================
# BOUTONS
# ============================================================

yes_button = pygame.Rect(
    250,
    320,
    140,
    50
)

no_button = pygame.Rect(
    410,
    320,
    140,
    50
)


# ============================================================
# BOUCLE PRINCIPALE
# ============================================================

running = True

while running:

    # --------------------------------------------------------
    # EVENEMENTS
    # --------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        # ----------------------------------------------------
        # CLAVIER
        # ----------------------------------------------------

        elif event.type == pygame.KEYDOWN:

            if input_active:

                if event.key == pygame.K_BACKSPACE:

                    name = name[:-1]

                elif event.key == pygame.K_RETURN:

                    print("Prénom :", name)

                else:

                    # Limite à 20 caractères
                    if len(name) < 20:

                        name += event.unicode


        # ----------------------------------------------------
        # SOURIS
        # ----------------------------------------------------

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # Champ de texte
                if input_box.collidepoint(event.pos):

                    input_active = True

                else:

                    input_active = False


                # Bouton OUI
                if yes_button.collidepoint(event.pos):

                    print("Tu as choisi OUI")
                    print("Prénom :", name)


                # Bouton NON
                elif no_button.collidepoint(event.pos):

                    print("Tu as choisi NON")
                    print("Prénom :", name)


    # ========================================================
    # AFFICHAGE
    # ========================================================

    screen.fill(WHITE)


    # --------------------------------------------------------
    # TITRE
    # --------------------------------------------------------

    title = title_font.render(
        "Bienvenue",
        True,
        BLACK
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, 80)
    )

    screen.blit(
        title,
        title_rect
    )


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    question = question_font.render(
        "Quel est ton prénom ?",
        True,
        BLACK
    )

    question_rect = question.get_rect(
        center=(WIDTH // 2, 160)
    )

    screen.blit(
        question,
        question_rect
    )


    # --------------------------------------------------------
    # CHAMP DE TEXTE
    # --------------------------------------------------------

    if input_active:

        pygame.draw.rect(
            screen,
            WHITE,
            input_box
        )

        pygame.draw.rect(
            screen,
            BLUE,
            input_box,
            2
        )

    else:

        pygame.draw.rect(
            screen,
            GRAY,
            input_box
        )

        pygame.draw.rect(
            screen,
            DARK_GRAY,
            input_box,
            2
        )


    # Texte du prénom
    text_surface = input_font.render(
        name,
        True,
        BLACK
    )

    screen.blit(
        text_surface,
        (
            input_box.x + 10,
            input_box.y + 12
        )
    )


    # --------------------------------------------------------
    # BOUTON OUI
    # --------------------------------------------------------

    mouse_position = pygame.mouse.get_pos()

    if yes_button.collidepoint(mouse_position):

        pygame.draw.rect(
            screen,
            BLUE_HOVER,
            yes_button,
            border_radius=8
        )

    else:

        pygame.draw.rect(
            screen,
            BLUE,
            yes_button,
            border_radius=8
        )


    yes_text = button_font.render(
        "Oui",
        True,
        WHITE
    )

    yes_text_rect = yes_text.get_rect(
        center=yes_button.center
    )

    screen.blit(
        yes_text,
        yes_text_rect
    )


    # --------------------------------------------------------
    # BOUTON NON
    # --------------------------------------------------------

    if no_button.collidepoint(mouse_position):

        pygame.draw.rect(
            screen,
            BLUE_HOVER,
            no_button,
            border_radius=8
        )

    else:

        pygame.draw.rect(
            screen,
            BLUE,
            no_button,
            border_radius=8
        )


    no_text = button_font.render(
        "Non",
        True,
        WHITE
    )

    no_text_rect = no_text.get_rect(
        center=no_button.center
    )

    screen.blit(
        no_text,
        no_text_rect
    )


    # ========================================================
    # AFFICHAGE FINAL
    # ========================================================

    pygame.display.flip()

    clock.tick(60)


# ============================================================
# FERMETURE
# ============================================================

pygame.quit()