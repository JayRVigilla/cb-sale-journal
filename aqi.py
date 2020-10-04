import requests
import json
from secrets import IQ_AIR_API


def get_aqi():
    """ makes request to IQ AIR for local AQI """
    res = requests.get(IQ_AIR_API, timeout=1.0).text
    json_to_dict = json.loads(res)
    return json_to_dict['data']['current']['pollution']['aqius']
