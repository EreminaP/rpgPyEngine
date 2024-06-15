from RpgPyEngine import *
from RpgPyEngine.slime import *
from RpgPyEngine.playerController import Player


window = Window(name="Distormium", paramLoad = True)


cam = Camera([0,0], 1, resolution, window)

player = Player([200, 200], cam, window)


dia = DialogWin(cam, player)

testNpc = Npc([200, 1100], [1/32*100,1/32*100], textures={"default": pyglet.image.load('res/cat.png')})

deley1 = Npc([500,600], [1/32*100,1/32*100], textures={"default": pyglet.image.load('res/deley.png')})
deley2 = Npc([500+7*100,600], [1/32*100,1/32*100], textures={"default": pyglet.image.load('res/deley.png')})
deley3 = Npc([500+7*200,600], [1/32*100,1/32*100], textures={"default": pyglet.image.load('res/deley.png')})

testNpc.useFunc = lambda: dia.set("Съешь же ещё этих мягких французских булок, да выпей чаю.", 0.1)
deley1.useFunc = lambda: dia.set("Это демонстрация трения - грязь, и она замедляет когда ступаешь на неё.", 1)
deley2.useFunc = lambda: dia.set("Это демонстрация трения - лёд, наступишь и улетишь в стратосферу.", 1)
deley3.useFunc = lambda: dia.set("Шипы, они наносят урон.", 1)

entitys = [testNpc, deley1, deley2, deley3]


loadMap = "maps/testPlace"

try:
    pass
    #DiscordStat(loadMap)
except:
    pass

map = Map(loadMap, "res/tiles/")


mouseX = 0
mouseY = 0

fade = Fade(255)
fade.set(0, 100)


def sizeUpdate():
    dia.sizeUpdate()



@window.event
def on_key_release(symbol, modifiers):
    player.controlRel(symbol)

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouseY, mouseX
    mouseX = x
    mouseY = y
@window.event
def on_key_press(symbol, modifiers):
    global menu, dia, selectLayer, player

    if symbol == key.SPACE:
        dia.end()

    if symbol == key.F and player.isControl:
        for entity in entitys:
            if type(entity) == Npc:
                if dist(player.getCenter(), entity.getCenter())<50:
                    entity.use()

    if symbol == key.F and player.canAttack:
        player.attack([mouseX, mouseY])



    if symbol == key._1:
        player.ret()



    player.controlPress(symbol) ##########

    if symbol == key.Q:
        cam.zoom-=0.1
        cam.pos[0]+= abs(resolution[0]*(cam.zoom+0.1)-resolution[0]*cam.zoom)/2
        cam.pos[1] += abs(resolution[1] * (cam.zoom + 0.1) - resolution[1] * cam.zoom)/2
        soundZoom1.play()
        if cam.zoom<0.1:
            cam.zoom = 0.1

    if symbol == key.E:
        cam.zoom+=0.1
        cam.pos[0] -= abs(resolution[0] * (cam.zoom + 0.1) - resolution[0] * cam.zoom) / 2
        cam.pos[1] -= abs(resolution[1] * (cam.zoom + 0.1) - resolution[1] * cam.zoom) / 2
        soundZoom2.play()

def update(dt):
    sl1.update(dt)
    sl1.phys(dt)
    sl1.colis(map, dt)
    sl1.ai(dt)

    player.update(dt, map)
    fade.on(dt)

    cam.center(player.pos, dt)


sl1 = Slime([100,100])
sl1.goal = player
window.entitys.append(sl1)
window.entitys.append(player)
player.liveEntityList = window.entitys
def ab1():
    map.matrix[1][12] = [4]    
    del map.spriteTiles[1,12]

def ab2():
    map.matrix[1][12] = [4, 10]
    del map.spriteTiles[1,12]
def ab3():
    dia.set("Синий цветок, очень красивый !!!", 1)

pResolution = [0,0]


tr1 = RectTrigger()
tr1.setTrigger(100,1200,100,100, player, "begin", ab1)

tr2 = RectTrigger()
tr2.setTrigger(100,1200,100,100, player, "end", ab2)

tr3 = RectTrigger()
tr3.setTrigger(300,600,100,100, player, "begin", ab3)
@window.event
def on_draw():

    global zoom, map, cam, menu, select, goSelect, selectTile, tick, selectLayer, mouseTiles, mouseX, mouseY, canPaint, canCat, hpDr, pResolution, liveEntityList


    window.clear()

    cam.begin()

    map.draw(cam.pos, cam.zoom)
    sl1.draw()
    tr1.on()
    tr2.on()
    tr3.on()
    pResolution = cam.resolution.copy()

    resolution[0] = window.width
    resolution[1] = window.height
    if cam.resolution[0] != pResolution[0] or cam.resolution[1] != pResolution[1]:
        sizeUpdate()

    testNpc.draw()
    deley1.draw()
    deley2.draw()
    deley3.draw()

    player.draw(cam)

    cam.end()

    player.drawGui(True)

    dia.draw()
    fade.draw(cam)
    window.drawInfo(cam)


window.start(update)











