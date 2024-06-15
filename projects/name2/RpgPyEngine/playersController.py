import pyglet.shapes

from RpgPyEngine.conf import *
from RpgPyEngine.gui import PlayerHud
from RpgPyEngine.player import PlayerForController
from math import atan2, cos, sin, dist

import math


def rotate_around_center(x, y, angle, width, height):
    """
    Вращает 2D объект вокруг его центра.

    Args:
    x (float): X координата левого нижнего угла объекта.
    y (float): Y координата левого нижнего угла объекта.
    angle (float): Угол поворота в градусах.
    width (float): Ширина объекта.
    height (float): Высота объекта.

    Returns:
    (float, float): Новые координаты центра объекта после поворота.
    """

    # Преобразование угла из градусов в радианы
    angle_rad = angle

    # Вычисление центра объекта до поворота
    cx = x - width / 2
    cy = y - height / 2

    # Вращение центра объекта
    new_x = math.cos(angle_rad) * (cx - x) - math.sin(angle_rad) * (cy - y) + x
    new_y = math.sin(angle_rad) * (cx - x) + math.cos(angle_rad) * (cy - y) + y

    return new_x, new_y


# Пример использования функции
x, y = rotate_around_center(0, 0, 45, 10, 20)
#print(f'Новые координаты центра: ({x}, {y})')


class PlayersController:
    def __init__(self, players, cam, window):
        self.selectPlayer = 0
        self.players = players
        self.playerHud = PlayerHud(cam, len(players), self.getHps(), window)
        self.isControl = True
        self.liveEntityList = []
        self.atPr = 255

        self.attackTex = pyglet.image.load(f"res/Attack1.png")
        self.attackSpr = pyglet.sprite.Sprite(self.attackTex, 0, 0)

    def getHps(self):
        hps = []
        for i in range(len(self.players)):
            hps.append(self.players[i].hp/self.players[i].maxHp)
        return hps
    def controlPress(self, symbol):
        if self.isControl == True:
            self.players[self.selectPlayer].controlPress(symbol)
    def controlRel(self, symbol):
        self.players[self.selectPlayer].controlRel(symbol)
    def attack(self, mPos):
        self.atPr = 255
        var = self.getSelectPlayer()
        var2 = var.getCenter()
        var1 = mPos
        var1[0]+=self.playerHud.cam.pos[0]
        var1[1] += self.playerHud.cam.pos[1]
        r = atan2(var1[1] - var2[1], var1[0] - var2[0])

        varya = rotate_around_center(var2[0], var2[1], r, 32*3, 32*3)
        self.attackSpr.scale = 3
        self.attackSpr.x = varya[0]+cos(r)*70
        self.attackSpr.y = varya[1]+sin(r)*70

        self.attackSpr.rotation = math.degrees(-r)
        #pyglet.shapes.Circle(var2[0]+cos(r)*50, var2[1]+sin(r)*50, 50).draw()

        for i in range(len(self.liveEntityList)):
            if dist([var2[0]+cos(r)*50, var2[1]+sin(r)*50], self.liveEntityList[i].getCenter())<50:
                self.liveEntityList[i].hp-=10
    def phys(self, dt):
        if self.atPr>=1:
            self.atPr-=dt*600
        if self.atPr<0:
            self.atPr = 0
        for player in self.players: player.phys(dt)
        if self.selectPlayer > len(self.players)-1:
            self.selectPlayer = len(self.players)-1
        if self.selectPlayer <0:
            self.selectPlayer = 0
    def ai(self, t, map):
        for i in range(1, len(self.players)):
            if i != self.selectPlayer:
                self.players[i].ai(t, map, tuple(pixToTail(self.getSelectPlayer().pos)))
    def colis(self, map, dt):
        for player in self.players: player.colis(map, dt)

    def getSelectPlayer(self):
        return self.players[self.selectPlayer]

    def draw(self, cam, mPos):
        var = self.getSelectPlayer()
        var2 = var.getCenter()
        var1 = mPos
        var1[0] += self.playerHud.cam.pos[0]
        var1[1] += self.playerHud.cam.pos[1]
        r = atan2(var1[1] - var2[1], var1[0] - var2[0])
        self.attackSpr.opacity = int(self.atPr)
        #pyglet.shapes.Circle(var2[0] + cos(r) * 50, var2[1] + sin(r) * 50, 50, color=(255,100,100, int(self.atPr))).draw()
        for player in self.players: player.draw(cam)
        self.attackSpr.draw()
    def movement(self, dt):
        if self.isControl == True:
            for player in self.players: player.movement(dt)
    def restart(self):
        self.getSelectPlayer().pos[0] = 100
        self.getSelectPlayer().pos[1] = 100
        self.getSelectPlayer().isDead = False
        self.getSelectPlayer().hp = 100
        self.playerHud.pushbutton.pop_handlers()

    def drawGui(self, drHp):
        if drHp:
            self.playerHud.draw(self.getSelectPlayer().isDead, self.restart)


class Player(PlayerForController):

    def __init__(self, pos, cam, window):
        super().__init__(pos, [1/32*100,1/32*100])
        self.selectPlayer = 0
        self.cam = cam
        self.playerHud = PlayerHud(cam, 1, self.hp, window)
        self.isControl = True
        self.liveEntityList = []
        self.atPr = 255

        self.attackTex = pyglet.image.load(f"res/Attack1.png")
        self.attackSpr = pyglet.sprite.Sprite(self.attackTex, 0, 0)



    def controlPress(self, symbol):
        if self.isControl:
            super().controlPress(symbol)

    def controlRel(self, symbol):
        super().controlRel(symbol)

    def attack(self, mPos):
        self.atPr = 255

        var2 = self.getCenter()
        var1 = mPos
        var1[0] += self.playerHud.cam.pos[0]
        var1[1] += self.playerHud.cam.pos[1]
        r = atan2(var1[1] - var2[1], var1[0] - var2[0])

        varya = rotate_around_center(var2[0], var2[1], r, 32 * 3, 32 * 3)
        self.attackSpr.scale = 3
        self.attackSpr.x = varya[0] + cos(r) * 70
        self.attackSpr.y = varya[1] + sin(r) * 70

        self.attackSpr.rotation = math.degrees(-r)
        # pyglet.shapes.Circle(var2[0]+cos(r)*50, var2[1]+sin(r)*50, 50).draw()

        for i in range(len(self.liveEntityList)):
            if dist([var2[0] + cos(r) * 50, var2[1] + sin(r) * 50], self.liveEntityList[i].getCenter()) < 50:
                self.liveEntityList[i].hp -= 10

    def phys(self, dt):
        if self.atPr >= 1:
            self.atPr -= dt * 600
        if self.atPr < 0:
            self.atPr = 0
        super().phys(dt)


    def colis(self, map, dt):
        super().colis(map, dt)
    #def updateAttack(self, mPos):

    def draw(self, cam):


        self.attackSpr.opacity = int(self.atPr)
        # pyglet.shapes.Circle(var2[0] + cos(r) * 50, var2[1] + sin(r) * 50, 50, color=(255,100,100, int(self.atPr))).draw()
        super().draw(cam)
        self.attackSpr.draw()

    def movement(self, dt):
        if self.isControl == True:
            super().movement(dt)
    def hpUpdate(self):
        self.playerHud.hps = self.hp
    def restart(self):
        self.pos[0] = 100
        self.pos[1] = 100
        self.isDead = False
        self.hp = 100
        self.playerHud.pushbutton.pop_handlers()

    def drawGui(self, drHp):
        if drHp:
            self.playerHud.draw(self.isDead, self.restart)
