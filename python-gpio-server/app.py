from flask import Flask, jsonify, request
from flask_cors import CORS
from dataclasses import dataclass
import gpiozero

app = Flask(__name__)
CORS(app)

PWM_PIN = 4


@dataclass
class ShockState:
    voltage: float | None = None  # 0-1
    state: bool | None = None  # True/False
    frequency: int | None = None  # 0-100_000
    dutyCycle: float | None = None  # 0-1

    def to_dict(self):
        return {
            "voltage": self.voltage,
            "state": self.state,
            "frequency": self.frequency,
            "dutyCycle": self.dutyCycle,
        }


shock_state = ShockState()
shock_state.state = False
shock_state.frequency = 1000
shock_state.dutyCycle = 0.5
shock_state.voltage = 0.0

pwm = gpiozero.PWMLED(
    PWM_PIN,
    frequency=shock_state.frequency,
    initial_value=0.0,
)

def update_pwm():
    pwm.frequency = shock_state.frequency
    pwm.value = shock_state.dutyCycle if shock_state.state else 0.0

@app.route("/api/shock", methods=["GET"])
def home():
    return jsonify(shock_state)


@app.route("/api/shock", methods=["POST"])
def api_data():
    global shock_state

    data = request.get_json()
    new_state = ShockState(**data)

    if new_state.voltage is not None:
        shock_state.voltage = new_state.voltage
    if new_state.state is not None:
        shock_state.state = new_state.state
    if new_state.frequency is not None:
        shock_state.frequency = new_state.frequency
    if new_state.dutyCycle is not None:
        shock_state.dutyCycle = new_state.dutyCycle

    if new_state.frequency or new_state.dutyCycle or new_state.state:
        update_pwm()

    return jsonify(shock_state)


if __name__ == "__main__":
    app.run(port=8000)
