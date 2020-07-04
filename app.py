import requests
import config

city_name = input()
API_KEY = config.API_KEY

def readdata(city_name,API_KEY):

    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"

    result = requests.get(base_url)

    crood = result.json()['coord']
    weather = result.json()['weather']
    visibility = result.json()['visibility']
    wind = result.json()['wind']
    clouds = result.json()['clouds']
    sys = result.json()['sys']
    timezone = result.json()['timezone']
    cod = result.json()['cod']
    name = result.json()['name']


    if (cod == 200):
        print('lon : ' + str(crood['lon']))
        print('lat : ' + str(crood['lat']))
        #print(weather)
        print('weather main : ' + weather[0]['main'])
        print('weather description : ' + weather[0]['description'])
        print('visibility : ' + str(visibility))
        print('wind speed : ' + str(wind['speed']))
        print('wind deg : ' + str(wind['deg']))
        print('numbers of clouds : ' + str(clouds["all"]))
        print('country : ' + sys['country'])
        print('sunrise : ' + str(sys['sunrise']))
        print('sunset : ' + str(sys['sunset']))
        print('time : ' + str(timezone))
        print('city : ' + str(name))

        tempmanualk = (result.json()['main']['temp'] + result.json()['main']['feels_like'] + result.json()['main'][
            'temp_min'] + result.json()['main']['temp_max']) / 4
        tempmanualc = tempmanualk - 273.15

        pressure = result.json()['main']['pressure']
        humidity = result.json()['main']['humidity']

        print("tempmanualc : " +str(tempmanualc))
        print("pressure : " +str(pressure))
        print("humidity : " +str(humidity))
    else:
        print("error")

readdata(city_name,API_KEY)