from math import *
from random import randint
from numpy import asarray, linalg, array
from PIL import Image
from pyglet.gl import GL_LINEAR

from RpgPyEngine.conf import *
from pyglet.window import key
try:source = pyglet.media.load('res/audio/step.mp3', streaming=False)
except:pass
def layer(img1, img2):
    numpydata1 = asarray(img1.image).copy()
    numpydata2 = asarray(img2.image).copy()
    for x in range(len(numpydata1)):
        for y in range(len(numpydata1[0])):
            if numpydata2[x][y][3]>200:
                numpydata1[x][y][0]=numpydata2[x][y][0]
                numpydata1[x][y][1] = numpydata2[x][y][1]
                numpydata1[x][y][2] = numpydata2[x][y][2]
    return Image.fromarray(numpydata1.astype('uint8'), 'RGBA')

def finb(str, text):
    if str.find(text) != -1:
        return True


from RpgPyEngine.entity import Entity
class PlayerForController(Entity):

    def __init__(self, pos, size, textures ={"default": None}):
        super().__init__(pos, size, textures ={"default": pyglet.image.load(f"res/player/playerS1.png")})
        self.speed = 1000#1000

        self.maxHp = 100
        #self.hud = PlayerHud(self.batc)
        self.cam = [0,0]
        self.pVelocity = [self.velocity[0], self.velocity[1]]
        self.keys = {'w':False,'s':False, 'd':False, 'a':False, 'f':False}
        self.t = 0
        self.tp = 0
        self.animW = [pyglet.image.load('res/player/playerW1.png'), pyglet.image.load('res/player/playerW2.png'), pyglet.image.load('res/player/playerW3.png')]
        self.animA = [pyglet.image.load('res/player/playerA1.png'), pyglet.image.load('res/player/playerA2.png'), pyglet.image.load('res/player/playerA3.png')]
        self.animS = [pyglet.image.load('res/player/playerS1.png'), pyglet.image.load('res/player/playerS2.png'), pyglet.image.load('res/player/playerS3.png')]
        self.animD = [pyglet.image.load('res/player/playerD1.png'), pyglet.image.load('res/player/playerD2.png'), pyglet.image.load('res/player/playerD3.png')]
        self.upProgress = 0
        self.canAttack = False
        self.t2 = 0
        self.last = ""

    def update(self, dt, map):
        self.phys(dt)

        # print(type(player.playerHud))
        self.hpUpdate()  ################
        self.movement(dt)
        self.colis(map, dt)
    def ret(self):
        if self.canAttack == False:
            self.canAttack = True
            self.animW = [pyglet.image.load('res/playerK/playerW1.png'), pyglet.image.load('res/playerK/playerW2.png'),
                          pyglet.image.load('res/playerK/playerW3.png')]
            self.animA = [pyglet.image.load('res/playerK/playerA1.png'), pyglet.image.load('res/playerK/playerA2.png'),
                          pyglet.image.load('res/playerK/playerA3.png')]
            self.animS = [pyglet.image.load('res/playerK/playerS1.png'), pyglet.image.load('res/playerK/playerS2.png'),
                          pyglet.image.load('res/playerK/playerS3.png')]
            self.animD = [pyglet.image.load('res/playerK/playerD1.png'), pyglet.image.load('res/playerK/playerD2.png'),
                          pyglet.image.load('res/playerK/playerD3.png')]
        else:
            self.canAttack = False
            self.animW = [pyglet.image.load('res/player/playerW1.png'), pyglet.image.load('res/player/playerW2.png'),
                          pyglet.image.load('res/player/playerW3.png')]
            self.animA = [pyglet.image.load('res/player/playerA1.png'), pyglet.image.load('res/player/playerA2.png'),
                          pyglet.image.load('res/player/playerA3.png')]
            self.animS = [pyglet.image.load('res/player/playerS1.png'), pyglet.image.load('res/player/playerS2.png'),
                          pyglet.image.load('res/player/playerS3.png')]
            self.animD = [pyglet.image.load('res/player/playerD1.png'), pyglet.image.load('res/player/playerD2.png'),
                          pyglet.image.load('res/player/playerD3.png')]
    def movement(self, dt):

        if self.keys['w']==True or self.keys['a']==True or self.keys['s']==True or self.keys['d']==True:
            self.tp = self.t
            self.t += 3
            self.t2 = 0
        if self.keys['w']:
            if self.t>33 and self.tp <= 33:
                source.play()
                self.spr = pyglet.sprite.Sprite(self.animW[1], 0, 0, batch = self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.t > 66 and self.tp <= 66:
                source.play()
                self.spr = pyglet.sprite.Sprite(self.animW[2], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.t > 100:
                source.play()
                self.t = 0
                self.spr = pyglet.sprite.Sprite(self.animW[0], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
        if self.keys['a']:
            if self.t>33 and self.tp <= 33:
                source.play()
                self.spr = pyglet.sprite.Sprite(self.animA[1], 0, 0, batch = self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.t > 66 and self.tp <= 66:
                source.play()
                self.spr = pyglet.sprite.Sprite(self.animA[2], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.t > 100:
                source.play()
                self.t = 0
                self.spr = pyglet.sprite.Sprite(self.animA[0], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
        if self.keys['d']:
            if self.t>33 and self.tp <= 33:
                source.play()
                self.spr = pyglet.sprite.Sprite(self.animD[1], 0, 0, batch = self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.t > 66 and self.tp <= 66:
                source.play()
                self.spr = pyglet.sprite.Sprite(self.animD[2], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.t > 100:
                source.play()
                self.t = 0
                self.spr = pyglet.sprite.Sprite(self.animD[0], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
        if self.keys['s']:
            if self.t>33 and self.tp <= 33:
                source.play()
                self.spr = pyglet.sprite.Sprite(self.animS[1], 0, 0, batch = self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.t > 66 and self.tp <= 66:
                source.play()
                self.spr = pyglet.sprite.Sprite(self.animS[2], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.t > 100:
                source.play()
                self.t = 0
                self.spr = pyglet.sprite.Sprite(self.animS[0], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]

        if self.isDead == False:
            if self.keys['w']:
                self.up(dt)
                self.last = "w"

            if self.keys['s']:
                self.down(dt)
                self.last = "s"

            if self.keys['a']:
                self.left(dt)
                self.last = "a"

            if self.keys['d']:
                self.right(dt)
                self.last = "d"
    def draw(self, cam):



        if self.t2>0.5:
            self.t2 = 0.5
            if self.last == "w":
                self.spr = pyglet.sprite.Sprite(self.animW[1], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.last == "s":
                self.spr = pyglet.sprite.Sprite(self.animS[1], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.last == "a":
                self.spr = pyglet.sprite.Sprite(self.animA[1], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]
            if self.last == "d":
                self.spr = pyglet.sprite.Sprite(self.animD[1], 0, 0, batch=self.batc)
                self.spr.scale_x = self.size[0]
                self.spr.scale_y = self.size[1]

        self.cam = cam
        super().draw()

    def phys(self, dt):
        self.t2 += dt*1
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

    def up(self, dt):
        self.velocity[1] += self.speed*dt

    def down(self, dt):
       self.velocity[1] -= self.speed*dt

    def right(self, dt):
        self.velocity[0] += self.speed*dt

    def left(self, dt):
        self.velocity[0] -= self.speed*dt

    def controlPress(self, symbol):
        if symbol == key.W:
            self.keys['w'] = True
        if symbol == key.S:
            self.keys['s'] = True
        if symbol == key.A:
            self.keys['a'] = True
        if symbol == key.D:
            self.keys['d'] = True
        if symbol == key.F:
            self.keys['f'] = True

    def controlRel(self, symbol):
        if symbol == key.W:
            self.keys['w'] = False
        if symbol == key.S:
            self.keys['s'] = False
        if symbol == key.A:
            self.keys['a'] = False
        if symbol == key.D:
            self.keys['d'] = False
        if symbol == key.F:
            self.keys['f'] = False


