from flask import Flask

from controller.neural_net_controller import neural_net_blueprint
from controller.ragweed_controller import ragweed_blueprint
from controller.weather_factor_controller import weather_factor_blueprint

if __name__ == '__main__':
    app = Flask(__name__)

    app.register_blueprint(neural_net_blueprint)
    app.register_blueprint(ragweed_blueprint)
    app.register_blueprint(weather_factor_blueprint)

    app.run(port=8000)
