from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        expression = request.form['calculation']
        next_input = request.form['next_input']
        full_expression = expression + next_input
        
        if 'submit' in request.form:
            try:
                # Calculate result using eval and clear next_input for new entries
                result = eval(full_expression)
                return_expression = f"{full_expression} = {result}"
            except:
                return_expression = "Error"
            return render_template_string(CALCULATOR_HTML, calculation=return_expression, next_input='')
        elif 'clear' in request.form:
            # Clear the calculation
            return render_template_string(CALCULATOR_HTML, calculation='', next_input='')
        else:
            # Continue adding to the calculation
            return render_template_string(CALCULATOR_HTML, calculation=expression, next_input=next_input)
    else:
        # Initial page load
        return render_template_string(CALCULATOR_HTML, calculation='', next_input='')

CALCULATOR_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; }
        #calculator {
            width: 340px;
            padding: 20px;
            margin: 20px auto;
            border: 2px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .tile, .tile-op {
            padding: 10px;
            margin: 3px;
            text-align: center;
            font-size: 20px;
            border: 1px solid #ccc;
            display: inline-block;
            width: 45px;
            height: 45px;
            line-height: 45px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
        }
        .tile:hover, .tile-op:hover {
            background-color: #e0e0e0;
        }
        .tile:active, .tile-op:active {
            transform: scale(0.95);
        }
        .tile { background-color: #f9f9f9; }
        .tile-op { background-color: #4CAF50; color: white; }
        #calc-input {
            width: 100%;
            margin: 10px 0;
            background-color: #f0f0f0;
            padding: 10px;
            display: block;
            border: 1px solid #ccc;
            font-size: 24px;
            color: #333;
            text-align: right;
        }
    </style>
</head>
<body>
    <div id="calculator">
        <h1>Calculator</h1>
        <div id="calc-input">{{ calculation }}{{ next_input }}</div>
        <form method="post">
            <input type="hidden" name="calculation" value="{{ calculation }}">
            <input type="hidden" name="next_input" id="nextInput">
            {% for number in range(10) %}
            <div class="tile" onclick="addToCalculation('{{ number }}')">{{ number }}</div>
            {% endfor %}
            <div class="tile-op" onclick="addToCalculation('+')">+</div>
            <div class="tile-op" onclick="addToCalculation('-')">-</div>
            <div class="tile-op" onclick="addToCalculation('*')">*</div>
            <div class="tile-op" onclick="addToCalculation('/')">/</div>
            <div class="tile-op" onclick="submitForm('submit')">=</div>
            <div class="tile-op" onclick="submitForm('clear')">C</div>
            <button type="submit" name="action" value="submit" style="display: none;">Submit</button>
            <button type="submit" name="action" value="clear" style="display: none;">Clear</button>
        </form>
    </div>
    <script>
        function addToCalculation(char) {
            document.getElementById('nextInput').value += char;
            document.getElementById('calc-input').textContent += document.getElementById('calc-input').textContent + char;
        }
        function submitForm(action) {
            document.querySelector('form').submit();
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
