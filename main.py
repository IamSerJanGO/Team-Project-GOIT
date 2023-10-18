from SotedFileLogick import select_and_sort_folder
from tkinter import simpledialog

# from tkinter import messagebox
import tkinter as tk
from AdressBookLogick import AddressBook, Record, Phone, Email
import NotesLogick as nl  # импорт всего модуля, ибо основные функции там не в классе


def get_contact_info(info_type):
    contact_info = simpledialog.askstring(
        "Додавання контакту", f"Введіть {info_type} (якщо ні - закрийте вікно):"
    )
    return contact_info if contact_info else None


def contact_name_request(name):
    contact = simpledialog.askstring("Введіть ім'я контакту:", f"Введіть {name}")
    return contact if contact else None


class CommandProcessorApp:
    def __init__(
        self, app, address_book, notes_book
    ):  # Добавила список заметок как аргумент в класс
        self.app = app
        self.address_book = address_book
        self.notes_book = notes_book
        self.app.geometry("500x500")
        self.app.configure(bg="#F5F5DC")
        self.app.title("Твій помічник 😊")

        # Создание метки для инструкций пользователя
        commands = [
            "add",
            "find contact",
            "check birthday",
            "search",
            "delete",
            "add phone",
            "add address",
            "remove address",
            "edit address",
            "remove phone",
            "edit phone",
            "find phone",
            "add email",
            "edit email",
            "remove email",
            "note",
            "search note",
            "edit note",
            "update note",
            "add tag",
            "with tag",
            "sort note",
            "remove note",
            "show note",
        ]

        descriptions = [
            "Додати контакт",
            "Знайти контакт за ім'ям",
            "Перевірити день народження",
            "Пошук",
            "Видалити контакт",
            "Додати телефон",
            "Додати адресу",
            "Видалити адресу",
            "Редагувати адресу",
            "Видалити телефон",
            "Редагувати телефон",
            "Знайти телефон",
            "Додати пошту",
            "Редагувати пошту",
            "Видалити пошту",
            "Додати нотатку",
            "Пошук нотатки",
            "Редагувати нотатку",
            "Відновити нотатку",
            "Додати тег до нотатку",
            "Пошук нотатків за тегом",
            "Сортувати нотатки",
            "Видалити нотатку",
            "Показати нотатки",
        ]

        # Создаем метку для перечня команд
        commands_label = tk.Label(
            app, text="Список команд:", background="#F5F5DC", justify="left"
        )
        commands_label.pack()

        # Создаем текстовое поле для перечня команд и описаний
        commands_text = tk.Text(
            app, wrap="word", height=10, width=40, background="#F5F5DC"
        )
        commands_text.pack()

        # Вставляем команды и описания в текстовое поле
        for command, description in zip(commands, descriptions):
            commands_text.insert(tk.END, f"{command} - {description}\n")

        # Создаем метку для ввода команды
        self.input_label = tk.Label(app, text="Введіть команду:", background="#F5F5DC")
        self.input_label.pack()

        # Создаем виджет ввода для пользователя
        self.input_entry = tk.Entry(app)
        self.input_entry.pack()

        # Создаем кнопку "Выполнить" и привязываем ее к функции execute_command
        self.submit_button = tk.Button(
            app, text="Виконати", command=self.execute_command
        )
        self.submit_button.pack()

        # Создаем метку для вывода результата
        self.result_label = tk.Label(app, text="")
        self.result_label.pack()

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.error_label = tk.Label(
            self.app, text="", foreground="red", background="#F5F5DC"
        )
        self.error_label.pack()

    def process_command(self, command):
        # Функция обработки команды
        if command == "sorted path":
            return select_and_sort_folder()
        elif command == "add":
            return self.add_contact()
        elif command == "find contact":
            return self.find_contact()
        elif command == "check birthday":
            return self.birthday()
        elif command == "search":
            return self.search_contact()
        elif command == "delete":
            return self.delete_contact()
        elif command == "add phone":
            return self.add_phone_to_contact()
        elif command == "add address":
            return self.add_address()
        elif command == "remove address":
            return self.remove_address_from_contact()
        elif command == "edit address":
            return self.edit_address()
        elif command == "remove phone":
            return self.remove_phone_in_contact()
        elif command == "edit phone":
            return self.edit_phone_contact()
        elif command == "find phone":
            return self.find_phone_contact()
        elif command == "add email":
            return self.add_email()
        elif command == "edit email":
            return self.edit_email()
        elif command == "remove email":
            return self.remove_email_in_contact()
        # Здесь добавила команды для заметок
        elif command == "note":
            return self.add_note()
        elif command == "search note":
            return self.search_note()
        elif command == "edit note":
            return self.edit_note()
        elif command == "update note":
            return self.update_note()
        elif command == "add tag":
            return self.add_tag()
        elif command == "with tag":
            return self.with_tag()
        elif command == "sort note":
            return self.sort_note()
        elif command == "remove note":
            return self.remove_note()
        elif command == "show note":
            return self.show_note()

    def show_note(self):  # показывает все заметки
        return nl.show_all_notes(notes_book)

    def add_note(self):  # добавляет заметку
        title = simpledialog.askstring("Додавання нотатку", "Введіть заголовок:")
        content = simpledialog.askstring("Додавання нотатку", "Введіть нотатку:")
        return nl.add_note(notes_book, content, title)

    def search_note(self):  # ищет заметку рандомному слову
        word = simpledialog.askstring("Пошук нотатки", "Введіть пошукове слово:")
        return nl.search_notes(notes_book, word)

    def edit_note(self):  # полностью переписывает заметку, находя ее по заголовку
        title = simpledialog.askstring("Редагування нотатки", "Введіть заголовок:")
        content = simpledialog.askstring("Редагування нотатки", "Введіть нову нотатку:")
        return nl.edit_note(notes_book, title, content)

    def update_note(self):  # дописывает текст в существующую заметку
        title = simpledialog.askstring("Доповнення нотатки", "Введіть заголовок:")
        content = simpledialog.askstring("Доповнення нотатки", "Введіть текст:")
        return nl.add_existing_note(notes_book, title, content)

    def add_tag(self):  # добавляет тэги в существующую заметку
        title = simpledialog.askstring(
            "Додавання тегу до нотатки", "Введіть заголовок:"
        )
        tag = simpledialog.askstring("Додавання тегу до нотатки", "Введіть тег:")
        return nl.add_tag(notes_book, title, tag)

    def with_tag(self):  # находит заметку по тэгу, пока что не работает, исправим позже
        tag = simpledialog.askstring("Пошук нотатків за тегом", "Введіть тег:")
        return nl.search_by_tag(notes_book, tag)

    def sort_note(self):  # сортирует заметки по дате добавления
        return nl.sort_notes(notes_book)

    def remove_note(self):  # удаляет заметку по ее заголовку
        title = simpledialog.askstring("Видалення нотатки", "Введіть заголовок:")
        return nl.remove_note(notes_book, title)

    def find_contact(self):  # Поиск контакта
        contact_name = contact_name_request("Ім'я")
        try:
            contact = address_book.find(contact_name)
            if contact:
                self.error_label.config(text="")
                return f"Контакт, який ви шукали: {contact}"
            else:
                self.error_label.config(
                    text=f"Контакт з ім'ям {contact_name} не знайдено"
                )
        except ValueError as e:
            self.error_label.config(text=str(e))

    def add_email(self):
        contact_name = simpledialog.askstring(
            "Додавання поштової адреси", "Введіть ім'я контакту:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                new_email = simpledialog.askstring(
                    "Додавання поштової адреси", "Введіть нову поштову адресу:"
                )
                if new_email:
                    try:
                        contact.add_email(
                            new_email
                        )  # Создаем экземпляр Email и добавляем его к контакту
                        return f"Ви додали поштову адресу {new_email} для {contact}."
                    except ValueError as e:
                        self.error_label.config(text=str(e))
                else:
                    self.error_label.config(text="Ви не ввели нову поштову адресу.")
            else:
                self.error_label.config(
                    text=f"Контакт з ім'ям {contact_name} не знайдено."
                )
        else:
            self.error_label.config(text="Ви не ввели ім'я контакту.")

    def edit_email(self):
        user_input = simpledialog.askstring("Введення данних", "Введіть ім'я контакту")
        if user_input:
            contact = self.address_book.find(user_input)
            if contact:
                if contact.emails:
                    old_email = simpledialog.askstring(
                        "Введення данних", "Введіть стару пошту"
                    )
                    if old_email:
                        new_email = simpledialog.askstring(
                            "Введення данних", "Введіть нову пошту"
                        )
                        if new_email:
                            try:
                                Email(new_email)
                                contact.edit_email(old_email, new_email)
                                return f"Ви змінили номер телефону у контакту {contact.name}: {old_email} -> {new_email}"
                            except ValueError as e:
                                self.error_label.config(text=str(e))
                        else:
                            self.error_label.config(text="Введіть нову поштову адресу.")
                    else:
                        self.error_label.config(text="Введіть стару поштову адресу.")
                else:
                    self.error_label.config(text=f"{contact} не має поштової адреси")
            else:
                self.error_label.config(text=f"Контакт {contact} не знайдено")
        else:
            self.error_label.config(text="Ви не ввели ім'я контакту.")

    def remove_email_in_contact(self):
        contact_name = simpledialog.askstring(
            "Видалення пошти", "Введіть ім'я контакту:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                removed_email = simpledialog.askstring(
                    "Видалення пошти", f"Введіть пошту для контакту {contact_name}:"
                )
                try:
                    contact.remove_email(removed_email)
                    return f'Ви видалили пошту "{removed_email}" для контакту "{contact_name}".'
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(
                    text=f"Контакт з ім'ям {contact_name} не знайдено."
                )
        else:
            self.error_label.config(text="Введіть ім'я контакту.")

    def add_contact(self):
        contact_name = simpledialog.askstring(
            "Додавання контакту", "Введіть ім'я контакту:"
        )
        contact_phone = simpledialog.askstring(
            "Додавання контакту", "Введіть номер контакту:"
        )

        # Проверка формата номера телефона
        try:
            Phone(contact_phone)  # Если прошло проверку формата, ничего не произойдет
        except ValueError as e:
            self.error_label.config(text=str(e))
            return

        contact_mail = get_contact_info("пошту контакту")

        # Проверка формата email
        if contact_mail is not None:  # Пользователь ввел email или нажал Отмена
            try:
                Email(
                    contact_mail
                )  # Если прошло проверку формата, ничего не произойдет
            except ValueError as e:
                self.error_label.config(text=str(e))
                return
        else:
            contact_mail = None

        contact_address = get_contact_info("адресу контакту")
        contact_birthday = get_contact_info("день народження контакту")

        contact = Record(
            contact_name,
            contact_phone,
            email=contact_mail,
            address=contact_address,
            birthday=contact_birthday,
        )

        self.address_book.add_record(contact)

        return f"Ви додали новий контакт: {contact_name} - {contact_phone}"

        # if contact_name and contact_phone: contact = Record(contact_name, contact_phone, email=contact_mail,
        # address=contact_address, birthday=contact_birthday) self.address_book.add_record(contact) return f'Вы
        # добавили новый контакт: {contact_name} - {contact_phone}'

    def add_phone_to_contact(self):
        contact_name = simpledialog.askstring(
            "Додавання номеру телефону", "Введіть ім'я контакту:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                phone_number = simpledialog.askstring(
                    "Додавання номеру телефону", "Введіть номер телефону:"
                )
                try:
                    Phone(phone_number)
                    contact.add_phone(phone_number)
                    # self.error_label.config(text=f'Вы добавили номер телефона для {contact_name}.')
                    return (
                        f"Ви додали номер телефону {phone_number} для {contact_name}."
                    )
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(
                    text=f"Контакт з ім'ям {contact_name} не знайдено."
                )
        else:
            self.error_label.config(text="Введіть ім'я контакту.")

    def edit_phone_contact(self):
        user_input = simpledialog.askstring("Вибір контакту", "Введіть ім'я контакту:")
        if user_input:
            contact = self.address_book.find(user_input)
            if contact:
                if contact.phones:
                    old_phone = simpledialog.askstring(
                        "Редагування телефону", "Введіть старий номер телефону:"
                    )
                    if old_phone:
                        new_phone = simpledialog.askstring(
                            "Редагування телефону", "Введіть новий номер телефону:"
                        )
                        if new_phone:
                            try:
                                # Проверка формата нового номера (вызывает исключение, если формат неверен)
                                Phone(new_phone)
                                # Обновление номера у объекта contact
                                contact.edit_phone(old_phone,new_phone)
                                return f"Ви змінили номер телефону у контакту {contact.name}: {old_phone} -> {new_phone}"
                            except ValueError as e:
                                self.error_label.config(text=str(e))
                        else:
                            self.error_label.config(
                                text="Введіть новий номер телефону."
                            )
                    else:
                        self.error_label.config(text="Введіть старий номер телефону.")
                else:
                    self.error_label.config(text=f"{contact} не має телефону")
            else:
                self.error_label.config(text=f"Контакт {user_input} не знайдено")
        else:
            self.error_label.config(text="Ви не ввели ім'я контакту.")

    def remove_phone_in_contact(self):
        contact_name = simpledialog.askstring(
            "Видалення телефону", "Введіть ім'я контакту:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                removed_phone = simpledialog.askstring(
                    "Видалення телефону",
                    f"Введіть номер телефону для контакту {contact_name}:",
                )
                try:
                    contact.remove_phone(removed_phone)
                    return f'Ви видалили телефон "{removed_phone}" для контакту "{contact_name}".'
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(
                    text=f"Контакт з ім'ям {contact_name} не знайдено."
                )
        else:
            self.error_label.config(text="Введіть ім'я контакту.")

    def find_phone_contact(self):
        user_input = simpledialog.askstring(
            "Пошук номера телефону", "Введіть номер телефону:"
        )
        if user_input:
            contact = self.address_book.find_contact_with_phone(user_input)
            if contact:
                return (
                    f"Знайдено контакт з номером телефону {user_input}: {contact.name}"
                )
            else:
                return f"Контакт з номером телефону {user_input} не знайдено."
        else:
            self.error_label.config(text="Введіть номер телефону.")

    def add_address(self):
        contact_name = simpledialog.askstring(
            "Додавання адреси", "Введіть ім'я контакту:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                contact_address = simpledialog.askstring(
                    "Додавання адреси", "Введіть адресу:"
                )
                try:
                    contact.add_address(contact_address)
                    return f"Ви додали адресу {contact_address} для {contact_name}."
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(
                    text=f"Контакт з ім'ям {contact_name} не знайдено."
                )
        else:
            self.error_label.config(text="Введіть ім'я контакту.")

    def remove_address_from_contact(self):
        contact_name = simpledialog.askstring(
            "Видалення адреси", "Введіть ім'я контакту:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                if contact.address is not None:
                    removed_address = contact.address.value
                    contact.remove_address()
                    return f'Ви видалили адресу "{removed_address}" для контакту "{contact_name}".'
                else:
                    self.error_label.config(text=f"{contact_name} не має адреси.")
            else:
                self.error_label.config(
                    text=f"Контакт з ім'ям {contact_name} не знайдено."
                )
        else:
            self.error_label.config(text="Введіть ім'я контакту.")

    def edit_address(self):
        user_input = simpledialog.askstring("Вибір контакту", "Введіть ім'я контакту:")
        if user_input:
            contact = self.address_book.find(user_input)
            if contact:
                if contact.address:
                    old_address = simpledialog.askstring(
                        "Редагування адреси", "Введіть стару адресу:"
                    )
                    new_address = simpledialog.askstring(
                        "Редагування адреси", "Введіть нову адресу:"
                    )
                    if old_address and new_address:
                        try:
                            contact.edit_address(old_address, new_address)
                            return f"Ви змінили адресу у контакту {contact.name}: {old_address} -> {new_address}"
                        except ValueError as e:
                            self.error_label.config(text=str(e))
                    else:
                        self.error_label.config(
                            text=f"Будь ласка, введіть і стару, і нову адресу."
                        )
                else:
                    self.error_label.config(text=f"{contact} не має адреси")
            else:
                self.error_label.config(text=f"Контакт {contact} не знайдено")
        else:
            self.error_label.config(text="Ви не ввели контакт для адреси")

    def delete_contact(self):
        user_input = simpledialog.askstring(
            "Видалення контакту", "Введіть ім'я контакту для видалення:"
        )
        if user_input:
            result = self.address_book.delete(user_input)
            if result:
                self.error_label.config(text=f"Ви видалили контакт: {result}")
            else:
                self.error_label.config(text="Контакт не знайдено")

    def search_contact(self):
        user_input = simpledialog.askstring("Вікно вводу", "Введіть данні для пошуку:")
        if user_input:
            matches = self.address_book.search(user_input)
            if matches:
                result = "Знайдені збіги в таких контактах:\n"
                result += "\n".join(str(record) for record in matches)
                return result
            else:
                return "Збігів не знайдено."

    def birthday(self):
        try:
            days = int(
                simpledialog.askstring(
                    "Перевірка днів народження", "Введіть кількість днів:"
                )
            )
            if isinstance(days, int):
                upcoming_birthdays = self.address_book.days_to_birthday(days)
                if upcoming_birthdays:
                    return f"Збіги знайдені з такими контактами:\n" + "\n".join(
                        upcoming_birthdays
                    )
                else:
                    return "Немає збігів."
            else:
                return f"{days} - друже, необхідно ввести кількість днів у числовому форматі."
        except ValueError:
            return (
                "Неправильний формат введення. Введіть кількість днів у числовому форматі."
            )

    def execute_command(self):
        # Функция, вызываемая при нажатии кнопки "Выполнить"
        user_input = self.input_entry.get()  # Получаем текст из виджета Entry
        result = self.process_command(user_input)  # Обрабатываем команду
        self.result_label.config(text=result)  # Обновляем виджет Label с результатом

    def on_closing(self):
        # Обработчик закрытия окна
        self.address_book.save_to_file("address-book")  # Сохраняем данные в файл
        nl.send_to_system(self.notes_book, "notes-book")  # Сохраняем данные в файл
        self.app.destroy()


if __name__ == "__main__":
    import os
    import atexit

    data_folder = "data"
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)

    address_book = AddressBook()
    notes_book = nl.NotesBook()
    address_book_file = os.path.join(data_folder, "address-book")
    notes_book_file = os.path.join(data_folder, "notes-book")

    address_book.load_from_file(address_book_file)
    nl.get_from_system(notes_book, notes_book_file)

    app = tk.Tk()
    command_processor = CommandProcessorApp(app, address_book, notes_book)
    app.protocol("WM_DELETE_WINDOW", app.quit)  # Обработчик закрытия окна

    # Функция для сохранения данных при закрытии приложения
    def save_data():
        address_book.save_to_file(address_book_file)
        nl.send_to_system(notes_book, notes_book_file)

    atexit.register(save_data)  # Регистрация функции для сохранения данных при выходе

    app.mainloop()
