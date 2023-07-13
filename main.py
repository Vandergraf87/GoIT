result = None
operand = None
operator = None
wait_for_number = True
a = 0
while True:
    if operator != '=':
        if wait_for_number == True:
            try:
                wait_for_number = False
                operand = input("Enter a number: ")
                operand = int(operand)
                if a < 1:
                    result = operand
            except ValueError:
                print(f"{operand} is not a number") 
                wait_for_number = True
            a += 1        
                
        elif wait_for_number == False:
            wait_for_number = True
            operator = input("Enter operator: ")
            
            if operator == '+':
                result = result + operand
           
            elif operator == '-':
                result = result - operand
           
            elif operator == '*':
                result = result * operand
           
            elif operator == '/':
                result = result / operand
          
            elif operator == '=':
                print(operator)
                pass
          
            else:
                print(f"{operator} is not '+' or '-' or '/' or '*'")
                wait_for_number = False
            
    elif operator == '=':
        print(result)
        break