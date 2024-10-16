import requests
from geopy.geocoders import Nominatim

# Function to get the user's location based on input
def get_user_location(): 
    geolocator = Nominatim(user_agent='location_app')
    user_location = None

    while user_location is None:
        # Prompt the user to input their location
        user_input = input('Please enter your location (city, country, etc.): ')
        
        try:
            # Get the location based on the input
            user_location = geolocator.geocode(user_input)
            
            # Check if the location was found
            if user_location is None:
                print("Location not found. Please try again.")
        
        except Exception as e:
            # Handle any errors that occur during geocoding
            print('An error occurred:', e)
            print('Please try again.')

    # Display the user's latitude and longitude
    print('\nYour GPS location:')
    print(f'Location: {user_location}')
    print(f'Latitude: {user_location.latitude}')
    print(f'Longitude: {user_location.longitude}')

    # Return the location object (latitude and longitude)
    return user_location


def get_weather():
    location = get_user_location()
    latitude = location.latitude
    longitude = location.longitude

    url_yr = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}'
    url_smhi = f'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json'

    #Define the headers (including User-Agent)
    headers = {
        'User-Agent': 'YourAppName/1.0 (your.email@example.com)'  # Replace with your app name and email
    }

    # Choose which API to use. For this example, let's use YR:
    response = requests.get(url_yr, headers=headers)

    if response.status_code == 200:
        weather_data = response.json()

        print("\nWeather Forecast Information:")

        first_forecast = weather_data['properties']['timeseries'][0]
        temperature = first_forecast['data']['instant']['details']['air_temperature']
        wind_speed = first_forecast['data']['instant']['details']['wind_speed']
        precipitation = first_forecast['data'].get('next_1_hours', {}).get('details', {}).get('precipitation_amount', 'N/A')

        print(f"Temperature: {temperature}°C")
        print(f"Wind Speed: {wind_speed} m/s")
        print(f"Precipitation (Next 1 Hour): {precipitation} mm")

    else:
        print(f"Error: Failed to retrieve weather data. Status code {response.status_code}")
 

get_weather()
