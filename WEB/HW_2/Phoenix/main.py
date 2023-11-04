from contacts.contacts import AddressBook
from notebook.notebook import Notebook, Note
from sorter.sorter import sorter
from abc import ABC, abstractmethod

class MyBaseClass(ABC):

    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_notes(self, notes):
        pass

    @abstractmethod
    def display_help(self):
        pass

    @abstractmethod
    def get_user_input(self, prompt):
        pass

    @abstractmethod
    def show_message(self, message):
        pass

    @abstractmethod
    def run(self):
        pass

class ConsoleInterface(MyBaseClass):
    def __init__(self):
        self.phone_book = AddressBook()
        self.notebook = Notebook()

    def display_contacts(self):
        self.phone_book.show_all()
        
    def display_notes(self, notes):
        for note in notes:
            print(f"Title: {note.name}")
            print(f"Text: {note.text}")
            print(f"Tags: {', '.join(note.tags)}")
        print(f"Tags: {','.join(self.tag_dictionary.keys())}")

    def display_help(self):
        print("\nContacts Menu:")
        print("1. Display Contacts")
        print("2. Add Contact")
        print("3. Edit Contact Phone")
        print("4. Edit Contact Name")
        print("5. Delete Contact")
        print("6. Search Contact")
        print("7. Add Contact Address")
        print("8. Add Contact Email")
        print("9. Edit Contact Address")
        print("10. Edit Contact Email")
        print("11. Add Contact Birthday")
        print("12. Edit Contact Birthday")
        print("13. Upcoming birthdays")
        print("14. Quit Contacts Menu")
        print("\nNotes Menu:")
        print("1. Add Note")
        print("2. Edit Note")
        print("3. Delete Note")
        print("4. Search Note Name")
        print("5. Add Tag")
        print("6. Search Note by Tag")
        print("7. Delete Tag")
        print("8. Display All Notes")
        print("9. Close Notes")

    def get_user_input(self, prompt):
        return input(prompt)

    def show_message(self, message):
        print(message)

    def handle_contacts_actions(self):
        while True:
            print("\nContacts Menu:")
            print("1. Display Contacts")
            print("2. Add Contact")
            print("3. Edit Contact Phone")
            print("4. Edit Contact Name")
            print("5. Delete Contact")
            print("6. Search Contact")
            print("7. Add Contact Address")
            print("8. Add Contact Email")
            print("9. Edit Contact Address")
            print("10. Edit Contact Email")
            print("11. Add Contact Birthday")
            print("12. Edit Contact Birthday")
            print("13. Upcoming birthdays")
            print("14. Quit Contacts Menu")

            option_select = input("Please select an option: ")

            if option_select == "1":
                self.display_contacts()

            elif option_select == "2":
                name = input("Enter contact name: ").lower()
                phone = input("Enter phone number: ")
                self.phone_book.add_contact(name, phone)
                self.phone_book.save_data()

            elif option_select == "3":
                name = input("Enter contact name to edit: ").lower()
                new_phone = input("Enter new phone number: ")
                self.phone_book.change_contact(name, new_phone)
                self.phone_book.save_data()

            elif option_select == "4":
                name = input("Enter contact name to edit: ").lower()
                new_name = input("Enter new contact name: ")
                self.phone_book.edit_name(name, new_name)
                self.phone_book.save_data()

            elif option_select == "5":
                name = input("Enter contact name to delete: ").lower()
                print(self.phone_book.delete_contact(name))
                self.phone_book.save_data()

            elif option_select == "6":
                query = input("Enter part of contact name: ").lower()
                self.phone_book.search(query)

            elif option_select == "7":
                name = input("Enter name: ").lower()
                address = input("Enter contact address: ")
                self.phone_book.add_address(name, address)
                self.phone_book.save_data()

            elif option_select == "8":
                name = input("Enter name: ").lower()
                email = input("Enter contact email: ")
                self.phone_book.add_email(name, email)
                self.phone_book.save_data()

            elif option_select == "9":
                name = input("Enter name: ").lower()
                new_address = input("Enter new contact address: ")
                self.phone_book.edit_address(name, new_address)
                self.phone_book.save_data()

            elif option_select == "10":
                name = input("Enter name: ").lower()
                old_email = input("Enter old email: ")
                new_email = input("Enter new email: ")
                self.phone_book.edit_email(name, old_email, new_email)
                self.phone_book.save_data()

            elif option_select == "11":
                name = input("Enter name: ").lower()
                birthday = input("Enter birthday in format 'YYYY-MM-DD': ")
                self.phone_book.add_birthday(name, birthday)
                self.phone_book.save_data()

            elif option_select == "12":
                name = input("Enter name: ").lower()
                new_birthday = input("Enter new birthday in format 'YYYY-MM-DD': ")
                self.phone_book.edit_birthday(name, new_birthday)
                self.phone_book.save_data()

            elif option_select == "13":
                days = int(input("Enter the number of upcoming days: "))
                upcoming_birthdays = self.phone_book.find_upcoming_birthdays(days)
                if upcoming_birthdays:
                    print("Upcoming Birthdays:")
                    for name, days_until_birthday in upcoming_birthdays:
                        print(f"{name} ({days_until_birthday} days until their birthday)")
                else:
                    print("No upcoming birthdays found.")

            elif option_select == "14":
                break

            else:
                print("Invalid option. Please select a valid option.")

    def handle_notes_action(self):
        while True:
            print("\nNotes Menu:")
            print("1. Add Note")
            print("2. Edit Note")
            print("3. Delete Note")
            print("4. Search Note Name")
            print("5. Add Tag")
            print("6. Search Note by Tag")
            print("7. Delete Tag")
            print("8. Display All Notes")
            print("9. Close Notes")

            option_select = input("Please select an option: ")

            if option_select == "1":
                note_name = input("Enter note name: ")
                note_text = input("Enter note text: ")
                note = Note(note_name)
                note.edit_text(note_text)
                self.notebook.save_data()

            elif option_select == "2":
                note_name = input("Enter note name: ")
                note_text = input("Enter new text: ")
                self.notebook.edit_note(note_name, note_text)
                self.notebook.save_data()

            elif option_select == "3":
                note_name = input("Enter note name: ")
                self.notebook.delete_note(note_name)
                self.notebook.save_data()

            elif option_select == "4":
                name = input("Enter note name: ")
                print(self.notebook.search_notes_by_name(name))

            elif option_select == "5":
                note_name = input("Enter note name: ")
                notes = self.notebook.search_notes_by_name(note_name)
                for note in notes:
                    self.notebook.add_tags(note, [input("Enter tag: ").lower()])
                self.notebook.save_data()

            elif option_select == "6":
                tag = input("Enter tag: ")
                print(self.notebook.search_notes_by_tag(tag))

            elif option_select == "7":
                tag = input("Enter tag: ")
                self.notebook.remove_tag(tag)
                self.notebook.save_data()

            elif option_select == "8":
                self.display_notes(self.notebook)

            elif option_select == "9":
                break

    def run(self):
        while True:
            user_input = self.get_user_input("Hello! How can I help you? (contacts, notes, sorter, exit): ").lower()

            if user_input == "contacts":
                self.handle_contacts_actions()

            elif user_input == "notes":
                self.handle_notes_action()

            elif user_input == "sorter":
                folder_path = input("Enter folder path: ")
                self.sorter(folder_path)

            elif user_input == "help":
                self.display_help()

            elif user_input in ["good bye", "close", "exit"]:
                self.show_message("Good bye!")
                return False

            else:
                self.show_message("Invalid command")

if __name__ == "__main__":
    ui = ConsoleInterface()
    ui.run()