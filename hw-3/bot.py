from address_book import AddressBook, Record
import pickle


def save_data_to_file(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def load_data_from_file(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            if not data:
                return None
            return data
    except (FileNotFoundError, EOFError):
        return None


def create_empty_address_book():
    return AddressBook()


# decorator
def input_error(func):
    def inner(args, book):
        try:
            return func(args, book)
        except KeyError:
            return "Give me defined contact please."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name please."
    return inner


@input_error
def hello_command(*args):
    return "How can I help you?"


@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)

    if record:
        record.add_phone(phone)
        return f"phone was added to {name}'s record"

    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return f"{name} was added to your book"


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)

    record.edit_phone(old_phone, new_phone)
    return f"{name}'s contact was updated"


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    # if None - no phones
    return str(record)


@input_error
def show_all(args, book):
    return str(book)


@input_error
def add_birthday(args, book):
    name, date = args
    user = book.find(name)

    if user:
        user.add_birthday(date)
        return f"Added birth date for {name}"
    else:
        return (
            f"No user with the name '{name}' found.\n"
            "Add contact first."
        )


@input_error
def show_birthday(args, book):
    name = args[0]
    user = book.find(name)

    if not user:
        return f"No saved birthday for {name}"

    birthday = user.birthday

    return str(birthday)


@input_error
def get_birthdays_per_week(args, book):
    users = book.get_birthdays_per_week()
    return users


# toDo - add birthdays!!!!!!!!!
# map command names to the corresponding functions
COMMANDS = {
    hello_command: ("hello",),
    add_contact: ("add",),
    change_contact: ("change",),
    show_phone: ("phone",),
    show_all: ("all",),
    add_birthday: ("add-birthday",),
    show_birthday: ("show-birthday",),
    get_birthdays_per_week: ("birthdays",),
}


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    # use AddressBook
    book = AddressBook()
    print("Welcome to the assistant bot!")
    loaded_book = load_data_from_file("address_book.pkl")
    if loaded_book:
        book = loaded_book
        print("Address book loaded from file.")

    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            continue
        command, *args = parse_input(user_input)

        if command == "clear":
            book = create_empty_address_book()
            print("Address book cleared.")
            continue

        if command in ["close", "exit"]:
            # toDo add variable for file name !!!!!!!
            save_data_to_file("address_book.pkl", book)
            print("Good bye! Address book saved to file.")
            break

        command_action = None

        for action, keys in COMMANDS.items():
            if command in keys:
                command_action = action
                break

        if command_action is not None:
            print(command_action(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
