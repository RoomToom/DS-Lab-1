from typing import Dict, List, Any

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def analyze_daily_weather(day: Dict[str, Any], temp_threshold: float = 30, 
                          wind_threshold: float = 15, humidity_threshold: float = 70) -> Dict[str, Any]:
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    return {
        **day,
        "is_hot_day": day['max_temperature'] > temp_threshold,
        "temperature_swing": day['max_temperature'] - day['min_temperature'],
        "is_windy_day": day['wind_speed'] > wind_threshold,
        "is_uncomfortable_day": day['humidity'] > humidity_threshold,
        "is_rainy_day": day['precipitation'] > 0,
    }


def generate_daily_report(analysis: Dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    lines = [
        f"Date: {analysis['date']}",
        f"Weather: {analysis['weather_description']}",
        f"Temperature: Max {analysis['max_temperature']}°C, Min {analysis['min_temperature']}°C "
        f"(Swing: {analysis['temperature_swing']}°C)",
        "It was a hot day." if analysis['is_hot_day'] else "It was not a hot day.",
        "The temperature swing was significant." if analysis['temperature_swing'] > 10
        else "The temperature swing was not significant.",
        "It was a windy day." if analysis['is_windy_day'] else "It was not a windy day.",
        "The humidity made the day uncomfortable." if analysis['is_uncomfortable_day']
        else "The humidity did not exceed the comfort threshold.",
    ]
    rain = analysis['precipitation']
    if analysis['is_rainy_day']:
        # Межі для добових опадів: до 5 мм, 5–10 мм і понад 10 мм.
        severity = 'light' if rain < 5 else 'moderate' if rain <= 10 else 'heavy'
        lines.append(f"It was a rainy day: {severity} rain ({rain} mm).")
    else:
        lines.append("There was no precipitation.")
    return '\n'.join(lines) + '\n'


def summarize_weather_analysis(analyses: List[Dict[str, Any]]) -> str:
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    if not analyses:
        raise ValueError("No daily weather data to summarize.")
    lines = ["Weather Summary:"]
    for label, key, description, unit in [
        ('Hottest', 'max_temperature', 'a maximum temperature of', '°C'),
        ('Windiest', 'wind_speed', 'wind speeds of', ' km/h'),
        ('Most humid', 'humidity', 'a humidity level of', '%'),
        ('Rainiest', 'precipitation', 'precipitation of', ' mm'),
    ]:
        day = max(analyses, key=lambda day: day[key])
        lines.append(f"{label} day: {day['date']} with {description} {day[key]}{unit}")
    return '\n'.join(lines)


if __name__ == "__main__":
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)
        print(f"City: {weather_data['city']} ({weather_data['latitude']}, {weather_data['longitude']})")
        print(f"Timezone: {weather_data['timezone']}\n")

        analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)

        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)
    except Exception as e:
        raise SystemExit(f"An error occurred: {e}")
