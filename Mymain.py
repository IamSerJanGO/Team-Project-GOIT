from collections import UserDict
from collections import UserList
from datetime import datetime
from pickle import load, dump

#class Field
class Field:
    def __init__(self, value = None):
        self._value = value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new_value):
        if self.is_valid(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid field value")
    def is_valid(self, value):
        return bool(value.strip())
    def __str__(self):
        return self._value
    
#class AddressBook
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record #here was record.name.value

    def iterator(self, num):
        count = 0
        result = ""
        for name in self.data:
            if count < int(num):
                count += 1
                result += str(self.data[name]) + "\n"
        return result
   
#class Record
class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday
    def add_phone(self, phone):
        self.phones.append(phone)
    def remove_phone(self, phone):
        self.phones.remove(phone)
    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone
    def __str__(self):
        return f"Name: {self.name.value}, Phones: {', '.join(str(phone) for phone in self.phones)}, Birthday: {self.birthday}"
    def days_until_next_birthday(self,birthday):
        current_date = datetime.now()
        next_birthday_year = current_date.year
        if current_date.month > int(birthday.month):
            next_birthday_year += 1
        next_birthday = datetime(year=next_birthday_year, month=int(birthday.month), day=int(birthday.day))
        days_left = (next_birthday - current_date).days
        return days_left
    def search_info(self, info):
        if (info in str(self.name) or
            any(info in str(phone) for phone in self.phones) or
            (info in str(self.birthday))):
            return True
        else:
            return False

#class Name
class Name(Field):
    def is_valid(self, value):
        return value is not None and value.isalpha() and value.strip()
 
#class Phone
class Phone(Field):
    def __init__(self, number):
        self.number = number
    def is_valid(self, value):
        return value is not None and 4 <= len(value) <= 15
    def __str__(self):
        return self.number

#class Birthday
class Birthday(Field):
    def __init__(self, day, month, year):
       self.day = day
       self.month = month
       self.year = year
    def is_valid(self, value):
        return bool(datetime.strptime(value, '%d-%m-%Y'))
    def __str__(self):
        return "-".join((self.day, self.month, self.year))

#class NoteBook
class NotesBook(UserList):
    def add_record(self, notes):
        self.data.append(notes)
    
#class Notes
#you can add tag and key_words
#also you can sort by tag
class Notes():
    dict_for_notes = NotesBook()
    def __init__(self, note, tag = None, key_words = None) -> None:
        self.note = note
        self.tag = tag
        self.key_words = key_words

#this function save note by function <add>, you add note to the list
def save_note(list_for_notes, note:Notes):
    dict_for_notes  ={}
    if (note.tag is not None ):
        dict_for_notes["tag"] = note.tag
    if (note.key_words is not None):
        dict_for_notes["key_words"] = note.key_word
    dict_for_notes["note"] = note.note
    list_for_notes.append(dict_for_notes)
    print (f"Note '{note.note}' with tag '{note.tag}' has been added.")
#add note to the list of notes
def add_note(list_for_notes,node):
    new_note = Notes(node)
    save_note(list_for_notes, new_note)

#using this you can search information in all notes
def search_notes(list_for_notes, search_word):
    res = "Notes: \n"
    for i in list_for_notes:
        if (search_word in i["note"]):
            res += str(i) + "\n"
    return res

#write error
def print_error(message):
    print("Error: " , message)
#generate the errors
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError:
            return "Error: Invalid input. Please enter name and phone number. Check the data of birth. Check parametrs."
        except IndexError:
            return "Error: Invalid input. Please enter name and phone number."
    return inner

#presents all notes
@input_error
def show_all_notes(list_for_notes):
    result = "Notes:\n"
    for record in list_for_notes:
        result += str(record) + "\n"
    return result


#presents all contacts
@input_error
def show_all_contacts(phone_book):
    result = "Contacts:\n"
    for record in phone_book.data.values():
        result += str(record) + "\n"
    return result

#using the function can add new contact
@input_error
def add_contact(phone_book, name, phone):
    the_name = Name(name)
    the_phone = Phone(phone)
    # If the contact already exists, update its phone list
    if the_name.is_valid(name) and the_phone.is_valid(phone):
        if name in phone_book.data:
            existing_record = phone_book.data[name]
            existing_record.add_phone(the_phone)
        else:
            new_record = Record(the_name)
            new_record.add_phone(the_phone)
            phone_book.add_record(new_record)
        return f"Contact '{name}' with phone '{phone}' has been added."
    raise ValueError

#adds the birthday
@input_error
def add_birthday(phone_book, name, birthday):
    the_name = Name(name)
    birthday_parts = birthday.split('-')
    the_birthday = Birthday(year=birthday_parts[2], month=birthday_parts[1], day=birthday_parts[0])
    data_now = datetime.now()
    if the_name.is_valid(name) and the_birthday.is_valid(birthday) and int(the_birthday.year) <= data_now.year :
        if name in phone_book.data:
            existing_record = phone_book.data[name]
            existing_record.birthday = (the_birthday)
        else:
            new_record = Record(the_name, birthday=the_birthday)
            phone_book.add_record(new_record)
        return f"Contact '{name}' with birthday '{birthday}' has been added."
    raise ValueError
    
#change the phone
@input_error
def change_phone(phone_book, name, old_phone, new_phone):
    
    #name_obj = Name(name)
    if name not in phone_book.data:
    #if name_obj not in phone_book.data:
        raise KeyError
    existing_record = phone_book.data[name]
    phone_new = Phone(new_phone)
    if phone_new.is_valid(new_phone):
        for num in existing_record.phones:
            if str(num) == old_phone:
                existing_record.edit_phone(num, phone_new)
                return f"Phone number for {name} has been changed to {new_phone}."
    raise ValueError

#get the phone
@input_error
def get_phone(phone_book, name):
    if name not in phone_book.data:
        raise KeyError
    existing_record = phone_book.data[name]
    phone_numbers = ', '.join(str(phone) for phone in existing_record.phones)
    result = f"Phone numbers for {name}: {phone_numbers}"
    return result

#delete the phone
@input_error
def delete_phone(phone_book, name, phone):
    if name not in phone_book.data:
        raise KeyError
    existing_record = phone_book.data[name]
    for num in existing_record.phones:
        if str(num) == phone:
            existing_record.remove_phone(num)
            return f"Phone number {phone} has been deleted from {name}."
    raise ValueError

#count the days until next birthday
@input_error
def happy_birthday(phone_book,name):
    if name not in phone_book.data:
        raise KeyError
    existing_record = phone_book.data[name]
    the_birthday = existing_record.birthday
    if the_birthday is None:
        raise KeyError
    return existing_record.days_until_next_birthday(the_birthday)

#show N contacts from the book
@input_error
def iteration_the_func(phone_book, number):
    if len(phone_book) < int(number):
        raise ValueError
    print("Contacts:")
    return phone_book.iterator(number)

#search some information in phone book
def search_information(phone_book, inform):
    res = "Contacts:\n"
    for name in phone_book.data:
        #print(name)
        ex_record  = phone_book.data[name]
        #print(ex_record)
        if ex_record.search_info(inform):
            res += str(ex_record) + '\n'
        #res += str(ex_record.search_info(inform)) + "\n"
    return res

#write information
def send_to_system(phone_book, filename):
    with open(filename, "wb") as f:
        for record in phone_book.data.values():
            dump(record, f)
#read information
def get_from_system(phone_book, filename):
   with open(filename, "rb") as f:
        while True:
            try:
                record = load(f)
                phone_book.add_record(record)
            except EOFError:
                break

#the main function
def main():
    #dictionary with the commands
    phone_book = AddressBook()
    list_for_notes = NotesBook()
    commands = {
        "hello": lambda: print("How can I help you?\n"),
        "good bye": lambda: print("Good bye!"),
        "close": lambda: print("Good bye!"),
        "exit": lambda: print("Good bye!"),
        "show all": lambda: print(show_all_contacts(phone_book)),
        "add": lambda: print(add_contact(phone_book,user_devided[1], user_devided[2])) if len(user_devided) == 3 else print_error("write name and phone."),
        "change": lambda: print(change_phone(phone_book,user_devided[1], user_devided[2], user_devided[3])) if len(user_devided) == 4 else print_error("write name and phone."),
        "phone": lambda: print(get_phone(phone_book, user_devided[1])) if len(user_devided) == 2 else print_error("write name."),
        "delete": lambda: print(delete_phone(phone_book,user_devided[1], user_devided[2])) if len(user_devided) == 3 else print_error("write name and phone."),
        "birth": lambda: print(add_birthday(phone_book, user_devided[1], user_devided[2])) if len(user_devided) == 3 else print_error("write name and birthday"),
        "days": lambda: print(happy_birthday(phone_book, user_devided[1])) if len(user_devided) == 2 else print_error("write name."),
        "iteration": lambda: print(iteration_the_func(phone_book, user_devided[1])) if len(user_devided) == 2 else print_error("write number."),
        "search": lambda: print(search_information(phone_book, user_devided[1])) if len(user_devided) == 2 else print_error("write information."),
        "send": lambda: send_to_system(phone_book, user_devided[1]) if len(user_devided) == 2 else print_error("write file."),
        "get": lambda: get_from_system(phone_book, user_devided[1]) if len(user_devided) == 2 else print_error("write file."),
        "note": lambda: (add_note(list_for_notes,note_text)) if len(user_devided) > 1 else print_error("write note."),
        "show note": lambda: print(show_all_notes(list_for_notes)),
        "search note": lambda: print(search_notes(list_for_notes, note_text_search)) if len(user_devided) > 1 else print_error("write search word."),
    }
    while True:
        user_input = input("Write command \t")
        user_devided = user_input.split(maxsplit=3)
        result_text = ""
        result_text_note = ""
        note_text = "" #use for note
        note_text_search = "" #use for note
        for char in user_input:
            if char != " ":
                result_text += char.lower()
            else: break
        result_text_note = "".join(user_input[0:11])
        note_text = " ".join(user_devided[1::])
        note_text_search=  " ".join(user_devided[2::])
    
        if result_text_note in commands:
            commands[result_text_note]()
            if user_input.lower() == "good bye":
                break
        elif result_text in commands:
            commands[result_text]()
            if result_text in ["close", "exit"]:
                break
        elif user_input.lower() in commands:
            commands[user_input.lower()]()
            if user_input.lower() == "good bye":
                break
        else:
            print("Invalid command. Use 'hello', 'add', 'change', 'phone', 'show all', 'good bye', 'close', or 'exit'")

if __name__ == '__main__':
    main()

