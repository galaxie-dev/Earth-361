from flask import Flask, request, jsonify
import requests
from datetime import datetime
import pytz
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#OpenWeatherMap API key
OPENWEATHER_API_KEY = "8f32d7de1d92b311c54557649ab2029b"

# @app.route('/test', methods=['GET'])
# def test():
#     return jsonify({"message": "Flask server is working!"})

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not city and (not lat or not lon):
        return jsonify({"error": "Either city or coordinates must be provided"}), 400
    
    try:
        # Current weather
        if city:
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        else:
            current_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        
        current_response = requests.get(current_url)
        current_data = current_response.json()
        
        if current_response.status_code != 200:
            return jsonify({"error": current_data.get("message", "Failed to fetch weather data")}), current_response.status_code
        
        # Forecast (prediction)
        if city:
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        else:
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        
        if forecast_response.status_code != 200:
            return jsonify({"error": forecast_data.get("message", "Failed to fetch forecast data")}), forecast_response.status_code
        
        # Process timezone and local time
        timezone = pytz.timezone(current_data.get('timezone', 'UTC'))
        local_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
        
        # Process forecast data for next 24 hours
        hourly_forecast = []
        for item in forecast_data['list'][:8]:  # Next 24 hours (3-hour intervals)
            forecast_time = datetime.fromtimestamp(item['dt'], timezone).strftime('%H:%M')
            hourly_forecast.append({
                'time': forecast_time,
                'temp': item['main']['temp'],
                'icon': item['weather'][0]['icon'],
                'description': item['weather'][0]['description']
            })
        
        # Prepare response
        response = {
            'current': {
                'city': current_data['name'],
                'country': current_data['sys']['country'],
                'temp': current_data['main']['temp'],
                'feels_like': current_data['main']['feels_like'],
                'humidity': current_data['main']['humidity'],
                'pressure': current_data['main']['pressure'],
                'wind_speed': current_data['wind']['speed'],
                'wind_deg': current_data['wind']['deg'],
                'weather': current_data['weather'][0]['main'],
                'description': current_data['weather'][0]['description'],
                'icon': current_data['weather'][0]['icon'],
                'visibility': current_data.get('visibility', 'N/A'),
                'clouds': current_data['clouds']['all'],
                'sunrise': datetime.fromtimestamp(current_data['sys']['sunrise'], timezone).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(current_data['sys']['sunset'], timezone).strftime('%H:%M'),
                'timezone': str(timezone),
                'local_time': local_time
            },
            'hourly_forecast': hourly_forecast,
            'daily_forecast': process_daily_forecast(forecast_data['list'], timezone)
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_daily_forecast(forecast_list, timezone):
    daily_data = {}
    
    for item in forecast_list:
        date = datetime.fromtimestamp(item['dt'], timezone).strftime('%Y-%m-%d')
        if date not in daily_data:
            daily_data[date] = {
                'temps': [],
                'icons': [],
                'descriptions': []
            }
        
        daily_data[date]['temps'].append(item['main']['temp'])
        daily_data[date]['icons'].append(item['weather'][0]['icon'])
        daily_data[date]['descriptions'].append(item['weather'][0]['description'])
    
    daily_forecast = []
    for date, data in daily_data.items():
        avg_temp = sum(data['temps']) / len(data['temps'])
        # Get most frequent icon/description for the day
        icon = max(set(data['icons']), key=data['icons'].count)
        description = max(set(data['descriptions']), key=data['descriptions'].count)
        
        daily_forecast.append({
            'date': datetime.strptime(date, '%Y-%m-%d').strftime('%a, %b %d'),
            'avg_temp': round(avg_temp, 1),
            'icon': icon,
            'description': description
        })
    
    return daily_forecast[:5]  # Return next 5 days

if __name__ == '__main__':
    app.run(debug=True)