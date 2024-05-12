from dao import weather_factor_dao, weather_dao
from dto.weather_factor_dto import WeatherFactorDTO


def define_weather_factor():
    for data in weather_dao.find_all_after_time(weather_factor_dao.get_time_of_last()):
        weather_factor_dao.save(
            WeatherFactorDTO(
                None,
                data.time,
                data.temp * data.pressure / 1 if data.hum == 0 else data.hum
            ))

    return "Success"
