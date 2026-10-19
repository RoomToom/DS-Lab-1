import csv
from typing import Any, Dict, List, Union, TextIO

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def summarize_weather_data(data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Summarize the weather data across all days.

    Args:
        data (list of dict): The daily weather data.

    Returns:
        dict: A summary of the key metrics across all days.
    """
    if not data:
        raise ValueError("No daily weather data to summarize.")
    return {
        "average_max_temp": sum(day['max_temperature'] for day in data) / len(data),
        "average_min_temp": sum(day['min_temperature'] for day in data) / len(data),
        "total_precipitation": sum(day['precipitation'] for day in data),
        "average_wind_speed": sum(day['wind_speed'] for day in data) / len(data),
        "average_humidity": sum(day['humidity'] for day in data) / len(data),
        "hot_days": sum(day['max_temperature'] > 30 for day in data),
        "windy_days": sum(day['wind_speed'] > 15 for day in data),
        "rainy_days": sum(day['precipitation'] > 0 for day in data),
    }


def export_to_csv(data: List[Dict[str, Any]], file: Union[str, TextIO]) -> None:
    """
    Export the summarized weather data to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): The name of the CSV file to save the data in, or a file-like object.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Precipitation", "Wind Speed", "Humidity",
               "Weather Description", "Is Hot Day", "Is Windy Day", "Is Rainy Day"]

    def write_data(writer: csv.DictWriter) -> None:
        """Helper function to write rows to the CSV.
        
        Args:
            writer (csv.DictWriter): The CSV writer object.
        """
        writer.writeheader()
        for day in data:
            writer.writerow(dict(zip(headers, [
                day['date'], day['max_temperature'], day['min_temperature'],
                day['precipitation'], day['wind_speed'], day['humidity'],
                day['weather_description'], day['max_temperature'] > 30,
                day['wind_speed'] > 15, day['precipitation'] > 0,
            ])))

    # Переданий файловий об’єкт залишається відкритим для подальшого читання.
    if isinstance(file, str):
        with open(file, 'w', newline='', encoding='utf-8') as output:
            write_data(csv.DictWriter(output, fieldnames=headers))
    else:
        write_data(csv.DictWriter(file, fieldnames=headers))


if __name__ == "__main__":
    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        summary = summarize_weather_data(weather_data['daily'])

        print("Weather Data Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        export_to_csv(weather_data['daily'], "tokyo_weather_summary.csv")

        print("Data successfully exported to tokyo_weather_summary.csv")
    except Exception as e:
        raise SystemExit(f"An error occurred: {e}")
