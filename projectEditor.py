# инициализация модулей
import pyglet.sprite
from RpgPyEngine import *
from PIL import ImageEnhance
import subprocess
import sys
from tkinter import filedialog as fd
from package.codeEditor import *
import os
import shutil
import tkinter as tk
from tkinter import simpledialog, messagebox



# установка интерполяции на метод ближайшего соседа
pyglet.image.Texture.default_min_filter = GL_NEAREST
pyglet.image.Texture.default_mag_filter = GL_NEAREST


# объявление переменных, заранее могут быть None или другому значению не имеющему смысла, это нужно чтобы просто объявить их здесь, они используются в коде позже
page = "editor"
pathForTextureTile = "" # путь к текстуре тайла, используется при создании тайла
tick = 0

trView = None # обьект для отображения триггера
canPaint2 = False # можно ли рисовать ? зависимость от того мешает ли интерфейс
loadMap = None # загружаемая карта - путь
map = None # объекат карты
tileSet = None # набор тайлов

scroll = 0 # прогресс пролситывания списка уровней
batchGui = pyglet.graphics.Batch() # пакет рендеринга для gui
spTop = None # спрайт чёлка, находится сверху
spBottom = None # спрайт, находится снизу

menu = False # открыто ли меню тайлов ?

select = [0, 0] # ппозиция для выбора тайла в меню

selectLayer = 0 # выбраный слой
selectTile = 0 # выбранный тайл int

mouseTiles = [] # тайлы по позиции мыши

mapPencil = MapPencil() # карандаш для рисования


fade = Fade(255) # затенение
fade.set(0, 100)
tick = 0


mouseX = 0
mouseY = 0
mousePress = False

canPaint = True

batch = pyglet.graphics.Batch()
pResolution = [0, 0]

tick = 0

pos1 = [100, 100]
keys = {"w": False, "a": False, "s": False, "d": False} # нажаты ли клавиши
window = 0 # окно
cam = 0 # камера
tilesMenu = 0
layerMenu = 0
setPage = 0
fps_display = 0

butGroups = dict()
butGroups["bottom"] = []
openMapName = None
pathToProj = None
mouseTilePos = [0,0]
colorBg = None
openWin= {"projManager": False, "addMap": False, "build": False, "help": False, "addTile": False, "codeEditor": False} # открыты ли окна
def unGroup(name): # отвязать группу кнопок
    for i in range(len(butGroups[name])):
        butGroups[name][i].unbind()
