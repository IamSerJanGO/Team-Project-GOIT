from collections import UserList
from pickle import load, dump
from datetime import datetime
from pathlib import Path

#class NoteBook
class NotesBook(UserList):
    def add_record(self, notes):
        self.data.append(notes)

#class Notes
#you can add tag and key_words
#also you can sort by tag
class Notes():
    dict_for_notes = NotesBook()
    def __init__(self, note, title, tag = None) -> None:
        self.note = note
        self.tag = tag
        self.title = title

        # Зберігаємо час нотаток для подальшого сортування
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#this function save note by function <add>, you add note to the list
def save_note(list_for_notes, note:Notes):
    dict_for_notes  ={}
    if (note.tag is not None ):
        dict_for_notes["tag"] = note.tag
    if (note.title is not None):
        dict_for_notes["key_words"] = note.title
    dict_for_notes["note"] = note.note
    dict_for_notes["timestamp"] = note.timestamp
    list_for_notes.append(dict_for_notes)
    print (f"Note '{note.note}' with title '{note.title}' has been added.")
#add note to the list of notes
def add_note(list_for_notes,node, title):
    new_note = Notes(node, title)
    save_note(list_for_notes, new_note)

# Функція, яка зберігає данні у файл
def saving(data):
    with open("saved_notes.txt", "wb") as fh:
        dump(data, fh)

file_path = Path("saved_notes.txt")

# Функція, яка зчитує данні з файлу та повертає їх
def loading(file_path: Path):
    try:
        with file_path.open("rb") as fh:
            unpacked = load(fh)
        return unpacked
    except FileNotFoundError:
        return {}

#using this you can search information in all notes
def search_notes(search_word):
    res = "Notes: \n"
    list_for_notes = loading(file_path)
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
def show_all_notes():
    result = "Notes:\n"
    list_for_notes = loading(file_path)
    for record in list_for_notes:
        result += str(record) + "\n"
    return result

# Ця функція повністю переписує нотатку за її заголовком
@input_error
def edit_note(title, new_text):
    list_note = loading(file_path)
    for i in list_note:
        if title in i['key words']:
            i['key words']= new_text
    saving(list_note)
    return f"The note '{title}' has been changed"

# Виводить індекс нотатку за титлом, для зменшення коду. Викликається в інших функціях
def find_title(list_note: list, title):
    for i in list_note:
        if title in i['key words']:
            return list_note.index(i)

# Ця функція додає текст до існуючого нотатку
@input_error
def add_existing_note(title, new_text):
    list_note = loading(file_path)
    list_note[find_title(list_note, title)]['note'] += f" {new_text}"
    saving(list_note)
    return f"The '{new_text}' has been added to note with '{title}' title"

# Ця функція видаляє нотатки за заголовком
@input_error
def remove_note(title):
    list_note = loading(file_path)
    del list_note[find_title(list_note, title)]
    saving(list_note)
    return f"The note {title} has been removed."    

# Пошук за тегом
@input_error
def search_by_tag(tag):
    res = "Notes: \n"
    list_note = loading(file_path)
    for inner_dict in list_note:
        if tag in inner_dict["tag"]:
            res += str(inner_dict) + "\n"
            return res
        return f"There is no note with '{tag}' tag"

# Ця функція додає тег до існуючих нотатків
@input_error
def add_tag(title, tag):
    list_note = loading(file_path)
    list_note[find_title(list_note, title)]["tag"] = tag
    saving(list_note)
    return f'The tag "{tag}" has been added to the note "{title}"'


# Сортування нотаток за часом збереження
def sort_notes():
    notes = loading(file_path)
    sorted_notes = sorted(notes, key=lambda x: x["timestamp"])

    # Я тут пробувала зробити вивод гарним, але щось не дуже. Спробуй ти, якщо є час
    table = "\n".join(str(note) for note in sorted_notes)
    return table

#the main function
def main():
    #dictionary with the commands
    list_for_notes = NotesBook()
    commands = {
        "hello": lambda: print("How can I help you?\n"),
        "good bye": lambda: print("Good bye!"),
        "close": lambda: print("Good bye!"),
        "exit": lambda: print("Good bye!"),
        "note": lambda: (add_note(list_for_notes,note_text)) if len(user_devided) > 1 else print_error("write note."),
        "show note": lambda: print(show_all_notes(list_for_notes)),
        "search note": lambda: print(search_notes(list_for_notes, note_text_search)) if len(user_devided) > 1 else print_error("write search word."),
        "edit": lambda: print(
            edit_note(ask_titles(), ask_note())
        ),  # Переписує текст нотатку на новий
        "update": lambda: print(
            add_existing_note(ask_titles(), ask_note())
        ),  # Додає до існуючого нотатку текст
        "sort": lambda: print(sort_notes()),  # Сортує за часом написання
        "add tag": lambda: print(add_tag(ask_titles(), ask_tag())),  # Додає тег
        "with tag": lambda: print(
            search_by_tag(note_text_search)
        ),  # Шукає нотатки за тегом
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


