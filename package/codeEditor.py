# инициализация модулей
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Listbox, Scrollbar, Text, Canvas

triggerPosSize = [2, 0, 0, 0, False] # информация о триггере, передаётся в редактор проекта, формат позиция - 2 числа, размер - 2 числа, видимый - bool
def getTriggerPosSize():
    global triggerPosSize
    return triggerPosSize
def setTriggerBool(bool):
    global triggerPosSize
    triggerPosSize[4] = bool
run = True
def winCodeEditor(PROJECT_PATH, window): # окно редактора кода
    global triggerPosSize, run

    # Ключевые слова Python для подсветки синтаксиса
    KEYWORDS = ["import ", "from ", "def ", "class ", "if ", "else", "elif ", "for ", "while ",
                "try", "except", "not ", "True", "False", "pass", "None"]

    def highlight_keywords(event=None):
        for keyword in KEYWORDS:
            editor.tag_remove(keyword, '1.0', tk.END)  # Удаление существующих тегов

        content = editor.get("1.0", tk.END)

        for keyword in KEYWORDS:
            start_pos = '1.0'
            while True:
                start_pos = editor.search(keyword, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(keyword)}c"
                editor.tag_add(keyword, start_pos, end_pos)
                editor.tag_config(keyword, foreground='orange')
                start_pos = end_pos

    def open_file(filepath):
        if filepath:
            editor.delete(1.0, tk.END)
            with open(filepath, "r", encoding="utf-8") as file:
                editor.insert(tk.END, file.read())
            root.title(f"Редактор кода - {os.path.basename(filepath)}")
            editor.filepath = filepath
        highlight_keywords()
        update_line_numbers()

    def save_file(ev=0):
        if hasattr(editor, 'filepath'):
            with open(editor.filepath, "w", encoding="utf-8") as file:
                file.write(editor.get(1.0, tk.END))
        else:
            save_file_as()

    def save_file_as():
        filepath = filedialog.asksaveasfilename(defaultextension=".py", initialdir=PROJECT_PATH, title="Сохранить пайтон",
                                                filetypes=(("Python файлы", "*.py"), ("Все файлы", "*.*")))
        if filepath:
            with open(filepath, "w") as file:
                file.write(editor.get(1.0, tk.END))
            root.title(f"Редактор кода - {os.path.basename(filepath)}")
            update_file_list()

    def update_file_list():
        file_listbox.delete(0, tk.END)
        for filename in os.listdir(PROJECT_PATH):
            if filename.endswith(".py"):
                file_listbox.insert(tk.END, filename)

    def add_file():
        filepath = filedialog.asksaveasfilename(defaultextension=".py", initialdir=PROJECT_PATH, title="Добавить файл",
                                                filetypes=(("Python файлы", "*.py"), ("Все файлы", "*.*")))
        if filepath:
            with open(filepath, "w") as file:
                file.write("")
            update_file_list()

    def delete_file():
        selected_file = file_listbox.get(tk.ACTIVE)
        filepath = os.path.join(PROJECT_PATH, selected_file)
        if messagebox.askyesno("Удаление файла", f"Вы уверены, что хотите удалить {selected_file}?"):
            os.remove(filepath)
            update_file_list()
            editor.delete(1.0, tk.END)
            root.title("Редактор кода")

    def on_file_select(event):
        selected_file = file_listbox.get(tk.ACTIVE)
        filepath = os.path.join(PROJECT_PATH, selected_file)
        open_file(filepath)
        highlight_keywords()

    def insert_spaces(event):
        # Получаем текущую позицию курсора
        cursor_position = editor.index(tk.INSERT)
        var = editor.get(f"{cursor_position}")
        # Проверяем, находится ли курсор на позиции TAB
        if editor.get(f"{cursor_position}-1c") == "\t":
            # Если да, то удаляем TAB
            editor.delete(f"{cursor_position}-1c", cursor_position)

        # Вставляем четыре пробела в текущую позицию курсора
        if var == "\n":
            editor.insert(f"{cursor_position}", " " * 4)
        else:
            editor.insert(f"{cursor_position}-1c", " " * 4)

        # Предотвращаем вставку табуляции по умолчанию
        return "break"

    def remove_spaces(event):
        # Получаем текущую позицию курсора
        cursor_position = editor.index(tk.INSERT)

        # Проверяем, находятся ли перед курсором 4 пробела
        if editor.get(f"{cursor_position}-3c", cursor_position) == "   ":
            # Если да, то удаляем 4 пробела
            editor.delete(f"{cursor_position}-3c", cursor_position)

        # Возвращаем стандартное поведение Backspace
        return

    def update_line_numbers(event=None):
        line_numbers = get_line_numbers()
        line_number_canvas.delete("all")
        line_number_canvas.create_text(2, 0, anchor='nw', text=line_numbers, font=("Consolas", 20), fill="#E6DDFF")
        line_number_canvas.config(scrollregion=line_number_canvas.bbox("all"))

    def get_line_numbers():
        output = ''
        row, col = editor.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
        return output

    def on_scroll(event):
        editor.yview_scroll(int(-1*(event.delta/120)), "units")
        line_number_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_editor_scroll(*args):
        line_number_canvas.yview_moveto(args[0])
        editor.yview_moveto(args[0])

    import tkinter as tk
    import re

    # Функция для парсинга чисел из строки
    def parse_trigger(event):
        global triggerPosSize
        widget = event.widget
        # Получаем индекс текущего слова в текстовом поле
        index = widget.index("@%d,%d" % (event.x, event.y))
        # Получаем текст в строке

        line_text = widget.get(index + " linestart", index + " lineend")
        match = re.search(r'\.setTrigger\((\d+),(\d+),(\d+),(\d+)', line_text)

        if match:
            numbers = match.groups()

            triggerPosSize = [numbers[0], numbers[1], numbers[2], numbers[3], False]


    # Функция для проверки выделенного текста
    def check_selection(event):
        widget = event.widget
        try:
            # Получаем выделенный текст
            selected_text = widget.selection_get()
            # Получаем индекс начала выделения
            start_index = widget.index(tk.SEL_FIRST)
            line_start_index = widget.index(f"{start_index} linestart")
            line_text = widget.get(line_start_index, f"{line_start_index} lineend")
            if ".setTrigger" not in line_text:

                triggerPosSize[4] = True

        except tk.TclError:
            # Если нет выделения текста

            triggerPosSize[4] = True

    # Функция для обработки выделения мышью
    def check_selection_mouse(event):

        widget = event.widget
        index = widget.index("@%d,%d" % (event.x, event.y))
        line_text = widget.get(index + " linestart", index + " lineend")
        if ".setTrigger" not in line_text:
            triggerPosSize[4] = True

    # Создаем главное окно

    # Привязываем события к текстовому полю


    # Запуск главного цикла обработки событий


    root = tk.Tk()
    root.iconbitmap("res/icon.ico")
    root.config(bg="#353535")
    root.geometry("800x600")
    root.title("Редактор кода")

    left_frame = tk.Frame(root,bg="#353535")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    file_listbox = Listbox(left_frame, bg="#545454", fg='#E6DDFF')
    file_listbox.pack(side=tk.LEFT, fill=tk.Y, expand=1)

    update_file_list()
    file_listbox.bind('<Button-1>', on_file_select)
    root.bind('<Control-s>', save_file)

    editor_frame = tk.Frame(root,bg="#353535")
    editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    line_number_canvas = Canvas(editor_frame, width=40, bg='#444444')

    editor = Text(editor_frame, wrap=tk.WORD, undo=True, bg="#444444", fg='#E6DDFF', font=("Consolas", 20))
    editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    editor.bind("<Button-1>", parse_trigger)
    editor.bind("<ButtonRelease-1>", check_selection_mouse)
    editor.bind("<B1-Motion>", check_selection_mouse)

    scroll = Scrollbar(editor_frame, command=on_editor_scroll)

    editor.config(yscrollcommand=scroll.set)
    line_number_canvas.config(yscrollcommand=scroll.set)

    editor.bind("<KeyRelease>", lambda x1: (highlight_keywords(), check_selection(x1)))
    editor.bind("<KeyRelease-Tab>", insert_spaces)
    editor.bind("<KeyRelease-BackSpace>", remove_spaces)
    editor.bind("<KeyRelease>", lambda x2: (highlight_keywords(), check_selection_mouse(x2)))
    editor.bind("<MouseWheel>", on_scroll)
    editor.bind("<Button-1>", lambda x3: (highlight_keywords, parse_trigger(x3)))

    line_number_canvas.bind("<MouseWheel>", on_scroll)

    selected_file = file_listbox.get(tk.ACTIVE)
    filepath = os.path.join(PROJECT_PATH, selected_file)
    open_file(filepath)

    # Добавляем меню для управления файлами
    menu = Menu(root)
    file_menu = Menu(menu, tearoff=0)
    file_menu.add_command(label="Создать", command=add_file)
    file_menu.add_command(label="Сохранить", command=save_file)
    file_menu.add_command(label="Сохранить как...", command=save_file_as)
    file_menu.add_command(label="Удалить", command=delete_file)
    menu.add_cascade(label="Файл", menu=file_menu)
    root.config(menu=menu)

    highlight_keywords()
    update_line_numbers()

    run = True
    def on_closing():
        global run
        run = False
        print("ЗАКРЫТО")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    while run:
        window.draw(1)
        root.update()
