import requests
import config
from flask import Flask , render_template,request , redirect,jsonify, flash, url_for, Response, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)

# config
app.config.update(
    SECRET_KEY = config.secret_key
)

limiter = Limiter(
    app,
    key_func=get_remote_address,
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "%d" % (self.id)


# create some users with ids 1 to 20       
user = User(0)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


city_name = input()
API_KEY = config.API_KEY

def check(username,password):
    res = False
    if username == config.usernamein and password == config.passwordin:
        res = True
    return res 

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

#readdata(city_name,API_KEY)

if __name__ == '__main__':
    app.run("0.0.0.0",5000,debug=True)