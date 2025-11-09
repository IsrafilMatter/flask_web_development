from flask import Flask, render_template, request

app = Flask(__name__)

def infix_to_postfix(infix_expression):
    """
    Convert an infix expression to postfix using the Shunting Yard Algorithm.
    
    Args:
        infix_expression: A string containing the infix expression (e.g., "A + B * C")
    
    Returns:
        A string containing the postfix expression (e.g., "A B C * +")
    """
    # Operator precedence dictionary (higher number = higher precedence)
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }
    
    # Operator associativity (True for left-associative, False for right-associative)
    associativity = {
        '+': True,
        '-': True,
        '*': True,
        '/': True,
        '^': False
    }
    
    output = []
    operator_stack = []
    
    # Remove whitespace and process each token
    tokens = infix_expression.replace(' ', '')
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # If token is an operand (letter or digit), add to output
        if token.isalnum():
            # Handle multi-character operands
            operand = token
            while i + 1 < len(tokens) and tokens[i + 1].isalnum():
                i += 1
                operand += tokens[i]
            output.append(operand)
        
        # If token is an opening parenthesis, push to stack
        elif token == '(':
            operator_stack.append(token)
        
        # If token is a closing parenthesis
        elif token == ')':
            # Pop operators until opening parenthesis is found
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            # Remove the opening parenthesis
            if operator_stack:
                operator_stack.pop()
        
        # If token is an operator
        elif token in precedence:
            # While there's an operator on top of stack with higher precedence
            # or same precedence and left-associative, pop it to output
            while operator_stack and operator_stack[-1] != '(':
                top_op = operator_stack[-1]
                if top_op in precedence:
                    if (precedence[top_op] > precedence[token]) or \
                       (precedence[top_op] == precedence[token] and associativity[token]):
                        output.append(operator_stack.pop())
                    else:
                        break
                else:
                    break
            # Push current operator to stack
            operator_stack.append(token)
        
        i += 1
    
    # Pop all remaining operators from stack to output
    while operator_stack:
        output.append(operator_stack.pop())
    
    # Join output with spaces for readability
    return ' '.join(output)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works', methods=['GET', 'POST'])
def works():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()
    return render_template('touppercase.html', result=result)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/areaOfCircle', methods=['GET', 'POST'])
def area_of_circle():
    area = None
    if request.method == 'POST':
        try:
            radius = float(request.form.get('radius', '0'))
            if radius >= 0:
                area = 3.141592653589793 * radius * radius
        except ValueError:
            area = None
    return render_template('area_circle.html', area=area)

@app.route('/areaOfTriangle', methods=['GET', 'POST'])
def area_of_triangle():
    area = None
    if request.method == 'POST':
        try:
            base = float(request.form.get('base', '0'))
            height = float(request.form.get('height', '0'))
            if base >= 0 and height >= 0:
                area = 0.5 * base * height
        except ValueError:
            area = None
    return render_template('area_triangle.html', area=area)

@app.route('/infixToPostfix', methods=['GET', 'POST'])
def infix_to_postfix_converter():
    postfix_result = None
    if request.method == 'POST':
        infix_expression = request.form.get('infixExpression', '').strip()
        if infix_expression:
            try:
                postfix_result = infix_to_postfix(infix_expression)
            except Exception as e:
                postfix_result = f"Error: {str(e)}"
    return render_template('infix_to_postfix.html', postfix_result=postfix_result)

if __name__ == "__main__":
    app.run(debug=True)
