from flask import Flask, request, jsonify
import configparser
import os
import RPi.GPIO as GPIO
from time import sleep


config = configparser.RawConfigParser()
config.read('config.cfg')
details_dict = dict(config.items('SECURITY'))

api_key = details_dict['api_key']

# setup GPIO
servo_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
print("start")
pwm.start(0)  # Initialisierung

app = Flask(__name__)


def set_angle(angle):
    # Convert angle (0-180) to duty cycle
    pulse_width = 500 + (angle / 180.0) * 2000  # convert angle to microseconds
    duty_cycle = pulse_width / 20000 * 100  # convert to duty cycle percentage (20ms period)
    # Note: 20 ms = 20000microseconds
    pwm.ChangeDutyCycle(duty_cycle)
    sleep(1)  # Allow time for the servo to reach its position
    pwm.ChangeDutyCycle(0)  # Stop sending the PWM signal to avoid jitter


@app.route('/dispense', methods=['POST'])
def dispense():
    print("0")
    set_angle(0)
    #p.ChangeDutyCycle(0)
    sleep(3)
    print("90")
    set_angle(90)
    sleep(3)
    print("180")
    set_angle(180)

    print("dispense")
    if 'X-API-Key' in request.headers:
        request_api_key = request.headers['X-API-Key']
    else:
        return "Missing api key", 401
    if request_api_key != api_key:
        return "Wrong api key", 401

    data = request.json  # Get the JSON data from the incoming request
    # Process the data and perform actions based on the event

    print(data["honey500"])
    return jsonify({'dispensed': data['honey500']}), 200


@app.route('/healthcheck', methods=['GET'])
def health_check():
    # data = request.json # Get the JSON data from the incoming request
    # Process the data and perform actions based on the event

    print("healthcheck")
    return jsonify({'health': 'ok'}), 200


if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(port=5001)  # Dev server
    else:
        print("Use Gunicorn for production")


def on_exit(server):
    # Your cleanup code here
    print("Shutting down gracefully...")
    # e.g., close database connections
    pwm.stop()
    GPIO.cleanup()
    print("Bye!")


# gunicorn hook to run on_exit() when shutting down
on_exit = on_exit
