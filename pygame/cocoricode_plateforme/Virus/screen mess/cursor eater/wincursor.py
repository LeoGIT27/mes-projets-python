"""API Windows (ctypes) pour Root : fenêtre overlay click-through par-dessus le
bureau, lecture globale souris/clavier, et remplacement du vrai curseur système.

Windows uniquement. Le curseur est restauré via restaurer_curseurs()
(enregistré en atexit dès la première modification).
"""

import atexit
import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_EX_TOOLWINDOW = 0x00000080
LWA_COLORKEY = 0x00000001
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040
OCR_NORMAL = 32512
# L'overlay est click-through : le curseur affiché dépend de la fenêtre dessous
# (flèche, texte, main…). On remplace donc toutes les formes courantes, sinon
# l'effet « mangé » disparaît dès que la souris survole un lien ou du texte.
OCR_REMPLACES = (32512, 32513, 32515, 32649)  # flèche, texte, croix, main
SPI_SETCURSORS = 0x0057
VK_ESCAPE = 0x1B
CURSOR_SHOWING = 0x0001
DI_NORMAL = 0x0003
BI_RGB = 0
DIB_RGB_COLORS = 0


class POINT(ctypes.Structure):
    _fields_ = (("x", ctypes.c_long), ("y", ctypes.c_long))


class ICONINFO(ctypes.Structure):
    _fields_ = (
        ("fIcon", wintypes.BOOL),
        ("xHotspot", wintypes.DWORD),
        ("yHotspot", wintypes.DWORD),
        ("hbmMask", ctypes.c_void_p),
        ("hbmColor", ctypes.c_void_p),
    )


class CURSORINFO(ctypes.Structure):
    _fields_ = (
        ("cbSize", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("hCursor", ctypes.c_void_p),
        ("ptScreenPos", POINT),
    )


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = (
        ("biSize", wintypes.DWORD),
        ("biWidth", ctypes.c_long),
        ("biHeight", ctypes.c_long),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", ctypes.c_long),
        ("biYPelsPerMeter", ctypes.c_long),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    )


class BITMAPINFO(ctypes.Structure):
    _fields_ = (("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wintypes.DWORD * 3))


# Sans restype/argtypes explicites, ctypes tronque les handles 64 bits en int 32 bits.
user32.CreateIconIndirect.restype = ctypes.c_void_p
user32.CreateIconIndirect.argtypes = (ctypes.POINTER(ICONINFO),)
user32.CreateCursor.restype = ctypes.c_void_p
user32.CreateCursor.argtypes = (
    ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_char_p, ctypes.c_char_p,
)
user32.SetSystemCursor.argtypes = (ctypes.c_void_p, wintypes.DWORD)
user32.GetDC.restype = ctypes.c_void_p
user32.GetDC.argtypes = (ctypes.c_void_p,)
user32.ReleaseDC.argtypes = (ctypes.c_void_p, ctypes.c_void_p)
user32.DrawIconEx.argtypes = (
    ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p,
    ctypes.c_int, ctypes.c_int, wintypes.UINT, ctypes.c_void_p, wintypes.UINT,
)
user32.GetCursorInfo.argtypes = (ctypes.POINTER(CURSORINFO),)
user32.GetAsyncKeyState.restype = ctypes.c_short
user32.GetAsyncKeyState.argtypes = (ctypes.c_int,)
user32.SetLayeredWindowAttributes.argtypes = (
    ctypes.c_void_p, wintypes.DWORD, ctypes.c_ubyte, wintypes.DWORD,
)
user32.SetWindowPos.argtypes = (
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int, wintypes.UINT,
)
user32.SystemParametersInfoW.argtypes = (
    wintypes.UINT, wintypes.UINT, ctypes.c_void_p, wintypes.UINT,
)
gdi32.CreateBitmap.restype = ctypes.c_void_p
gdi32.CreateBitmap.argtypes = (
    ctypes.c_int, ctypes.c_int, wintypes.UINT, wintypes.UINT, ctypes.c_char_p,
)
gdi32.CreateCompatibleDC.restype = ctypes.c_void_p
gdi32.CreateCompatibleDC.argtypes = (ctypes.c_void_p,)
gdi32.CreateDIBSection.restype = ctypes.c_void_p
gdi32.CreateDIBSection.argtypes = (
    ctypes.c_void_p, ctypes.POINTER(BITMAPINFO), wintypes.UINT,
    ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p, wintypes.DWORD,
)
gdi32.SelectObject.restype = ctypes.c_void_p
gdi32.SelectObject.argtypes = (ctypes.c_void_p, ctypes.c_void_p)
gdi32.DeleteObject.argtypes = (ctypes.c_void_p,)
gdi32.DeleteDC.argtypes = (ctypes.c_void_p,)

if ctypes.sizeof(ctypes.c_void_p) == 8:
    _get_window_long = user32.GetWindowLongPtrW
    _set_window_long = user32.SetWindowLongPtrW
    _get_window_long.restype = ctypes.c_longlong
    _get_window_long.argtypes = (ctypes.c_void_p, ctypes.c_int)
    _set_window_long.restype = ctypes.c_longlong
    _set_window_long.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_longlong)
else:
    _get_window_long = user32.GetWindowLongW
    _set_window_long = user32.SetWindowLongW

_curseur_modifie = False


def activer_dpi():
    """À appeler avant pygame, sinon GetCursorPos et la fenêtre divergent sur écran mis à l'échelle."""
    try:
        ctypes.WinDLL("shcore").SetProcessDpiAwareness(2)
    except Exception:
        user32.SetProcessDPIAware()


def rendre_overlay(hwnd, couleur_cle=(255, 0, 255)):
    """Fenêtre topmost, click-through, absente d'Alt+Tab ; couleur_cle devient transparente."""
    style = _get_window_long(hwnd, GWL_EXSTYLE)
    _set_window_long(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW)
    r, g, b = couleur_cle
    colorref = r | (g << 8) | (b << 16)
    user32.SetLayeredWindowAttributes(hwnd, colorref, 0, LWA_COLORKEY)
    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW)


def position_souris():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def fixer_position_souris(x, y):
    user32.SetCursorPos(int(x), int(y))


def echap_presse():
    # 0x8000 : touche enfoncée maintenant ; 0x0001 : pressée depuis le dernier
    # appel — indispensable pour ne pas rater un appui plus court qu'une frame.
    return bool(user32.GetAsyncKeyState(VK_ESCAPE) & 0x8001)


def _marquer_modifie():
    global _curseur_modifie
    if not _curseur_modifie:
        _curseur_modifie = True
        atexit.register(restaurer_curseurs)


def appliquer_curseur_pixels(pixels_bgra, largeur, hauteur, hotspot=(0, 0)):
    """Remplace les curseurs système courants par un bitmap BGRA prémultiplié top-down."""
    _marquer_modifie()
    for ocr in OCR_REMPLACES:
        hbm_couleur = gdi32.CreateBitmap(largeur, hauteur, 1, 32, pixels_bgra)
        hbm_masque = gdi32.CreateBitmap(largeur, hauteur, 1, 1, None)
        info = ICONINFO(False, hotspot[0], hotspot[1], hbm_masque, hbm_couleur)
        hcur = user32.CreateIconIndirect(ctypes.byref(info))
        gdi32.DeleteObject(hbm_couleur)
        gdi32.DeleteObject(hbm_masque)
        if not hcur:
            raise ctypes.WinError(ctypes.get_last_error())
        # SetSystemCursor détruit le handle qu'on lui donne : un par forme.
        if not user32.SetSystemCursor(hcur, ocr):
            raise ctypes.WinError(ctypes.get_last_error())


def appliquer_curseur_invisible():
    """Curseur monochrome AND=1/XOR=0 : totalement transparent mais toujours « présent »."""
    taille = 32
    octets = taille * taille // 8
    _marquer_modifie()
    for ocr in OCR_REMPLACES:
        hcur = user32.CreateCursor(None, 0, 0, taille, taille, b"\xff" * octets, b"\x00" * octets)
        if not hcur:
            raise ctypes.WinError(ctypes.get_last_error())
        if not user32.SetSystemCursor(hcur, ocr):
            raise ctypes.WinError(ctypes.get_last_error())


def restaurer_curseurs():
    """Restaure tous les curseurs Windows par défaut."""
    user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, 0)


