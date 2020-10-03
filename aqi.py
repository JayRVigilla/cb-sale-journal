import requests
import json
from secrets import IQ_AIR_KEY


# def get_aqi():
#     """ makes request to IQ AIR for local AQI """
#     res = requests.get(f"""http://api.airvisual.com/v2/
#     city?city=Berkeley&state=California&country=USA&key={IQ_AIR_KEY}""",
#                        timeout=1.0).json()
#     return res.data.current.pollution['aqius']

def get_aqi():
    """ makes request to IQ AIR for local AQI """
    res = requests.get(f"""http://api.airvisual.com/v2/nearest_city?key=71d21fba-0115-4854-94b1-60bdea46a3c5""",
                       timeout=1.0).text
    json_to_dict = json.loads(res)
    print(f" \n\n\n ***** json_to_dict is {json_to_dict} ***** \n\n\n")
    print(f" \n\n\n ***** type {type(json_to_dict)} ***** \n\n\n")
    print(f" \n\n\n ***** keys {json_to_dict.keys()} ***** \n\n\n")
    print(f" \n\n\n ***** data is {json_to_dict.get('data')} ***** \n\n\n")
    # return json_to_dict.data.current.pollution['aqius']
    return json_to_dict['data']['current']['pollution']['aqius']
