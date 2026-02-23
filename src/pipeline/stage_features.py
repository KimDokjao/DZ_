import pandas as pd
from .base import Handler
from utils.parsers import extract_age, extract_experience_months, extract_city_name, extract_position_name
from utils.helpers import find_column_name

class FeatureExtractionHandler(Handler):
    """
    Обработчик для извлечения числовых и текстовых признаков из DataFrame.

    Извлекает:
    - `age` (возраст в годах)
    - `is_male` (бинарный признак пола)
    - `exp_total` (опыт работы в месяцах)
    - `city_name` (название города)
    - `position_name` (название должности)

    Эти признаки добавляются как новые колонки в DataFrame.
    """

    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Извлекает и добавляет признаки возраста, пола, опыта работы, города и должности.

        Args:
            df: Входной DataFrame после очистки.

        Returns:
            DataFrame с добавленными числовыми и текстовыми признаками.

        Raises:
            KeyError: Если одна из необходимых колонок не найдена.
        """
        try:
            col_person = find_column_name(df, ['Пол', 'возраст'])
            col_exp = find_column_name(df, ['Опыт'])
            col_city = find_column_name(df, ['Город'])
            col_position = find_column_name(df, ['Ищет работу', 'Должность', 'Профессия'])
        except KeyError as e:
            raise KeyError(
                f"[{self.__class__.__name__}] Ошибка: Необходимая колонка не найдена для извлечения признаков. {e}")

        # Извлечение числовых признаков
        df['age'] = df[col_person].apply(extract_age)
        df['is_male'] = df[col_person].apply(lambda x: 1 if 'Мужчина' in str(x) else 0)
        df['exp_total'] = df[col_exp].apply(extract_experience_months)

        # Извлечение текстовых признаков
        df['city_name'] = df[col_city].apply(extract_city_name)
        df['position_name'] = df[col_position].apply(extract_position_name)

        print(f"[{self.__class__.__name__}] Извлечены признаки: возраст, пол, опыт, город, должность.")
        return super().handle(df)