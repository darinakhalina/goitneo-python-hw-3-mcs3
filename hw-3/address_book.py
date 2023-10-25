from collections import UserDict, defaultdict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("The number must contain 10 digits.")
        super().__init__(value)

    def __eq__(self, other):
        return self.value == other.value


class Birthday(Field):
    def __init__(self, value):
        super().__init__(datetime.strptime(value, "%d.%m.%Y").date())

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        phone = Phone(phone)
        if phone in self.phones:
            self.phones.remove(phone)

    def find_phone(self, phone_number):
        phone = None
        for p in self.phones:
            if p.value == phone_number:
                phone = p
                break
        return phone

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone:
            phone.value = new_phone

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def __str__(self):
        result = (
            f"Contact name: {self.name.value}, phones: "
            f"{'; '.join(p.value for p in self.phones)}"
        )

        if self.birthday:
            result += f". Birthday {str(self.birthday)}"
        else:
            result += "."

        return result


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name] if name in self.data else None

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)

    def get_birthdays_per_week(self):
        users = self.data.values()
        birthdays = defaultdict(list)
        today = datetime.today().date()

        for user in users:
            name = user.name.value
            birthday = user.birthday.value
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(
                    year=today.year + 1
                )

            # if the day of the week is Saturday
            if birthday_this_year.weekday() == 5:
                # moves birthday to the following Monday
                birthday_this_year += timedelta(days=2)
            # if the day of the week is Sunday
            elif birthday_this_year.weekday() == 6:
                # moves birthday to the following Monday
                birthday_this_year += timedelta(days=1)

            delta_days = (birthday_this_year - today).days
            if delta_days > 0 and delta_days <= 7:
                birthdays[birthday_this_year].append(name)

        if len(birthdays) == 0:
            print("No birthdays found")

        # sort birthdays
        sorted_birthdays = sorted(birthdays.keys())

        result = ""
        for day in sorted_birthdays:
            result += f"{day.strftime('%A')}: {', '.join(birthdays[day])}\n"

        return result

    def __str__(self):
        # add if len = 0 no contacts
        result = ""
        for name in sorted(self.data.keys()):
            result += str(self.data[name]) + "\n"

        return result.rstrip()


def main():
    try:
        # Створення нової адресної книги
        book = AddressBook()

        # Створення запису для John
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
        # Додавання дня народження для John
        john_record.add_birthday("25.10.2000")

        # Додавання запису John до адресної книги
        book.add_record(john_record)

        # Створення та додавання нового запису для Jane
        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        # Додавання дня народження для Jane
        jane_record.add_birthday("27.10.2001")
        book.add_record(jane_record)

        # Виведення всіх записів у книзі
        for name, record in book.data.items():
            print(record)

        # Знаходження та редагування телефону для John
        john = book.find("John")
        john.edit_phone("1234567890", "1112223333")

        print(john)

        # Пошук конкретного телефону у записі John
        found_phone = john.find_phone("5555555555")
        # Виведення: John: 5555555555
        print(f"{john.name}: {found_phone}")

        # Виведення ДН на тиждень
        result = book.get_birthdays_per_week()
        print(result)

        # Видалення запису Jane
        book.delete("Jane")

        # Виведення всіх записів у книзі
        # після видалення запису Jane та оновлення запису John
        for name, record in book.data.items():
            print(record)

    except Exception as e:
        print(f'An error occurred: {str(e)}')


if __name__ == "__main__":
    main()
