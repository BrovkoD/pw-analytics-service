from flask import Blueprint

from service import weather_factor_service

weather_factor_blueprint = Blueprint("weather_factor_blueprint", __name__, url_prefix="/weather-factor")


@weather_factor_blueprint.route("/define")
def define_weather_factor():
    return weather_factor_service.define_weather_factor()
