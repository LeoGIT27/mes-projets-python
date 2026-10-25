"""Secours : restaure les curseurs Windows par défaut.

À lancer si Root a planté en laissant le curseur mangé :  py restaure_curseur.py
(Équivalent : Paramètres > Bluetooth et appareils > Souris > Paramètres souris supplémentaires.)
"""

import ctypes

SPI_SETCURSORS = 0x0057
ctypes.WinDLL("user32").SystemParametersInfoW(SPI_SETCURSORS, 0, None, 0)
print("Curseurs Windows restaurés.")
