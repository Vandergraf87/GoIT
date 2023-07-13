number = int(input("Enter natural number: "))

result = (number % 2 == 0) and "Even" or "Odd"

print(f'The number {number} is {result}.')