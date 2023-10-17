from SotedFileLogick import select_and_sort_folder
from tkinter import simpledialog
# from tkinter import messagebox
import tkinter as tk
from AdressBookLogick import AddressBook, Record, PhoneInvalidFormatError


def get_contact_info(info_type):
    contact_info = simpledialog.askstring("Добавление контакта", f"Введите {info_type} (если нет - закрой окно):")
    return contact_info if contact_info else None


def contact_name_request(name):
    contact = simpledialog.askstring('Введи имя контакта:', f'Введите {name}')
    return contact if contact else None


class CommandProcessorApp:
    def __init__(self, app, address_book):
        self.app = app
        self.address_book = address_book
        self.app.geometry("300x200")
        self.app.configure(bg="#F5F5DC")
        self.app.title("Твой помошник 😊")

        # Создание метки для инструкций пользователя
        self.input_label = tk.Label(app, text="Введите команду:\nспсиок команд", background='#F5F5DC')
        self.input_label.pack()

        # Создание виджета ввода для пользователя
        self.input_entry = tk.Entry(app)
        self.input_entry.pack()

        # Создание кнопки "Выполнить" и привязка ее к функции execute_command
        self.submit_button = tk.Button(app, text="Выполнить", command=self.execute_command)
        self.submit_button.pack()

        # Создание метки для вывода результата
        self.result_label = tk.Label(app, text="")
        self.result_label.pack()

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.error_label = tk.Label(self.app, text="", foreground="red", background='#F5F5DC')
        self.error_label.pack()

    def process_command(self, command):
        # Функция обработки команды
        if command == "sorted path":
            return select_and_sort_folder()
        elif command == 'add':
            return self.add_contact()
        elif command == 'find contact':
            return self.find_contact()
        elif command == 'check birthday':
            return self.birthday()
        elif command == 'search':
            return self.search_contact()
        elif command == 'delete':
            return self.delete_contact()

    def find_contact(self):  # Поиск контакта
        contact_name = contact_name_request('Имя')
        try:
            contact = address_book.find(contact_name)
            if contact:
                self.error_label.config(text="")
                return f'Контакт, который вы искали: {contact}'
            else:
                self.error_label.config(text=f'Контакт с именем {contact_name} не найден')
        except ValueError as e:
            self.error_label.config(text=str(e))
        return ""

    def add_contact(self):  # Добовляем контакт
        contact_name = simpledialog.askstring("Добавление контакта", "Введите имя контакта:")
        contact_phone = simpledialog.askstring("Добавление контакта", "Введите номер контакта:")

        contact_mail = get_contact_info("почту контакта")
        contact_address = get_contact_info("адрес контакта")
        contact_birthday = get_contact_info("день рождения контакта")

        try:
            contact = Record(contact_name, contact_phone, email=contact_mail, address=contact_address,
                             birthday=contact_birthday)
            self.address_book.add_record(contact)
        except PhoneInvalidFormatError:
            self.error_label.config(text="Invalid phone number.")
            return
        except ValueError as e:
            self.error_label.config(text=str(e))
            return
        self.error_label.config(text="")
        return f'Вы добавили новый контакт: {contact_name} - {contact_phone}'

        # if contact_name and contact_phone: contact = Record(contact_name, contact_phone, email=contact_mail,
        # address=contact_address, birthday=contact_birthday) self.address_book.add_record(contact) return f'Вы
        # добавили новый контакт: {contact_name} - {contact_phone}'

    def delete_contact(self):
        user_input = simpledialog.askstring('Удаление контакта', 'Введите имя контакта для удаления:')
        if user_input:
            result = self.address_book.delete(user_input)
            if result:
                self.error_label.config(text=f'Вы удалили контакт: {result}')
            else:
                self.error_label.config(text='Контакт не найден')

    def search_contact(self):
        user_input = simpledialog.askstring('Окно ввода', "Введите данные для поиска:")
        if user_input:
            matches = self.address_book.search(user_input)
            if matches:
                result = 'Найдены совпадения в таких контактах:\n'
                result += '\n'.join(str(record) for record in matches)
                return result
            else:
                return 'Совпадений не найдено.'

    def birthday(self):
        try:
            days = int(simpledialog.askstring('Проверка дней рождения', 'Введите количество дней:'))
            if isinstance(days, int):
                upcoming_birthdays = self.address_book.days_to_birthday(days)
                if upcoming_birthdays:
                    return f'Співпадіння знайдені з такими контактами:\n' + '\n'.join(upcoming_birthdays)
                else:
                    return 'Немає збігів.'
            else:
                return f'{days} - дорогой, нужно вводить количество дней в числовом формате.'
        except ValueError:
            return 'Неправильный формат ввода. Введите количество дней в числовом формате.'

    def execute_command(self):
        # Функция, вызываемая при нажатии кнопки "Выполнить"
        user_input = self.input_entry.get()  # Получаем текст из виджета Entry
        result = self.process_command(user_input)  # Обрабатываем команду
        self.result_label.config(text=result)  # Обновляем виджет Label с результатом

    def on_closing(self):
        # Обработчик закрытия окна
        self.address_book.save_to_file('address-book')  # Сохраняем данные в файл
        self.app.destroy()


if __name__ == "__main__":
    address_book = AddressBook()
    address_book.load_from_file('address-book')
    app = tk.Tk()
    command_processor = CommandProcessorApp(app, address_book)  # Создание экземпляра класса
    app.mainloop()  # Запуск графического интерфейса
