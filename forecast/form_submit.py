import forecast
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')


@app.route('/getForecast')
def get_forecast():
    timestamp = request.args.get('timestamp')
    distance_from_shore = request.args.get('distance_from_shore')
    distance_from_port = request.args.get('distance_from_port')
    speed = request.args.get('speed')
    course = request.args.get('course')
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    answer = '{:,}'.format(int(forecast.get_forecast(timestamp, distance_from_shore, distance_from_port, speed, course, lat, lon)))
    return render_template('answer_forecast.html', answer=answer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)