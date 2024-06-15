from PIL import ImageFont, ImageDraw, Image
import pyglet
font = ImageFont.truetype("arial", 36)

class DialogWin:
    def __init__(self, cam, playerController):
        self.playerController = playerController
        self.textProcess = 0
        self.text = "Пример текста"
        self.fontSize = 20

        self.cam = cam
        self.hide = True
        self.pad = 50
        self.padMini = 10
        self.posX = self.pad
        self.sizeX = cam.resolution[0] - self.pad * 2
        self.sizeY = cam.resolution[1] / 4
        self.speed = 0.4
        try:
            self.texture = pyglet.image.load(f"res/gui/diaWin.png")
            self.imgWidth = self.texture.width
            self.imgHeight = self.texture.height
            self.sp = pyglet.sprite.Sprite(self.texture, 0, 0)
        except:
            pass
        self.label = pyglet.text.Label("",
                                  font_name='Times New Roman',
                                  font_size=self.fontSize,
                                  x=self.posX + self.padMini, y=self.sizeY - self.fontSize - self.padMini,
                                  multiline=True, width=self.sizeX - self.padMini-42)


    def sizeUpdate(self):
        try:
            self.sizeX = self.cam.resolution[0] - self.pad * 2
            self.sizeY = self.cam.resolution[1] / 4
            self.label.x = self.posX + self.padMini+(21*(self.sizeX/self.imgWidth))
            self.label.y = self.sizeY - self.fontSize - self.padMini-(12*(self.sizeY/self.imgHeight))
            self.label.width = self.sizeX - self.padMini-(42*(self.sizeX/self.imgWidth))
        except:
            self.sizeX = self.cam.resolution[0] - self.pad * 2
            self.sizeY = self.cam.resolution[1] / 4
            self.label.x = self.posX + self.padMini
            self.label.y = self.sizeY - self.fontSize - self.padMini
            self.label.width = self.sizeX - self.padMini
    def draw(self):
        if not self.hide:
            self.textProcess +=self.speed
            if self.textProcess > len(self.text):
                self.textProcess = len(self.text)

            #pyglet.shapes.Rectangle(self.posX, 0, self.sizeX, self.sizeY, color=(255, 255, 255, 255)).draw()
            #pyglet.shapes.Rectangle(self.posX+self.padMini, 0+self.padMini, self.sizeX-self.padMini*2, self.sizeY-self.padMini*2, color=(0, 0, 0, 255)).draw()
            try:
                self.sp.x = self.posX
                self.sp.y = 0
                self.sp.scale_x = 1/ self.imgWidth * self.sizeX
                self.sp.scale_y = 1 / self.imgHeight * self.sizeY
                self.sp.draw()
            except:
                pyglet.shapes.Rectangle(self.posX, 0, self.sizeX, self.sizeY, color=(255, 255, 255, 255)).draw()
                pyglet.shapes.Rectangle(self.posX + self.padMini, 0 + self.padMini, self.sizeX - self.padMini * 2,
                                        self.sizeY - self.padMini * 2, color=(0, 0, 0, 255)).draw()
            newText = self.text[:int(self.textProcess)]
            self.label.text = newText


            self.label.draw()

    def set(self, text, speed=0.4):
        self.hide = False
        self.textProcess = 0
        self.text = text
        self.speed = speed
        self.playerController.isControl = False


    def end(self):
        self.playerController.isControl = True
        self.hide = True