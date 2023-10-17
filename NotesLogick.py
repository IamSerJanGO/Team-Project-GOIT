from collections import UserList
from pickle import load, dump
from datetime import datetime
#from pathlib import Path

#class NoteBook - список, що зберігає словники нотатків
class NotesBook(UserList):
    def add_record(self, notes):
        self.data.append(notes)

#class Notes - створює нотатки
class Notes():
    dict_for_notes = NotesBook()
    def __init__(self, note, title, tag = None) -> None:
        self.note = note
        self.tag = tag
        self.title = title

        # Зберігаємо час нотаток для подальшого сортування
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Додає нотатки до списку за функцією <add>
def save_note(list_for_notes, note:Notes):
    dict_for_notes  ={}
    if (note.tag is not None ):
        dict_for_notes["tag"] = note.tag
    dict_for_notes["title"] = note.title
    dict_for_notes["note"] = note.note
    dict_for_notes["timestamp"] = note.timestamp
    list_for_notes.append(dict_for_notes)
    #saving(list_for_notes)
    print (f"Note '{note.note}' with title '{note.title}' has been added.")

# Додає нотатки до списку
def add_note(list_for_notes,node, title):
    new_note = Notes(node, title)
    save_note(list_for_notes, new_note)


# Знаходить нотатки за рандомними словами
def search_notes(list_for_notes,search_word):
    res = "Notes: \n"
    #list_for_notes = loading(file_path)
    for i in list_for_notes:
        if (search_word in i["note"]):
            res += str(i) + "\n"
    return res

# Пише помилки
def print_error(message):
    print("Error: " , message)

# Декоратор для помилок
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

# Показує всі нотатки
@input_error
def show_all_notes(list_for_notes):
    result = "Notes:\n"
    #list_for_note= loading(file_path)
    for record in list_for_notes:
        result += str(record) + "\n"
    return result

# Ця функція повністю переписує нотатку за її заголовком
# Трішки змінила для покращення працездатності
@input_error
def edit_note(list_for_notes,title, new_text):
    #list_note = loading(file_path)
    for i in list_for_notes:
        if title == i['title']:
            i['note']= new_text
    #saving(list_note)
    return f"The note '{title}' has been changed"

# Виводить індекс нотатку за титлом, для зменшення коду. Викликається в інших функціях
def find_title(list_note: list, title):
    for i in list_note:
        if title == i['title']:
            return list_note.index(i)

# Ця функція додає текст до існуючого нотатку
@input_error
def add_existing_note(list_for_notes,title, new_text):
    #list_note = loading(file_path)
    list_for_notes[find_title(list_for_notes, title)]['note'] += f" {new_text}"
    #saving(list_note)
    return f"The '{new_text}' has been added to note with '{title}' title"

# Ця функція видаляє нотатки за заголовком
@input_error
def remove_note(list_for_notes, title):
    del list_for_notes[find_title(list_for_notes, title)]
    return f"The note {title} has been removed."

# Пошук за тегом оновлено
@input_error
def search_by_tag(list_for_notes,tag):
    res = "Notes: \n"
    #list_note = loading(file_path)
    for inner_dict in list_for_notes:
        if tag == inner_dict["tag"]:
            res += str(inner_dict) + "\n"
    return res
        #else:
            #return f"There is no note with '{tag}' tag"

# Ця функція додає тег до існуючих нотатків оновлено
@input_error
def add_tag(list_for_notes,title, tag):
    #list_note = loading(file_path)
    list_for_notes[find_title(list_for_notes, title)]["tag"] = tag
    #saving(list_note)
    return f'The tag "{tag}" has been added to the note "{title}"'


# Сортування нотаток за часом збереження оновлено
def sort_notes(list_for_notes):
    #notes = loading(file_path)
    result = "Sorting by data: \n"
    sorted_notes = sorted(list_for_notes, key=lambda x: x["timestamp"])
    for r in sorted_notes:
        result += str(r) + "\n"
    return result
   

# Зберігає інформацію в файл
def send_to_system(list_for_notes, filename):
    with open(filename, "wb") as f:
        for record in list_for_notes:
            dump(record, f)

# Зчитує інфу з файлу
def get_from_system(list_for_notes, filename):
   with open(filename, "rb") as f:
        while True:
            try:
                record = load(f)
                list_for_notes.append(record)
            except EOFError:
                break


# Головна функція
def main():
    #Словник команд
    list_for_notes = NotesBook()
    commands = {
        "hello": lambda: print("How can I help you?\n"),
        "good bye": lambda: print("Good bye!"),
        "close": lambda: print("Good bye!"),
        "exit": lambda: print("Good bye!"),
        "note": lambda: (add_note(list_for_notes,list_n2[1],list_n2[0])),
        "show note": lambda: print(show_all_notes(list_for_notes)),
        "search note": lambda: print(search_notes(list_for_notes, note_text_search)) if len(user_devided) > 1 else print_error("write search word."),
        "edit": lambda: print(
            edit_note(list_for_notes, list_n2[0],list_n2[1].strip())
        ),  # Переписує текст нотатку на новий
        "update": lambda: print(
            add_existing_note(list_for_notes, list_n2[0], list_n2[1].strip())
        ),  # Додає до існуючого нотатку текст
        "sort": lambda: print(sort_notes(list_for_notes)),  # Сортує за часом написання
        "add tag": lambda: print(add_tag(list_for_notes, list_n2[0],list_n2[1].strip())),  # Додає тег
        "with tag": lambda: print(
            search_by_tag(list_for_notes, note_text_search)
        ),  # Шукає нотатки за тегом
        #"saving": lambda:print(saving()),
        "send": lambda: print(send_to_system(list_for_notes, user_devided[1])),
        "get": lambda: print(get_from_system(list_for_notes, user_devided[1])),
        "remove": lambda: print(remove_note(list_for_notes, note_text_search)) 
    }
    while True:
        user_input = input("Write command \t")
        user_devided = user_input.split(maxsplit=3)
        result_text = ""
        result_text_note = ""
        note_text = ""  # use for note
        note_text_search = ""  # use for note
        note_tag  = user_input[0:7].lower()
        list_n = []
        list_n2 = []
        for char in user_input:
            if char != " ":
                result_text += char.lower()
            else:
                break
        result_text_note = "".join(user_input[0:11])
        note_text = " ".join(user_devided[1::])
        note_text_search = " ".join(user_devided[2::])
        print(user_input[0:7])
        if user_input.lower() in commands:
            commands[user_input.lower()]()
            if user_input.lower() == "good bye" or user_input.lower() in ["close", "exit"]:
                #commands[user_input.lower()]()
                break
        elif user_input[0:8].lower() in commands:
            commands[user_input[0:8].lower()]()
        elif result_text_note in commands:
            commands[result_text_note]()
            if user_input.lower() == "good bye":
                break
        elif note_tag in commands:
            list_n = user_input.split("<")
            list_n2 = list_n[1].split(">")
            print(list_n2[0], list_n2[1])
            commands[note_tag]()
        elif result_text  in commands:
            if result_text == "note" or result_text == "edit" or result_text == "update" or result_text == "add tag":
                list_n = user_input.split("<")
                list_n2 = list_n[1].split(">")
                
               # commands[re]
            commands[result_text]()
            #print(result_text)
            if result_text in ["close", "exit"]:
                break
        else:
            print(
                "Invalid command. Use 'hello', 'note', 'edit', 'update', 'show note', 'good bye', 'close', 'with tag', 'sort', 'remove', 'add tag', 'search note' or 'exit'"
            )


if __name__ == "__main__":
    main()


