import pygame
import sys
import random


pygame.init()

width = 900
height = 600

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

speed = 0
gravity = 1
on_ground = False

background = pygame.image.load("sky.jpeg")
background = pygame.transform.scale(background, (width, height))

platforms = [(pygame.image.load(f"plat_{i}.png"),
              pygame.image.load(f"plat_{i}.png").get_rect())
             for i in range(1, 8)]

platforms[0][1].midbottom = (width / 2, 580)
platforms[1][1].midbottom = (600, 500)

# Placement aléatoire des autres plateformes au début du jeu

for i in range(2, len(platforms)):
    platforms[i][1].top = platforms[i - 1][1].top - random.randint(70, 100)
    platforms[i][1].centerx = platforms[i - 1][1].centerx + random.randint(-120, 120)

    if platforms[i][1].left < 0:
        platforms[i][1].left = 0

    if platforms[i][1].right > width:
        platforms[i][1].right = width

michel = pygame.image.load("images.png")
michel = pygame.transform.rotozoom(michel, 0, 0.25)
michel_rect = michel.get_rect(center=(width / 2, height / 2))

camera = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if on_ground:
                    speed = -17
                    on_ground = False

    # Déplacement et collisions horizontales

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        michel_rect.x += 5

        for platform in platforms:
            if michel_rect.colliderect(platform[1]):
                michel_rect.right = platform[1].left

    if keys[pygame.K_LEFT]:
        michel_rect.x -= 5

        for platform in platforms:
            if michel_rect.colliderect(platform[1]):
                michel_rect.left = platform[1].right

    # Gravité et collisions verticales

    speed += gravity

    if speed >= 15:
        speed = 15

    michel_rect.y += speed

    on_ground = False

    for platform in platforms:
        if michel_rect.colliderect(platform[1]):
            if speed > 0:
                michel_rect.bottom = platform[1].top
                on_ground = True

            else:
                michel_rect.top = platform[1].bottom

            speed = 0

    # Limites horizontales

    if michel_rect.left <= 0:
        michel_rect.left = 0

    if michel_rect.right >= width:
        michel_rect.right = width

    # Caméra

    camera = min(camera, michel_rect.centery - int(height / 2))

    # Recherche de la plateforme la plus haute

    highest_platform = platforms[0]

    for platform in platforms:
        if platform[1].top < highest_platform[1].top:
            highest_platform = platform

    # Création d'une nouvelle plateforme au-dessus de l'écran

    if highest_platform[1].top - camera >= 0:
        platform_image = random.choice(platforms)[0]
        platform_rect = platform_image.get_rect()

        platform_rect.top = highest_platform[1].top - random.randint(70, 100)
        platform_rect.centerx = highest_platform[1].centerx + random.randint(-120, 120)

        if platform_rect.left < 0:
            platform_rect.left = 0

        if platform_rect.right > width:
            platform_rect.right = width

        platforms.append((platform_image, platform_rect))

    # Suppression des plateformes sorties sous l'écran

    for platform in platforms[:]:
        if platform[1].top - camera > height:
            platforms.remove(platform)

    # Affichage

    screen.blit(background, (0, 0))

    for platform in platforms:
        screen.blit(
            platform[0],
            (platform[1].x, platform[1].y - camera)
        )

    screen.blit(
        michel,
        (michel_rect.x, michel_rect.y - camera)
    )

    pygame.display.update()
    clock.tick(60)