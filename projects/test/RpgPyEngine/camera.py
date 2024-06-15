class Camera:
    def __init__(self, pos, zoom, resolution, window):
        self.pos = pos
        self.zoom = zoom
        self.var1 = 0.5
        self.resolution = resolution
        self.speedMag = 2
        self.window = window
        self.padX = 0
        self.padY = 0
    def on(self):
        self.var1 = self.zoom / 2
        if self.var1 == 0:
            self.var1 = 0.01
    def go(self, pos):
        self.pos = [pos[0]-self.resolution[0]*self.var1, pos[1]-self.resolution[1]*self.var1]


    def begin(self):
        self.window.view = self.window.view.from_translation((-int((self.pos[0]+self.padX) / self.zoom), -int((self.pos[1]+self.padY) / self.zoom), 0))
        self.window.view = self.window.view.scale((1 / self.zoom, 1 / self.zoom, 1))

    def end(self):
        self.window.view = self.window.view.from_translation((0, 0, 0))
        #window.view = window.view.scale((1 / self.zoom, 1 / self.zoom, 1))

    def center(self, pos, dt):

        posTo = [pos[0]-self.zoom*(self.resolution[0]/2),
                pos[1]-self.zoom*(self.resolution[1]/2)]
        self.pos[0] -= (self.pos[0] - posTo[0]) * self.speedMag*dt
        self.pos[1] -= (self.pos[1] - posTo[1]) * self.speedMag*dt
        #self.pos[0] = int(self.pos[0])
        #self.pos[1] = int(self.pos[1])