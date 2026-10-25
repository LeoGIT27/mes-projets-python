import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import subprocess
import ctypes
import sys


# ============================================================
# CONFIGURATION
# ============================================================

ANIMATION_INTERVAL = 90
SHAKE_INTERVAL = 55
DESKTOP_SHIFT_INTERVAL = 90

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 760

ANGRY_WINDOW_SIZE = 300

DISCLAIMER = (
    "I am not responsible for any damage potentially caused on this machine.\n"
    "This is an educational program. You have been warned."
)

TREATH_MESSAGE = (
    "If you've heard I'm not Soffitrj, I'm worse.\n"
    "I dare you: don't try to kill me."
)


# ============================================================
# CHEMIN DES ASSETS
# ============================================================

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def asset(filename):
    return os.path.join(ASSETS_DIR, filename)


# ============================================================
# VARIABLES
# ============================================================

scene = "warning"

talking = False

neutral_image = None
talking_image = None
angry_image = None

neutral_photo = None
talking_photo = None
angry_photo = None

music_process = None
music_loops = 0

angry_windows = [None, None]
angry_origins = [(0, 0), (0, 0)]
angry_shake_steps = [0, 17]

animation_job = None
music_job = None
shake_job = None
desktop_job = None


# ============================================================
# AUDIO
# ============================================================

def stop_audio():
    global music_process

    if music_process is not None:

        try:
            music_process.terminate()
        except Exception:
            pass

        music_process = None


def play_file(filename):
    """
    Joue un fichier audio avec Windows Media Player.
    """

    path = asset(filename)

    if not os.path.exists(path):
        return None

    try:
        process = subprocess.Popen(
            [
                "wmplayer.exe",
                "/play",
                "/close",
                "/quiet",
                path
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        return process

    except Exception as e:
        print("Erreur audio :", e)
        return None


def play_music_once():
    global music_process
    global music_loops

    if music_process is not None:
        return

    if music_loops >= 3:
        return

    path = asset("NotSoffizMusic.mp3")

    if not os.path.exists(path):
        print("Musique introuvable :", path)
        return

    music_process = play_file("NotSoffizMusic.mp3")

    if music_process is not None:
        music_loops += 1


def play_dialogue_sound():
    global music_process

    path = asset("NotSoffizSFX1.m4a")

    if not os.path.exists(path):
        print("Son introuvable :", path)
        return

    process = play_file("NotSoffizSFX1.m4a")

    if process is not None:
        music_process = process


# ============================================================
# EFFET DE DÉPLACEMENT DU BUREAU
# ============================================================

def shift_desktop():
    """
    Reproduit le BitBlt du programme C++.

    ATTENTION :
    Cette partie est spécifique à Windows.
    """

    if sys.platform != "win32":
        return

    try:
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32

        # Coordonnées du bureau virtuel
        SM_XVIRTUALSCREEN = 76
        SM_YVIRTUALSCREEN = 77
        SM_CXVIRTUALSCREEN = 78
        SM_CYVIRTUALSCREEN = 79

        left = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
        top = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
        width = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
        height = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)

        hdc = user32.GetDC(0)

        if not hdc:
            return

        offset_x = random.randint(-8, 7)
        offset_y = random.randint(-8, 7)

        SRCCOPY = 0x00CC0020

        gdi32.BitBlt(
            hdc,
            left + offset_x,
            top + offset_y,
            width,
            height,
            hdc,
            left,
            top,
            SRCCOPY
        )

        user32.ReleaseDC(0, hdc)

    except Exception as e:
        print("Erreur ShiftDesktop :", e)


# ============================================================
# CHARGEMENT DES IMAGES
# ============================================================

def load_assets():

    global neutral_image
    global talking_image
    global angry_image

    global neutral_photo
    global talking_photo
    global angry_photo

    try:
        neutral_image = Image.open(
            asset("NotSoffiz.jpg")
        ).convert("RGB")

        talking_image = Image.open(
            asset("TalkingNotSoffiz.jpg")
        ).convert("RGB")

        angry_image = Image.open(
            asset("AngryNotSoffiz.jpg")
        ).convert("RGB")

    except Exception as e:
        print("Erreur lors du chargement des images :")
        print(e)
        return False

    # Image principale : 290 x 290
    neutral_resized = neutral_image.resize(
        (290, 290),
        Image.Resampling.LANCZOS
    )

    talking_resized = talking_image.resize(
        (290, 290),
        Image.Resampling.LANCZOS
    )

    neutral_photo = ImageTk.PhotoImage(neutral_resized)
    talking_photo = ImageTk.PhotoImage(talking_resized)

    return True


# ============================================================
# FENÊTRE PRINCIPALE
# ============================================================

root = tk.Tk()

root.title("Not Soffiz")

root.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
)

