import pyglet.shapes


class RectTrigger:
    def __init__(self):
        self.pos = [0, 0]
        self.size = [0, 0]
        self.targetPos = [0, 0]
        self.targetPos1 = [0, 0]
        self.targetSize = [0, 0]

        self.func = None
        self.event = "" # begin inProgress  end
        self.condition = False
    def updateTargetPos(self):
        #print(self.targetPos)
        self.targetPos = [self.targetPos1[0], self.targetPos1[1]]
    def setTrigger(self, x,y,sX,sY, entity, event, func):
        ePos = entity.getCenter().copy()
        eSize = [entity.colisSize,entity.colisSize]
        self.targetSize = [eSize[0]*2, eSize[1]*2]
        self.targetPos1 = entity.pos

        self.event = event
        self.func = func

        self.pos[0] = x
        self.pos[1] = y
        self.size[0] = sX
        self.size[1] = sY



    def startFunc(self):
        if self.func != None: self.func()

    def on(self):
        #pyglet.shapes.Rectangle(self.targetPos[0], self.targetPos[1], self.targetSize[0], self.targetSize[1]).draw()
        self.updateTargetPos()
        self_left = self.pos[0]
        self_right = self.pos[0] + self.size[0]
        self_top = self.pos[1]
        self_bottom = self.pos[1] + self.size[1]

        # Определяем границы целевого прямоугольника
        target_left = self.targetPos[0]
        target_right = self.targetPos[0] + self.targetSize[0]
        target_top = self.targetPos[1]
        target_bottom = self.targetPos[1] + self.targetSize[1]

        # Проверка на пересечение
        if self_left < target_right and self_right > target_left and self_top < target_bottom and self_bottom > target_top:
            if not self.condition:
                if self.event == "begin":
                    self.condition = True
                    self.startFunc()
            self.condition = True
            if self.event == "inProgress":
                self.startFunc()
        else:
            if self.condition:
                if self.event == "end":

                    self.startFunc()
            self.condition = False
