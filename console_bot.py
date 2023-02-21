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

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        return self.value == other.value


class Name(Field):
    """Клас --- обов'язкове поле з ім'ям."""

    pass


class Phone(Field):
    """Клас -- необов'язкове поле з телефоном та таких один записів (Record)
    може містити кілька."""

    pass


class Birthday(Field):
    """Клас -- необов'язкове поле з датою народження."""

    pass


class Record:
    """Клас відповідає за логіку додавання/видалення/редагування
    необов'язкових полів та зберігання обов'язкового поля Name."""

    records = {}

    # Забороняємо створювати кілька об'єктів з однаковиси полями Name
    def __new__(cls, name: Name, *args, **kwargs):
        if name.value in cls.records:
            return cls.records[name.value]
        return super().__new__(cls)

    def __init__(
        self,
        name: Name,
        phones: list[Phone] = None,
        birthday: Birthday = None,
    ):

        # якщо об'єк було створено, то припинити роботу конструктора
        if name.value in self.records:
            return
        # інакше запустити конструктор
        self.name = name  # Name --- атрибут ля зберігання об'єкту Name
        self.phones = phones or []
        self.birthday = birthday
        # Додаємо в словник об'єктів новий об'єкт
        self.records[name.value] = self

    def add_phone(self, phone: Phone):
        """Метод додає об'єкт телефон до запису."""

        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        """Метод видаляє об'єкт телефон із запису."""

        self.phones.remove(phone.value)

    def change_phone(self, old_phone: Phone, new_phone: Phone) -> bool:
        """Метод змінює об'єкт телефон в записі на новий."""

        phones_list_str = (phone.value for phone in self.phones)
        if old_phone.value in phones_list_str:
            idx = phones_list_str.index(old_phone.value)
            self.phones[idx] = new_phone
            return True
        return False

    def __iter__(self):
        return iter(self.phones)

    def __str__(self):
        return ", ".join([phone.value for phone in self.phones])


class AddressBook(UserDict):
    """Клас містить логіку пошуку за записами до цього класу."""

    def add_record(self, record: Record):
        """Метод додає запис до списку контактів."""

        self.data[record.name.value] = record

    def __str__(self):
        """метод який представляє дінні у вигляді name: phone, phone, ..."""

        items = [
            f"{k}: {', '.join(str(i) for i in v.phones)}"
            for k, v in self.items()
        ]

        if items:
            return "\n".join(items)
        return "Book is empty"


# ================================= Decorator ================================#


def input_error(func):
    def wrapper(*func_args, **func_kwargs):
        try:
            return func(*func_args, **func_kwargs)
        except KeyError:
            return "Give me a name, please"
        except ValueError:
            return "Give me a phone, please"

    return wrapper


# ================================== handlers ================================#


def hello(*args):
    return "How can I help you?"


def good_bye(*args):
    return "Good bye!"


def undefined(*args):
    return "What do you mean?"


def show_all(*args):
    """Функція-handler показує книгу контактів."""

    return contacts


@input_error
def add_contact(*args):
    """Функція-handler додає телефон до контакту."""

    if not args[0]:
        raise KeyError

    if not args[1]:
        raise ValueError

    name = Name(args[0])
    phone = Phone(args[1])
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)

    return f"I added a nomber {args[1]} to contact {args[0]}"


@input_error
def get_phones(*args):
    """Функція-handler показує телефонні номери відповідного контакту."""

    if not args[0]:
        raise KeyError

    name = Name(args[0])

    phones = Record(name).phones

    if phones:
        return f"{name.value}: " + ", ".join(
            f"{element}" for element in phones
        )


@input_error
def remove_contact(*args):
    """Функція-handler видаляє запис з книги."""

    if not args[0]:
        raise KeyError

    name = Name(args[0])

    del contacts[name.value]

    return f"Contact {name.value} was removed"


@input_error
def change_contact(*args):
    """Функція-handler змінює телефон контакту."""

    if not args[0]:
        raise KeyError

    if not args[1]:
        raise ValueError("Old phone number is required")

    if not args[2]:
        raise ValueError("New phone number is required")

    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])

    if name.value not in contacts:
        return f"Contact {name.value} not found"

    contact_list = contacts[name.value].phones
    for number in contact_list:
        if number == old_phone:
            idx = contact_list.index(number)
            contact_list[idx] = new_phone
            break
        return f"Phone {old_phone.value} not found for {name.value}"

    return f"Contact {name.value} with phone number {old_phone.value} was updated with new phone number {new_phone.value}"


# =============================== handler loader =============================#


def get_handler(*args):
    """Функція викликає відповідний handler."""

    COMMANDS = {
        "hello": hello,
        "add": add_contact,
        "change": change_contact,
        "phones": get_phones,
        "show all": show_all,
        "remove": remove_contact,
        "good bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
    }
    return COMMANDS.get(args[0], undefined)


# ================================ main function =============================#


def main():

    pattern = re.compile(
        r"\b(\.|hello|add|remove|clear number|change|phones|show all|good bye|close|exit)\b"
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

# ================================ Для теста ==================================

rec1 = Record(Name('UserA'), [Phone('1111111111'), Phone('2222222222')])
rec2 = Record(Name('UserB'), [Phone('3333333333'), Phone('5555555555')])
rec3 = Record(Name('UserC'))
rec4 = Record(Name('UserD'), [Phone('1212121212'), Phone('3434343434')])
contacts.add_record(rec1)
contacts.add_record(rec2)
contacts.add_record(rec3)

# =============================================================================


# ================================ main programm =============================#

if __name__ == "__main__":

    main()
