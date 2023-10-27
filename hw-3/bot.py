from address_book import AddressBook, Record
import pickle

ADDRESS_BOOK_FILE = "address_book.pkl"


# save data
def save_data_to_file(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


# load data
def load_data_from_file(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            if not data:
                return None
            return data
    except (FileNotFoundError, EOFError):
        return None


# empty address book
def create_empty_address_book():
    return AddressBook()


def input_error(func):
    def inner(args, book):
        try:
            return func(args, book)
        except KeyError:
            return "Give me defined contact please."
        except ValueError:
            return (
                "Give me correct command please. "
                "To view all commands enter 'commands'."
            )
        except IndexError:
            return "Give me name please."
    return inner


# command: hello
@input_error
def hello_command(*args):
    return "How can I help you?"


# command: commands
@input_error
def show_commands(*args):
    return (
        "command 'hello': show a welcome message. "
        "format: 'hello'\n"
        "command 'exit': close the bot. "
        "format: 'exit'\n"
        "command 'add': add new contact. number must contain 10 digits. "
        "format: 'add Test 1111111111'\n"
        "command 'change': change a number. number must contain 10 digits. "
        "format: 'change Test 1111111111 2222222222'\n"
        "command 'phone': show a contact. "
        "format: 'phone Test'\n"
        "command 'all': show all contacts. "
        "format: 'all'\n"
        "command 'clear': clear all contacts. "
        "format: 'clear'\n"
        "command 'add-birthday': add birthday to contact. "
        "format: 'add-birthday Test 01.11.2000'\n"
        "command 'show-birthday': show a birthday. "
        "format: 'show-birthday Test'\n"
        "command 'birthdays': shows contacts to congratulate this week. "
        "format: 'birthdays'"
    )


# command: add Test 1111111111 - number must contain 10 digits
@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)

    if record:
        record.add_phone(phone)
        return f"Phone is added to {name}'s record"

    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return f"{name} is added to your book"


# command: change Test 1111111111 2222222222 - number must contain 10 digits
@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)

    record.edit_phone(old_phone, new_phone)
    return f"{name}'s contact is updated"


# command: phone Test
@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return f"No saved contacts for {name}"
    return str(record)


# command: all
@input_error
def show_all(args, book):
    return str(book)


# command: add-birthday Test 01.11.2000
@input_error
def add_birthday(args, book):
    name, date = args
    user = book.find(name)

    if user:
        try:
            user.add_birthday(date)
            return f"Added birth date for {name}"
        except Exception:
            print("Use dd.mm.yyyy format")
    else:
        return (
            f"No user with the name '{name}' found.\n"
            "Add contact first."
        )


# command: show-birthday Test
@input_error
def show_birthday(args, book):
    name = args[0]
    user = book.find(name)

    if not user:
        return f"No saved birthday for {name}"

    birthday = user.birthday

    return str(birthday)


# command: birthdays
@input_error
def get_birthdays_per_week(args, book):
    users = book.get_birthdays_per_week()
    return users


COMMANDS = {
    hello_command: ("hello",),
    add_contact: ("add",),
    change_contact: ("change",),
    show_phone: ("phone",),
    show_all: ("all",),
    add_birthday: ("add-birthday",),
    show_birthday: ("show-birthday",),
    get_birthdays_per_week: ("birthdays",),
    show_commands: ("commands",),
}


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    # use AddressBook
    book = AddressBook()
    print("Welcome to the assistant bot!")
    loaded_book = load_data_from_file(ADDRESS_BOOK_FILE)
    if loaded_book:
        book = loaded_book
        print("Address book is loaded.")

    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            continue
        command, *args = parse_input(user_input)

        if command == "clear":
            book = create_empty_address_book()
            print("Address book is cleared.")
            continue

        if command in ["close", "exit"]:
            save_data_to_file(ADDRESS_BOOK_FILE, book)
            print("Good bye! Address book is saved.")
            break

        command_action = None

        for action, keys in COMMANDS.items():
            if command in keys:
                command_action = action
                break

        if command_action is not None:
            print(command_action(args, book))
        else:
            print("Invalid command. To view all commands enter 'commands'.")


if __name__ == "__main__":
    main()
