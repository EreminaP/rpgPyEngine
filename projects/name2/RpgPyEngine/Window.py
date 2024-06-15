import pyglet
from pyglet.gl import *
from RpgPyEngine.console import closeConsole


def projParam(pathToConf):
    config = dict()
    config["win"] = 0
    config["fps"] = True

    file = open(f"{pathToConf}params.txt", "r")
    lines = file.readlines()
    file.close()
    try:
        for line in lines:
            line = line.replace(" ", "").split("#")[0]
            if line.find("=") != -1:
                div = line.split("=")
                if line.find(",") != -1:
                    var = div[1].replace("\n", "").split(",")
                    for i in range(len(var)):
                        var[i] = int(var[i])
                    config[div[0]] = var
                else:
                    config[div[0]] = div[1]
        for i in config:
            config[i] = str(config[i]).replace("\n", "").replace(" ", "")
            if config[i] == "True":
                config[i] = True
            elif config[i] == "False":
                config[i] = False
            elif config[i].find(".") != -1:
                config[i] = float(config[i])
            else:
                config[i] = int(config[i])
                # 1print(3)
        return config
    except:
        pass

class Window(pyglet.window.Window):
    def __init__(self,sizeX=500,sizeY=500, name="Безымянное окно", resizable=True, vsync = False, fps = 60, paramLoad = False):
        self.entitys = []
        if paramLoad:


            fps = 60
            pp = projParam("")
            if type(pp["fps"]) == bool:
                if pp["fps"]:
                    vsync = True
                else:
                    vsync = False
            else:
                vsync = False
                fps = pp["fps"]

            resolutions = [[800, 600], [1024, 768], [1280, 720]]

            var = resolutions[pp["win"]]

            config = pyglet.gl.Config(double_buffer=True)
            super().__init__(var[0], var[1], name, config=config, resizable=resizable)
        else:
            config = pyglet.gl.Config(double_buffer=True)
            super().__init__(sizeX, sizeY, name, config=config, resizable=resizable)
        pyglet.image.Texture.default_min_filter = GL_NEAREST
        pyglet.image.Texture.default_mag_filter = GL_NEAREST







        try:
            icon = pyglet.image.load('res/icon.ico')
            self.set_icon(icon)
        except:
            pass

        self.limitFps = vsync
        self.set_vsync(self.limitFps)
        self.fps = fps

        self.fps_display = pyglet.window.FPSDisplay(window=self, color=(70, 255, 70, 255), samples=10)
        self.zoomText = pyglet.text.Label(color=(70, 255, 70, 255))

    def start(self, update=None):
        if self.limitFps:
            if update != None: pyglet.clock.schedule_interval(update, 1 / 60)
            pyglet.app.run(interval=1/self.fps)
        else:
            if update != None: pyglet.clock.schedule_interval(update, 1 / 60)
            pyglet.app.run(interval=0)
    def close(self):
        print("Окно закрыто !!!")
        super().close()
        closeConsole()
    def drawInfo(self, cam):
        try:
            self.fps_display.label.position = (0, 0, 0)
            pass
        except:
            pass

        self.zoomText.position = ([self.size[0] - 200, self.size[1] - (self.size[1]) / 7, 0])
        self.zoomText.font_size = 30
        self.zoomText.text = f"zoom: {cam.zoom:.2f}"
        self.fps_display.draw()
        self.zoomText.draw()
