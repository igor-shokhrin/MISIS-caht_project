import requests
s_city = "Washington,USA"
city_id = 0
appid = "5da5d9d9d904b8690207d2baa190e04b"
def GetCityId(s_city, appid):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        # print("city:", cities)
        city_id = data['list'][0]['id']
        # print('city_id=', city_id)
        return city_id
    except Exception as e:
        print("Exception (find):", e)
        pass
def WeatherNow(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])
    except Exception as e:
        print("Exception (weather):", e)
        pass
def WeatherToFiveDays(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            print(i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description'])
    except Exception as e:
        print("Exception (forecast):", e)
        pass
s_city_1 = "Moscow"

city_id_1 = GetCityId(s_city_1, appid)
print(s_city_1)
WeatherNow(city_id_1)
WeatherToFiveDays(city_id_1)