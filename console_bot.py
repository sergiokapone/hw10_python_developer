import re
from collections import UserDict

# ================================== Classes =================================#


"""
- Записи <Record> у <AddressBook> зберігаються як значення у словнику.
  В якості ключів використовується значення <Record.name.value>.
- <Record> зберігає об'єкт <Name> в окремому атрибуті.
- <Record> зберігає список об'єктів <Phone> в окремому атрибуті.
- <Record> реалізує методи додавання/видалення/редагування об'єктів <Phone>.
- <AddressBook> реалізує метод <add_record>, який додає <Record> у <self.data>.

"""


class Field:
    """Клас є батьківським для всіх полів, у ньому реалізується логіка,
    загальна для всіх полів."""

    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"{self.value}"


class Name(Field):
    """Клас --- обов'язкове поле з ім'ям."""

    pass


class Phone(Field):
    """Клас -- необов'язкове поле з телефоном та таких один записів (Record)
    може містити кілька."""

    def validate(self):
        if len(str(self.value)) != 10:
            return False


class Record:
    """Клас відповідає за логіку додавання/видалення/редагування
    необов'язкових полів та зберігання обов'язкового поля Name."""

    records = {}

    # Забороняємо створювати кілька об'єктів з однаковиси полями Name
    def __new__(cls, name: Name):
        if name.value in cls.records:
            return cls.records[name.value]
        return super().__new__(cls)

    @classmethod
    def is_exist(cls, name: Name) -> bool:
        if name.value in cls.records:
            return True
        return False

    def __init__(self, name: Name):
        if name.value in self.records:
            return
        self.name = name
        self.phones = []
        self.records[name.value] = self

    def add_phone(self, *phones: list[Phone]):
        """Додає номери телефонів до списку записів."""

        for phone in phones:
            if phone not in self.phones:
                self.phones.append(phone)

    def update_phone(self, old_phone: str, new_phone: str) -> bool:
        """Змінює номер телефону у записі зі старим номером old_number
        на новий номер new_number."""

        for phone in self.phones:
            if phone.value == old_phone.value:
                phone.value = new_phone.value
                return True
        return False

    def remove_phone(self, *phones: Phone):
        """Видаляє телефони з запису."""
        for phone in phones:
            if phone in self.phones:
                self.phones.remove(phone)

    def edit_record(self, name: Name = None, phones: list[Phone] = None):
        """Редагує запис."""

        if name:
            self.name.value = name
        if phones:
            self.phones = phones

    def get_phones(self):
        return list(self.phones)

    def __str__(self):
        return f"{self.name.value}: {', '.join(map(str, self.phones))}"


class AddressBook(UserDict):
    """Клас містить логіку пошуку за записами до цього класу."""

    def __init__(self):
        self.data = {}

    def search_by_name(self, name: str) -> list[Phone]:
        """Шукає номери контакту."""
        return self.data.get(name, [])

    def add_record(self, record: Record):
        """Додає запис до списку контактів."""

        name = record.name.value  # name: str
        if name in self.data:
            self.data[name].add_phone(*record.phones)
        else:
            self.data[name] = record

    def remove_record(self, record: Record):
        """Видаляє запис зі списку контактів."""

        name = record.name.value  # name: str
        if name in self.data:
            del self.data[name]

    def __str__(self):
        result = []
        for record in self.data.values():
            result.append(str(record))
        return "\n".join(result)


# ================================= Decorator ================================#


def input_error(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"<{args[0]}> does not appear in list"
        except ValueError:
            return "Give me a name and phone, please"

    return wrapper


# ================================== handlers ================================#


def hello(*args):
    return "How can I help you?"


def good_bye(*args):
    return "Good bye!"


def undefined(*args):
    return "What do you mean?"


@input_error
def remove_contact(*args):
    name = Name(args[0])
    if Record.is_exist(name):
        contacts.remove_record(Record(name))
        return f"Contact {name} was removed"
    raise KeyError


def show_all(*args):
    if contacts.data:
        return contacts
    return "Contact list is empty"


def get_phone(*args):
    name = Name(args[0])
    if Record.is_exist(name):
        return contacts.search_by_name(args[0])
    return f"Contact {name} not found in the list"


@input_error
def clear_number(*args):
    """Функція видаляє контакт з книги."""

    name = Name(args[0])
    phone = Phone(args[1])

    if phone.validate() is False:
        raise ValueError("Телефонный номер має бути десятизначним числом")

    user = Record(name)
    user.remove_phone(phone)
    return f"Phone '{phone}' was removed."


# @input_error
def add_contact(*args):
    """Функція додає новый контакт в адресну книгу."""

    if not args[0]:
        raise ValueError("Ім'я не має бути порожнім")

    name = Name(args[0])
    phone = Phone(args[1])

    if phone.validate() is False:
        raise ValueError("Телефонний номер має бути десятизначним числом")

    if phone.value in Record(name).get_phones():
        return f"Number {args[1]} already in contact list"

    user = Record(name)
    user.add_phone(phone)
    contacts.add_record(user)

    return f"Contact '{name}' added to the address book."


@input_error
def change_contact(*args):
    if args[0] and args[1] and args[2]:
        name = Name(args[0])
        if Record.is_exist(name):
            phone1 = Phone(args[1])
            phone2 = Phone(args[2])
            user = Record(name)
            user.update_phone(phone1, phone2)
            return f"I changed contact for {name}"
        else:
            return f"{name} is not in list"
    else:
        raise ValueError


# =============================== handler loader =============================#


def get_handler(*args):
    COMMANDS = {
        "hello": hello,
        "add": add_contact,
        "change": change_contact,
        "phone": get_phone,
        "show all": show_all,
        "clear number": clear_number,
        "remove": remove_contact,
        "good bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
    }
    return COMMANDS.get(args[0], undefined)


# ================================ main function =============================#


def main():

    pattern = re.compile(
        r"\b(\.|hello|add|remove|clear number|change|phone|show all|good bye|close|exit)\b"
        r"(?:\s+([a-zA-Z]+))?"
        r"(?:\s+(\d{10}))?"
        r"(?:\s+(\d{10})?)?",
        re.IGNORECASE,
    )

    while True:

        # waiting for nonempty input
        while True:
            inp = input(">>> ").strip()
            if inp == "":
                continue
            break

        text = pattern.search(inp)

        params = (
            tuple(
                map(
                    # Made a commands to be a uppercase
                    lambda x: x.lower() if text.groups().index(x) == 0 else x,
                    text.groups(),
                )
            )
            if text
            else (None, 0, 0)
        )
        handler = get_handler(*params)
        response = handler(*params[1:])
        if inp.strip() == ".":
            return
        print(response)
        if response == "Good bye!":
            return


contacts = AddressBook()  # Global variable for storing contacts


# ================================ main programm =============================#

if __name__ == "__main__":

    name = Name("Sergiy")

    # Sergiy = Record(name)
    # Sergiy.add_phone(Phone("0123456789"))
    # Sergiy.add_phone(Phone("1111111111"))
    # contacts.add_record(Sergiy)
    # print(Record(name).get_phones())
    # # print(contacts)
    main()
