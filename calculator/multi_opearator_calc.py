
def parse_expression(expression):
    # 연산자 우선순위에 따라 괄호를 추가하여 표현식을 파싱합니다.
    expression = expression.replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ').replace('(', ' ( ').replace(')', ' ) ')
    tokens = expression.split()
    return tokens
# parse_expression 함수는 str을 받고, list를 반환함.

def parse_tonum(expression):
    for i in range(len(expression)):
        if expression[i] != '+' and expression[i] != '-' and expression[i] != '*' and expression[i] != '/' and  expression[i] != '(' and expression[i] != ')':
            expression[i] =  float(expression[i])
    return expression
# parse_toint 함수는 list를 받고, list를 반환함.
# parse_toint 함수는 parse_expression 함수의 결과를 받아서, 숫자만 int로 변환함.

#parse함수는 list를 반환함.
def parse(expression):
    return parse_tonum(parse_expression(expression))


## 조심: one_operator_calc 함수는 파싱이 이미 다 된 상태에서 사용해야함.
def one_operator_calc(expression):
    
    for i in range(len(expression)):
        if expression[i] == '+':
            result = expression[i-1] + expression[i+1]
            return result
        elif expression[i] == '-':
            result = expression[i-1] - expression[i+1]
            return result
        elif expression[i] == '*':
            result = expression[i-1] * expression[i+1]
            return result
        elif expression[i] == '/':
            result = expression[i-1] / expression[i+1]
            return result

def multi_operator_calc(expression):
    
    expression = parse(expression)
    
    num_operators = 0
    for i in range(len(expression)):
        if expression[i] == '+' or expression[i] == '-' or expression[i] == '*' or expression[i] == '/':
            num_operators += 1
    
    if num_operators == 0:
        return expression[0]
    
    while num_operators > 0:
        
        i=0
        while i < len(expression) - 1:
            if expression[i] == '*' or expression[i] == '/':
                result = one_operator_calc(expression[i-1:i+2])
                expression[i-1] = result
                del expression[i:i+2]
                num_operators -= 1
            
            else:
                i += 1
            
            if len(expression) == 3:
                return one_operator_calc(expression)
            
        i=0 
        while i < len(expression) - 1:
            if expression[i] == '+' or expression[i] == '-':
                result = one_operator_calc(expression[i-1:i+2])
                expression[i-1] = result
                del expression[i:i+2]
                num_operators -= 1
                
            else:
                i += 1
                
            if len(expression) == 3:
                return one_operator_calc(expression)


def paranthesis_calc(expression):
    
    #input_check(expression)
    
    num_paranthesis = 0
    for i in range(len(expression)):
        if expression[i] == '(' or expression[i] == ')':
            num_paranthesis += 1
            
    while num_paranthesis > 0:
        for i in range(len(expression)):
            if expression[-i-1] == '(':
                start_paranthesis = len(expression) - i - 1
                break
        for i in range(start_paranthesis+1, len(expression)):
            if expression[i] == ')':
                end_paranthesis = i
                break
            
        for i in range(start_paranthesis+1, end_paranthesis):
            is_operator = False
            if expression[i] == '+' or expression[i] == '-' or expression[i] == '*' or expression[i] == '/':
                is_operator = True
                break
        
                
        expression = expression[:start_paranthesis] + str(multi_operator_calc(expression[start_paranthesis+1:end_paranthesis])) + expression[end_paranthesis+1:]
        num_paranthesis -= 2
        return paranthesis_calc(expression)
    return multi_operator_calc(expression)

def input_check(expression):
    # 입력된 수식이 올바른지 확인하는 함수입니다.
    
    # 1: 숫자와 연산자 외의 문자가 포함되어 있는지 확인합니다.
    # a + b 를 걸러냅니다.
    for char in expression:
        if not (char.isdigit() or char in "+-*/()."):
            raise ValueError("잘못된 입력입니다. 숫자와 연산자만 포함되어야 합니다.")
    
    # 2: 괄호의 개수가 맞는지 확인합니다.
    # 1+(2 , 2+3) 등을 걸러냅니다.
    if expression.count('(') != expression.count(')'):
        raise ValueError("괄호의 개수가 맞지 않습니다.")
    
    # 3: 괄호가 짝이 맞는지 확인합니다.
    # )2+3( 등을 걸러냅니다.
    if expression.rfind("(") > expression.find(")"):
        raise ValueError("짝이 맞지 않은 괄호가 있습니다.")
    
    # 4: 0으로 나누는지 확인합니다.
    # 1/0 등을 걸러냅니다.
    if "/0" in expression:
        raise ValueError("0으로 나눌 수 없습니다.")
    
    #5: 괄호로 시작하는지 확인합니다.
    #(1+2) 등을 걸러냅니다.
    if expression[0] == '(' or expression[-1] == ')':
        raise ValueError("괄호로 식 전체를 묶을 수는 없습니다.")
    
    # 6: 연산자가 숫자와 짝이 맞는지 확인합니다. 
    # +3 , 4-7*-3등을 걸러냅니다.
    is_nonum = True
    for i in range(len(expression) - 1):
        if expression[i] == "+" or "-" or "*" or "/" and expression[i+1] == "+" or "-" or "*" or "/":
            is_nonum = False
        
        if expression[0].isdigit() == False or expression[-1].isdigit() == False or is_nonum == False:
            raise ValueError("연산자와 숫자가 짝지어 지지 않습니다.")
        
    return True


print("계산기 ver1.0 - 2025.05.04")
print("사칙연산과 괄호가 들어간 한줄의 수식을 계산할 수 있습니다. 소수점 계산도 가능합니다.")
print("예시: 1.1+2.4*(3-4)/5+6*7-8/9")
print("=" * 50)
print("1 . 이 계산기는 음수 입력을 지원합니다. 다만, 음수를 계산하고 싶으시다면 반드시 괄호를 씌인 채로 쓰셔야 합니다. ")
print("잘못된 예시: 1+2*(-3-4)/5+6*7-8/9")
print("올바른 예시: 1+2*(-3-4)/5+6*7-8/9")
print("=" * 50)
print("2. 이 계산기는 괄호 입력을 지원합니다. 다만, 입력하고자 하는 식의 전체를 괄호로 묶을 수는 없습니다.")
print("잘못된 예시: (2+(4/1))")
print("올바른 예시: 2+(4/1) ")
print("=" * 50)
print("3. 수식의 입력에 만약 잘못된 부분이 있다면, 에러가 발생할 수 있으므로 주의하시기 바랍니다.")
print("잘못된 예시: +4/2 , a+b, 1/0 기타 등등")
print("=" * 50)
print(paranthesis_calc(input("계산할 식을 입력하세요: ")))
    

