from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
app = Flask(__name__)

# OpenWeatherMap API key
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def convert_epoch_to_time(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%H:%M:%S')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.json.get('city')

    if not city:
        return jsonify({'error': 'Şehir adı gerekli'}), 400
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'tr'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    
        weather_info = {
            'city': data['name'].title(),
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'].title(),
            'wind_speed': data['wind']['speed'],
            'wind_degree': data['wind']['deg'],
            'icon': "https://openweathermap.org/img/wn/" + data['weather'][0]['icon'] + "@2x.png",
            'sunrise': convert_epoch_to_time(data['sys']['sunrise']),
            'sunset': convert_epoch_to_time(data['sys']['sunset'])
        }
        
        return jsonify(weather_info)
    
    except requests.exceptions.HTTPError:
        return jsonify({'error': 'Şehir bulunamadı.Tekrar Deneyiniz'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8000)