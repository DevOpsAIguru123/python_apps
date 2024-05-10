from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        try:
            # Calculate the result using Python's eval() function
            result = eval(request.form['calculation'])
        except:
            result = "Error"
        return render_template_string(CALCULATOR_HTML, calculation=request.form['calculation'], result=result)
    
    return render_template_string(CALCULATOR_HTML, calculation='', result='0')

CALCULATOR_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tile Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; }
        #calculator {
            width: 320px;
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
        #calc-input, #result {
            width: 100%;
            margin: 10px 0;
            background-color: #f0f0f0;
            padding: 10px;
            display: block;
            border: 1px solid #ccc;
        }
        #result { font-size: 24px; color: #333; }
    </style>
</head>
<body>
    <div id="calculator">
        <h1>Calculator</h1>
        <div id="calc-input">{{ calculation }}</div>
        <div id="result">{{ result }}</div>
        <form method="post">
            <input type="hidden" name="calculation" id="hiddenCalc">
            {% for number in range(10) %}
            <div class="tile" onclick="addToCalculation('{{ number }}')">{{ number }}</div>
            {% endfor %}
            <div class="tile-op" onclick="addToCalculation('+')">+</div>
            <div class="tile-op" onclick="addToCalculation('-')">-</div>
            <div class="tile-op" onclick="addToCalculation('*')">*</div>
            <div class="tile-op" onclick="addToCalculation('/')">/</div>
            <div class="tile-op" onclick="addToCalculation('(')">(</div>
            <div class="tile-op" onclick="addToCalculation(')')">)</div>
            <div class="tile-op" onclick="submitCalculation()">=</div>
            <div class="tile-op" onclick="clearCalculation()">C</div>
        </form>
    </div>
    <script>
        function addToCalculation(char) {
            document.getElementById('hiddenCalc').value += char;
            document.getElementById('calc-input').textContent += char;
        }
        function submitCalculation() {
            document.querySelector('form').submit();
        }
        function clearCalculation() {
            document.getElementById('hiddenCalc').value = '';
            document.getElementById('calc-input').textContent = '';
            document.getElementById('result').textContent = '0';
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
