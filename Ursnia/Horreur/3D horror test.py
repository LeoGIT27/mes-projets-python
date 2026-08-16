from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

fullscreen = True

# ============================================================
# TEXTURES
# ============================================================

texture = {
    1: load_texture("mur.jpeg"),
    2: load_texture("sol.jpeg"),
    3: load_texture("sky.jpeg")
}


# ============================================================
# CIEL
# ============================================================

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=texture[3],
            scale=150,
            double_sided=True
        )


# ============================================================
# PARAMÈTRES
# ============================================================

SIZE = 30
WALL_HEIGHT = 5
WALL_THICKNESS = 0.5

FLOOR_1_Y = 0
FLOOR_2_Y = 5
FLOOR_3_Y = 10


# ============================================================
# 1ER ÉTAGE
# ============================================================

floor_1 = Entity(
    model="cube",
    scale=(SIZE, 0.2, SIZE),
    position=(0, FLOOR_1_Y, 0),
    texture=texture[2],
    color=color.gray,
    collider="box"
)


# ============================================================
# PLANCHER DU 2E ÉTAGE
#
# Deux trous :
# - premier escalier : x = 0
# - deuxième escalier : x = 8
# ============================================================

# Partie avant
floor_2_front = Entity(
    model="cube",
    scale=(SIZE, 0.2, 10),
    position=(0, 5, -10),
    texture=texture[2],
    color=color.gray,
    collider="box"
)

# Partie arrière
floor_2_back = Entity(
    model="cube",
    scale=(SIZE, 0.2, 12),
    position=(0, 5, 9),
    texture=texture[2],
    color=color.gray,
    collider="box"
)

# Partie gauche
floor_2_left = Entity(
    model="cube",
    scale=(13, 0.2, 8),
    position=(-8.5, 5, -1),
    texture=texture[2],
    color=color.gray,
    collider="box"
)

# Partie entre les deux escaliers
floor_2_middle = Entity(
    model="cube",
    scale=(4, 0.2, 8),
    position=(4, 5, -1),
    texture=texture[2],
    color=color.gray,
    collider="box"
)

# Partie droite
floor_2_right = Entity(
    model="cube",
    scale=(5, 0.2, 8),
    position=(12.5, 5, -1),
    texture=texture[2],
    color=color.gray,
    collider="box"
)


# ============================================================
# MURS DU 1ER ÉTAGE
# ============================================================

wall1 = Entity(
    model="cube",
    scale=(SIZE, WALL_HEIGHT, WALL_THICKNESS),
    position=(0, 2.5, 15),
    texture=texture[1],
    collider="box"
)

wall2 = Entity(
    model="cube",
    scale=(SIZE, WALL_HEIGHT, WALL_THICKNESS),
    position=(0, 2.5, -15),
    texture=texture[1],
    collider="box"
)

wall3 = Entity(
    model="cube",
    scale=(WALL_THICKNESS, WALL_HEIGHT, SIZE),
    position=(15, 2.5, 0),
    texture=texture[1],
    collider="box"
)

wall4 = Entity(
    model="cube",
    scale=(WALL_THICKNESS, WALL_HEIGHT, SIZE),
    position=(-15, 2.5, 0),
    texture=texture[1],
    collider="box"
)


# ============================================================
# ESCALIER 1 -> 2
#
# L'escalier est au centre.
# La rampe invisible permet de monter et descendre
# sans devoir sauter.
# ============================================================

STAIR_X = 0
STAIR_Z_START = -5
STAIR_LENGTH = 8

# Rampe de collision
ramp_1 = Entity(
    model="cube",
    scale=(4, 0.2, 8.6),
    position=(STAIR_X, 2.5, -1),
    rotation_x=-32,
    color=color.clear,
    collider="box"
)

# Marches visibles
for i in range(20):

    step_height = 0.25 * i

    Entity(
        model="cube",
        scale=(4, 0.25, 0.4),
        position=(
            STAIR_X,
            0.125 + step_height,
            -4.8 + i * 0.4
        ),
        texture=texture[1]
    )


# ============================================================
# MURS DU 2E ÉTAGE
# ============================================================

wall5 = Entity(
    model="cube",
    scale=(SIZE, WALL_HEIGHT, WALL_THICKNESS),
    position=(0, 7.5, 15),
    texture=texture[1],
    collider="box"
)

wall6 = Entity(
    model="cube",
    scale=(SIZE, WALL_HEIGHT, WALL_THICKNESS),
    position=(0, 7.5, -15),
    texture=texture[1],
    collider="box"
)

wall7 = Entity(
    model="cube",
    scale=(WALL_THICKNESS, WALL_HEIGHT, SIZE),
    position=(15, 7.5, 0),
    texture=texture[1],
    collider="box"
)

wall8 = Entity(
    model="cube",
    scale=(WALL_THICKNESS, WALL_HEIGHT, SIZE),
    position=(-15, 7.5, 0),
    texture=texture[1],
    collider="box"
)


# ============================================================
# ESCALIER 2 -> 3
#
# Déplacé à droite pour ne pas traverser le premier escalier.
# ============================================================

STAIR_2_X = 8
STAIR_2_Z_START = -5

# Rampe invisible de collision
ramp_2 = Entity(
    model="cube",
    scale=(4, 0.2, 8.6),
    position=(STAIR_2_X, 7.5, -1),
    rotation_x=-32,
    color=color.clear,
    collider="box"
)