root.resizable(False, False)

root.configure(
    bg="#0A0A0E"
)


# ============================================================
# CANVAS PRINCIPAL
# ============================================================

canvas = tk.Canvas(
    root,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    bg="#0A0A0E",
    highlightthickness=0
)

canvas.pack()


# ============================================================
# DESSIN DE LA FENÊTRE
# ============================================================

def draw_main_window():

    canvas.delete("all")

    # --------------------------------------------------------
    # Fond
    # --------------------------------------------------------

    canvas.create_rectangle(
        0,
        0,
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        fill="#0A0A0E",
        outline=""
    )

    # --------------------------------------------------------
    # Visage
    # --------------------------------------------------------

    current_photo = (
        talking_photo
        if talking and talking_photo is not None
        else neutral_photo
    )

    if current_photo is not None:

        canvas.create_image(
            WINDOW_WIDTH // 2,
            28 + 145,
            image=current_photo,
            anchor="center"
        )

    # --------------------------------------------------------
    # Dialogue box
    # --------------------------------------------------------

    dialogue_x1 = 32
    dialogue_y1 = 342
    dialogue_x2 = WINDOW_WIDTH - 32
    dialogue_y2 = WINDOW_HEIGHT - 36

    canvas.create_rectangle(
        dialogue_x1,
        dialogue_y1,
        dialogue_x2,
        dialogue_y2,
        fill="#16171D",
        outline="#E2365E",
        width=2
    )

    # --------------------------------------------------------
    # NOT SOFFIZ
    # --------------------------------------------------------

    canvas.create_text(
        WINDOW_WIDTH // 2,
        374,
        text="NOT SOFFIZ",
        fill="#FFD140",
        font=("Consolas", 20, "bold")
    )

    # --------------------------------------------------------
    # Message
    # --------------------------------------------------------

    if scene == "warning":
        message = DISCLAIMER
    else:
        message = TREATH_MESSAGE

    canvas.create_text(
        WINDOW_WIDTH // 2,
        450,
        text=message,
        fill="#F0F0F0",
        font=("Consolas", 18),
        justify="center",
        width=520
    )

    # --------------------------------------------------------
    # ENTER
    # --------------------------------------------------------

    if scene == "warning":
        bottom_text = "[ ENTER ] CONTINUE"
    else:
        bottom_text = "[ ENTER ] CLOSE"

    canvas.create_text(
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT - 48,
        text=bottom_text,
        fill="#A0A0A0",
        font=("Consolas", 14)
    )


# ============================================================
# ANIMATION DU VISAGE
# ============================================================

def animation_loop():

    global talking

    if scene != "anger":

        talking = not talking

        draw_main_window()

    global animation_job

    animation_job = root.after(
        ANIMATION_INTERVAL,
        animation_loop
    )


# ============================================================
# FENÊTRES ANGRY
# ============================================================

