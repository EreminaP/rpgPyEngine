import pyglet
from RpgPyEngine.conf import tileParam, void
import os
import pickle

class Tile(): # класс тайла
    def __init__(self, texture=void, empty=False):
        self.name = ""
        self.texture = texture
        self.solid = False
        self.empty = empty
        self.friction = 1.05
        self.rotation = 0
        self.damage = 0
def paramToTile(tile, param): # применение параметров к тайлу
    tile.solid = param["solid"]
    tile.friction = param["friction"]
    tile.name = param["name"]
    tile.rotation = param["rotation"]
    tile.damage = int(param["damage"])


def loadPick(path): # загрузка файла в формате pickle
    with open(path+'/tilesId.pickle', 'rb') as handle:
        b = pickle.load(handle)
    return b

def savePick(path, a): # сохранение файла в формате pickle
    with open(path+'/tilesId.pickle', 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

def getWorkTiles(tilesId, pathToTiles): # проверка какие есть тайлы в дериктории и в tilesId
    existTiles = os.listdir(pathToTiles)
    res = []
    for i in tilesId:
        for i2 in existTiles:
            if i == i2:
                res.append(i)
    return res

def loadTile(name, pathToTiles): # загрузка тайла

    tile = Tile(pyglet.image.load(f"{pathToTiles}{name}/image.png"))

    param = tileParam(f"{pathToTiles}{name}")
    paramToTile(tile, param)
    return tile


def createEmptyTileSet(workTilesInt): # создание пустого набора тайлов
    workTilesInt = list(workTilesInt)
    for i in range(len(workTilesInt)):
        workTilesInt[i] = int(workTilesInt[i][1])
    var = max(workTilesInt) + 1

    tileSet = [Tile(empty=True)] * var
    tileSet[0] = Tile()

    return tileSet

def getNotWorkTiles(workTiles, listDir): # получение тех тайлов которые есть в папке, но нету в tilesId
    try:
        return [tile for tile in listDir if tile not in workTiles]
    except Exception as e:
        print(str(e))


def loadTileSet(pathToMap = "test", pathToTiles=""): # загрузка набора тайлов
    pathToMap = f"{pathToMap}"
    res = []

    listDir = os.listdir(pathToMap)
    listDirTiles = os.listdir(pathToTiles)
    existFlag = False
    for i in range(len(listDir)):
        if listDir[i] == "tilesId.pickle":
            existFlag = True
            break
    if existFlag:
        tilesId = loadPick(f"{pathToMap}")
        print(tilesId)
        workTiles = getWorkTiles(tilesId, pathToTiles)
        items = tilesId.items()
        res = createEmptyTileSet(items)
        #print(tilesId)
        for i in tilesId:
            print(tilesId)
            if i != "":

                try:

                    res[tilesId[i]] = loadTile(i.split("/")[-1], pathToTiles)
                except Exception as e: print(e)
        print("list", workTiles)
        forAdd = getNotWorkTiles(workTiles, listDirTiles)
        print("forAdd", forAdd)
        numAdd = len(forAdd)
        #print("forAdd", forAdd)
        for i in range(1, len(res)):
            if len(forAdd) == 0:
                break
            if res[i].empty:
                print(forAdd[0])
                res[i] = loadTile(forAdd[0], pathToTiles)
                numAdd -=1
                forAdd.pop(0)

        for i in range(len(forAdd)):
            res.append(loadTile(forAdd[i], pathToTiles))
    else:
        res.append(Tile())
        for i in listDirTiles:
            res.append(loadTile(i, pathToTiles))
    forSave = dict()
    for i in range(len(res)):
        forSave[res[i].name] = i

    savePick(pathToMap, forSave)
    return res