maps = None
def startEd(window, setPag, pathToPro): # перезапись окна под редактор проекта
    global cam, tilesMenu, layerMenu, setPage, fps_display, spTop, spBottom, butGroups, loadMap, map, tileSet, openMapName, pathToProj, maps, colorBg, g, trView, scroll

    class RectTriggerView: # класс для отображения триггера
        def __init__(self):
            self.size = [100,100]
            self.pos = [0, 0]
            self.hide = False

        def draw(self):

            if not self.hide:
                pyglet.shapes.BorderedRectangle(self.pos[0], self.pos[1], self.size[0], self.size[1],
                                                color=(255, 210, 66, 100), border_color=(255, 210, 66, 100)).draw()

        def setGeometry(self, triggerPosSize): # установка размера триггера
            self.pos[0]=int(triggerPosSize[0])
            self.pos[1] = int(triggerPosSize[1])
            self.size[0] = int(triggerPosSize[2])
            self.size[1] = int(triggerPosSize[3])
            self.hide = int(triggerPosSize[4])

    colorBg = [21,52,21]
    pathToProj = pathToPro
    loadMap =     f"{pathToProj}/maps/"
    pathToTiles = f"{pathToProj}/res/tiles/"
    openMapName = ""
    for i in os.listdir(loadMap):
        try:
            print(i)
            openMapName = i
            map = Map(loadMap+i, pathToTiles)
            break
        except Exception as er:
            print(er)
        if i == len(os.listdir(loadMap))-1:
            pass

    if openMapName != "":


        maps = os.listdir(loadMap)

        tileSet = map.simpleTiles
    else:
        maps = []
        map = Map(loadMap, pathToTiles, empty=True)
    spTop = pyglet.sprite.Sprite(pyglet.image.load("res/gui/top.png"), x=0, y=0, batch=batchGui)
    spBottom = pyglet.sprite.Sprite(pyglet.image.load("res/gui/bottom.png"), x=0, y=0, batch=batchGui)
    setPage = setPag
    projName = pathToProj.split("/")[-1]
    fps_display = pyglet.window.FPSDisplay(window=window, color=(70, 255, 70, 255), samples=10)

    class simpleButton(pyglet.gui.PushButton): # класс простая кнопка, используется для всех кнопок pyglet

        def __init__(self, x, y, pathToTexture):
            ImageEnhance.Brightness(Image.open(pathToTexture).convert("RGBA")).enhance(0.5).save("cache/imgSB.png")
            self.batch = pyglet.graphics.Batch()
            super().__init__(x, y, depressed=pyglet.image.load(pathToTexture),pressed=pyglet.image.load("cache/imgSB.png"), batch=self.batch)
            window.push_handlers(self)
            self.func = None

        def draw(self):
            self.batch.draw()

        def bind(self, func, group):
            butGroups[group].append(self)
            self.func = func
            self.set_handler('on_press', func)
        def unbind(self):
            if self.func != None:
                self.remove_handler('on_press', self.func)

    display = pyglet.canvas.Display()
    screen = display.get_default_screen()
    screen_width = screen.width
    screen_height = screen.height
    window.set_location(0,30)
    window.set_size(screen_width, screen_height-65)
    cam = Camera([0, 0], 1, resolution, window) # Создаётся камера
    if openMapName != "":
        tilesMenu = TilesMenu(cam, tileSet, f"{loadMap}{openMapName}", window, pathToTiles)

        layerMenu = LayerMenu(cam, tileSet)

    def sizeUpdate():
        if openMapName != "":
            tilesMenu.sizeUpdate()


    @window.event
    def on_key_release(symbol, modifiers):
        if symbol == key.W:
            keys["w"] = False
        if symbol == key.A:
            keys["a"] = False
        if symbol == key.S:
            keys["s"] = False
        if symbol == key.D:
            keys["d"] = False

    def openProjPy(projName): # открытие проекта как игры

        proj = os.path.abspath(f"projects/{projName}")

        wd = os.getcwd()
        os.chdir(proj)

        subprocess.Popen([sys.executable, proj+"\\"+'main.py'])

        os.chdir(wd)

    def projManager(): # при нажатии на *Проекты*
        global page, setPage

        def no():
            root.destroy()

        def yes():
            global page, setPage
            unGroup("bottom")
            setPage[0]("main")
            setPage[1]()
            pyglet.clock.unschedule(update)
            page = "main"
            root.destroy()

        if not openWin["projManager"]:
            root = tk.Tk()
            root.resizable(height=False, width=False)
            root.iconbitmap("res/icon.ico")
            root.title("Предупреждение")
            root.config(bg="#444444")
            tk.Label(text="Вы точно хотите выйти ?", bg="#444444", fg = "#eeeeee").grid(row=0, column=0, columnspan = 2)
            tk.Label(text="Все несохраненные данные будут утеряны !", bg="#444444", fg = "#eeeeee").grid(row=1, column=0, columnspan = 2)
            tk.Button(text="Нет", bg="#444444", fg = "#eeeeee", command=no).grid(row=2, column=0)
            tk.Button(text="Да", bg="#444444", fg = "#eeeeee", command=yes).grid(row=2, column=1)
            openWin["projManager"] = True
            root.mainloop()
            openWin["projManager"] = False
        
        

    @window.event
    def on_key_press(symbol, modifiers):
        global menu, dia, map, selectLayer, playerController, mouseX, mouseY, setPage, page

        if symbol == key.P:
            projManager()
        if symbol == key.W:
            keys["w"] = True
        if symbol == key.A:
            keys["a"] = True
        if symbol == key.S:
            keys["s"] = True
        if symbol == key.D:
            keys["d"] = True

        if symbol == key.UP:
            selectLayer+=1
            soundSelectLayer.play()
        if symbol == key.DOWN:
            selectLayer -= 1
            soundSelectLayer.play()
        if symbol == key.R:
            dia.textProcess = 0

        if symbol == key.TAB and menu == False:
            menu = True

        elif symbol == key.TAB and menu == True:
            menu = False

        # Зум перемещение происходит из за того что при изменении масштаба, он меняется относительно угла камеры а не центра
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

        if menu:
            tilesMenu.keyboard(symbol)
        else:
            if symbol == key.DELETE:
                var1 = pixToTail([mouseX * cam.zoom + cam.pos[0] - 50, mouseY * cam.zoom + cam.pos[1] - 50])
                map.matrix[var1[0]][var1[1]] = map.matrix[var1[0]][var1[1]][:len(map.matrix[var1[0]][var1[1]])-1]
                del map.spriteTiles[var1[0], var1[1]]

        if symbol == key.Z:
            mapPencil.undo(map)

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        global mouseTiles, mouseX, mouseY, canPaint, canPaint2, mouseTilePos
        var1 = pixToTail([x * cam.zoom + cam.pos[0] - 50, y * cam.zoom + cam.pos[1] - 50])
        mouseTilePos = var1.copy()
        try: mouseTiles = map.matrix[var1[0]][var1[1]]
        except: pass
        mouseX = x
        mouseY = y
        if x>200 and x <resolution[0]-200 and y>61 and y<resolution[1]-25:
            canPaint2 = True
        else:
            canPaint2 = False

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        global mousePress
        mousePress = False

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y1):
        global scroll
        scroll_y = -scroll_y1
        scroll += scroll_y * 20
        if scroll < 0:
            scroll = 0

        if scroll_y > 0 and resolution[1]-100-33*len(maps)+scroll  > 100:
            scroll -= scroll_y * 20



    @window.event
    def on_mouse_press(x, y, button, modifiers):
        global map, cam, select, goSelect, selectTile, tilesMenu, mouseX, mouseY, mousePress, canPaint, maps, layerMenu, openMapName

        for i in range(len(maps)):
            boxPos = [6, resolution[1]-100-33*i+scroll]
            boxSize = [188, 27]
            if y>boxPos[1] and y<boxPos[1]+ boxSize[1] and x<boxSize[0]+boxPos[0]:
                try:

                    map = Map(loadMap + maps[i], pathToTiles)

                    maps = os.listdir(loadMap)

                    tileSet = map.simpleTiles
                    tilesMenu.tileSet = tileSet
                    layerMenu.tileSet = tileSet
                    openMapName = maps[i]
                except:
                    pass

        mousePress = True

        try:
            if not menu:
                if canPaint and canPaint2:
                    mapPencil.startPaint()
                    mapPencil.paint(x, y, map, cam.zoom, cam.pos, selectLayer)
        except: pass
        if menu:
            v = tilesMenu.control(x, y)
            if v != -1:
                mapPencil.selectTile = v


    def newMap(): # Создание новой карты
        global maps, openMapName

        def createMap():
            global maps, openMapName, map, tilesMenu, layerMenu

            maps.append(str(nameEnt.get()))
            map.create2(str(nameEnt.get()), int(sizeXEnt.get()), int(sizeYEnt.get()), loadMap)
            if openMapName == "":
                openMapName = str(nameEnt.get())
                map = Map(loadMap+openMapName, pathToTiles)
                tileSet = map.simpleTiles
                tilesMenu = TilesMenu(cam, tileSet, f"projects/name2/maps/{openMapName}", window, pathToTiles)
                layerMenu = LayerMenu(cam, tileSet)

                tilesMenu.tileSet = tileSet
                layerMenu.tileSet = tileSet
            root.destroy()

        if not openWin["addMap"]:
            root = tk.Tk()
            root.iconbitmap("res/icon.ico")
            root.title("Создание новой карты")
            root.config(bg="#444444")
            root.resizable(height = False, width = False)
            tk.Label(text="Название", bg="#444444", fg = "#eeeeee").grid(row=0, column=0)
            nameEnt = tk.Entry(bg="#444444")
            nameEnt.grid(row=1, column=0)
            tk.Label(text = "Размер по X", bg="#444444", fg = "#eeeeee").grid(row=2, column=0)
            tk.Label(text="Размер по Y", bg="#444444", fg = "#eeeeee").grid(row=2, column=1)
            sizeXEnt = tk.Entry(bg="#444444")
            sizeXEnt.grid(row=3, column=0)
            sizeYEnt = tk.Entry(bg="#444444")
            sizeYEnt.grid(row=3, column=1)
            doneBut = tk.Button(text="Создать", bg="#444444", fg = "#eeeeee", command=createMap)
            doneBut.grid(row=4, column=0)
            openWin["addMap"] = True
            root.mainloop()
            openWin["addMap"] = False

    @window.event
    def on_mouse_drag(x, y, dx, dy, button, modifiers):
        global zoom, map, cam, selectTile, menu, selectLayer
    
        if not menu:

            if canPaint and canPaint2:
                mapPencil.paint(x, y, map, cam.zoom, cam.pos, selectLayer)
                #soundSet.play()

    def createBuild(): # открытие менеджера сборок
        import tkinter as tk
        from tkinter import ttk, messagebox
        import os
        import shutil
        from datetime import datetime

        # Функция для обновления таблицы с содержимым директории
        def update_table():
            for i in tree.get_children():
                tree.delete(i)
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                is_dir = os.path.isdir(item_path)
                if is_dir:
                    creation_time = os.path.getctime(item_path)
                    m_time = os.path.getmtime(item_path)
                    creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
                    creation_time_str = datetime.fromtimestamp(creation_time).strftime('%H:%M:%S')
                    tree.insert("", "end", values=(item, creation_date, creation_time_str))

        # Функция для добавления новой папки
        def add_folder():
            new_folder_name = folder_name_entry.get()
            if new_folder_name:
                new_folder_path = os.path.join(folder_path, new_folder_name)
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                    update_table()

                    pyInstallerPath = os.path.abspath("venv/Scripts/pyinstaller")
                    iconPath = os.path.abspath(f"{pathToProj}/res/icon.ico")
                    codePath = os.path.abspath(f"{pathToProj}/main.py")

                    buildFolder = os.path.abspath(f"builds/{new_folder_name}")

                    shutil.copytree(f"{pathToProj}/res", f"{buildFolder}/res")
                    shutil.copytree(f"{pathToProj}/maps", f"{buildFolder}/maps")
                    shutil.copyfile(f"{pathToProj}/params.txt", f"{buildFolder}/params.txt")
                    #subprocess.run([pyInstallerPath, "-w", "-F","--distpath", f"{buildFolder}",
                    #                f"--icon={iconPath}", codePath])
                    import PyInstaller.__main__
                    PyInstaller.__main__.run([
                        codePath,
                        '--onefile',
                        '--windowed',"-w", "-F","--distpath", f"{buildFolder}",
                                    f"--icon={iconPath}"
                    ])

                else:
                    messagebox.showerror("Ошибка", "Такая сборка уже существует")
            else:
                messagebox.showerror("Ошибка", "Имя сборки не может быть пустым")

        # Функция для удаления выбранной папки
        def delete_folder():
            selected_item = tree.selection()
            if selected_item:
                folder_name = tree.item(selected_item, 'values')[0]
                folder_path_to_delete = os.path.join(folder_path, folder_name)
                if os.path.isdir(folder_path_to_delete):
                    shutil.rmtree(folder_path_to_delete)
                    update_table()

            else:
                messagebox.showerror("Ошибка", "Выберите сборку для удаления")
        if not openWin["build"]:
            # Настройка главного окна
            root = tk.Tk()
            root.resizable(height=False, width=False)
            root.config(bg="#444444")
            root.title("Управление сборками")
            root.iconbitmap("res/icon.ico")
            root.geometry("600x400")

            # Путь к папке, содержимое которой отображается в таблице
            folder_path = "builds"  # Замените на ваш путь
            style = ttk.Style(root)
            style.theme_use("clam")  # set theam to clam
            style.configure("Treeview", background="black",
                            fieldbackground="#444444", foreground="white")
            style.configure('Treeview.Heading', background="PowderBlue")
            # Создание виджета Treeview
            tree = ttk.Treeview(root, columns=("name", "creation_date", "creation_time"), show='headings')
            tree.heading("name", text="Название")
            tree.heading("creation_date", text="Дата создания")
            tree.heading("creation_time", text="Время создания")
            tree.pack(fill=tk.BOTH, expand=True)

            # Панель управления
            control_frame = tk.Frame(root, bg="#444444")
            control_frame.pack(fill=tk.X)

            tk.Label(control_frame, bg="#444444", text="Имя сборки:",fg="#eeeeee").pack(side=tk.LEFT)
            folder_name_entry = tk.Entry(control_frame, bg="#444444",fg="#eeeeee")
            folder_name_entry.pack(side=tk.LEFT, padx=5)
            tk.Button(control_frame,fg="#eeeeee", bg="#444444", text="Добавить сборку", command=add_folder).pack(side=tk.LEFT, padx=5)
            tk.Button(control_frame,fg="#eeeeee", bg="#444444", text="Удалить сборку", command=delete_folder).pack(side=tk.LEFT, padx=5)

            # Обновление таблицы с содержимым директории при запуске программы
            update_table()
            openWin["build"] = True
            root.mainloop()
            openWin["build"] = False


    def update(dt):
        global fade, g
        setTriggerBool(True)
        pos = [0, 0]
        fade.on(dt)

        speed = 10

        if keys["d"]:
            cam.pos[0] += speed
        if keys["a"]:
            cam.pos[0] -= speed
        if keys["w"]:
            cam.pos[1] += speed
        if keys["s"]:
            cam.pos[1] -= speed

    def mapSave():
        np.save(os.path.abspath(loadMap+openMapName+"/grid.npy"), map.matrix, allow_pickle=True)
        print("Карта сохранена !!!")

    def addTile(): # окно добавления тайла
        import os
        import shutil

        def manage_file_and_folder(file_path, folder_path, text, folder_name):
            # Полный путь до новой папки
            new_folder_path = os.path.join(folder_path, folder_name)

            # Создаем новую папку
            os.makedirs(new_folder_path, exist_ok=True)

            # Копируем и переименовываем файл в новую папку
            new_file_path = os.path.join(new_folder_path, 'image.png')
            shutil.copyfile(file_path, new_file_path)

            # Создаем и записываем текст в файл params.txt в новой папке
            params_file_path = os.path.join(new_folder_path, 'params.txt')
            with open(params_file_path, 'w') as params_file:
                params_file.write(text)

        def winRein(): # окно сообщающее о перезаходе для применения изменений
            map.reLoad()
            tilesMenu.tileSet = map.simpleTiles
            root = tk.Tk()
            root.resizable(height=False, width=False)
            root.title("Предупреждение")
            root.config(bg="#444444")
            root.iconbitmap("res/icon.ico")

            tk.Label(text="После этого действия, требуется перезапуск.", bg="#444444", fg = "#eeeeee").pack()
            root.mainloop()
        pathForTextureTile = ""

        def iconSeter():
            global pathForTextureTile
            #print(name123)
            pathForTextureTile = fd.askopenfilename()
            but1["text"] = pathForTextureTile.split("/")[-1]

        def createTile():
            global pathForTextureTile
            params = ""
            params += "friction = "+ str(fricEnt.get()) +"\n"
            params += "solid = " + str(bool(var1.get()))
            manage_file_and_folder(pathForTextureTile, pathToTiles, params, str(nameEnt.get()))
            root.destroy()
            winRein()

        if not openWin["addTile"]:
            root = tk.Tk()
            root.iconbitmap("res/icon.ico")
            var1 = tk.BooleanVar()
            var1.set(0)
            root.resizable(height=False, width=False)
            root.title("Создание тайла")
            root.config(bg="#444444")
            but1 = tk.Button(text="Выбрать текстуру", fg = "#eeeeee", command=iconSeter,bg="#444444")
            but1.grid(row=0, column=0)
            tk.Label(text="Название", bg="#444444", fg = "#eeeeee").grid(row=1, column=0)
            nameEnt = tk.Entry(bg="#444444")
            nameEnt.grid(row=2, column=0)
            tk.Label(text="Трение", bg="#444444", fg = "#eeeeee").grid(row=1, column=2)
            fricEnt = tk.Entry(bg="#444444")
            fricEnt.grid(row=2, column=2)
            tk.Label(text="Твёрдый", bg="#444444", fg = "#eeeeee").grid(row=3, column=0)
            solidEnt = tk.Checkbutton(variable=var1, bg="#444444",
                     onvalue=1, offvalue=0)
            solidEnt.grid(row=4, column=0)
            tk.Button(text="Создать тайл", fg = "#eeeeee", command=createTile, bg="#444444").grid(row=4, column=1)

            openWin["addTile"] = True
            root.mainloop()
            openWin["addTile"] = False
    saveBut = simpleButton(0, 0, "res/gui/save.png")
    saveBut.bind(mapSave, "bottom")

    playBut = simpleButton(0, 0, "res/gui/play.png")
    playBut.bind(lambda: openProjPy(projName), "bottom")

    projManagerBut = simpleButton(0, 0, "res/gui/proj.png")
    projManagerBut.bind(projManager, "bottom")

    plusBut = simpleButton(0, 0, "res/gui/plus.png")
    plusBut.bind(newMap, "bottom")
    def helpP(): # справка

        root = tk.Tk()
        root.title("Справка")
        root.config(bg="#444444")
        tk.Label(text="Заготовка\nдля\nсправки", bg="#444444").pack()
        root.mainloop()

    def propLevel(): # окно свойства уровня
        global maps
        level_path = f"{pathToProj}/maps/{openMapName}"
        def rename_level():
            level_path = f"{pathToProj}/maps/{openMapName}"
            new_name = simpledialog.askstring("Переименовать уровень", "Введите новое имя уровня:")
            if new_name:
                new_path = os.path.join(os.path.dirname(level_path), new_name)
                if not os.path.exists(new_path):
                    os.rename(level_path, new_path)
                    print(level_path, new_path)
                    level_path = new_path
                    level_name.set(f"Уровень: {new_name}")
                    messagebox.showinfo("Успех", "Уровень переименован успешно!")
                else:
                    messagebox.showerror("Ошибка", "Папка с таким именем уже существует!")

        def delete_level():
            confirm = messagebox.askyesno("Удалить уровень", "Вы уверены, что хотите удалить этот уровень?")
            if confirm:
                shutil.rmtree(level_path)
                messagebox.showinfo("Успех", "Уровень удалён успешно!")
                root.destroy()

        root = tk.Tk()
        root.title("Свойства уровня")
        root.iconbitmap("res/icon.ico")
        root.config(bg="#444444")
        level_name = tk.StringVar(value=f"Уровень: {os.path.basename(level_path)}")

        label = tk.Label(root, textvariable=level_name, bg="#444444", fg= "#eeeeee")
        label.pack(pady=10)

        rename_button = tk.Button(root, text="Переименовать уровень", command=rename_level, bg="#444444", fg= "#eeeeee")
        rename_button.pack(pady=5)

        delete_button = tk.Button(root, text="Удалить уровень", command=delete_level, bg="#444444", fg= "#eeeeee")
        delete_button.pack(pady=5)

        root.mainloop()
        maps = os.listdir(loadMap)

    def propProj(): # окно свойства проекта
        import tkinter as tk
        from tkinter import ttk
        def delProj():
            result = messagebox.askyesno("Подтверждение удаления", "Вы уверены, что хотите удалить проект?")
            if result:
                folder_path = pathToProj  # Укажите путь к папке, которую хотите удалить
                if os.path.exists(folder_path):
                    try:
                        shutil.rmtree(folder_path)
                        messagebox.showinfo("Успех", "Папка успешно удалена!")
                    except Exception as e:
                        messagebox.showerror("Ошибка", f"Не удалось удалить папку: {e}")
                else:
                    messagebox.showwarning("Предупреждение", "Папка не существует!")

            @window.event
            def on_draw():
                pass
            global page, setPage
            unGroup("bottom")
            setPage[0]("main")
            setPage[1]()
            pyglet.clock.unschedule(update)
            page = "main"
            root.destroy()

        def save_settings():
            global settingsProject
            selected_resolution = resolutions_combobox.get()
            fps_selection = fps_var.get()
            if fps_selection == 'VSync':
                fps = 'True'
            else:
                fps = fps_entry.get()
                if fps.isdigit():
                    fps = int(fps)
                else:
                    fps = 'Неправильный ввод fps, пожалуста вводите только числа'
            win_number = resolutions.index(selected_resolution)
            settingsProject = f"win = {win_number}\nfps = {fps}"
            result_label.config(text=f"Настройки сохранены: win={win_number - 1}, fps={fps}")
            with open(f"{pathToPro}/params.txt", "w") as file:
                file.write(settingsProject)

        root = tk.Tk()
        root.config(bg="#444444")
        root.title("Настройка Параметров")
        root.iconbitmap("res/icon.ico")
        root.geometry("300x250")
        # Переключатели для выбора VSync
        fps_var = tk.StringVar()
        fps_radiobutton1 = tk.Radiobutton(root, text="VSync", variable=fps_var, value="VSync", bg="#444444", activebackground="#343434")
        fps_radiobutton1.pack(anchor="w")
        # Поле ввода для точного задания FPS
        fps_radiobutton2 = tk.Radiobutton(root, text="Значение FPS:", variable=fps_var, value="Custom FPS", bg="#444444",  activebackground="#343434")
        fps_radiobutton2.pack(anchor="w")
        fps_entry = tk.Entry(root, bg="#444444", fg= "#eeeeee")
        fps_entry.pack(anchor="w")
        # Комбобокс для выбора разрешения экрана
        resolutions = ["800x600", "1024x768", "1280x720"]
        resolutions_combobox = ttk.Combobox(root, values=resolutions, background= "#343434", foreground="#343434")
        resolutions_combobox.set("Выберите разрешение")
        resolutions_combobox.pack(pady=10)
        # Кнопка для сохранения настроек
        save_button = tk.Button(root, text="Сохранить", command=save_settings, bg="#444444", fg= "#eeeeee")
        save_button.pack(pady=10)
        tk.Button(root, text="Удалить проект", command=delProj, bg="#444444", fg= "#eeeeee").pack(pady=10)
        # Метка для отображения результатов
        result_label = tk.Label(root, text="", bg="#444444", fg= "#eeeeee")
        result_label.pack()
        root.mainloop()

    helpBut = simpleButton(0, 0, "res/gui/help.png")
    helpBut.bind(helpP, "bottom")

    buildBut = simpleButton(0, 0, "res/gui/buildButton.png")
    buildBut.bind(createBuild, "bottom")

    tileBut = simpleButton(0, 0, "res/gui/tileBut.png")
    tileBut.bind(addTile, "bottom")

    propertyLevelBut = simpleButton(0, 0, "res/gui/propertyLevelBut.png")
    propertyLevelBut.bind(propLevel, "bottom")

    propertyProjBut = simpleButton(0, 0, "res/gui/propertyProjBut.png")
    propertyProjBut.bind(propProj, "bottom")

    def projParam(pathToConf): # Применение параметров проекта по файлу
        config = dict()
        config["win"] = 0
        config["fps"] = True

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

            return config
        except:
            pass

    codeBut = simpleButton(0, 0, "res/gui/codeBut.png")

    def varFunc(pathToProj, win): # открытие окна редактора кода
        if not openWin["codeEditor"]:
            openWin["codeEditor"] = True
            winCodeEditor(pathToProj, win)
            openWin["codeEditor"] = False
            g[4] = True
    codeBut.bind(lambda: varFunc(pathToProj, window), "bottom")

    trView = RectTriggerView()

    mapInfo = pyglet.text.Label("", # текст информации о карте
                              font_name='Arial',
                              font_size=14,
                              color=(230, 221, 255, 255),
                              x=resolution[0]/2, y=resolution[1] - 18, anchor_x = 'center')

    mapProperty = pyglet.text.Label(
        f"",
        font_name='Arial',
        font_size=14,
        color=(230, 221, 255, 255),
        x=resolution[0] - 190, y=resolution[1] - 160, multiline=True, width=500)
    labelAll = pyglet.text.Label("...",
                                      font_name='Arial',
                                      font_size=15,
                                      color=(230, 221, 255, 255),
                                      x=6 + 3, y=resolution[1] - 100 - 33 * 1 + 4, align="center")
    @window.event
    def on_draw():

        global zoom, spTop,trView, map,g, cam, menu, select, goSelect, selectTile, tick, selectLayer, mouseTiles, mouseX, mouseY, canPaint, canCat, hpDr, pResolution, liveEntityList, sleepForPage

        try:
            if getTriggerPosSize() != None:
                trView.setGeometry(getTriggerPosSize())
        except:pass

        tick+=1

        window.clear()
        pyglet.gl.glClearColor(map.colorBg[0]/255, map.colorBg[1]/255, map.colorBg[2]/255, 1)
        cam.begin()

        v = int(70+cos(tick/30)*33)
        try:
            if openMapName != "":
                pyglet.shapes.Rectangle(0,0, 100 *(map.size[0]-1), 100 *(map.size[1]-1), color=(v,v,v,255)).draw()
        except: pass

        if openMapName != "":
            map.draw(cam.pos, cam.zoom)
        trView.draw()

        pResolution = cam.resolution.copy()
        resolution[0] = window.width
        resolution[1] = window.height
        if cam.resolution[0] != pResolution[0] or cam.resolution[1] != pResolution[1]:
            sizeUpdate()

        cam.end()

        spTop.position = (0, resolution[1]- spTop.height, 0)

        batchGui.draw()
        pyglet.shapes.Rectangle(0,61,200,resolution[1]-(61+25), color=(55-30,53-30,61-30,255)).draw()
        pyglet.shapes.Rectangle(resolution[0]-200, 61, 200, resolution[1] - (61 + 25), color=(55 - 30, 53 - 30, 61 - 30, 255)).draw()

        saveBut.x = resolution[0]/2-32-64
        saveBut.draw()

        playBut.x = resolution[0]/2-32
        playBut.draw()

        projManagerBut.y = resolution[1] - projManagerBut.height-2
        projManagerBut.draw()
        plusBut.x = 150

        try:
            plusBut.y = resolution[1] - 100 - 33 * len(maps) + 4-20
        except:
            plusBut.y = resolution[1] - 100 - 33 * 0 + 4 - 20
        plusBut.draw()

        buildBut.x = 93
        buildBut.y =  resolution[1] - projManagerBut.height-2
        buildBut.draw()

        helpBut.x = 173
        helpBut.y =  resolution[1] - projManagerBut.height-2
        helpBut.draw()

        tileBut.y = resolution[1]-100
        tileBut.x = resolution[0]-tileBut.width-6
        tileBut.draw()

        codeBut.y = resolution[1] - 140
        codeBut.x = resolution[0] - tileBut.width - 6
        codeBut.draw()

        propertyLevelBut.y = resolution[1] - 180
        propertyLevelBut.x = resolution[0] - tileBut.width - 6
        propertyLevelBut.draw()

        propertyProjBut.y = resolution[1] - 220
        propertyProjBut.x = resolution[0] - tileBut.width - 6
        propertyProjBut.draw()

        if openMapName != "":
            for i in range(len(maps)):

                varNum = (resolution[1] - 100 - 33 * 1 + 4) - (resolution[1] - 100 - 33 * i + 4 + scroll - 80)
                varNum2 = (resolution[1] - 100 - 33 * i + 4 + scroll - 120) - (resolution[1] - 100 - 33 * 29 + 4)
                varNum *= 5
                if varNum < 0:
                    varNum = 0
                if varNum > 255:
                    varNum = 255

                varNum2 *= 5
                if varNum2 < 0:
                    varNum2 = 0
                if varNum2 > 255:
                    varNum2 = 255

                vart = pyglet.shapes.Rectangle(6, resolution[1]-100-33*i+scroll, 188, 27, color=(71, 68, 79, 255))
                vart.opacity = int(min(varNum, varNum2))
                vart.draw()
                varText = maps[i]

                labelAll.opacity = min(varNum, varNum2)
                if len(varText)>9:
                    labelAll.y = resolution[1] - 100 - 33 * i + 4+scroll
                    labelAll.text = varText[:9]+"..."

                    labelAll.draw()
                else:
                    labelAll.y = resolution[1] - 100 - 33 * i + 4+scroll
                    labelAll.text = varText
                    labelAll.draw()

        try:
            mapInfo.x = resolution[0] / 2
            mapInfo.y = resolution[1] - 18
            mapInfo.text = f"Название уровня: {openMapName} | Размер уровня: {map.size[0], map.size[1]} | Фон: {map.colorBg}"
            mapInfo.draw()
        except: pass

        projPar = projParam(pathToPro)

        textVar = "fpsMax: "
        if projPar["fps"] == True:
            textVar +="vsync"

        elif projPar["fps"] == False:
            textVar += "unlimit"

        else:
            textVar += str(projPar['fps'])

        resolutions = [[800, 600], [1024, 768], [1280, 1024]]

        var = resolutions[projPar["win"]]
        textVar += f"\nОкно: {var}"
        mapProperty.text = textVar
        mapProperty.x = resolution[0] - 190
        mapProperty.y = resolution[1] - 250
        mapProperty.draw()

        fps_display.draw()

        batch.draw()

        try:
            if openMapName != "":
                if canPaint:
                    if menu:
                        tilesMenu.draw()

                    else:
                        layerMenu.draw(mouseTiles, selectLayer, mouseTilePos)
        except: pass

    pyglet.clock.schedule_interval(update, 1 / 60)

