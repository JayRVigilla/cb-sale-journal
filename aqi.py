import requests
from secrets import IQ_AIR_KEY


def get_aqi():
    """ makes request to IQ AIR for local AQI """
    res = requests.get(f"""http://api.airvisual.com/v2/
    city?city=Berkeley&state=California&country=USA&key={IQ_AIR_KEY}""",
                       timeout=1.0).json()
    return res.data.current.pollution[aqius]
