#$user/bin/python3

# include libraries
import requests
import config
from flask import Flask , render_template,request , redirect,jsonify, flash, url_for, Response, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# start flask app
app = Flask(__name__)

# config
app.config.update(
    SECRET_KEY = config.secret_key
)

# configure flask limmiter
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

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    ''' this is function for logouting from server site '''
    logout_user()
    return redirect('login')   
    
@app.route('/login',methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    '''this function return login page'''
    error = None
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["Password"]
        if check(username,password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = '!!!invalid user!!!' 
               
    return render_template('login.html', error=error)

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)    

@app.route("/ok")
def sys_check():
    '''this function tell that falsk server is ok and running!!'''
    ret = {'status':'ok','message':'[+] flask server is running'}
    return jsonify(ret) , 200

@app.route('/',methods=["GET", "POST"])
@login_required
def index(): 

    if request.method == 'POST':
        cityname = request.form["name"]
        # TODO : make this variable jinja for .html template
        print(cityname)

    return render_template('index.html')

@app.route('/photos')
@login_required
def photos_page(): 

    return render_template('photos.html')

@app.route('/contact',methods=["GET", "POST"])
@login_required
def contact():
    ''' this is function for routing to the contact  '''
    if request.method == 'POST':
        return redirect('/')

    else:
        return render_template('contact.html')

#city_name = input()
API_KEY = config.API_KEY

def check(username,password):
    res = False
    if username == config.usernamein and password == config.passwordin:
        res = True
    return res 

# TODO : connect this function to the others and project
def readdata(city_name,API_KEY):
    ''' this is function for collecting datas from api online '''
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

# main first run part
if __name__ == '__main__':
    app.run("0.0.0.0",5000,debug=True)