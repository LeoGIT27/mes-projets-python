from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

window.title = "Warning"
window.borderless = False
window.size = (1200, 2100)

# -------------------------------------------------
# Couleurs des blocs (plus de textures)
# -------------------------------------------------

block_colors = {
    1: color.green,
    2: color.red,
    3: color.brown,
    4: color.gray,
    5: color.orange,
    6: color.black,
}

block_pick = 1

# -------------------------------------------------
# MENU
# -------------------------------------------------

menu = Entity(parent=camera.ui)

Panel(parent=menu, scale=(0.8, 0.75), color=color.dark_gray)

Text(
    parent=menu,
    text=
    "WARNING!\n\n"
    "This program may cause severe system slowdowns,\n"
    "high CPU usage, and temporary instability.\n\n"
    "Running this code is at YOUR OWN RISK.\n"
    "The author is not responsible for any damage\n"
    "or data loss caused by this program.\n\n"
    "Do you want to continue?",
    origin=(0,0),
    scale=1.2,
    y=.18
)

game = Entity(enabled=False)

player = None

# -------------------------------------------------
# BLOCS
# -------------------------------------------------

class Block(Button):
    def __init__(self, position=(0,0,0), block_color=color.green, breakable=True):
        super().__init__(
            parent=game,
            model='cube',
            position=position,
            color=block_color,
            collider='box',
            highlight_color=color.white,
            scale=1
        )

        self.breakable = breakable

    def input(self, key):
        global block_pick

        if self.hovered:

            if key == 'left mouse down':
                Block(
                    position=self.position + mouse.normal,
                    block_color=block_colors[block_pick]
                )

            if key == 'right mouse down':
                if self.breakable:
                    destroy(self)

# -------------------------------------------------
# CIEL
# -------------------------------------------------

Sky(parent=game, model='sphere', scale=150,
    color=color.azure, double_sided=True)

# -------------------------------------------------
# LANCEMENT
# -------------------------------------------------

def launch():

    global player

    menu.enabled = False
    game.enabled = True

    for z in range(99999999999999999999999999999999999999999999999):
        for x in range(99999999999999999999999999999999999999999999999):
            Block((x,0,z), block_colors[1])
            Block((x,-1,z), block_colors[4])
            Block((x,-2,z), block_colors[6], False)

    player = FirstPersonController(position=(7,2,7))
    mouse.locked = True

Button(
    parent=menu,
    text="Launch",
    color=color.green,
    scale=(0.22,.08),
    y=-.25,
    on_click=launch
)

Button(
    parent=menu,
    text="Quit",
    color=color.red,
    scale=(0.22,.08),
    y=-.37,
    on_click=application.quit
)

# -------------------------------------------------
# UPDATE
# -------------------------------------------------

def update():

    global block_pick

    if not game.enabled:
        return

    for i in range(1,6):
        if held_keys[str(i)]:
            block_pick = i

app.run()