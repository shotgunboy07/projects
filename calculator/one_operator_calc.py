## a+b 형 계산기 

user_input = input("계산할 식을 입력하세요 (예: 1+2): ")
for i in range(len(user_input)):
    if user_input[i] == '+':
        a = int(user_input[:i])
        b = int(user_input[i+1:])
        result = a + b
        print(f"{a} + {b} = {result}")
        break
    elif user_input[i] == '-':
        a = int(user_input[:i])
        b = int(user_input[i+1:])
        result = a - b
        print(f"{a} - {b} = {result}")
        break
    elif user_input[i] == '*':
        a = int(user_input[:i])
        b = int(user_input[i+1:])
        result = a * b
        print(f"{a} * {b} = {result}")
        break
    elif user_input[i] == '/':
        a = int(user_input[:i])
        b = int(user_input[i+1:])
        result = a / b
        print(f"{a} / {b} = {result}")
        break