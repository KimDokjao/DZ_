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


class DataCleanHandler(Handler):
    """
    Обработчик для первичной очистки DataFrame.
    """

    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Удаляет строки с NaN в критических колонках и сбрасывает индекс.
        """
        try:
            col_person = find_column_name(df, ['Пол', 'возраст'])
            col_salary = find_column_name(df, ['ЗП'])
            col_exp = find_column_name(df, ['Опыт'])
            col_city = find_column_name(df, ['Город'])
            col_position = find_column_name(df, ['Ищет работу', 'Должность', 'Профессия'])
        except KeyError as e:
            raise KeyError(f"[{self.__class__.__name__}] Ошибка: Необходимая колонка не найдена. {e}")

        initial_rows = df.shape[0]
        df_cleaned = df.dropna(subset=[col_person, col_salary, col_exp, col_city, col_position]).reset_index(drop=True)
        rows_after_drop = df_cleaned.shape[0]

        if initial_rows > rows_after_drop:
            print(
                f"[{self.__class__.__name__}] Удалено {initial_rows - rows_after_drop} строк из-за пропущенных значений.")

        return super().handle(df_cleaned)