def create_angry_window(index):

    global angry_image
    global angry_photo

    if angry_windows[index] is not None:
        return

    window = tk.Toplevel(root)

    window.title("Not Soffiz?!")

    window.geometry(
        f"{ANGRY_WINDOW_SIZE}x{ANGRY_WINDOW_SIZE}"
    )

    window.resizable(False, False)

    window.overrideredirect(True)

    window.attributes("-topmost", True)

    # --------------------------------------------------------
    # Position
    # --------------------------------------------------------

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (
        (screen_width - ANGRY_WINDOW_SIZE)
        * (index + 1)
        // 3
    )

    y = (
        (screen_height - ANGRY_WINDOW_SIZE)
        // 2
    )

    angry_origins[index] = (x, y)

    window.geometry(
        f"{ANGRY_WINDOW_SIZE}x{ANGRY_WINDOW_SIZE}+{x}+{y}"
    )

    # --------------------------------------------------------
    # Image
    # --------------------------------------------------------

    if angry_image is not None:

        resized = angry_image.resize(
            (ANGRY_WINDOW_SIZE, ANGRY_WINDOW_SIZE),
            Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(resized)

        # On garde la référence dans la fenêtre
        window.angry_photo = photo

        label = tk.Label(
            window,
            image=photo,
            bg="#0A0A0E"
        )

    else:

        label = tk.Label(
            window,
            text="ANGRY",
            fg="white",
            bg="#0A0A0E",
            font=("Consolas", 30, "bold")
        )

    label.pack(
        fill="both",
        expand=True
    )

    # --------------------------------------------------------
    # Fermer les fenêtres Angry
    # --------------------------------------------------------

    def close_angry():
        stop_angry_scene()

    window.protocol(
        "WM_DELETE_WINDOW",
        close_angry
    )

    angry_windows[index] = window


# ============================================================
# DÉMARRER LA SCÈNE ANGER
# ============================================================

def start_anger_scene():

    global scene
    global music_loops

    scene = "anger"

    # Arrêt de l'animation
    global animation_job

    if animation_job is not None:
        root.after_cancel(animation_job)
        animation_job = None

    # Arrêt du dialogue animé
    global talking

    talking = False

    # Création des deux fenêtres
    create_angry_window(0)
    create_angry_window(1)

    # Musique
    music_loops = 0

    play_music_once()

    # Timers
    root.after(
        500,
        music_loop
    )

    root.after(
        SHAKE_INTERVAL,
        shake_loop
    )

    root.after(
        DESKTOP_SHIFT_INTERVAL,
        desktop_shift_loop
    )


# ============================================================
# MUSIQUE
# ============================================================

def music_loop():

    global music_process

    if scene != "anger":
        return

    if music_process is not None:

        try:
            finished = (
                music_process.poll()
                is not None
            )

        except Exception:
            finished = True

        if finished:
            music_process = None
            play_music_once()

    root.after(
        500,
        music_loop
    )


# ============================================================
# TREMBLEMENT DES FENÊTRES
# ============================================================

TREMOR_PATTERN = [
    (-12, 8),
    (10, -6),
    (-7, -10),
    (13, 4),
    (-4, 12),
    (8, -3),
    (-11, -7),
    (5, 6)
]


def shake_loop():

    if scene != "anger":
        return

    for index in range(2):

        window = angry_windows[index]

        if window is None:
            continue

        step = angry_shake_steps[index]

        tremor = TREMOR_PATTERN[
            step % len(TREMOR_PATTERN)
        ]

        origin_x, origin_y = angry_origins[index]

        x = origin_x + tremor[0]
        y = origin_y + tremor[1]

        window.geometry(
            f"{ANGRY_WINDOW_SIZE}x{ANGRY_WINDOW_SIZE}"
            f"+{x}+{y}"
        )

        angry_shake_steps[index] += 1

    root.after(
        SHAKE_INTERVAL,
        shake_loop
    )


# ============================================================
# DÉPLACEMENT DU BUREAU
# ============================================================

def desktop_shift_loop():

    if scene != "anger":
        return

    shift_desktop()

    root.after(
        DESKTOP_SHIFT_INTERVAL,
        desktop_shift_loop
    )


# ============================================================
# ARRÊTER LA SCÈNE ANGER
# ============================================================

def stop_angry_scene():

    global scene
    global music_process

    scene = "anger"

    stop_audio()

    for index in range(2):

        window = angry_windows[index]

        if window is not None:

            try:
                window.destroy()
            except Exception:
                pass

            angry_windows[index] = None

    # Ferme la fenêtre principale
    root.destroy()


# ============================================================
# TOUCHE ENTRÉE
# ============================================================

def on_enter(event=None):

    global scene

    if scene == "warning":

        scene = "threat"

        draw_main_window()

    elif scene == "threat":

        start_anger_scene()

    elif scene == "anger":

        stop_angry_scene()


root.bind(
    "<Return>",
    on_enter
)


# ============================================================
# FERMETURE DE LA FENÊTRE
# ============================================================

def on_close():

    if scene != "anger":

        start_anger_scene()

    else:

        stop_angry_scene()


root.protocol(
    "WM_DELETE_WINDOW",
    on_close
)


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    if not os.path.exists(ASSETS_DIR):

        print(
            "ERREUR : dossier 'assets' introuvable."
        )

        print(
            "Le dossier doit être ici :"
        )

        print(
            ASSETS_DIR
        )

        sys.exit(1)

    if not load_assets():

        sys.exit(1)

    draw_main_window()

    # Son de dialogue au lancement
    play_dialogue_sound()

    # Animation
    animation_loop()

    # Boucle principale
    root.mainloop()

    # Nettoyage
    stop_audio()