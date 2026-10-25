import pygame

pygame.init()

height = 800
width = 600

tries_to_escaper_counter = 0

window_title_1 = "My project"
window_title_2 = "virus"


background = pygame.image.load('hacked.jpeg')
background = pygame.transform.scale(background,(height, width))

screen = pygame.display.set_mode((height, width))
pygame.display.set_caption(window_title_1)




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tries_to_escaper_counter +=1

    screen.blit(background, (0, 0))
    pygame.display.update()