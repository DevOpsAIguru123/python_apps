from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        api_key = os.getenv('API_KEY')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
        else:
            weather_data = {'error': 'City not found'}

    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
