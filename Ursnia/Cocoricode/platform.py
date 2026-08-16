from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController as FPC

app = Ursina()

grid = Entity(model = Grid(20, 20), scale = 50, color = color.white, rotation_x = 90,y = 1, collider = "box") #god class

player = FPC(
    model = None,
    position = (0.5,1,0.5),
    speed = 8,
    jump_height= 4,
    gravity = 1,
)
player.visible = False
player.cursor.visible = False



water = Entity(model = Plane(subdivisions=(2,8)), scale = 50, texture = "water.jpg", rotation_x = 0, y = 1, rotation_y = 180)


#MURS
wall1 = Entity(model = "cube", scale =(20,12,1), texture = "sunset.jpeg", collider = "box", x = 0, z = 2, y = 7)
wall2 = Entity(model = "cube", scale =(20,12,1), texture = "sunset.jpeg", collider = "box", x = 0, z = 22, y = 7)
#wall3 = Entity(model = "cube", scale =(20,12,1), texture = "grass.jpeg", collider = "box", x = 10, z = 10, rotation_y = 90, y = 7)
wall4 = Entity(model = "cube", scale =(20,12,1), texture = "VRAIPIERRE.jpg", collider = "box", x =10, z = 12, rotation_y = 90, y = 7)



start = Entity(model = "cube", scale = (2, 1, 2), color = color.red, collider = "box", x = 0, z = 0)
finish = Entity(model = "cube", scale = (2, 1, 2), color = color.red, collider = "box", x = 0, z = 20)

#obstacles

def create_blocks():
    global blocks, original_blocks_position
    blocks = []
    original_blocks_position = []
    z = 0

    for i in range(3):
        z += 3
        for u in range(3):
            x = random.randrange(-8, 8, 3)
            original_blocks_position.append((x,z))
            b = Entity(
                model = "cube",
                scale = (2, 1, 2),
                color = color.orange,
                texture = "stone.png",
                collider = "box",
                x = x,
                z = 8
                )
            blocks.append(b)

create_blocks()






#Update fonction
def update():
    if held_keys["escape"]:
        application.quit()




if __name__ == '__main__':
    app.run()
