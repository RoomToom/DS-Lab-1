import xml.etree.ElementTree as ET
import csv
from typing import Any, List, Dict


def parse_weather_xml(xml_file: str) -> List[Dict[str, Any]]:
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.

    Raises:
        FileNotFoundError: If the XML file does not exist.
        ET.ParseError: If the XML file is malformed.
    """
    root = ET.parse(xml_file).getroot()
    data = []
    for day in root.findall('day'):
        if any(not day.findtext(key) for key in ('date', 'temperature', 'humidity', 'precipitation')):
            raise ValueError("An XML day is missing a required weather field.")
        data.append({
            'date': day.findtext('date'),
            'temperature': float(day.findtext('temperature')),
            'humidity': int(day.findtext('humidity')),
            'precipitation': float(day.findtext('precipitation')),
        })
    return data


def save_to_csv(data: List[Dict[str, Any]], filename: str = "parsed_weather_data.csv") -> None:
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output)
        writer.writerow(['Date', 'Temperature', 'Humidity', 'Precipitation'])
        writer.writerows([day['date'], day['temperature'], day['humidity'], day['precipitation']]
                        for day in data)


if __name__ == "__main__":
    try:
        # Parse the XML file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")
        weather_data = parse_weather_xml(xml_path)

        # Save the parsed data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        raise SystemExit(f"An error occurred: {e}")
