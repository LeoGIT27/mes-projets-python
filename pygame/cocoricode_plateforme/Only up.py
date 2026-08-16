import pygame
import sys


pygame.init()

width = 900
height = 600

screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()


speed = 0
gravity = 1
on_ground = False


background = pygame.image.load('sky.jpeg')
background = pygame.transform.scale(background,(width,height))


platforms = [(pygame.image.load(f'plat_{i}.png'),pygame.image.load(f'plat_{i}.png').get_rect()) for i in range(1,8)]

platforms[0][1].midbottom = (width/2, 580)
platforms[1][1].midbottom = (600,500)
platforms[2][1].bottomright = (900,-200)

michel = pygame.image.load("images.png")
michel = pygame.transform.rotozoom(michel,0,0.25)
michel_rect = michel.get_rect(center = (width/2, height/2))

camera = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if on_ground:
                    speed = -17
    #on_ground = False

    #deplacement & collision horizontal
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        michel_rect.x = michel_rect.x + 5
        for skibidi in platforms:
            if michel_rect.colliderect(skibidi[1]):
                michel_rect.right = skibidi[1].left

    if keys[pygame.K_LEFT]:
        michel_rect.x = michel_rect.x - 5
        for platform in platforms:
            if michel_rect.colliderect(platform[1]):
                michel_rect.left = platform[1].right


    #gravité michel et collision vertical

    camera_y = michel_rect.centery - int(height / 2)
    for platform in platforms:
        platform[1].centery -= camera_y



    speed += gravity
    if speed >= 15:
        speed = 15

    michel_rect.y += speed


    for skibidi in platforms:
        if michel_rect.colliderect(skibidi[1]):
            if speed > 0:
                michel_rect.bottom = skibidi[1].top
                on_ground = True

            else:
                michel_rect.top = skibidi[1].bottom
            speed = 0


    #if michel_rect.bottom >= height:
        #michel_rect.bottom = height
        #speed = 0
        #on_ground = True

    if michel_rect.left <= 0:
        michel_rect.left = 0

    if michel_rect.right >= width:
        michel_rect.right = width

    if michel_rect.top <= 0:
        michel_rect.top = 0






    screen.blit(background,(0,0))
    for platform in platforms:
        screen.blit(platform[0], platform[1])
    screen.blit(michel, michel_rect)
    pygame.display.update()
    clock.tick(60)

