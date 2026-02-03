import argparse
import os
import sys

from pipeline.base import Handler
from pipeline.stage_load import DataLoadHandler, DataCleanHandler
from pipeline.stage_features import FeatureExtractionHandler
from pipeline.stage_transform import FeatureTransformHandler
from pipeline.stage_encode import EncodingHandler
from pipeline.stage_export import SaveNumpyHandler

# Константы для путей
DATA_DIR = 'data'

def parse_data_pipeline(csv_path: str) -> None:
    """
    Запускает пайплайн обработки CSV-файла: загрузка -> очистка -> извлечение признаков ->
    трансформация признаков -> кодирование в NumPy -> сохранение .npy.

    Этот скрипт читает исходный CSV-файл, извлекает необходимые признаки (пол, возраст,
    опыт, город, должность, зарплата), масштабирует числовые признаки, векторизует
    текстовые и сохраняет результат в 'data/x_data.npy' (признаки) и 'data/y_data.npy'
    (целевые значения). Также будут сохранены обученные 'scaler.pkl' и 'vectorizer.pkl'
    в папку 'resources/'.

    Args:
        csv_path: Путь к исходному CSV-файлу.
    """
    print(f"\n--- Запуск пайплайна парсинга данных из '{os.path.basename(csv_path)}' ---")

    # Проверка существования CSV-файла
    if not os.path.exists(csv_path):
        print(f"Ошибка: CSV-файл '{csv_path}' не найден. Пожалуйста, укажите корректный путь.")
        sys.exit(1)

    # Инициализация всех звеньев Chain of Responsibility
    loader = DataLoadHandler()
    cleaner = DataCleanHandler()
    features = FeatureExtractionHandler()
    transformer = FeatureTransformHandler()
    encoder = EncodingHandler()
    exporter = SaveNumpyHandler(os.path.abspath(csv_path))  # Путь для сохранения .npy в директорию data/

    # Строим цепочку: определяем порядок выполнения стадий
    # loader -> cleaner -> features -> transformer -> encoder -> exporter
    loader.set_next(cleaner) \
        .set_next(features) \
        .set_next(transformer) \
        .set_next(encoder) \
        .set_next(exporter)

    try:
        # Запускаем пайплайн, передавая путь к файлу первому обработчику
        status_message = loader.handle(csv_path)
        print(status_message)
    except Exception as e:
        print(f"Критическая ошибка в пайплайне: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="HH Salary Predictor: Обработка исходного CSV-файла в формат .npy."
    )
    parser.add_argument(
        "csv_path",
        help="Путь к исходному CSV-файлу резюме HeadHunter (например, 'data/hh.csv')."
    )
    args = parser.parse_args()
    parse_data_pipeline(args.csv_path)