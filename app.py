from flask import Flask, render_template, url_for, request, redirect
import pickle
import numpy as np
import requests
app = Flask(__name__)

model = pickle.load(open('crop_dtc.pkl', 'rb'))

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = "24aa99d5fa8b02da318a7232b349fdfc"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None


@app.route('/',methods=['POST','GET'])
def index():
	if request.method == "POST":
		N = int(request.form['N'])
		P = int(request.form['P'])
		K = int(request.form['K'])
		R = float(request.form['R'])
		A = float(request.form['A'])
		city = request.form['C']
		if weather_fetch(city) != None:
			temperature,humidity = weather_fetch(city)
			data = np.array([[N,P,K,temperature,humidity,A,R]])
			my_prediction = model.predict(data)[0]
			return render_template('home.html',ans=my_prediction)

	else:
		return render_template('home.html')

if __name__ == '__main__':
	app.run(debug=False)