from sympy import sympify
from num2words import num2words

def solve_expression(expr):
    try:
        # Step 1: Use sympy to evaluate
        result = sympify(expr)
        if result is None:
            return None, "Unable to solve"

        # Step 2: Convert result to int if possible
        numeric_result = float(result)
        if numeric_result.is_integer():
            numeric_result = int(numeric_result)

        # Step 3: Convert expression and result to words
        expr_words = expression_to_words(expr)
        result_words = num2words(numeric_result)

        # Step 4: Final sentence
        spoken = f"{expr_words} equals {result_words}"
        return numeric_result, spoken

    except Exception as e:
        print(f"[SOLVER ERROR] {e}")
        return None, "Could not evaluate the expression"
        

def expression_to_words(expr):
    # Convert a math expression like 8+4*2 to words
    symbols = {
        '+': 'plus',
        '-': 'minus',
        '*': 'times',
        '/': 'divided by'
    }

    tokens = []
    number = ''
    for char in expr:
        if char.isdigit():
            number += char
        else:
            if number:
                tokens.append(num2words(int(number)))
                number = ''
            tokens.append(symbols.get(char, char))
    if number:
        tokens.append(num2words(int(number)))

    return ' '.join(tokens)
