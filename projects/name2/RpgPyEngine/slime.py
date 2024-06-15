from math import *
from random import randint
from numpy import asarray, linalg, array
from PIL import Image
from pyglet.gl import GL_LINEAR
from RpgPyEngine.animationController import *
from RpgPyEngine.conf import *
from pyglet.window import key
from random import randint
from RpgPyEngine.entity import Entity
source = pyglet.media.load('res/audio/step.mp3', streaming=False)


class Slime(Entity):

    def __init__(self, pos, size = [1/32*100,1/32*100], textures ={"default": None}):
        size = [1/32*1000,1/32*1000]
        super().__init__(pos, size, textures ={"default": pyglet.image.load(f"res/player/playerS1.png")})
        self.speed = 900
        self.maxHp = 100
        #self.hud = PlayerHud(self.batc)

        self.animControl = AnimationController(self.pos)
        self.animControl.addAnim("test", [pyglet.image.load("res/sl/1.png"), pyglet.image.load("res/sl/2.png"),pyglet.image.load("res/sl/3.png"),pyglet.image.load("res/sl/4.png")], [0.1, 0.2, 0.3, 0.4])
        self.animControl.addAnim("test2", [pyglet.image.load("res/sl/1f.png"), pyglet.image.load("res/sl/2f.png"),
                                          pyglet.image.load("res/sl/3f.png"), pyglet.image.load("res/sl/4f.png")],
                                 [0.1, 0.2, 0.3, 0.4])
        self.animControl.selectAnim = "test"
        self.attackProcess = 0

        self.stepProcess = randint(0,10)/5
        self.waitProcess = randint(0,10)/5

        self.upProgress = randint(0,10)/5
    def draw(self):
        #super().draw()
        self.animControl.draw()
    def update(self, dt):
        try:
            if dist(self.goal.getCenter(), [self.pos[0]+(100)/2, self.pos[1]+(100)/2])<30:
                self.goalNearby = True
            else:
                self.goalNearby = False
        except:
            self.goalNearby = False
        if self.attackProcess>0.5 and self.goalNearby:
            self.goal.hp -=10
            self.attackProcess = 0
        self.attackProcess += dt
        if self.hp>0:
            self.animControl.update(dt)



    def ai(self, dt):

        if self.hp > 0:
            self.waitProcess += (1 + randint(0, 10) / 10) * dt


            self.rand = randint(-20, 20) / 10
            if self.waitProcess > 1:
                self.stepProcess += (1 + randint(0, 10) / 10) * dt

                var1 = self.goal.getCenter()
                var2 = [self.pos[0] + (100) / 2, self.pos[1] + (100) / 2]
                if var1[0] > var2[0]:
                   self.animControl.selectAnim = "test"
                else:
                   self.animControl.selectAnim = "test2"
                r = atan2(var2[1] - var1[1], var2[0] - var1[0])
                self.velocity[0] -= cos(r + self.rand) * dt * self.speed
                self.velocity[1] -= sin(r + self.rand) * dt * self.speed

                self.pos[1] -= cos(self.stepProcess * pi + pi) * 10
            else:
                self.animControl.anims["test"].process = 0
                self.animControl.anims["test2"].process = 0
            if self.stepProcess > 1:

                self.stepProcess = 0
                self.waitProcess = 0
                self.animControl.process = 0
                self.animControl.goal = 0

    def getCenter(self):
        return [self.pos[0]+(100)/2, self.pos[1]+(100)/2]
    def setGoal(self, goal):
        self.goal = goal
    def phys(self, dt):
        super().phys(dt)
        if self.pos[0]<0:
            self.pos[0] = 0
        if self.pos[1]<0:
            self.pos[1] = 0

        if self.pos[0]>100*70-200:
            self.pos[0] = 100*70-200
        if self.pos[1]>100*70-200:
            self.pos[1] = 100*70-200

    def colis(self, map, dt):
        super().colis(map, dt)

