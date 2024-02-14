from flask import Flask , render_template , url_for
import get_weather

app = Flask(__name__)
metrics = get_weather.get_weather()   
stats_name = ["Condition", "Temperature", "Feels Like","Sunrise","Moonrise","Sunset","Moonset","Illumination"]
try:
    stats = zip(stats_name , metrics)
except TypeError:
    stats = None
@app.route("/")
@app.route("/home")
def weather():
    return render_template("weather.html", stats = stats)   #  weather_stats=weather_stats , weather_desc=weather_desc  )



if __name__ == "__main__":
    app.run(debug=True)