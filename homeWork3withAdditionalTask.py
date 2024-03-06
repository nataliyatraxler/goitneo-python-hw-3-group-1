import pickle
from datetime import datetime, timedelta

class Birthday:
    def __init__(self, date):
        self.date = date

class Record:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone, birthday=None):
        if not self._validate_phone(phone):
            return "Invalid phone number format. Phone number must be 10 digits long and contain only digits."

        if birthday:
            if not self._validate_birthday(birthday):
                return "Invalid birthday format. Use: DD-MM-YYYY"

        contact = {"name": name, "phone": phone, "birthday": birthday}
        self.contacts.append(contact)
        return "Contact added."

    def add_birthday(self, name, birthday):
        for contact in self.contacts:
            if contact["name"] == name:
                if self._validate_birthday(birthday):
                    contact["birthday"] = birthday
                    return "Birthday added for the contact."
                else:
                    return "Invalid birthday format. Use: DD-MM-YYYY"
        return "Contact not found."

    def change_phone(self, name, new_phone):
        for contact in self.contacts:
            if contact["name"] == name:
                if self._validate_phone(new_phone):
                    contact["phone"] = new_phone
                    return f"Phone number updated for {contact['name']}."
                else:
                    return "Invalid phone number format. Phone number must be 10 digits long and contain only digits."
        return "Contact not found."

    def show_phone(self, name):
        for contact in self.contacts:
            if contact["name"] == name:
                return f"Phone number for {name}: {contact['phone']}"
        return "Contact not found."

    def show_birthday(self, name):
        for contact in self.contacts:
            if contact["name"] == name:
                return f"Birthday for {name}: {contact.get('birthday', 'N/A')}"
        return "Contact not found."

    def show_all_contacts(self):
        if not self.contacts:
            return "No contacts found."

        for contact in self.contacts:
            print(f"Name: {contact['name']}, Phone: {contact['phone']}, Birthday: {contact.get('birthday', 'N/A')}")

    def get_birthdays_per_week(self):
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        birthdays = []

        for contact in self.contacts:
            if "birthday" in contact and self._validate_birthday(contact["birthday"]):
                try:
                    contact_birthday = datetime.strptime(contact["birthday"], "%d-%m-%Y").date()
                    contact_birthday = contact_birthday.replace(year=today.year)
                    if contact_birthday < today:
                        contact_birthday = contact_birthday.replace(year=today.year + 1)
                except ValueError:
                    print(f"Invalid birthday format for {contact['name']}. Skipping.")
                    continue
                if today < contact_birthday <= next_week:
                    birthdays.append((contact["name"], contact_birthday))

        return birthdays

    def _validate_phone(self, phone):
        return len(phone) == 10 and phone.isdigit()

    def _validate_birthday(self, birthday):
        try:
            datetime.strptime(birthday, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.contacts = pickle.load(file)
            print("Address book loaded successfully.")
        except FileNotFoundError:
            print("File not found. Creating a new address book.")
            self.contacts = []

class AddressBook(Record):
    pass

def parse_input(user_input):
    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]
    return command, args

def main():
    book = AddressBook()
    book.load_from_file("address_book.pkl")
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Saving address book...")
            book.save_to_file("address_book.pkl")
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            if len(args) != 2:
                print("Invalid number of arguments. Usage: add [name] [phone]")
            else:
                print(book.add_contact(*args))
        elif command == "add-birthday":
            if len(args) != 2:
                print("Invalid number of arguments. Usage: add-birthday [name] [birthday]")
            else:
                print(book.add_birthday(*args))
        elif command == "change":
            if len(args) != 2:
                print("Invalid number of arguments. Usage: change [name] [new_phone]")
            else:
                print(book.change_phone(*args))
        elif command == "all":
            if len(args) != 0:
                print("Invalid number of arguments. Usage: all")
            else:
                book.show_all_contacts()
        elif command == "phone":
            if len(args) != 1:
                print("Invalid number of arguments. Usage: phone [name]")
            else:
                print(book.show_phone(*args))
        elif command == "show-birthday":
            if len(args) != 1:
                print("Invalid number of arguments. Usage: show-birthday [name]")
            else:
                print(book.show_birthday(*args))
        elif command == "birthdays":
            if len(args) != 0:
                print("Invalid number of arguments. Usage: birthdays")
            else:
                upcoming_birthdays = book.get_birthdays_per_week()
                if upcoming_birthdays:
                    print("Colleagues to congratulate on their birthdays next week:")
                    for name, birthday in upcoming_birthdays:
                        print(f"{name}: {birthday.strftime('%Y-%m-%d')}")
                else:
                    print("No birthdays coming up next week.")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

