from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from math import atan2, degrees, sqrt
import json
import os


# =========================================================
# INITIALISATION
# =========================================================

app = Ursina()

window.size = (1280, 720)
window.title = "Backrooms - Système de collision"


# =========================================================
# MAP
# =========================================================

backrooms = Entity(
    model="backrooms_another_level.glb",
    texture="Pumpkin_Color.png",
    scale=1.5,
    position=(-19, 0, 0),
    collider=None,
    double_sided=True
)


# =========================================================
# SOL DE SÉCURITÉ
# =========================================================

ground = Entity(
    model="cube",
    position=(-19, 0, 0),
    scale=(200, 0.2, 200),
    collider="box",
    visible=False
)


# =========================================================
# JOUEUR
# =========================================================

player = FirstPersonController()

player.position = (
    24.79775,
    1,
    35.68929
)

player.gravity = 0.5
player.speed = 5

player.scale = 0.8
player.camera_pivot.y = 2.5

player.cursor.visible = False


# =========================================================
# INTERFACE
# =========================================================

position_text = Text(
    text="",
    position=(-0.85, 0.45),
    scale=1.1,
    background=True
)

help_text = Text(
    text=(
        "F6 : créer un mur\n"
        "F7 : créer un poteau\n"
        "F8 : sauvegarder\n"
        "F3 : coordonnées\n"
        "F4 : debug\n"
        "F5 : analyser"
    ),
    position=(-0.85, 0.25),
    scale=0.8,
    background=True
)


# =========================================================
# VARIABLES DEBUG
# =========================================================

debug = False


# =========================================================
# VARIABLES COLLISIONS
# =========================================================

collision_walls = []

# Premier point d'un mur
wall_start = None

# Hauteur des murs
WALL_HEIGHT = 4

# Épaisseur des murs
WALL_THICKNESS = 0.3


# =========================================================
# DIMENSIONS DES POTEAUX
# =========================================================

POST_WIDTH = 1
POST_DEPTH = 1
POST_HEIGHT = 4


# =========================================================
# FICHIER DE SAUVEGARDE
# =========================================================

SAVE_FILE = "collisions.json"


# =========================================================
# CRÉATION D'UN MUR
# =========================================================

def create_wall(point_a, point_b):

    dx = point_b.x - point_a.x
    dz = point_b.z - point_a.z

    length = sqrt(dx * dx + dz * dz)

    if length < 0.2:

        print("Mur trop court, création annulée.")
        return


    # -----------------------------------------------------
    # CENTRE DU MUR
    # -----------------------------------------------------

    center_x = (point_a.x + point_b.x) / 2
    center_z = (point_a.z + point_b.z) / 2

    center_y = WALL_HEIGHT / 2


    # -----------------------------------------------------
    # ROTATION
    # -----------------------------------------------------

    rotation_y = degrees(atan2(dx, dz))


    # -----------------------------------------------------
    # COLLIDER
    # -----------------------------------------------------

    wall = Entity(
        model="cube",

        position=(
            center_x,
            center_y,
            center_z
        ),

        scale=(
            WALL_THICKNESS,
            WALL_HEIGHT,
            length
        ),

        rotation_y=rotation_y,

        collider="box",

        # Visible pendant la construction
        visible=True,

        # Rouge semi-transparent
        color=color.rgba(255, 0, 0, 100)
    )


    collision_walls.append(wall)


    # -----------------------------------------------------
    # INFORMATIONS
    # -----------------------------------------------------

    print("\n========== MUR CRÉÉ ==========")

    print(
        f"Point A : "
        f"X={point_a.x:.2f} "
        f"Z={point_a.z:.2f}"
    )

    print(
        f"Point B : "
        f"X={point_b.x:.2f} "
        f"Z={point_b.z:.2f}"
    )

    print(
        f"Longueur : {length:.2f}"
    )

    print(
        f"Rotation : {rotation_y:.2f}°"
    )

    print("==============================\n")


# =========================================================
# CRÉATION D'UN POTEAU
# =========================================================

