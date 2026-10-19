import csv
import re
from typing import Any, List, Dict


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    # Replace non-breaking spaces and other non-ASCII characters
    return line.replace('\u00a0', ' ').replace('\u2212', '-').encode('ascii', errors='ignore').decode('ascii').strip()


def extract_weather_data(text_file: str) -> List[Dict[str, Any]]:
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.

    Raises:
        FileNotFoundError: If the text file does not exist.
    """
    number = r'([+-]?\d+(?:\.\d+)?)'
    pattern = re.compile(
        r'Date:\s*(\d{4}-\d{2}-\d{2}),\s*Max Temp:\s*' + number +
        r'\s*C,\s*Min Temp:\s*' + number + r'\s*C,\s*Humidity:\s*(\d+)\s*%,\s*Precipitation:\s*' +
        number + r'\s*mm'
    )
    data = []
    with open(text_file, encoding='utf-8-sig') as source:
        for line_number, line in enumerate(source, 1):
            line = clean_text(line)
            if not line:
                continue
            match = pattern.fullmatch(line)
            if match is None:
                raise ValueError(f"Invalid weather report on line {line_number}.")
            date, maximum, minimum, humidity, precipitation = match.groups()
            data.append({
                'date': date,
                'max_temperature': float(maximum),
                'min_temperature': float(minimum),
                'humidity': int(humidity),
                'precipitation': float(precipitation),
            })
    return data


def save_to_csv(data: List[Dict[str, Any]], filename: str = "extracted_weather_data.csv") -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]
    with open(filename, 'w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows([day['date'], day['max_temperature'], day['min_temperature'],
                         day['humidity'], day['precipitation']] for day in data)


if __name__ == "__main__":
    try:
        # Extract data from the text file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        # Save the extracted data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        raise SystemExit(f"An error occurred: {e}")
