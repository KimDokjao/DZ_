import pandas as pd
import os
from .base import Handler
from utils.helpers import find_column_name

class DataLoadHandler(Handler):
    """
    Обработчик, отвечающий за загрузку данных из CSV-файла.
    Автоматически определяет разделитель и кодировку ('utf-8' или 'cp1251').
    """
    def handle(self, path: str) -> pd.DataFrame:
        """
        Загружает CSV-файл в DataFrame.
        """
        try:
            df = pd.read_csv(path, sep=None, engine='python', encoding='utf-8')
        except UnicodeDecodeError:
            print(f"[{self.__class__.__name__}] Не удалось загрузить с utf-8, пробуем cp1251...")
            df = pd.read_csv(path, sep=None, engine='python', encoding='cp1251')
        except Exception as e:
            raise Exception(f"[{self.__class__.__name__}] Произошла ошибка при чтении файла CSV: {e}")

        print(f"[{self.__class__.__name__}] Файл '{os.path.basename(path)}' загружен. Строк: {df.shape[0]}")
        return super().handle(df)