def create_post(position):

    post = Entity(
        model="cube",

        position=(
            position.x,
            POST_HEIGHT / 2,
            position.z
        ),

        scale=(
            POST_WIDTH,
            POST_HEIGHT,
            POST_DEPTH
        ),

        collider="box",

        # Visible pendant la construction
        visible=False
    )


    collision_walls.append(post)


    # -----------------------------------------------------
    # INFORMATIONS
    # -----------------------------------------------------

    print("\n========== POTEAU CRÉÉ ==========")

    print(
        f"Position : "
        f"X={position.x:.2f} "
        f"Z={position.z:.2f}"
    )

    print(
        f"Largeur : {POST_WIDTH:.2f}"
    )

    print(
        f"Profondeur : {POST_DEPTH:.2f}"
    )

    print(
        f"Hauteur : {POST_HEIGHT:.2f}"
    )

    print("=================================\n")


# =========================================================
# SAUVEGARDE DES COLLISIONS
# =========================================================

def save_walls():

    data = []


    # -----------------------------------------------------
    # RÉCUPÉRATION DES COLLIDERS
    # -----------------------------------------------------

    for wall in collision_walls:

        data.append({

            "x": wall.x,
            "y": wall.y,
            "z": wall.z,

            "scale_x": wall.scale_x,
            "scale_y": wall.scale_y,
            "scale_z": wall.scale_z,

            "rotation_y": wall.rotation_y

        })


    # -----------------------------------------------------
    # ÉCRITURE DU FICHIER
    # -----------------------------------------------------

    try:

        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )


        print("\n================================")
        print("COLLISIONS SAUVEGARDÉES")
        print(
            f"Nombre de colliders : {len(data)}"
        )
        print(
            f"Fichier : {SAVE_FILE}"
        )
        print("================================\n")


    except Exception as error:

        print("\nERREUR DE SAUVEGARDE :")
        print(error)


# =========================================================
# CHARGEMENT DES COLLISIONS
# =========================================================

def load_walls():

    if not os.path.exists(SAVE_FILE):

        print(
            "Aucun fichier collisions.json trouvé."
        )

        print(
            "La map démarre sans collisions "
            "supplémentaires."
        )

        return


    # -----------------------------------------------------
    # LECTURE
    # -----------------------------------------------------

    try:

        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)


        # -------------------------------------------------
        # RECRÉATION
        # -------------------------------------------------

        for collision in data:

            wall = Entity(

                model="cube",

                position=(
                    collision["x"],
                    collision["y"],
                    collision["z"]
                ),

                scale=(
                    collision["scale_x"],
                    collision["scale_y"],
                    collision["scale_z"]
                ),

                rotation_y=collision["rotation_y"],

                collider="box",

                visible=True,

                color=color.rgba(
                    255,
                    0,
                    0,
                    100
                )
            )


            collision_walls.append(wall)


        print("\n================================")
        print("COLLISIONS CHARGÉES")

        print(
            f"Nombre de colliders : "
            f"{len(collision_walls)}"
        )

        print("================================\n")


    except Exception as error:

        print("\nERREUR DE CHARGEMENT :")
        print(error)


# =========================================================
# DEBUG COLLISION
# =========================================================

