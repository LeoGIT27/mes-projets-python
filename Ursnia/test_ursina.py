from ursina import *
from ursina.prefabs import first_person_controller
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.size = (1500, 600)


player = first_person_controller


grid = Entity(
    scale=(10, 1, 10),
    color=rgb(50, 35, 45),
    position=(0, 0, 0),
    visible=True
)


def Update():

    if held_keys == "escape":
        application.quit()



app.run()