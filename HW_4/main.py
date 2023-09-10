
contact_list = dict()

def main():
    while True:
        user_input = input('Please enter something: ')
        if user_input.lower().find('hello') != -1:
            print('How can I help you?')
        elif user_input.lower().find('good bye') != -1 or user_input.lower().find('close') != -1 or user_input.lower().find('exit') != -1:
            print('Good bye!')
            break
        else:
            print(contact_list)
            command_parser(user_input)

def command_parser(input_command):
    if input_command.lower().find('add') != -1:
        add_contact(input_command)
    elif input_command.lower().find('change') != -1:
        change_contact(input_command)
    elif input_command.lower().find('phone') != -1:
        show_phone_number(input_command)
    elif input_command.lower().find('show all') != -1:
        show_all_contact(input_command)

def add_contact(input_text):
    convert_2_list = input_text.split()
    print(convert_2_list)
    contact_list.update({convert_2_list[1]: convert_2_list[2]})

def change_contact(input_text):
    convert_2_list = input_text.split()
    contact_list[convert_2_list[1]] = convert_2_list[2]

def show_phone_number(input_text):
    convert_2_list = input_text.split()
    print(contact_list[convert_2_list[1]])

def show_all_contact(input_text):
    for name, phone in contact_list.items():
        print(f'{name}: {phone}')

main()