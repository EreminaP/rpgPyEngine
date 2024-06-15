# инициализация модулей
import pyglet.sprite
from pyglet.window import key
import os
from RpgPyEngine.load import savePick
import stat
from math import dist
from random import randint

try:soundSelect = pyglet.media.load('res/audio/select.mp3')
except:pass


def fadeNormal(progress, target, speed, dt): # функция изменения fade
    if progress < target:
        progress += speed * dt
    else:
        progress -= speed * dt
    if dist([progress], [target]) <= speed * dt:
        progress = target
    return progress

class Fade: # класс объекта для затемнения экрана
    def __init__(self, start):
        self.batch = pyglet.graphics.Batch()
        texture = pyglet.image.load("res/gui/fade.png")
        self.sp = pyglet.sprite.Sprite(texture, 0, 0, batch=self.batch)
        self.progress = start
        self.func = "normal"
        self.speed = 50
        self.target = 0

    def on(self, dt):
        match self.func:
            case "normal":
                self.progress = fadeNormal(self.progress, self.target, self.speed, dt)

    def set(self, target, speed):
        self.target = target
        self.speed = speed

    def draw(self, cam):
        self.sp.scale_x = 1 / 800 * cam.resolution[0]
        self.sp.scale_y = 1 / 600 * cam.resolution[1]
        self.sp.opacity = self.progress
        self.sp.draw()


class PlayerHud: # hud игрока
    def __init__(self, cam, numPl, hps, window):
        self.batch = pyglet.graphics.Batch()
        self.cam = cam
        self.div = 1/numPl
        self.sp = []
        self.numPl = numPl # количество игроков для отображения нескольких полосок hp
        self.hps = hps
        self.window = window
        self.texGameOver = pyglet.image.load(f"res/gui/gameOvers/winGameOver1.png")
        self.texBut = pyglet.image.load(f"res/gui/butReborn.png")
        self.batch = pyglet.graphics.Batch()
        self.spGameOver = pyglet.sprite.Sprite(self.texGameOver, 0, 0)
        self.pushbutton = pyglet.gui.PushButton(0, 0, pressed=self.texBut, depressed=self.texBut, batch=self.batch)
        self.pIsGameOver = False


    def draw(self, isGameOver, restart):

        if isGameOver != self.pIsGameOver:
            rand = randint(1,4)
            self.texGameOver = pyglet.image.load(f"res/gui/gameOvers/winGameOver{rand}.png")
            self.spGameOver = pyglet.sprite.Sprite(self.texGameOver, 0, 0)


        if self.hps < 0:
            newHps = 0
        else:
            newHps = self.hps/100
        div = self.cam.resolution[0]/1
        pad = div*0.1
        padSize = 5
        posX = div*0 + pad
        posY = self.cam.resolution[1] - 40
        sizeX = div - pad*2
        sizeY = 30
        pyglet.shapes.Rectangle(posX, posY, sizeX, sizeY, color=(40, 40, 40)).draw()
        pyglet.shapes.Rectangle(posX + padSize, posY + padSize, (sizeX - padSize*2) * newHps, sizeY - padSize*2, color=(200,100,100)).draw()

        self.pIsGameOver = isGameOver
        if isGameOver:
            self.pushbutton = pyglet.gui.PushButton(0, 0, pressed=self.texBut, depressed=self.texBut, batch=self.batch)


            center = [self.cam.resolution[0] / 2, self.cam.resolution[1] / 2]

            self.spGameOver.position = (center[0]-400/2, center[1]-280/2, 0)
            self.spGameOver.draw()

            self.pushbutton.x = center[0]-254/2
            self.pushbutton.y = center[1]-280/2+30

            self.window.push_handlers(self.pushbutton)
            self.pushbutton.set_handler('on_press', restart)

            self.batch.draw()
        else:
            pass
        return False

