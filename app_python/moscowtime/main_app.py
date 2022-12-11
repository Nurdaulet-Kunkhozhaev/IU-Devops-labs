from datetime import datetime

import pytz
from flask import Flask, render_template, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)


@app.route('/')
def moscow_time():
    t_zone = pytz.timezone('Europe/Moscow')
    time_now = datetime.now(t_zone)  # current date and time in timezone = t_zone
    formatted_time = time_now.strftime("%H:%M:%S")
    with open('./access.log', 'a') as file:
        file.write(formatted_time + '\n')
    return render_template("moscow_timezone.html", time=formatted_time)


@app.route('/visits')
def show_visits():
    with open('./access.log', 'r') as file:
        return '<div>'.join(file.readlines())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
