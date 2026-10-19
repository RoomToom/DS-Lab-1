# Методи Data Science — лабораторна №1

Варіант 7. Збір та обробка даних.

[Умови завдання](https://github.com/UNI-DS/DS-Lab-1)

## Запуск

Python 3.11+. Команди виконуються з кореня репозиторію:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/task1_scrape.py
python src/task2_fetch_tokyo_weather.py
python src/task3_complex_weather_analysis.py
python src/task4_weather_summary_export.py
python src/task5_parse_weather_xml.py
python src/task6_extract_weather_data.py
```

Перевірка: `python -m pytest tests/ -v`.
Панель результатів: `streamlit run streamlit_app.py`.

Завдання 1–2 потребують інтернету. JSON і CSV зберігаються в корені проєкту,
а звіт завдання 3 виводиться в термінал. Повторний запуск оновлює файли результатів.
Дані у `src/` — навчальні приклади за серпень 2024 року.

## Результати

- `extracted_wikipedia_data.json` — заголовок і перше речення статті Wikipedia.
- `tokyo_weather.json` — максимальна температура на завтра за часом Токіо.
- `tokyo_weather_summary.csv` — погодні показники за чотири дні та ознаки спекотного, вітряного й дощового дня.
- `parsed_weather_data.csv` — дані з XML.
- `extracted_weather_data.csv` — дані з текстового звіту.

Завдання 3 друкує щоденні звіти й підсумок у терміналі.
Для класифікації опадів використано межі: до 5 мм — слабкий дощ,
5–10 мм — помірний, понад 10 мм — сильний; 0 мм — без опадів.
