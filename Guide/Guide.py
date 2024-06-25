from tkinter import *
from tkinter import ttk, filedialog, messagebox


def work_with_phonebook():
    patch = "phon.txt"

    def save_info():
        name = entry_name.get()
        surname = entry_surname.get()
        patronymic = entry_patronymic.get()
        phone_number = entry_phone_number.get()

        # Проверка, что ФИО содержат только буквы
        if not (name.isalpha() and surname.isalpha() and patronymic.isalpha()):
            messagebox.showerror(
                "Ошибка", "Имя, фамилия и отчество должны содержать только буквы")
            return

        # Проверка, что номер телефона содержит только цифры
        if not phone_number.isdigit():
            messagebox.showerror(
                "Ошибка", "Номер телефона должен содержать только цифры")
            return

        # Добавление данных в список
        phonebook.append({
            "name": name,
            "surname": surname,
            "patronymic": patronymic,
            "phone_number": phone_number
        })

        save_file(name, surname, patronymic, phone_number)
        messagebox.showinfo("Успех", "Данные успешно сохранены!")
        print(phonebook)  # Для проверки, что информация сохраняется

    def save_file(name, surname, patronymic, phone_number):
        with open(patch, "a", encoding="utf-8") as file:
            file.write(f"{name} {surname} {patronymic} {phone_number}\n")

    def deleted_info_data():
        data = {search_entry_name.get().strip().lower(), search_entry_surname.get().strip().lower(),
                search_entry_patronymic.get().strip().lower(), search_entry_phone_number.get().strip()}

        data_copy = data.copy()
        for i in data_copy:
            if i in 'имя':
                data.remove(i)
            elif i in 'фамилия':
                data.remove(i)
            elif i in 'отчество':
                data.remove(i)
            elif i in 'Номер телефона без +':
                data.remove(i)
        return data

    def search_info():
        results = []
        result_data = ' '.join(deleted_info_data()).split()
        print(result_data)
        with open(patch, "r", encoding="utf-8") as file:
            for line in file:
                words = line.lower().split()  # Разбиваем строку на слова
                if all(data in words for data in result_data):
                    results.append(line)

        results_str = '\n'.join(list(results))

        messagebox.showinfo(
            "Результат поиска", f"Результат поиска:\n{results_str}")

    def create_entry_with_placeholder(parent, placeholder_text, row):
        entry = Entry(parent)
        entry.insert(0, placeholder_text)
        entry.bind("<FocusIn>", lambda event: entry.delete(0, END))
        entry.grid(column=1, row=row, padx=10, pady=10)
        return entry

    def copy_selected_line_to_file():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showerror("Ошибка", "Выберите строку для копирования")
            return

        selected_line = listbox.get(selected_index[0])

        dst_filename = filedialog.asksaveasfilename(
            title="Выбрать файл для сохранения", filetypes=[("Текстовые файлы", "*.txt")]
        )
        if not dst_filename:
            return

        try:
            with open(dst_filename, "w", encoding="utf-8") as dst_file:
                dst_file.write(selected_line.strip())
            messagebox.showinfo(
                "Успех", "Выбранная строка успешно скопирована!")
        except Exception as e:
            messagebox.showerror(
                "Ошибка", f"Ошибка при копировании строки:\n{e}")

    def load_lines_to_listbox():
        listbox.delete(0, END)  # Очищаем содержимое listbox

        try:
            with open(patch, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    # Добавляем строки в listbox
                    listbox.insert(END, line.strip())
        except Exception as e:
            messagebox.showerror(
                "Ошибка", f"Ошибка при загрузке данных из файла:\n{e}")

    window = Tk()
    window.title("Телефонный справочник")

    tab_control = ttk.Notebook(window)

    tab_add = Frame(tab_control)
    tab_search = Frame(tab_control)
    tab_copy = Frame(tab_control)

    tab_control.add(tab_add, text='Добавление')
    tab_control.add(tab_search, text='Поиск')
    tab_control.add(tab_copy, text='Копировать')
    tab_control.pack(expand=1, fill='both')

    # Вкладка добавления
    Label(tab_add, text="Введите ваше имя").grid(
        column=0, row=0, padx=10, pady=10)
    entry_name = create_entry_with_placeholder(tab_add, "Имя", 0)

    Label(tab_add, text="Введите вашу фамилию").grid(
        column=0, row=1, padx=10, pady=10)
    entry_surname = create_entry_with_placeholder(tab_add, "Фамилия", 1)

    Label(tab_add, text="Введите ваше отчество").grid(
        column=0, row=2, padx=10, pady=10)
    entry_patronymic = create_entry_with_placeholder(tab_add, "Отчество", 2)

    Label(tab_add, text="Введите ваш номер телефона").grid(
        column=0, row=3, padx=10, pady=10)
    entry_phone_number = create_entry_with_placeholder(
        tab_add, "Пишите номер без +", 3)

    btn_save = Button(tab_add, text="Сохранить", command=save_info)
    btn_save.grid(column=1, row=4, padx=10, pady=20)

    # Вкладка поиска
    Label(tab_search, text="Введите ваше имя").grid(
        column=0, row=0, padx=10, pady=10)
    search_entry_name = create_entry_with_placeholder(tab_search, "Имя", 0)

    Label(tab_search, text="Введите вашу фамилию").grid(
        column=0, row=1, padx=10, pady=10)
    search_entry_surname = create_entry_with_placeholder(
        tab_search, "Фамилия", 1)

    Label(tab_search, text="Введите ваше отчество").grid(
        column=0, row=2, padx=10, pady=10)
    search_entry_patronymic = create_entry_with_placeholder(
        tab_search, "Отчество", 2)

    Label(tab_search, text="Введите ваш номер телефона").grid(
        column=0, row=3, padx=10, pady=10)
    search_entry_phone_number = create_entry_with_placeholder(
        tab_search, "Пишите номер без +", 3)

    btn_search = Button(tab_search, text="Поиск", command=search_info)
    btn_search.grid(column=1, row=4, padx=10, pady=20)

    result_label = Label(tab_search, text="")
    result_label.grid(column=0, row=5, columnspan=2, padx=10, pady=10)

    # Вкладка копирования
    Label(tab_copy, text="Выберите строку для копирования:").grid(
        column=0, row=0, padx=10, pady=10)

    listbox = Listbox(tab_copy, selectmode=SINGLE)
    listbox.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

    btn_load_lines = Button(
        tab_copy, text="Загрузить строки", command=load_lines_to_listbox)
    btn_load_lines.grid(column=0, row=2, padx=10, pady=10)

    btn_copy_line = Button(
        tab_copy, text="Копировать выбранную строку", command=copy_selected_line_to_file)
    btn_copy_line.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    window.mainloop()


# Список для хранения данных
phonebook = []

# Вызов функции для запуска приложения
work_with_phonebook()
