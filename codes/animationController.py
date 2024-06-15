import pyglet
class Animation:
    def __init__(self, frames, nums, loop = True):
        self.frames = frames
        self.nums = nums
        self.loop = loop
        self.speed = [1]
        self.pos = [0, 0]
        self.process = 0
        self.viewFrame = pyglet.sprite.Sprite(self.frames[0], self.pos[0], self.pos[1])
        self.goal = 0
    def update(self, dt):
        try:
            if self.nums[self.goal]<self.process:
                self.goal+=1
                self.viewFrame = pyglet.sprite.Sprite(self.frames[self.goal], self.pos[0], self.pos[1])
        except:
            self.process = 0
            self.goal = 0
            self.viewFrame = pyglet.sprite.Sprite(self.frames[self.goal], self.pos[0], self.pos[1])
        self.viewFrame.position = (self.pos[0], self.pos[1], 0)
        self.process += dt*self.speed[0]
class AnimationController:
    def __init__(self, pos):
        self.anims = {}
        self.pos = pos
        self.speed = 1
        self.selectAnim = ""
    def addAnim(self, name, frames, nums):
        self.anims[name] = Animation(frames, nums, loop = True)
        self.anims[name].pos = self.pos
        self.anims[name].speed = [self.speed]
    def update(self, dt):
        self.anims[self.selectAnim].update(dt)
    def draw(self):
        self.anims[self.selectAnim].viewFrame.scale = 3
        self.anims[self.selectAnim].viewFrame.draw()


