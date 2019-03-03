import pyowm
import random

from typing import Dict

from pyowm.weatherapi25.weather import Weather
from pyowm.exceptions.api_response_error import UnauthorizedError


class ForecastFetcher:
    """
    This object makes it easy for the frontend to request the weather data and
    use it.

    Example usage:

    ff = ForecastFetcher(OWM_API_KEY_PATH)
    ff.fetch_forecast_7_days('Berlin', unit='Celsius')

    """
    def __init__(self, api_key_path: str):
        """Returns a ForecastFetcher object which fetched the weather for the
           next seven days.

        :param: api_key_path: The path to a file with an API key for the
            openweathermap.org service.

        """

        api_key = load_owm_api_key(api_key_path)
        self.owm = pyowm.OWM(api_key)

        try:
            self.owm.daily_forecast("New York")
        except UnauthorizedError:
            raise AttributeError(f"The provided API key is not valid: {api_key}")

    def fetch_forecast_7_days(self, location: str,
                              unit: str) -> [Dict[str, str]]:
        """Fetches the forecast for the next seven days from openweathermap.org

        :param location: The name of the location this
        :param unit: Defines the units for the temperature. Only accepts
                    'celsius', 'fahrenheit', 'kelvin' and 'random'.
        """

        forecasts = self.owm.daily_forecast(location).get_forecast()

        if forecasts is None:
            msg = f"There is no weather data for this location={location}"
            raise AttributeError(msg)

        forecast_dicts = [format_forecast(f, unit) for f in forecasts]
        return forecast_dicts


def format_forecast(weather: Weather, unit: str) -> Dict[str, str]:
    """Formats an pyowm.weatherapi25.weather.Weather to an easy to use
    dictionary for the frontend.

    :param weather: A pyowm.weatherapi25.weather.Weather object
    :param unit: Defines the units for the temperature in the output
                 dictionary. Only accepts 'celsius', 'fahrenheit', 'kelvin' and
                 'random'.

    :raises AttributeError: If an invalid unit has been supplied
    """
    units = {'celsius', 'fahrenheit', 'kelvin'}
    unit_symbols = {'celsius': '°C', 'fahrenheit': '°F', 'kelvin': 'K'}

    if unit not in units and not unit == 'random':
        msg = "This is not a valid input unit, please enter one of the " \
              "following: {}"
        raise AttributeError(msg.format(' '.join(units)))

    if unit == 'random':
        unit = random.sample(units, 1)

    output_dict = {}

    temperatures = weather.get_temperature(unit)
    temperature_naming = {'min': 'lowest',
                          'max': 'highest',
                          'eve': 'evening',
                          'morn': 'morning'}
    for t in temperatures:
        key = temperature_naming.get(t, t) + ' temperature'
        output_dict[key] = str(temperatures[t]) + ' ' + unit_symbols[unit]

    output_dict['weather_status'] = weather.get_status()
    return output_dict


def load_owm_api_key(path: str) -> str:
    """Loads the Open-Weather-Map API key from the provided file.

    :param path: The path to the OWM_API_KEY, defaults to just OWM_API_KEY.
    :return The api key as a string
    """
    with open(path, 'r') as infile:
        return infile.read().strip()
