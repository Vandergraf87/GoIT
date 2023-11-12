
contact_list = dict()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Invalid command"
    return inner

@input_error
def main():
    while True:
        user_input = input('Please enter something: ')
        if user_input.lower().find('hello') != -1:
            print('How can I help you?')
        elif user_input.lower().find('good bye') != -1 or user_input.lower().find('close') != -1 or user_input.lower().find('exit') != -1:
            print('Good bye!')
            break
        elif user_input.lower().find('add') != -1 or user_input.lower().find('change') != -1 or\
             user_input.lower().find('phone') != -1 or user_input.lower().find('show all') != -1:
            if command_handler(user_input) is None:
                pass 
            else:
                print(command_handler(user_input))
        else:
            print("Invalid command")


@input_error
def command_handler(input_command):
    if input_command.lower().find('add') != -1:
        return add_contact(input_command)
    elif input_command.lower().find('change') != -1:
        return change_contact(input_command)
    elif input_command.lower().find('phone') != -1:
        return show_phone_number(input_command)
    elif input_command.lower().find('show all') != -1:
        return show_all_contact(input_command)

@input_error
def add_contact(input_text):
    convert_2_list = input_text.split()
    contact_list.update({convert_2_list[1]: convert_2_list[2]})

@input_error
def change_contact(input_text):
    convert_2_list = input_text.split()
    contact_list[convert_2_list[1]] = convert_2_list[2]

@input_error
def show_phone_number(input_text):
    convert_2_list = input_text.split()
    if convert_2_list[1] in contact_list:
        return contact_list[convert_2_list[1]]
    else:
        return 'Not found'

@input_error
def show_all_contact(input_text):
    if not contact_list:
        return 'No records found'
    else:
        return "\n".join([f"{name.title()}: {phone}" for name, phone in contact_list.items()])

if __name__ == "__main__":
    main()