from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country', 'us')
    api_key = 'eed42de32fa4109e44ba9cd03e2d9967'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={api_key}'

    response = requests.get(url)
    data = response.json()

    if data['cod'] != 200:
        return f'<h1>Error: {data["message"]}</h1>'

    temperature = round((data['main']['temp'] - 273.15) * 9/5 + 32, 2)
    description = data['weather'][0]['description'].capitalize()
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    wind_direction = data['wind']['deg']
    cloudiness = data['clouds']['all']
    icon_code = data['weather'][0]['icon']
    icon_url = f'http://openweathermap.org/img/wn/{icon_code}.png'

    return render_template('weather.html',
        city=city,
        state=state,
        temperature=temperature,
        description=description,
        humidity=humidity,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        cloudiness=cloudiness,
        icon_url=icon_url)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
