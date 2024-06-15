# инициализация модулей
from package.gui import * # кнопка с текстом
from datetime import datetime # для даты и времени
from projectEditor import * # редактор проектов
import tkinter as tk
from tkinter import ttk, Tk, Entry, Button




def openEditor(setPage, selectProj): # открытие редактора проекта
    startEd(window, setPage, f"projects/{selectProj}")

def openSelectProj(): # открытие редактора согласно выбраному проекту
    global page, setPage, overwriteWinMain, selectProj
    if selectProj != None:
        page = "something"

        settings.remove_handler('on_press', restart)
        openBut.remove_handler('on_press', openSelectProj)
        createBut1.remove_handler('on_press', createProject)

        openEditor([setPage, overwriteWinMain], projList[selectProj][2].text)





def copyFiles(source_folder, destination_folder):# копирование всех файлов из одной папки в другую папку
    # Получаем список файлов в исходной папке
    files = os.listdir(source_folder)
    for file in files:
        source_file = os.path.join(source_folder, file)
        if os.path.isfile(source_file):
            destination_file = os.path.join(destination_folder, file)
            shutil.copy2(source_file, destination_file)


def restart():
    print("Заглушка, потом настройки проекта") # Заглушка, потом настройки проекта



def pref(): # окно параметров проекта


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


        result_label.config(text=f"Настройки сохранены: win={win_number-1}, fps={fps}")

    root = tk.Tk()
    root.config(bg="#444444")
    root.title("Настройка Параметров")
    root.geometry("300x250")
    # Переключатели для выбора VSync
    fps_var = tk.StringVar()

    fps_radiobutton1 = tk.Radiobutton(root, text="VSync", variable=fps_var, value="VSync", bg="#444444",
                                      activebackground="#343434")
    fps_radiobutton1.pack(anchor="w")
    # Поле ввода для точного задания FPS
    fps_radiobutton2 = tk.Radiobutton(root, text="Значение FPS:", variable=fps_var, value="Custom FPS", bg="#444444",
                                      activebackground="#343434")
    fps_radiobutton2.pack(anchor="w")
    fps_entry = tk.Entry(root, bg="#444444", fg="#eeeeee")
    fps_entry.pack(anchor="w")
    # Комбобокс для выбора разрешения экрана
    resolutions = ["800x600", "1024x768", "1280x720"]
    resolutions_combobox = ttk.Combobox(root, values=resolutions, background="#343434", foreground="#343434")
    resolutions_combobox.set("Выберите разрешение")
    resolutions_combobox.pack(pady=10)
    # Кнопка для сохранения настроек
    save_button = tk.Button(root, text="Сохранить", command=save_settings, bg="#444444", fg="#eeeeee")
    save_button.pack(pady=10)

    # Метка для отображения результатов
    result_label = tk.Label(root, text="", bg="#444444", fg="#eeeeee")
    result_label.pack()

    root.mainloop()


def createProject(): # переключение на страницу создания проекта
    global page, createBut1, openBut, settings



    settings.remove_handler('on_press', restart)
    openBut.remove_handler('on_press', openSelectProj)
    createBut1.remove_handler('on_press', createProject)
    page = "createPrj"

    nameSet.set_handler('on_press', openWinName)
    createBut2.set_handler('on_press', createProjectFiles)
    propertyBut.set_handler('on_press', pref)
    backBut.set_handler('on_press', back)
    frameIcon.set_handler('on_press', setIcon)


def createProjectFiles(): # создание файлов проекта
    global entText
    name = entText
    os.mkdir(f"projects/{name}")
    Image.open("cache/icon.png").save(f"projects/{name}/icon.png")
    updateProj()
    os.mkdir(f"projects/{name}/RpgPyEngine")
    os.mkdir(f"projects/{name}/res")
    os.mkdir(f"projects/{name}/res/tiles")
    os.mkdir(f"projects/{name}/maps")
    os.mkdir(f"projects/{name}/res/texture")

    shutil.copy2("res/texture/void.png", f"projects/{name}/res/texture/void.png")
    copyFiles("RpgPyEngine", f"projects/{name}/RpgPyEngine")
    with open(f"projects/{name}/params.txt", "w") as file:
        file.write(settingsProject)
    with open(f"projects/{name}/main.py", "w") as file:
        file.write("""
from RpgPyEngine import *
        
window = Window(paramLoad=True)
        
def update(dt):
    pass

window.start(update)
""")
    Image.open("cache/icon.png").save(f"projects/{name}/res/icon.ico")
    back()



