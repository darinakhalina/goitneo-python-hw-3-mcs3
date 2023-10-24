def hello_command(*args):
    return "How can I help you?"


def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."


def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        return f"Contact with '{name}' name is not found."


def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        return f"Contact with '{name}' name is not found."


def show_all(args, contacts):
    all_contacts = []
    for name, phone in contacts.items():
        all_contacts.append(f"{name} - {phone}")
    return "\n".join(all_contacts)


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
    # initializing an empty dictionary for contacts
    contacts = {}
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
            print(command_action(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
