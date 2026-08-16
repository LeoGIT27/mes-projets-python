import pygame
import random
import math
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maison des Murmures - Version Horreur")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 20)
BIG = pygame.font.SysFont("consolas", 50)

# =========================
# SON AMBIANCE
# =========================
try:
    pygame.mixer.music.load("ambiance.mp3")  # ajoute un fichier ambiance.mp3
    pygame.mixer.music.play(-1)
except:
    pass  # si pas de son, continue quand même

# =========================
# CARTE DES PIÈCES
# =========================

rooms_pos = {
    "Salon": (550, 350),
    "Cuisine": (350, 350),
    "Couloir": (550, 200),
    "Chambre": (750, 200),
    "Salle de bain": (550, 80),
    "Cave": (200, 500),
    "Grenier": (550, 50),
    "Bibliothèque": (850, 200),
}

connections = {
    "Salon":["Cuisine","Couloir"],
    "Cuisine":["Salon","Cave"],
    "Couloir":["Salon","Chambre","Salle de bain","Grenier","Bibliothèque"],
    "Chambre":["Couloir"],
    "Salle de bain":["Couloir"],
    "Cave":["Cuisine"],
    "Grenier":["Couloir"],
    "Bibliothèque":["Couloir"]
}

locked_doors = {"Cave":True}

items_spawn = {
    "Chambre":["lampe"],
    "Salle de bain":["medicament"],
    "Cuisine":["couteau"],
    "Bibliothèque":["radio"],
    "Grenier":["fausse clé","pile"],
    "Cave":["clé principale"]
}

# =========================
# JOUEUR
# =========================

class Player:
    def __init__(self, color):
        self.room = "Salon"
        self.color = color
        self.x, self.y = rooms_pos[self.room]
        self.speed = 4
        self.noise = 0
        self.hp = 100
        self.sanity = 100
        self.inventory = []
        self.lamp = True
        self.battery = 100

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.noise += (abs(dx)+abs(dy))*0.5

    def update(self):
        # batterie lampe
        if self.lamp:
            self.battery -= 0.05
            if self.battery <= 0:
                self.lamp = False

        # régénération noise
        self.noise = max(0, self.noise - 0.2)
        # folie progressive
        self.sanity -= 0.01

    def draw(self):
        # Lumière dynamique
        if self.lamp:
            radius = 150
            s = pygame.Surface((WIDTH, HEIGHT))
            s.set_alpha(200)
            s.fill((0,0,0))
            pygame.draw.circle(s, (0,0,0,0), (int(self.x), int(self.y)), radius)
            screen.blit(s, (0,0))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 15)

# =========================
# MONSTRE
# =========================

class Monster:
    def __init__(self):
        self.room = random.choice(list(rooms_pos.keys()))
        self.x, self.y = rooms_pos[self.room]
        self.target_x, self.target_y = self.x, self.y
        self.speed = 2

    def update(self, players):
        target = max(players, key=lambda p:p.noise)
        # IA améliorée : suit le joueur si noise > 5
        if target.noise > 5:
            dx = target.x - self.x
            dy = target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 1:
                self.x += dx/dist * self.speed
                self.y += dy/dist * self.speed
        else:
            # sinon bouge aléatoirement
            self.x += random.uniform(-1,1)
            self.y += random.uniform(-1,1)

    def draw(self):
        pygame.draw.circle(screen, (200,0,0), (int(self.x), int(self.y)), 20)

# =========================
# OBJETS
# =========================

def check_pickup(player):
    for room, items in items_spawn.items():
        for item in items[:]:
            if math.hypot(player.x - rooms_pos[room][0], player.y - rooms_pos[room][1]) < 30:
                player.inventory.append(item)
                items.remove(item)
                print(f"Ramassé : {item}")

# =========================
# INITIALISATION
# =========================

player1 = Player((0,200,255))
monster = Monster()
shake = 0

running = True

while running:
    dt = clock.tick(60)/1000
    screen.fill((10,10,20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -----------------
    # INPUT
    # -----------------
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_z] or keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_s]:
        dy = 1
    if keys[pygame.K_q] or keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1

    player1.move(dx, dy)
    player1.update()
    check_pickup(player1)

    monster.update([player1])

    # -----------------
    # COLLISION MONSTRE
    # -----------------
    if math.hypot(player1.x - monster.x, player1.y - monster.y) < 25:
        player1.hp -= 0.5
        shake = 8
        player1.sanity -= 0.5

    # -----------------
    # DESSIN CARTE
    # -----------------
    for room, links in connections.items():
        for link in links:
            pygame.draw.line(screen, (50,50,80),
                             rooms_pos[room],
                             rooms_pos[link], 2)

    for room, pos in rooms_pos.items():
        pygame.draw.circle(screen, (100,100,150), pos, 25)
        text = FONT.render(room, True, (255,255,255))
        screen.blit(text, (pos[0]-40, pos[1]-40))

    # -----------------
    # DESSIN JOUEUR ET MONSTRE
    # -----------------
    if shake>0:
        offset_x = random.randint(-shake,shake)
        offset_y = random.randint(-shake,shake)
        shake -= 1
    else:
        offset_x = offset_y = 0

    temp_surface = pygame.Surface((WIDTH, HEIGHT))
    temp_surface.fill((0,0,0))
    temp_surface.blit(screen, (offset_x, offset_y))
    screen.blit(temp_surface, (0,0))

    player1.draw()
    monster.draw()

    # -----------------
    # HUD
    # -----------------
    hud_text = f"HP:{int(player1.hp)} | SAN:{int(player1.sanity)} | BAT:{int(player1.battery)} | INVENTAIRE:{player1.inventory}"
    screen.blit(FONT.render(hud_text, True, (255,255,255)), (20,20))

    # -----------------
    # HALLUCINATIONS
    # -----------------
    if player1.sanity < 40 and random.random()<0.02:
        screen.blit(BIG.render("IL EST DERRIÈRE TOI", True, (150,0,0)), (200,300))

    # -----------------
    # FINS
    # -----------------
    ending = None
    if "clé principale" in player1.inventory and math.hypot(player1.x - rooms_pos["Salon"][0], player1.y - rooms_pos["Salon"][1])<30:
        ending = "good"
    if player1.sanity <= 0:
        ending = "mad"
    if player1.hp <=0:
        ending = "death"

    if ending:
        screen.fill((0,0,0))
        if ending=="good":
            screen.blit(BIG.render("VOUS ÊTES LIBRES", True, (0,200,0)), (200,300))
        elif ending=="death":
            screen.blit(BIG.render("IL VOUS A EU", True, (200,0,0)), (200,300))
        elif ending=="mad":
            screen.blit(BIG.render("LA FOLIE VOUS EMPORTE", True, (150,0,150)), (150,300))
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()