import random
import keyboard
from itertools import count


number = 0
how_much = 0


for i in range(how_much):
    number = random.randint(1,2)


def result():
    if number == 1:
        print("I love poop")
    elif number == 2:
        print("gogogaga")


run = True
while run:
    if keyboard.is_pressed("1"):
        how_much = 10
    elif keyboard.is_pressed("2"):
        how_much = 100
    elif keyboard.is_pressed("3"):
        how_much = 1000
    elif keyboard.is_pressed("4"):
        how_much = 10000
    elif keyboard.is_pressed("5"):
        how_much = 100000
    elif keyboard.is_pressed("6"):
        how_much = 1000000
    elif keyboard.is_pressed("7"):
        how_much = count()