def setIcon(): # установка икноки проекту
    global iconSpr

    name= fd.askopenfilename()
    print(name)
    Image.open(name).resize((666,500)).save(f"cache/icon.png")

    iconTex = pyglet.image.load(f"cache/icon.png")
    iconSpr = pyglet.sprite.Sprite(iconTex, 0, 25)
    iconSpr.scale_x = 0.3
    iconSpr.scale_y = 0.3
def back(): # возвращение из окна создания проекта в менеджер проектов
    global page, settings, createBut1, openBut
    createBut2.remove_handler('on_press', createProjectFiles)
    propertyBut.remove_handler('on_press', pref)
    backBut.remove_handler('on_press', back)
    frameIcon.remove_handler('on_press', setIcon)
    nameSet.remove_handler('on_press', openWinName)
    page = "main"
    settings = pyglet.gui.PushButton(25, 25, pressed=pyglet.image.load(f"res/ui/buttonSettingsP.png"),
                                     depressed=pyglet.image.load(f"res/ui/buttonSettings.png"), batch=batch)
    createBut1 = textButton1("Создать проект", [25, 0])
    openBut = textButton1("Открыть проект", [25, 0])

    window.push_handlers(settings)
    window.push_handlers(createBut1)
    window.push_handlers(openBut)

    settings.set_handler('on_press', restart)
    openBut.set_handler('on_press', openSelectProj)
    createBut1.set_handler('on_press', createProject)


def updateProj(): # proj содержит в себе все графические элементы для отображения списка проектов, это обновление proj
    global projs, projList
    projs = os.listdir("projects")
    projList = []
    for i in range(len(projs)):
        timeVar = str(datetime.fromtimestamp(os.stat(f"projects/{projs[i]}/icon.png").st_ctime))
        timeVar = timeVar.split(":")[0]+":"+timeVar.split(":")[1]
        projList.append([projs[i], timeVar])


    elemsY = resolution[1]-abs(resolution[1]-listProjSpr.height)/2
    for i in range(len(projList)):
        var = projList[i].copy()

        projList[i] = [pyglet.sprite.Sprite(pyglet.image.load(f"res/ui/elem.png"), resolution[0] - listProjSpr.width - 25+9, i * -70+elemsY),
                       pyglet.sprite.Sprite(pyglet.image.load(f"projects/{var[0]}/icon.png"),resolution[0] - listProjSpr.width - 25+18, i * -70 +8+elemsY),
                       pyglet.text.Label(var[0],
                                           font_name='Arial',
                                           font_size=18,
                                           color=(126,106,148,255),
                                           x=resolution[0] - listProjSpr.width-25+90, y=i*-70+5+35+elemsY),
                       pyglet.text.Label(var[1],
                                         font_name='Arial',
                                         font_size=13,
                                         color=(126,106,148, 255),
                                         x=resolution[0] - listProjSpr.width - 25+90, y=i * -70+15+elemsY)

                       ]
    for i in range(len(projList)):
        projList[i][0].scale_x = 0.7
        projList[i][0].scale_y = 0.7
        projList[i][1].scale_x = 0.1
        projList[i][1].scale_y = 0.1

window = pyglet.window.Window(800,600, "rpgPyEngine", resizable=True, vsync=True) # создание окна
iconA = pyglet.image.load('res/icon.ico')
window.set_icon(iconA)# установка иконки окну
resolution = (window.width, window.height)

page = "main"

def pyst():
    pass


createBut1 = textButton1("Создать проект", [25, 0])
window.push_handlers(createBut1)
openBut = textButton1("Открыть проект", [25,0])
window.push_handlers(openBut)

bolvanka = textButton1("", [-2000,0])
window.push_handlers(bolvanka)
bolvanka.set_handler("on_press", pyst)

window.set_minimum_size(800,600)

batch = pyglet.graphics.Batch()

