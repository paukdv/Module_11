from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, new_value):
        self.value = new_value 

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.is_valid_phone(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid phone number format")
        
    def _is_valid_phone(self, phone):
        if phone.isdigit() and  len(phone) == 10:
            return True
        return False

class Birthday(Field):
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.is_valid_birthday(new_value):
            self._value = new_value
        else:
            raise ValueError("Invalid birthday format")
        
    def is_valid_birthday(self, birthday):
        try:
            day, month, year = birthday.split('.')
            day = int(day)
            month = int(month)
            year = int(year)
            if 1 <= day <= 31 and 1 <= month <= 12:
                return True
        except (ValueError, AttributeError):
            return False
         
class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.birthday = birthday
        if phone:
            self.phones = []
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()  
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            return (next_birthday - today).days
        else:
            return None          
                
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n=5):
        records = list(self.data.values())
        total_records = len(records)
        current_index = 0

        while current_index < total_records:
            end_index = min(current_index + n, total_records)
            yield records[current_index:end_index]
            current_index += n