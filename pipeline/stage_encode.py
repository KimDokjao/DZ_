import pandas as pd
import numpy as np
from .base import Handler
from utils.parsers import extract_salary
from utils.helpers import find_column_name

class EncodingHandler(Handler):
    """
    Формирует финальные X и y. Очищает данные от NaN,
    возникших при ошибках парсинга зарплаты или признаков.
    """
    def handle(self, df: pd.DataFrame) -> dict:
        col_salary = find_column_name(df, ['ЗП'])

        # 1. Извлекаем ЗП и превращаем в числа. Ошибки станут NaN
        y_series = df[col_salary].apply(extract_salary)
        y_series = pd.to_numeric(y_series, errors='coerce')

        # 2. Определяем матрицу признаков X (все, кроме колонки ЗП)
        x_df = df.drop(columns=[col_salary])

        # 3. Синхронная очистка X и y от любых NaN
        # Объединяем их временно, чтобы dropna удалила строки целиком
        combined = pd.concat([x_df, y_series.rename('target')], axis=1)
        initial_count = len(combined)
        combined = combined.dropna()

        if len(combined) < initial_count:
            print(
                f"[{self.__class__.__name__}] Удалено {initial_count - len(combined)} строк с некорректными данными (NaN/строки).")

        # 4. Преобразование в финальные массивы float32
        x_data = combined.drop(columns=['target']).values.astype(np.float32)
        y_data = combined['target'].values.astype(np.float32)

        print(f"[{self.__class__.__name__}] Итог: X{x_data.shape}, y{y_data.shape}")

        return super().handle({'x': x_data, 'y': y_data})