class LayerMenu: # меню выюора слоя на котором будет происходить рисование тайлами
    def __init__(self,cam, tileSet):
        self.cam = cam
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.tileSet = tileSet
        self.info = pyglet.text.Label(
                f"",
                font_name='Arial',
                font_size=14,
                color=(230, 221, 255, 255),
                x=210, y= 300, multiline=True, width=500)

    def draw(self, tiles, layer, pos =[0,0]):
        self.sprites = []

        pyglet.shapes.BorderedRectangle(self.cam.resolution[0] - 100-10, 0,
                                        100 + 10, 100 * (len(tiles))+10, color=(60,60,60),
                                        border_color=(60,60,60), border=10).draw()
        try:
            for i in range(len(tiles)):
                self.sprites.append(pyglet.sprite.Sprite(self.tileSet[tiles[i]].texture,    self.cam.resolution[0]-100, 100 * (i), batch=self.batch))
                self.sprites[-1].scale_x = 1 / 32 * 100
                self.sprites[-1].scale_y = 1 / 32 * 100


            self.batch.draw()
            pyglet.shapes.BorderedRectangle(self.cam.resolution[0]-100,    100*(layer), 100, 100,
                                            border_color=(100, 100, 255, 100), border=10).draw()
            varText = ""
            varText += f"Название: {self.tileSet[tiles[layer]].name}\n"
            varText += f"Индентификатор: {tiles[layer]}\n"
            varText += f"Тип объекта: {type(self.tileSet[tiles[layer]])}\n"
            varText += f"Размер: {self.tileSet[tiles[layer]].texture.width,self.tileSet[tiles[layer]].texture.height}\n"
            varText += f"Позиция: {pos}\n"
            dictParam = {'Твёрдый': self.tileSet[tiles[layer]].solid, 'Трение': self.tileSet[tiles[layer]].friction}
            varText += f"Свойства: {dictParam}"


            self.info.text = f"{varText}"
            self.info.draw()

        except Exception as err:
            print(err)