settings = pyglet.gui.PushButton(25,25, pressed= pyglet.image.load(f"res/ui/buttonSettingsP.png"), depressed= pyglet.image.load(f"res/ui/buttonSettings.png"), batch=batch)
window.push_handlers(settings)

listProjTex = pyglet.image.load(f"res/ui/listProjects.png")
listProjSpr = pyglet.sprite.Sprite(listProjTex, 0, 25)
listProjSpr.scale_x = 0.7
listProjSpr.scale_y = 0.7


projs = []
projList = []
updateProj()

elemTex = pyglet.image.load(f"res/ui/elem.png")
elemSpr = pyglet.sprite.Sprite(elemTex, 0, 25)

batch2 = pyglet.graphics.Batch()




def openWinName(): # открытие окна для ввода названия проекта
    global entText
    def on_close():

        root.destroy()
    def on_set():
        nonlocal project_name
        project_name = entry.get()
        root.destroy()
    project_name = ""
    root = Tk()
    root.title("Введите название проекта")
    root.iconbitmap("res/icon.ico")
    root.config(bg = "#444444")
    root.geometry("300x100")

    entry = Entry(root, width=40)
    entry.pack(pady=10)

    button = Button(root, text="OK", bg = "#444444", fg="#eeeeee", command=on_set)
    button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

    if project_name !="": entText = project_name





nameSetTex = pyglet.image.load(f"res/gui/nameSet.png")
nameSet = pyglet.gui.PushButton(25,25, pressed=nameSetTex, depressed=nameSetTex, batch=batch2)
window.push_handlers(nameSet)

entText = "�������������"




frameIconTex = pyglet.image.load(f"res/ui/frameIcon.png")
frameIconTexP = pyglet.image.load(f"res/ui/frameIconP.png")
frameIcon = pyglet.gui.PushButton(25,25, pressed=frameIconTexP, depressed=frameIconTex, batch=batch2)

window.push_handlers(frameIcon)
def setPage(id): # функция для открытия нужной страницы, используется при переходе из редактора проектов в менеджер проектов
    global page
    page = id
    var = [pyglet.canvas.Display().get_default_screen().width, pyglet.canvas.Display().get_default_screen().height]
    window.set_size(800, 600)
    window.set_location(int(var[0] / 2 - 400), int(var[1] / 2 - 300))

backBut = textButton1("Назад", [25,0])
window.push_handlers(backBut)

propertyBut = textButton1("Свойства проекта", [25,0])
window.push_handlers(propertyBut)

createBut2 = textButton1("Создать проект", [25,0])
window.push_handlers(createBut2)


scrollProc = 0 # позиция прокручивания списка


bg = pyglet.sprite.Sprite(pyglet.image.load(f"res/gui/background.png"), 0,0)
bg2 = pyglet.sprite.Sprite(pyglet.image.load(f"res/gui/background2.png"), 0,0)

iconTex = pyglet.image.load(f"res/texture/invisible.png")
iconSpr = pyglet.sprite.Sprite(iconTex, 0, 25)
batch3 = pyglet.graphics.Batch()
gg = pyglet.gui.TextEntry("gh",10,10, 300, batch=batch3, color=(127,107,148,255), text_color=(180,153,206,255))
window.push_handlers(gg)

