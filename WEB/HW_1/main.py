from contacts import contacts
from notebook import Note, Notebook
from sorter import sorter


def main():
    def handle_new_contact(phone_book):
        name = input("Enter contact name: ").lower()
        phone = input("Enter phone number: ")
        print(phone_book.add_contact(name, phone))
        phone_book.save_data()

    def handle_change_phone(phone_book):
        name = input("Enter contact name: ").lower()
        phone = input("Enter phone number: ")
        print(phone_book.change_contact(name, phone))
        phone_book.save_data()

    def handle_edit_name(phone_book):
        old_name = input("Enter old contact name: ").lower()
        new_name = input("Enter new contact name: ").lower()
        phone_book.edit_name(old_name, new_name)
        phone_book.save_data()
        print(f"Name updated for {old_name.title()} to {new_name.title()}")

    def handle_delete_contact(phone_book):
        name = input("Enter contact name which you want to delete: ").lower()
        print(phone_book.delete_contact(name))
        phone_book.save_data()

    def handle_search_contact(phone_book):
        query = input("Enter part of contact name: ").lower()
        phone_book.search(query)

    def handle_show_all_contacts(phone_book):
        print(phone_book.show_all())

    def handle_add_address(phone_book):
        name = input("Enter name: ").lower()
        address = input("Enter contact address: ")
        phone_book.add_address(name, address)
        phone_book.save_data()

    def handle_edit_address(phone_book):
        name = input("Enter name: ").lower()
        new_address = input("Enter new contact address: ")
        phone_book.edit_address(name, new_address)
        phone_book.save_data()

    def handle_add_email(phone_book):
        name = input("Enter name: ").lower()
        email = input("Enter contact email: ")
        phone_book.add_email(name, email)
        phone_book.save_data()

    def handle_edit_email(phone_book):
        name = input("Enter name: ").lower()
        old_email = input("Enter old email: ")
        new_email = input("Enter new email: ")
        phone_book.edit_email(name, old_email, new_email)
        phone_book.save_data()

    def handle_add_birthday(phone_book):
        name = input("Enter name: ").lower()
        birthday = input("Enter birthday in format 'YYYY-MM-DD': ")
        phone_book.add_birthday(name, birthday)
        phone_book.save_data()

    def handle_edit_birthday(phone_book):
        name = input("Enter name: ").lower()
        new_birthday = input("Enter new birthday in format 'YYYY-MM-DD': ")
        phone_book.edit_birthday(name, new_birthday)
        phone_book.save_data()

    def handle_upcoming_birthdays(phone_book):
        days = int(input("Enter the number of upcoming days: "))
        upcoming_birthdays = phone_book.find_upcoming_birthdays(days)
        if upcoming_birthdays:
            print("Upcoming Birthdays:")
            for name, days_until_birthday in upcoming_birthdays:
                print(f"{name} ({days_until_birthday} days until their birthday)")
        else:
            print("No upcoming birthdays found.")

    def handle_contacts():
        phone_book = contacts.AddressBook()
        phone_book.load_data()
        while True:
            user_input = input("Enter command: ").lower()

            if user_input == "back":
                return True

            commands = {
                "new contact": handle_new_contact,
                "change phone": handle_change_phone,
                "edit name": handle_edit_name,
                "delete contact": handle_delete_contact,
                "search contact": handle_search_contact,
                "add address": handle_add_address,
                "edit address": handle_edit_address,
                "add email": handle_add_email,
                "edit email": handle_edit_email,
                "add birthday": handle_add_birthday,
                "edit birthday": handle_edit_birthday,
                "upcoming birthday": handle_upcoming_birthdays,
                "show all contacts": handle_show_all_contacts,
                "back or close": "return back"
            }

            if user_input in commands:
                commands[user_input](phone_book)
                
            if user_input == "close":
                break

            if user_input not in commands:
                keys_as_string = "\n".join(commands.keys())
                print(f"Use this commands {keys_as_string}")

    def handle_add_note(notebook):
        note_name = input("Enter note name: ")
        note_text = input("Enter note text: ")
        note = Note(note_name)
        note.edit_text(note_text)
        notebook.add_note(note)
        notebook.save_data()

    def handle_edit_note(notebook):
        note_name = input("Enter note name: ")
        note_text = input("Enter new text: ")
        notebook.edit_note(note_name, note_text)
        notebook.save_data()

    def handle_delete_note(notebook):
        note_name = input("Enter note name: ")
        notebook.delete_note(note_name)
        notebook.save_data()

    def handle_add_tag(notebook):
        note_name = input("Enter note name: ")
        notes = notebook.search_notes_by_name(note_name)
        for note in notes:
            notebook.add_tags(note, [input("Enter tag: ").lower()])
        notebook.save_data()

    def handle_delete_tag(notebook):
        tag = input("Enter tag: ")
        notebook.remove_tag(tag)
        notebook.save_data()

    def handle_search_note_by_tag(notebook):
        tag = input("Enter tag: ")
        print(notebook.search_notes_by_tag(tag))

    def handle_search_note_by_name(notebook):
        name = input("Enter note name: ")
        print(notebook.search_notes_by_name(name))

    def handle_view_notes(notebook):
        print(notebook.view_notes())

    def handle_notes():
        notebook = Notebook()
        notebook.load_data()

        while True:
            user_input = input("Enter command: ").lower()

            if user_input == "back":
                return True

            commands = {
                "add note": handle_add_note,
                "edit note": handle_edit_note,
                "delete note": handle_delete_note,
                "search note name": handle_search_note_by_name,
                "search note by tag": handle_search_note_by_tag,
                "add tag": handle_add_tag,
                "delete tag": handle_delete_tag,
                "view all notes": handle_view_notes,
                "back or close": "return back"
            }

            if user_input in commands:
                commands[user_input](notebook)
                
            if user_input == "close":
                break

            if user_input not in commands:
                keys_as_string = "\n".join(commands.keys())
                print(f"Use this commands {keys_as_string}")

    while True:
        user_input = input("Hello! I am your personal assistant! How can I help you? Choose one option"
                           "(contacts, notes, sorter): ").lower()

        if user_input == "contacts":
            handle_contacts()

        elif user_input == "notes":
            handle_notes()

        elif user_input == "sorter":
            folder_path = input("Enter folder path: ")
            sorter(folder_path)

        elif user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            return False

        else:
            print("invalid command")


if __name__ == "__main__":
    main() 