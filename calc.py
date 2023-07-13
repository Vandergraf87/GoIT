result = None
operand = 0
operator = ""
wait_for_number = True

while operator != "=":
    if wait_for_number:
        try:
            inputNumber = input("Enter a number: ")
            operand = int(inputNumber)
        except ValueError: 
            print(f"{inputNumber} is not a number. Try again.")
            continue
        
    else:
        operator = input("Enter operator: ")
        if (operator == "+" or operator == "-" or  operator == "*" or operator == "/" or operator == "=") != True:
            print(f"{operator} is not '+' or '-' or '/' or '*'. Try again")
            continue
    wait_for_number = not wait_for_number
    
    if result is None:
        result = operand

    if not wait_for_number:
        if operator == "+":
            result += operand
        elif operator == "-":
            result -= operand
        elif operator == "*":
            result *= operand
        elif operator == "/":
            result /= operand
    
print(f"Result: {result}")