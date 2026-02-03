import re
import numpy as np
import pandas as pd

def extract_age(text: str) -> float:
    """
    Извлекает возраст в годах из текстовой строки.
    Парсит первое найденное число, за которым следуют слова 'год', 'года' или 'лет'.
    Возвращает np.nan, если возраст не найден или входные данные некорректны.

    Args:
        text: Входная строка, содержащая информацию о возрасте

    Returns:
        Возраст в годах (float) или np.nan.
    """
    if not isinstance(text, str):
        return np.nan
    match = re.search(r'(\d+)\s+(?:год|года|лет)', text, re.IGNORECASE)
    return float(match.group(1)) if match else np.nan

def extract_experience_months(text: str) -> float:
    """
    Извлекает опыт работы из текстовой строки и конвертирует его в общее количество месяцев.
    Парсит числа перед словами 'год/лет/года' и 'месяц/месяца/месяцев'.
    Возвращает np.nan, если опыт не указан или не может быть извлечен.

    Args:
        text: Входная строка с информацией об опыте работы.

    Returns:
        Общее количество месяцев опыта (float) или np.nan.
    """
    s = str(text).lower()
    if 'не указано' in s or s == 'nan' or not isinstance(text, str):
        return np.nan

    years_match = re.search(r'(\d+)\s*(?:год|лет|года)', s)
    months_match = re.search(r'(\d+)\s*(?:месяц|месяца|месяцев)', s)

    y = int(years_match.group(1)) if years_match else 0
    m = int(months_match.group(1)) if months_match else 0

    # Если ничего не найдено, считаем пропуском
    if y == 0 and m == 0 and not (years_match or months_match):
        return np.nan

    # Простая эвристика: если лет очень много (похоже на год), игнорируем
    if y > 100:
        y = 0

    return float(y * 12 + m)

def extract_salary(text: str) -> float:
    """
    Извлекает числовое значение зарплаты из текстовой строки и конвертирует в рубли.
    Поддерживает USD, EUR, KZT, UAH/ГРН.

    Args:
        text: Входная строка с информацией о зарплате (например, '100 000 руб.', '200 USD').

    Returns:
        Числовое значение зарплаты в рублях (float) или np.nan.
    """
    if not isinstance(text, str):
        return np.nan

    # Удаляем все, кроме цифр, чтобы получить числовое значение
    num_match = re.sub(r'[^\d]', '', text)
    if not num_match:
        return np.nan
    amount = float(num_match)

    # Конвертация валют (приблизительные курсы на февраль 2026)
    text_upper = text.upper()
    if 'USD' in text_upper:
        amount *= 90.0
    elif 'EUR' in text_upper:
        amount *= 98.0
    elif 'KZT' in text_upper:
        amount *= 0.20
    elif 'ГРН' in text_upper or 'UAH' in text_upper:
        amount *= 2.5

    return amount

def extract_city_name(text: str) -> str:
    """
    Извлекает название города из текстовой строки.
    Берет часть строки до первой запятой.

    Args:
        text: Входная строка, содержащая информацию о городе (например, 'Москва, готов к переезду').

    Returns:
        Название города (str) или пустую строку, если город не найден.
    """
    if not isinstance(text, str):
        return ""
    return text.split(',')[0].strip()

def extract_position_name(text: str) -> str:
    """
    Извлекает название должности из текстовой строки.
    По сути, просто возвращает входную строку, заполняя NaN.

    Args:
        text: Входная строка, содержащая название должности.

    Returns:
        Название должности (str) или 'не указана', если входные данные некорректны.
    """
    if not isinstance(text, str) or pd.isna(text):
        return "не указана"
    return text.strip()