class TilesMenu: # меню выбора тайла для рисования
    def __init__(self, cam, tileSet, pathToMap, window, proj):

        self.proj = proj

        self.window = window
        self.cam = cam
        self.batch = pyglet.graphics.Batch()
        self.winBatch = pyglet.graphics.Batch()
        self.win2Batch = pyglet.graphics.Batch()
        self.sprites = []
        self.tileSet = tileSet
        self.selectTile = 0
        self.selectProc = 255
        self.pathToMap = pathToMap
        self.spCurs = pyglet.sprite.Sprite(tileSet[self.selectTile].texture,0, 0, batch=self.batch)
        self.delMessage = False


        self.texYes = pyglet.image.load('res/gui/да.png')
        self.texNo = pyglet.image.load('res/gui/нет.png')

        self.winDel = pyglet.sprite.Sprite(pyglet.image.load('res/gui/tileDel.png'), cam.resolution[0]/2-200, cam.resolution[1]/2-200, batch=self.win2Batch)
        self.butYes = pyglet.gui.PushButton(cam.resolution[0]/2-154/2-80, cam.resolution[1]/2-141/2-50, pressed=self.texYes, depressed=self.texYes, batch=self.winBatch)
        self.butNo = pyglet.gui.PushButton(cam.resolution[0]/2-154/2+80, cam.resolution[1]/2-141/2-50, pressed=self.texNo, depressed=self.texNo, batch=self.winBatch)
        self.sizeUpdate()

    def draw(self):
        self.selectProc-=30
        if self.selectProc<0:
            self.selectProc = 0
        self.sizeUpdate()
        self.spCurs = pyglet.sprite.Sprite(self.tileSet[self.selectTile].texture,    self.cam.resolution[0]-100, 0, batch=self.batch)
        self.spCurs.scale_x = 1 / 32 * 100
        self.spCurs.scale_y = 1 / 32 * 100

        pyglet.shapes.Rectangle(0,0, self.cam.resolution[0], self.cam.resolution[0], color=(40,40,40,200)).draw()
        self.batch.draw()
        pyglet.shapes.BorderedRectangle(self.cam.resolution[0]-100, 0, 100, 100,
                                        border_color=(255, 255, 100, self.selectProc), border=10).draw()
        if self.delMessage:
            self.win2Batch.draw()
            self.winBatch.draw()
    def control(self, x, y):
        self.selectProc = 255
        select = [int((x) / self.cam.resolution[0] * 10), int((self.cam.resolution[1] - y) / self.cam.resolution[1] * 10)]
        for i in range(len(self.sprites)):
            y = i // 10
            x = i % 10
            if x == select[0] and y == select[1]:
                if i <= len(self.tileSet):
                    self.selectTile = i
                    try: soundSelect.play()
                    except: pass

        return self.selectTile
    def sizeUpdate(self): # обновление размера при изменении разрешения окна игры
        self.winDel.x = self.cam.resolution[0] / 2 - 200
        self.winDel.y = self.cam.resolution[1] / 2 - 200

        self.butYes.x = self.cam.resolution[0] / 2 - 154 / 2 - 80
        self.butYes.y = self.cam.resolution[1] / 2 - 141 / 2 - 50
        self.butNo.x = self.cam.resolution[0] / 2 - 154 / 2 + 80
        self.butNo.y = self.cam.resolution[1] / 2 - 141 / 2 - 50


        self.sprites = []
        endFlag = False
        i = 0
        for y in range(5):
            if endFlag:
                break
            for x in range(10):
                if i == len(self.tileSet):
                    endFlag = True
                    break
                self.sprites.append(pyglet.sprite.Sprite(self.tileSet[i].texture, x * (self.cam.resolution[0] / 10),
                                                         self.cam.resolution[1] - (1+y) * 100,
                                                         batch=self.batch))
                self.sprites[len(self.sprites)-1].scale_x = 1/32 * self.cam.resolution[1]/10
                self.sprites[len(self.sprites) - 1].scale_y = 1/32 * self.cam.resolution[1]/10

                i += 1

    def noDelTile(self): # при отказе от удаления тайла
        self.delMessage = False
        self.winDel = pyglet.sprite.Sprite(pyglet.image.load('res/gui/tileDel.png'), self.cam.resolution[0] / 2 - 200,
                                           self.cam.resolution[1] / 2 - 200, batch=self.win2Batch)
        self.butYes = pyglet.gui.PushButton(self.cam.resolution[0] / 2 - 154 / 2 - 80,
                                            self.cam.resolution[1] / 2 - 141 / 2 - 50, pressed=self.texYes,
                                            depressed=self.texYes, batch=self.winBatch)
        self.butNo = pyglet.gui.PushButton(self.cam.resolution[0] / 2 - 154 / 2 + 80,
                                           self.cam.resolution[1] / 2 - 141 / 2 - 50, pressed=self.texNo,
                                           depressed=self.texNo, batch=self.winBatch)

    def delTile(self): # при удалении тайла
        proj = self.proj
        self.delMessage = False
        self.winDel = pyglet.sprite.Sprite(pyglet.image.load('res/gui/tileDel.png'), self.cam.resolution[0] / 2 - 200,
                                           self.cam.resolution[1] / 2 - 200, batch=self.win2Batch)
        self.butYes = pyglet.gui.PushButton(self.cam.resolution[0] / 2 - 154 / 2 - 80,
                                            self.cam.resolution[1] / 2 - 141 / 2 - 50, pressed=self.texYes,
                                            depressed=self.texYes, batch=self.winBatch)
        self.butNo = pyglet.gui.PushButton(self.cam.resolution[0] / 2 - 154 / 2 + 80,
                                           self.cam.resolution[1] / 2 - 141 / 2 - 50, pressed=self.texNo,
                                           depressed=self.texNo, batch=self.winBatch)

        listDir = os.listdir(f"{proj}")
        for i in range(len(listDir)):

            self.tileSet[self.selectTile].name = str(self.tileSet[self.selectTile].name)
            listDir[i] = str(listDir[i])
            if str(self.tileSet[self.selectTile].name) == str(listDir[i]):

                dirPath = f"{proj}{self.tileSet[self.selectTile].name}"

                listDir2 = os.listdir(dirPath)
                for i2 in range(len(listDir2)):
                    os.remove(dirPath + "/" + listDir2[i2])
                os.rmdir(dirPath)
                break

        self.tileSet[self.selectTile] = self.tileSet[0]
        self.tileSet[self.selectTile].empty = True

        forSave = dict()
        for i in range(len(self.tileSet)):
            forSave[self.tileSet[i].name] = i

        savePick(self.pathToMap, forSave)
        self.sprites[self.selectTile] = pyglet.sprite.Sprite(self.tileSet[0].texture, 0, 0, batch=self.batch)

    def keyboard(self, symbol):
        if symbol == key.DELETE:
            self.delMessage = True
            self.window.push_handlers(self.butYes)
            self.butYes.set_handler('on_press', self.delTile)

            self.window.push_handlers(self.butNo)
            self.butNo.set_handler('on_press', self.noDelTile)







