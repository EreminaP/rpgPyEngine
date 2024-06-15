import pyglet

class textButton(pyglet.gui.PushButton):
    def __init__(self, text, pos, pressed, depressed):
        self.pos = pos
        self.text = text
        self.padX = 35
        self.padY = 25
        self.batch = pyglet.graphics.Batch()
        super().__init__(self.pos[0], self.pos[1], pressed=pressed, depressed=depressed, batch=self.batch)
        self.label = pyglet.text.Label(self.text,
                                       font_name='Arial',
                                       font_size=20,
                                       color=(40,40,40,255),
                                       x=self.padX+self.pos[0], y=self.padY+self.pos[1])
    def update(self):
        self.label.x = self.padX+self.pos[0]
        self.label.y = self.padY+self.pos[1]
        self.x = self.pos[0]
        self.y = self.pos[1]
    def draw(self):
        self.batch.draw()
        self.label.draw()

class textButton1(textButton):
    def __init__(self, text, pos):
        self.pos = pos
        self.text = text
        self.padX = 35
        self.padY = 25
        super().__init__(text, pos, pyglet.image.load(f"res/ui/buttonP.png"), pyglet.image.load(f"res/ui/button.png"))

