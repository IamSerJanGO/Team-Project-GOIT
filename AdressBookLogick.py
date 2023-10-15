from collections import UserDict
from datetime import *
import pickle
import re

# Перш за все, давайте визначимо власну помилку для некоректного формату номеру телефону.
class PhoneInvalidFormatError(ValueError):
    pass

# Базовий клас Field для представлення поля зі значенням.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас Name успадкований від Field і представляє ім'я.
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

# Клас Phone успадкований від Field і представляє номер телефону.
class Phone(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if (value.startswith('+') and len(value[1:]) == 12 and value[1:].isdigit()) or (value.isdigit() and len(value) in (10, 12)):
            self._value = value
        else:
            raise PhoneInvalidFormatError('Invalid phone format')

# Декоратор для перевірки правильності набору мейлу.
def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email format")

# Клас Email успадкований від Field і представляє електронну адресу.
class Email(Field):
    def __init__(self, value):
        validate_email(value)
        super().__init__(value)

class Birthday(Field):

    def __init__(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format for Birthday")
        super().__init__(value)


class Address(Field):
    def __init__(self, value):
        words = value.split()
        if len(words) >= 2 and all(len(word) > 3 for word in words):
            super().__init__(value)
        else:
            raise ValueError('Invalid data format for Address')


# Клас Record для представлення контакту в адресній книзі.
class Record:
    def __init__(self, name, phone, email=None, address=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.email = Email(email) if email else None
        self.address = Address(address) if address else None
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Видаляємо телефон зі списку, залишаючи всі інші.
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError(f"Phone number '{old_phone}' not found")

    def find_phone(self, phone):
        # Пошук і повернення телефону за його номером.
        phones_found = [p for p in self.phones if p.value == phone]
        return phones_found[0] if phones_found else None

    def __str__(self):
        # Повертає рядок, представляючи контакт.
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, email: {self.email.value}"

    # def days_to_birthday(self):
    #     if not self.birthday:
    #         return -1
    #
    #     today = datetime.now().date()
    #     next_birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d").date().replace(year=today.year)
    #     if today > next_birthday:
    #         next_birthday = next_birthday.replace(year=today.year + 1)
    #
    #     days_until_birthday = (next_birthday - today).days
    #     return days_until_birthday

# Клас AddressBook успадкований від UserDict і представляє адресну книгу.
class AddressBook(UserDict):
    def add_record(self, record):
        # Додає контакт до адресної книги, використовуючи ім'я контакту як ключ.
        self.data[record.name.value] = record

    def find(self, name):
        # Пошук і повернення контакту за ім'ям.
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        # Видалення контакту з адресної книги за ім'ям.
        if name in self.data:
            del self.data[name]

    def __iter__(self):
        self.current_record = 0
        self.records = list(self.data.values())
        return self

    def __next__(self):
        if self.current_record < len(self.records):
            record = self.records[self.current_record]
            self.current_record += 1
            return record
        else:
            raise StopIteration

    def search(self, query):
        results = []
        for record in self.data.values():
            if (
                query.lower() in record.name.value.lower() or
                any(query.lower() in phone.value for phone in record.phones)
            ):
                results.append(record)
        return results

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}


    def days_to_birthday(self, days_to_filter):
        today = datetime.now().date()
        future_date = today + timedelta(days=days_to_filter)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                next_birthday = datetime.strptime(record.birthday.value, "%Y-%m-%d").date().replace(year=today.year)
                if today <= next_birthday <= future_date:
                    upcoming_birthdays.append(str(record))
        print(upcoming_birthdays)
        return upcoming_birthdays

'''
Метод days_to_birthday який виводить список контактів, у яких день народження через задану кількість днів
від поточної дати
'''


if __name__ == "__main__":
    # Створення адресної книги під час запуску скрипта.
    address_book = AddressBook()
    john_record = Record("John", '+380676757690')
    john_record.add_phone("+380676757690")
    john_record.add_phone("+378886230216")
    address_book.add_record(john_record)
    jane_record = Record("Jane", '+380676757690')
    jane_record.add_phone("+378886230216")
    address_book.add_record(jane_record)
    address_book.days_to_birthday(50)
    print(address_book.find("Jane"))