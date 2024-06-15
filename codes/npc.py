from numpy import asarray, linalg, array
from PIL import Image
from pyglet.gl import GL_LINEAR
from RpgPyEngine.entity import *
from RpgPyEngine.conf import *
from pyglet.window import key

def voidFunc():
    print("Yes")

class Npc(Entity):
    def __init__(self, pos, size, textures={"default": None}):
        super().__init__(pos, size, textures=textures)
        self.useFunc = voidFunc
    def draw(self):
        super().draw()

    def use(self):
        self.useFunc()
    
    def phys(self, dt):
        super().phys(dt)
    
    
    def colis(self, map, dt):
        super().colis(map, dt)