from addressbook import AddressBook, Record


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


# add decorator
@input_error
def hello_command(*args):
    return "How can I help you?"


# Example for ValueError
# Enter a command: add testname - without phone
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


# Example for KeyError
# Enter a command: change invalidcontact 12345678 - with incorrect contact
@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)

    record.edit_phone(old_phone, new_phone)
    return f"{name}'s contact was updated"


# Example for IndexError
# Enter a command: phone - without name
@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    # if None - no phones
    return str(record)


@input_error
def show_all(args, book):
    return str(book)


# map command names to the corresponding functions
COMMANDS = {
    hello_command: ("hello",),
    add_contact: ("add",),
    change_contact: ("change",),
    show_phone: ("phone",),
    show_all: ("all",),
}


# command and arguments from user input
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    # use AddressBook
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        # check if the user entered "close" or "exit" to exit
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        command_action = None

        # identify the correct command
        for action, keys in COMMANDS.items():
            if command in keys:
                command_action = action
                break

        # invalid command
        if command_action is not None:
            print(command_action(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
