from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# =========================
# WINDOW
# =========================
window.title = "Minecraft Deluxe"
window.fullscreen = True
window.borderless = True
window.fps_counter.enabled = True

# =========================
# LIGHT (STABLE SETUP)
# =========================
DirectionalLight().look_at(Vec3(1, -1, -1))
AmbientLight(color=color.rgba(150, 150, 150, 255))

# =========================
# SKY
# =========================
Sky()

# =========================
# TEXTURES
# =========================
textures = {
    1: load_texture("grass.jpeg"),
    2: load_texture("dirt.jpeg"),
    3: load_texture("stone.png"),
    4: load_texture("wood.jpeg"),
    5: load_texture("bedrock.png"),
}

selected_block = 1

# =========================
# STATE
# =========================
game_running = False
game = Entity(enabled=False)
player = None

# =========================
# BLOCK (FIXED STABLE VERSION)
# =========================
class Block(Entity):
    def __init__(self, position=(0,0,0), texture=None, breakable=True):
        super().__init__(
            parent=game,
            model='cube',
            position=position,
            texture=texture,
            collider='box',
            color=color.white,   # IMPORTANT: force stable rendering
            origin_y=0.5
        )

        self.breakable = breakable

    def input(self, key):
        if not game_running:
            return

        if self.hovered:

            if key == 'right mouse down' and self.breakable:
                destroy(self)

            if key == 'left mouse down':
                Block(
                    position=self.position + mouse.normal,
                    texture=textures[selected_block]
                )

# =========================
# MENU
# =========================
menu = Entity(parent=camera.ui)

Panel(parent=menu, scale=(0.85, 0.75), color=color.dark_gray)

Text(
    parent=menu,
    text=
    "WARNING!\n\n"
    "This program may cause instability.\n\n"
    "Do you want to continue?",
    origin=(0,0),
    y=0.15,
    scale=1.3,
    color=color.red
)

# =========================
# WORLD
# =========================
def create_world():
    global player

    size = 15        #size x size = X x Y = plateau

    for x in range(size):
        for z in range(size):

            Block((x, 0, z), textures[1])
            Block((x, -1, z), textures[2])
            Block((x, -2, z), textures[5], breakable=False)

    player = FirstPersonController(position=(size//2, 3, size//2))
    mouse.locked = True

# =========================
# UI
# =========================
hotbar = []

def create_ui():

    # crosshair
    Entity(
        parent=camera.ui,
        model='quad',
        color=color.white,
        scale=0.008,
        rotation_z=45
    )

    # hotbar
    for i in range(5):
        slot = Entity(
            parent=camera.ui,
            model='quad',
            color=color.dark_gray,
            scale=(0.08, 0.08),
            x=-0.2 + i * 0.1,
            y=-0.45
        )
        hotbar.append(slot)

    update_hotbar()


def update_hotbar():
    for i, slot in enumerate(hotbar):
        slot.color = color.white if i + 1 == selected_block else color.dark_gray

# =========================
# START / QUIT
# =========================
def start_game():
    global game_running

    menu.enabled = False
    game.enabled = True
    game_running = True

    create_world()
    create_ui()

def quit_game():
    application.quit()

Button(
    parent=menu,
    text="LAUNCH",
    color=color.green,
    scale=(0.25, 0.08),
    y=-0.2,
    on_click=start_game
)

Button(
    parent=menu,
    text="QUIT",
    color=color.red,
    scale=(0.25, 0.08),
    y=-0.33,
    on_click=quit_game
)

# =========================
# UPDATE
# =========================
def update():
    global selected_block

    if game_running:

        if held_keys['escape']:
            application.quit()

        for i in range(1, 6):
            if held_keys[str(i)]:
                selected_block = i
                update_hotbar()

app.run()