# Домашнє завдання №10


- Записи `Record` у `AddressBook` зберігаються як значення у словнику.
  В якості ключів використовується значення `Record.name.value`.
- `Record` зберігає об'єкт <Name> в окремому атрибуті.
- `Record` зберігає список об'єктів `Phone` в окремому атрибуті.
- `Record` реалізує методи додавання/видалення/редагування об'єктів `Phone`.
- `AddressBook` реалізує метод `add_record`, який додає <Record> у `self.data`.


## Комвнди
- `hello` --- чат вітається.
- `add` --- чат додає ім'я і телефон, приклад `add Sergiy 0936564532`.
- `chage` --- чат змінює номер для відповідного контакту, приклад `change Sergiy 0936564532 0634564545`.
- `phones` --- чат виводить номери телефонів контакту, приклад `phone Sergiy`.
- `show all`--- чат показує усі контакти та їх номери, приклад `show all`
- `remove` --- чат видаляє запис з вказаним іменем, приклад `remove Sergiy`.
- `good bye`, `good`, `exit` --- чат прощається і завершує роботу.
- `.` --- чат перериває свою роботу без попереджень.


```
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
```
