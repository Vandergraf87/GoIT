from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone_number):
        if not self.validate_phone_number(phone_number):
            raise ValueError("Invalid phone number format")
        super().__init__(phone_number)

    @staticmethod
    def validate_phone_number(phone_number):
        return len(phone_number) == 10 and phone_number.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        if not Phone.validate_phone_number(new_phone_number):
            raise ValueError("Invalid phone number format")
        
        found = False
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                found = True
        
        if not found:
            raise ValueError("Phone number not found in the record")
            

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]