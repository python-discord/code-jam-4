from pyowm.weatherapi25.weather import Weather
from project.services.weather import format_forecast


def test_format_forecast():
    """
    Testing the correctness of the values and the output format of the function `format_forecast`.

    In this test only the 'kelvin' will be tested because the conversion is unnessesary of the elements
    """
    weather_json = {"reference_time": 1551027600,
                    "sunset_time": 0,
                    "sunrise_time": 0,
                    "clouds": 88,
                    "rain": {"all": 10.49},
                    "snow": {},
                    "wind": {"speed": 3.85, "deg": 200},
                    "humidity": 93,
                    "pressure": {"press": 999.95, "sea_level": None},
                    "temperature": {"day": 282.86, "min": 275.18, "max": 282.86,
                                    "night": 275.18, "eve": 281.87, "morn": 279.83},
                    "status": "Rain",
                    "detailed_status": "moderate rain",
                    "weather_code": 501,
                    "weather_icon_name": "10d",
                    "visibility_distance": None,
                    "dewpoint": None,
                    "humidex": None,
                    "heat_index": None}

    w = Weather(**weather_json)

    formated = format_forecast(weather=w, unit='kelvin')
    expected = {"day temperature": "282.86 K",
                "lowest temperature": "275.18 K",
                "highest temperature": "282.86 K",
                "night temperature": "275.18 K",
                "evening temperature": "281.87 K",
                "morning temperature": "279.83 K"}

    for k in formated:
        assert formated[k] == expected[k]
