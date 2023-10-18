from SotedFileLogick import select_and_sort_folder
from tkinter import simpledialog
# from tkinter import messagebox
import tkinter as tk
from AdressBookLogick import AddressBook, Record, Phone, Email


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
        elif command == 'add phone':
            return self.add_phone_to_contact()
        elif command == 'add address':
            return self.add_address()
        elif command == 'remove address':
            return self.remove_address_from_contact()
        elif command == 'edit address':
            return self.edit_address()
        elif command == 'remove phone':
            return self.remove_phone_in_contact()
        elif command == 'edit phone':
            return self.edit_phone_contact()
        elif command == 'find phone':
            return self.find_phone_contact()
        elif command == 'add email':
            return self.add_email()

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

    def add_email(self):
        contact_name = simpledialog.askstring('Добавление почтового ящика', 'Введите имя контакта:')
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                new_email = simpledialog.askstring('Добавление почтового ящика', 'Введите новый почтовый адрес:')
                if new_email:
                    try:
                        contact.add_email(new_email)  # Создаем экземпляр Email и добавляем его к контакту
                        return f'Вы добавили почтовый адрес {new_email} для {contact}.'
                    except ValueError as e:
                        self.error_label.config(text=str(e))
                else:
                    self.error_label.config(text='Вы не ввели новый почтовый адрес.')
            else:
                self.error_label.config(text=f'Контакт с именем {contact_name} не найден.')
        else:
            self.error_label.config(text='Вы не ввели имя контакта.')

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
        except ValueError:
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

    def add_phone_to_contact(self):
        contact_name = simpledialog.askstring("Добавление номера телефона", "Введите имя контакта:")
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                phone_number = simpledialog.askstring("Добавление номера телефона", "Введите номер телефона:")
                try:
                    Phone(phone_number)
                    contact.add_phone(phone_number)
                    # self.error_label.config(text=f'Вы добавили номер телефона для {contact_name}.')
                    return f'Вы добавили номер телефона {phone_number} для {contact_name}.'
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(text=f'Контакт с именем {contact_name} не найден.')
        else:
            self.error_label.config(text='Введите имя контакта.')

    def edit_phone_contact(self):
        user_input = simpledialog.askstring('Выбор контакта', 'Введите имя контакта:')
        if user_input:
            contact = self.address_book.find(user_input)
            if contact:
                if contact.phones:
                    old_phone = simpledialog.askstring('Редактирование телефона', 'Введите старый номер телефона:')
                    if old_phone:
                        new_phone = simpledialog.askstring('Редактирование телефона', 'Введите новый номер телефона:')
                        if new_phone:
                            try:
                                # Проверка формата нового номера (вызывает исключение, если формат неверен)
                                Phone(new_phone)
                                # Обновление номера у объекта contact
                                contact.phone.value = new_phone
                                return f'Вы изменили номер телефона у контакта {contact.name}: {old_phone} -> {new_phone}'
                            except ValueError as e:
                                self.error_label.config(text=str(e))
                        else:
                            self.error_label.config(text='Введите новый номер телефона.')
                    else:
                        self.error_label.config(text='Введите старый номер телефона.')
                else:
                    self.error_label.config(text=f'{contact} не имеет телефона')
            else:
                self.error_label.config(text=f'Контакт {user_input} не найден')
        else:
            self.error_label.config(text='Вы не ввели имя контакта.')

    def remove_phone_in_contact(self):
        contact_name = simpledialog.askstring("Удаление телефона", "Введите имя контакта:")
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                removed_phone = simpledialog.askstring("Удаление телефона",
                                                       f"Введите номер телефона для контакта {contact_name}:")
                try:
                    contact.remove_phone(removed_phone)
                    return f'Вы удалили телефон "{removed_phone}" для контакта "{contact_name}".'
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(text=f'Контакт с именем {contact_name} не найден.')
        else:
            self.error_label.config(text='Введите имя контакта.')

    def find_phone_contact(self):
        user_input = simpledialog.askstring('Поиск номера телефона', 'Введите номер телефона:')
        if user_input:
            contact = self.address_book.find_contact_with_phone(user_input)
            if contact:
                return f'Найден контакт с номером телефона {user_input}: {contact.name}'
            else:
                return f'Контакт с номером телефона {user_input} не найден.'
        else:
            self.error_label.config(text='Введите номер телефона.')

    def add_address(self):
        contact_name = simpledialog.askstring('Добалвение адреса', 'Введите имя контакта:')
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                contact_address = simpledialog.askstring('Добалвение адреса', 'Введите адрес:')
                try:
                    contact.add_address(contact_address)
                    return f'Вы добавили адрес {contact_address} для {contact_name}.'
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(text=f'Контакт с именем {contact_name} не найден.')
        else:
            self.error_label.config(text='Введите имя контакта.')

    def remove_address_from_contact(self):
        contact_name = simpledialog.askstring("Удаление адреса", "Введите имя контакта:")
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                if contact.address is not None:
                    removed_address = contact.address.value
                    contact.remove_address()
                    return f'Вы удалили адрес "{removed_address}" для контакта "{contact_name}".'
                else:
                    self.error_label.config(text=f'{contact_name} не имеет адреса.')
            else:
                self.error_label.config(text=f'Контакт с именем {contact_name} не найден.')
        else:
            self.error_label.config(text='Введите имя контакта.')

    def edit_address(self):
        user_input = simpledialog.askstring('Выбор каогтакта', 'Введите имя контакте:')
        if user_input:
            contact = self.address_book.find(user_input)
            if contact:
                if contact.address:
                    old_address = simpledialog.askstring('Редактирование адреса', 'Введите старый адрес:')
                    new_address = simpledialog.askstring('Редактирование адреса', 'Введите новый адрес:')
                    if old_address and new_address:
                        try:
                            contact.edit_address(old_address, new_address)
                            return f'Вы изменили адрес у контакта {contact.name}: {old_address} -> {new_address}'
                        except ValueError as e:
                            self.error_label.config(text=str(e))
                    else:
                        self.error_label.config(text=f'Пожалуйста, введите и старый адрес, и новый адрес.')
                else:
                    self.error_label.config(text=f'{contact} не имеет адреса')
            else:
                self.error_label.config(text=f'Контакт {contact} не найден')
        else:
            self.error_label.config(text='Вы не ввели контакт для адреса')

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