def collision_debug():

    print("\n")
    print("========================================")
    print("       ANALYSE DE COLLISION")
    print("========================================")

    print(
        f"Position joueur : "
        f"X={player.x:.2f} "
        f"Y={player.y:.2f} "
        f"Z={player.z:.2f}"
    )


    # -----------------------------------------------------
    # DIRECTION
    # -----------------------------------------------------

    direction = player.forward


    # -----------------------------------------------------
    # ORIGINE
    # -----------------------------------------------------

    origin = (
        player.world_position
        + Vec3(0, 1, 0)
    )


    # -----------------------------------------------------
    # RAYCAST
    # -----------------------------------------------------

    hit = raycast(

        origin,

        direction,

        distance=2,

        ignore=[player]

    )


    # -----------------------------------------------------
    # RESULTAT
    # -----------------------------------------------------

    if hit.hit:

        print(">>> OBSTACLE DETECTE")

        print(
            f"Point : "
            f"{hit.world_point}"
        )

        print(
            f"Distance : "
            f"{hit.distance:.2f}"
        )

        print(
            f"Normale : "
            f"{hit.normal}"
        )

        print(
            f"Entite : "
            f"{hit.entity}"
        )


        # -------------------------------------------------
        # TYPE
        # -------------------------------------------------

        if abs(hit.normal.y) < 0.2:

            print(
                "Type probable : "
                "SURFACE VERTICALE"
            )

        elif hit.normal.y > 0.8:

            print(
                "Type probable : SOL"
            )

        elif hit.normal.y < -0.8:

            print(
                "Type probable : PLAFOND"
            )

        else:

            print(
                "Type : SURFACE INCLINEE"
            )


    else:

        print(
            ">>> Aucun obstacle devant le joueur"
        )


    print(
        "========================================"
    )

    print()


# =========================================================
# INPUT
# =========================================================

def input(key):

    global debug
    global wall_start


    # =====================================================
    # F3 : COORDONNÉES
    # =====================================================

    if key == "f3":

        position_text.enabled = (
            not position_text.enabled
        )


    # =====================================================
    # F4 : DEBUG
    # =====================================================

    if key == "f4":

        debug = not debug

        print(
            "MODE DEBUG :",
            "ACTIVE" if debug else "DESACTIVE"
        )


    # =====================================================
    # F5 : ANALYSE
    # =====================================================

    if key == "f5":

        collision_debug()


    # =====================================================
    # F6 : CRÉER UN MUR
    # =====================================================

    if key == "f6":

        # -------------------------------------------------
        # PREMIER APPUI
        # -------------------------------------------------

        if wall_start is None:

            wall_start = Vec3(
                player.x,
                0,
                player.z
            )


            print("\n========== MUR ==========")

            print(
                "Point A enregistré : "
                f"X={wall_start.x:.2f} "
                f"Z={wall_start.z:.2f}"
            )

            print(
                "Déplace-toi jusqu'à "
                "l'autre extrémité "
                "puis appuie sur F6."
            )

            print(
                "==========================\n"
            )


        # -------------------------------------------------
        # DEUXIÈME APPUI
        # -------------------------------------------------

        else:

            wall_end = Vec3(
                player.x,
                0,
                player.z
            )


            create_wall(
                wall_start,
                wall_end
            )


            wall_start = None


    # =====================================================
    # F7 : CRÉER UN POTEAU
    # =====================================================

    if key == "f7":

        post_position = Vec3(
            player.x,
            0,
            player.z
        )


        create_post(
            post_position
        )


    # =====================================================
    # F8 : SAUVEGARDER
    # =====================================================

    if key == "f8":

        save_walls()


# =========================================================
# UPDATE
# =========================================================

def update():

    # =====================================================
    # QUITTER
    # =====================================================

    if held_keys["escape"]:

        application.quit()


    # =====================================================
    # COORDONNÉES
    # =====================================================

    position_text.text = (

        f"X : {player.x:.2f}\n"

        f"Y : {player.y:.2f}\n"

        f"Z : {player.z:.2f}"

    )


    # =====================================================
    # DEBUG
    # =====================================================

    if debug:

        if (

            held_keys["w"]

            or held_keys["s"]

            or held_keys["a"]

            or held_keys["d"]

        ):

            print(

                f"Position : "

                f"X={player.x:.2f} "

                f"Y={player.y:.2f} "

                f"Z={player.z:.2f}"

            )


    # =====================================================
    # SÉCURITÉ ANTI-CHUTE
    # =====================================================

    if player.y < -10:

        player.position = (

            24.79775,

            1,

            35.68929

        )


# =========================================================
# CHARGEMENT DES COLLISIONS
# =========================================================

load_walls()


# =========================================================
# LANCEMENT
# =========================================================

app.run()