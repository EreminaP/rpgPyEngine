import pyglet

void = pyglet.image.load('res/texture/void.png')

resolution = [900, 900]

def pixToTail(pos): # координаты по пикселям переводятся в коардинаты тайловые
    return [int((pos[0] + 50) / 100),int((pos[1] + 50) / 100)]

def mapParam(pathToConf): # загрузка параметров карты
    config = dict()
    config["sizeX"] = 100
    config["sizeY"] = 100
    config["spawnX"] = 0
    config["spawnY"] = 0
    config["colorBgR"] = 0
    config["colorBgG"] =0
    config["colorBgB"] =0
    file = open(f"{pathToConf}/params.txt", "r")
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

    except:
        pass
        print("bruh")
    return config

def tileParam(pathToConf): # загрузка параметров тайла
    config = dict()
    config["solid"] = False
    config["friction"] = 1.05
    config["rotation"] = 0
    config["name"] = pathToConf.split("/")[-1]
    config["damage"] = 0
    file = open(f"{pathToConf}/params.txt", "r")
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

    except:pass

    return config

def limitCam(vec, size): # ограничение вектора по размеру карты
    if vec[0]<0:
        vec[0] = 0
    if vec[1]<0:
        vec[1] = 0
    if vec[0]>size[0]-1:
        vec[0] = size[0]-1
    if vec[1]>size[1]-1:
        vec[1] = size[1]-1
    return vec