from flask import Flask, jsonify, request
from flask_cors import CORS
from dataclasses import dataclass
import gpiozero
from smbus2 import SMBus

app = Flask(__name__)
CORS(app)

PWM_PIN = 4
HW_EN_PIN = 17
VOLTAGE_POT_ADDR = 0x2e


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
pwm.value = 0.0

i2c = SMBus(1) # Pin 2, 3
i2c.write_byte_data(VOLTAGE_POT_ADDR, 0x00, 127)

hw_enable_pin = gpiozero.LED(HW_EN_PIN) # Pin 11
hw_enable_pin.value = 0

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

    if (
        new_state.frequency is not None
        or new_state.dutyCycle is not None
        or new_state.state is not None
    ):
        update_pwm()

    if new_state.state is not None:
        new_voltage_value = int((1 - shock_state.voltage) * 127) & 127
        i2c.write_byte_data(VOLTAGE_POT_ADDR, 0x00, new_voltage_value)

    if new_state.state is not None:
        hw_enable_pin.value = 1 if shock_state.state else 0

    return jsonify(shock_state)


if __name__ == "__main__":
    app.run(port=8000)
