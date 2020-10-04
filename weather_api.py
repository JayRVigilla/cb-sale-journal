import requests
import json
from secrets import W_API


def get_weather():
    """ makes request to IQ AIR for local AQI """
    res = requests.get(W_API, timeout=1.0).text
    json_to_dict = json.loads(res)
    weather = json_to_dict['weather']
    temps = json_to_dict['main']

    def k_to_f(num):
        """ kelvin to fahrenheit """
        f = (num - 273.15) * 9/5 + 32
        return f

    low = str(k_to_f(temps['temp_min']))
    high = str(k_to_f(temps['temp_max']))
    desc = f"{weather['main']}: {low}°F - {high}°F. {weather['description']}"
    return desc