selectProj = None
def overwriteWinMain(): # функция для записи в окно, привязки к событиям
    global nameEnt, createBut1
    updateProj()
    selectProj = None


    settings.set_handler('on_press', restart)
    createBut1.set_handler('on_press', createProject)
    window.push_handlers(bolvanka)
    bolvanka.set_handler("on_press", pyst)
    openBut.set_handler('on_press', openSelectProj)

    window.push_handlers(bolvanka)
    bolvanka.set_handler("on_press", pyst)

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y1):
        global scrollProc
        scroll_y = -scroll_y1
        print(scroll_y)
        scrollProc+=scroll_y*20
        if scrollProc<0:
            scrollProc=0
        elemsY = resolution[1] - abs(resolution[1] - listProjSpr.height) / 2 - 65 - 10
        print(len(projList) * -70 + 5 + 35 + elemsY+scrollProc)
        if scroll_y > 0 and len(projList) * -70 + 5 + 35 + elemsY+scrollProc>20:
            scrollProc -=scroll_y*20


    @window.event
    def on_mouse_press(x, y, button, modifiers):
        global selectProj
        for i in range(len(projList)):
            if y>projList[i][0].y and y<projList[i][0].y+ projList[i][0].height and x>projList[i][0].x:
                if selectProj != None: projList[selectProj][0].color = (255,255,255)
                projList[i][0].color = (50,50,50)
                selectProj = i
                pass

    @window.event
    def on_draw(): # цикл рисования
        resolution = (window.width, window.height)


        match page:
            case "main": # страница main



                window.clear()
                bg.scale_x = resolution[0] / 1280
                bg.scale_y = resolution[1] / 800
                bg.draw()
                elemsY = resolution[1] - abs(resolution[1] - listProjSpr.height) / 2 -65-10
                for i in range(len(projList)):
                    for i2 in range(len(projList[0])):


                        projList[i][0].x = resolution[0] - listProjSpr.width - 25 + 9
                        projList[i][0].y = i * -70 + elemsY+scrollProc
                        projList[i][1].x = resolution[0] - listProjSpr.width - 25 + 18
                        projList[i][1].y = i * -70 + 8 + elemsY+scrollProc
                        projList[i][2].x = resolution[0] - listProjSpr.width - 25 + 90
                        projList[i][2].y = i * -70 + 5 + 35 + elemsY+scrollProc
                        projList[i][3].x = resolution[0] - listProjSpr.width - 25 + 90
                        projList[i][3].y = i * -70 + 15 + elemsY+scrollProc
                        varNum = (1 * -70 + 15 + elemsY)-(i * -70 + 15 + elemsY+scrollProc-120)
                        varNum2 = (i * -70 + 15 + elemsY + scrollProc - 120) - (9 * -70 + 15 + elemsY)
                        varNum*=5
                        if varNum<0:
                            varNum=0
                        if varNum>255:
                            varNum=255

                        varNum2 *= 5
                        if varNum2 < 0:
                            varNum2 = 0
                        if varNum2 > 255:
                            varNum2 = 255

                        projList[i][0].opacity = min(varNum, varNum2)
                        projList[i][1].opacity = min(varNum, varNum2)
                        projList[i][2].opacity = min(varNum, varNum2)
                        projList[i][3].opacity = min(varNum, varNum2)







                createBut1.update()
                createBut1.pos[1] = resolution[1] - resolution[1] / 4
                createBut1.draw()

                openBut.update()
                openBut.pos[1] = resolution[1] - resolution[1] / 2
                openBut.draw()
                batch.draw()
                listProjSpr.y = resolution[1]/2-listProjSpr.height/2
                listProjSpr.x = resolution[0] - listProjSpr.width-25
                listProjSpr.draw()

                for i in range(len(projList)):
                    for i2 in range(len(projList[0])):
                        projList[i][i2].draw()
            case "createPrj": # страница createPrj
                window.clear()
                bg2.scale_x = resolution[0] / 1280
                bg2.scale_y = resolution[1] / 800
                bg2.draw()

                batch2.draw()
                backBut.pos[1] = resolution[1] -resolution[1]/1.1
                backBut.update()
                backBut.draw()
                propertyBut.pos[1] = resolution[1] -resolution[1]/2
                propertyBut.update()
                propertyBut.draw()
                createBut2.pos[1] = resolution[1] -resolution[1]/1.1
                createBut2.pos[0] = resolution[0]-createBut2.width-25
                createBut2.update()
                createBut2.draw()
                frameIcon.y = resolution[1] - resolution[1]/3
                frameIcon.x = resolution[0]-frameIcon.width-25
                iconSpr.y = resolution[1] - resolution[1]/3+21
                iconSpr.x = resolution[0]-frameIcon.width-25+15
                iconSpr.draw()

                pyglet.text.Label(entText, font_name='Arial', font_size=18, color=(255, 255, 255, 255),
                          x=38, y= resolution[1] - resolution[1] / 3 + 5).draw()
                nameSet.y = resolution[1] - resolution[1] / 3 + 5
                nameSet.x = resolution[0]-400
    createProject()
    back()
overwriteWinMain()

if __name__ == "__main__":
    pyglet.app.run(interval=1 / 60) # запуск окна