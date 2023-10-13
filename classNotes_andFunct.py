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


