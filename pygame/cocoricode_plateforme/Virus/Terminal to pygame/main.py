import time
import pygame
import tkinter as tk
import random

height = 800
width = 600
WINDOW_WIDTH = 250
WINDOW_HEIGHT = 100

root = tk.Tk()
root.withdraw()
background = pygame.image.load("../pygame virus/hacked.jpeg")
background = pygame.transform.scale(background, (height, width))
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption("Virus")


def virus_open():
    pygame.init()
    popup = tk.Toplevel(root)
    popup.title("Virus")

    x = random.randint(0, 1000)
    y = random.randint(0, 700)

    popup.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    popup.config(bg="black")


    tk.Label(
        popup,
        text="You've been hacked",
        fg="red",
        bg="black",
        font=("Arial", 1, 'bold')
    )



not_understood = 0
tried_to_exit_the_virus_attempts = 0



print("Hi, what's you're name?")
name = input()

print("Ok, hi",name)
time.sleep(0.5)

print("Do you want to be hacked?")
anwser = input().lower()

virus = True
while virus:
    if anwser == "yes":
        print("The virus has started.")
        virus_open()
        virus = False

    elif anwser == "no":
        print("Too late, the virus has already started.")
        time.sleep(1)
        virus_open()
        virus = False

    else:
        print("Say either 'yes' or 'no' or i won't understand.")
        not_understood += 1
        anwser = input()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tried_to_exit_the_virus_attempts += 1

    screen.blit(background, (0, 0))
    pygame.display.update()