# Marches visibles
for i in range(20):

    step_height = 0.25 * i

    Entity(
        model="cube",
        scale=(4, 0.25, 0.4),
        position=(
            STAIR_2_X,
            5.125 + step_height,
            -4.8 + i * 0.4
        ),
        texture=texture[1]
    )


# ============================================================
# PLANCHER DU 3E ÉTAGE
#
# Un vrai trou est placé au niveau du deuxième escalier.
# ============================================================

# Partie avant
floor_3_front = Entity(
    model="cube",
    scale=(SIZE, 0.2, 10),
    position=(0, 10, -10),
    #texture=texture[2],
    color=color.red,
    collider="box"
)

# Partie arrière
floor_3_back = Entity(
    model="cube",
    scale=(SIZE, 0.2, 12),
    position=(0, 10, 9),
    #texture=texture[2],
    color=color.black,
    collider="box"
)

# Partie gauche
floor_3_left = Entity(
    model="cube",
    scale=(21, 0.2, 8),
    position=(-4.5, 10, -1),
    #texture=texture[2],
    color=color.green,
    collider="box"
)

# Partie droite
floor_3_right = Entity(
    model="cube",
    scale=(5, 0.2, 8),
    position=(12.5, 10, -1),
    #texture=texture[2],
    color=color.gray,
    collider="box"
)


# ============================================================
# MURS DU 3E ÉTAGE
# ============================================================

wall9 = Entity(
    model="cube",
    scale=(SIZE, WALL_HEIGHT, WALL_THICKNESS),
    position=(0, 12.5, 15),
    texture=texture[1],
    collider="box"
)

wall10 = Entity(
    model="cube",
    scale=(SIZE, WALL_HEIGHT, WALL_THICKNESS),
    position=(0, 12.5, -15),
    texture=texture[1],
    collider="box"
)

wall11 = Entity(
    model="cube",
    scale=(WALL_THICKNESS, WALL_HEIGHT, SIZE),
    position=(15, 12.5, 0),
    texture=texture[1],
    collider="box"
)

wall12 = Entity(
    model="cube",
    scale=(WALL_THICKNESS, WALL_HEIGHT, SIZE),
    position=(-15, 12.5, 0),
    texture=texture[1],
    collider="box"
)


# ============================================================
# OBJETS INTERACTIFS
# ============================================================

cube = Entity(
    model="cube",
    color=color.azure,
    scale=2,
    position=(0, 1, 5),
    collider="box"
)

sphere = Entity(
    model="sphere",
    color=color.red,
    scale=1.5,
    position=(5, 1, -3),
    collider="box"
)

pyramid = Entity(
    model="cube",
    color=color.yellow,
    scale=1.5,
    position=(-5, 1, -5),
    collider="box"
)

secret = Entity(
    model="sphere",
    color=color.black,
    scale=1,
    position=(8, 1, 8),
    enabled=False,
    collider="box"
)


# ============================================================
# JOUEUR
# ============================================================

player = FirstPersonController()

player.gravity = 0.5
player.cursor.visible = False
player.position = (0, 1, 0)


# ============================================================
# CIEL
# ============================================================

sky = Sky()


# ============================================================
# NARRATEUR
# ============================================================

narrator_text = Text(
    text="Narrateur : Il n'y a rien ici... vraiment rien.",
    position=(0, 0.45),
    origin=(0, 0),
    scale=1.5
)

discovered = set()


# ============================================================
# INTERACTION
# ============================================================

def input(key):

    if key == "left mouse down":

        hovered_obj = None

        for obj in [cube, sphere, pyramid, secret]:

            if obj.hovered:

                hovered_obj = obj
                break

        if hovered_obj:

            discovered.add(hovered_obj)

            hovered_obj.color = color.lime

            if hovered_obj == cube:

                narrator_text.text = (
                    "Narrateur : Ce cube… comment as-tu trouvé ça ?!"
                )

            elif hovered_obj == sphere:

                narrator_text.text = (
                    "Narrateur : Cette sphère n'était pas supposée être vue !"
                )

            elif hovered_obj == pyramid:

                narrator_text.text = (
                    "Narrateur : Bon, ok… tu prouves qu'il y a un jeu !"
                )

            elif hovered_obj == secret:

                narrator_text.text = (
                    "Narrateur : Mais… comment as-tu découvert l'objet secret ?!"
                )

        else:

            narrator_text.text = (
                "Narrateur : Je t'avais dit qu'il n'y avait rien ici..."
            )


# ============================================================
# LOGIQUE SECRÈTE
# ============================================================

def update():

    # Faire apparaître l'objet secret
    # si le cube et la sphère ont été découverts.

    if cube in discovered and sphere in discovered:

        secret.enabled = True


    # Ending
    if len(discovered) == 4:

        narrator_text.text = (
            "Narrateur : Très bien… je dois l'admettre. "
            "Il y a vraiment un jeu ici. Tu as gagné !"
        )


    # Empêcher le joueur de tomber sous la map
    if player.y < -1:

        player.position = (0, 1, 0)


    # Quitter
    if held_keys["escape"]:

        application.quit()


# ============================================================
# LANCEMENT
# ============================================================

app.run()