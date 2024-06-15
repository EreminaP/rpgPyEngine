from RpgPyEngine.player import *
from RpgPyEngine.map import *
from RpgPyEngine.gui import *
from RpgPyEngine.playersController import PlayersController
from RpgPyEngine.characters import *
from RpgPyEngine.dialogWin import *
from RpgPyEngine.conf import *
from RpgPyEngine.camera import Camera
from RpgPyEngine.load import loadTileSet
from RpgPyEngine.mapTools import *
from RpgPyEngine.npc import *
from RpgPyEngine.animationController import *
from RpgPyEngine.discord import DiscordStat
from RpgPyEngine.Window import *
from RpgPyEngine.console import *
from RpgPyEngine.triggers import *

version = "v0.1.5.0"

print(f"RpgPyEngine: {version}")

try:
    soundMenu = pyglet.media.load('res/audio/menu.mp3', streaming=False)
    soundSet = pyglet.media.load('res/audio/set.mp3')
    soundSelectLayer = pyglet.media.load('res/audio/selectLayer.mp3')

    soundZoom1 = pyglet.media.load('res/audio/zoom+.mp3')
    soundZoom2 = pyglet.media.load('res/audio/zoom-.mp3')
except:pass