def capturer_curseur(chemin, taille=96, fond=(24, 24, 32)):
    """Outil de test : dessine le curseur système actuel sur un fond uni et sauve un PNG."""
    from PIL import Image

    ci = CURSORINFO()
    ci.cbSize = ctypes.sizeof(CURSORINFO)
    user32.GetCursorInfo(ctypes.byref(ci))

    hdc_ecran = user32.GetDC(None)
    hdc = gdi32.CreateCompatibleDC(hdc_ecran)
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = taille
    bmi.bmiHeader.biHeight = -taille  # top-down
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = BI_RGB
    bits = ctypes.c_void_p()
    hbm = gdi32.CreateDIBSection(hdc, ctypes.byref(bmi), DIB_RGB_COLORS, ctypes.byref(bits), None, 0)
    ancien = gdi32.SelectObject(hdc, hbm)

    b, g, r = fond[2], fond[1], fond[0]
    rangee = bytes((b, g, r, 255)) * taille
    ctypes.memmove(bits, rangee * taille, taille * taille * 4)
    if ci.flags & CURSOR_SHOWING and ci.hCursor:
        user32.DrawIconEx(hdc, 8, 8, ci.hCursor, 0, 0, 0, None, DI_NORMAL)

    donnees = ctypes.string_at(bits, taille * taille * 4)
    img = Image.frombuffer("RGB", (taille, taille), donnees, "raw", "BGRX", 0, 1)
    img.save(chemin)

    gdi32.SelectObject(hdc, ancien)
    gdi32.DeleteObject(hbm)
    gdi32.DeleteDC(hdc)
    user32.ReleaseDC(None, hdc_ecran)
