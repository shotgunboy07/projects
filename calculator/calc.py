def parse(expression):
    """Parse a simple arithmetic expression into a list of operands and operators.
    
    Args:
        expression : 
                      str: A string representing a simple arithmetic expression, e.g., "3 + 5 * 2".
                      
    Raises:
        ValueError: If the expression contains invalid characters.
        
    Returns:
        list : A list containing operands as floats and operators as strings, e.g., [3.0, '+', 5.0, '*', 2.0].
        
    """
    expression = expression.strip()
   
    for c in expression:
        if c not in "0123456789+-*/(). ":
            raise ValueError(f"Invalid character '{c}' in expression.")
    
    expression = expression.replace('(', ' ( ').replace(')', ' ) ').replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ')
                
    ret = expression.split()
    
    for i in range(len(ret)):
        if ret[i] not in "+-*/()":
            ret[i] = float(ret[i])
            
    return ret
    
def ops(expression):
    """Evaluate a simple arithmetic expression with multiple operands and operators.

    Args:
        expression : user side input ex: "3 + 5 * 2 - 8 / 4"
                     

    Raises:
        ZeroDivisionError: If division by zero is attempted.
        ValueError: If an invalid operator is provided.

    Returns:
        int or float : The result of the arithmetic operation. Type depends on the operands' types.
    """
    # Parse the expression into a list of operands and operators
    expression = parse(expression)
    
    # First pass: handle * and / : Explained in the PPT file given prior to this assignment.
    i = 1
    while i < len(expression) - 1:
        if expression[i] in '*/':
            a = expression[i - 1]
            op = expression[i]
            b = expression[i + 1]
            if op == '*':
                result = a * b
            elif op == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                #You will need this line to raise the ZeroDivisionError if b is 0.
                #Or else, you can just let Python handle it automatically. 
                #This line is just for clarity and educational purpose.
                result = a / b
            expression = expression[:i - 1] + [result] + expression[i + 2:]
        else:
            i += 2

    # Second pass: handle + and -. 
    # Below code blocks are very similar to the first pass. Well, it works properly as expected.
    '''
    
    while i < len(expression) - 1:
        if expression[i] in '+-':
            a = expression[i - 1]
            op = expression[i]
            b = expression[i + 1]
            if op == '+':
                result = a + b
            elif op == '-':
                result = a - b
            expression = expression[:i - 1] + [result] + expression[i + 2:]
        else:
            i += 2
            
    '''
    
    # Don't you see any potential improvements in the second pass? 
    
    
            
            
    
    # Second pass enhanced: You don't need the a / op / b since the operator you would like to process is fixed in the 
    # 1nd position via 0-based indexing. Which is, not only that you don't need the while iteration to find where the operators at,
    # at line 66, but also you don't need the if conditionals for line 67-74.
    # You can directly process the operator at index 1. So, the code can be simplified as follows:
    
    while len(expression) > 1:
        
        if expression[1] == '+':
            result = expression[0] + expression[2]
        elif expression[1] == '-':
            result = expression[0] - expression[2]
        expression = [result] + expression[3:]

    return expression[0]

def calc(expression):
    """ Works for paranthesis input, not like ops(). So, this is a more advanced calculator.
    We reuse the parse() function from above and also the ops() function from above.
    
    The key feature of this function is that this can handle nested parentheses as well.
    
    The basic idea is to find the innermost parentheses, evaluate the expression inside it using ops(),
    and replace the parentheses with the result. Repeat until there are no more parentheses. 
    
    Finding matching parentheses can be tricky, but we can do it by finding the first closing parenthesis and 
    then looking backwards for the corresponding opening parenthesis. This ensures we always evaluate the innermost 
    expression first, which is the correct order of operations. We repeat this process until there are no more 
    parentheses left in the expression.
    
    After all iteratoins, we evaluate the final expression using ops(). The logic is similar to the ops() function above.
    So, in order to comprehend the code below, you should first understand the ops() function above.
    
    
    Args:
        expression : user side input ex: "( 3 + 5 ) * 2 - ( 8 / 4 )"
        
    Raises:
        ValueError: If the expression contains invalid characters or mismatched parentheses.
        ZeroDivisionError: If division by zero is attempted.
        Exception: For any other errors during evaluation.
        
    Returns:
        int or float : The result of the arithmetic operation. Type depends on the operands' types.
    """
    while '(' in expression:
        # Find the innermost right parentheses
        close_idx = expression.index(')')
        # Find the corresponding left parenthesis for the found right parenthesis above.
        open_idx = max(i for i in range(close_idx) if expression[i] == '(')
        # Evaluate the expression inside the parentheses and replace it in the original expression.
        # This line is very similar to the logic in the ops() function above, line 65.
        expression = expression[:open_idx] + str(ops(expression[open_idx + 1:close_idx])) + expression[close_idx + 1:]
    
    #After the while loop, there should be no parentheses left in the expression.
    #So, we can directly evaluate the final expression using ops().
    return ops(expression)
    # End of calc() function
    
# Main program loop
print("eungryee's Summer Project.") 
print( "Calculator : 2025.08.16 ~ 09.08" )
while True:
    user = input("Enter an expression (or 'f' to quit): ")
    if user.lower() == 'f':
        print("Exiting the calculator. Goodbye!")
        break
    else:
        print(f"Parsed: {parse(user)}")
        result = calc(user)
        print(f"Result: {result}")