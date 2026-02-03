import pandas as pd
from typing import List

def find_column_name(df: pd.DataFrame, keywords: List[str]) -> str:
    """
    Осуществляет поиск названия колонки в DataFrame по списку ключевых слов.
    Поиск выполняется без учета регистра и частичным совпадением.

    Args:
        df: pandas.DataFrame, в котором производится поиск.
        keywords: Список ключевых слов, по которым осуществляется поиск колонки.
                  Будет найдена первая колонка, содержащая любое из ключевых слов.

    Returns:
        Точное название колонки (str), содержащей ключевое слово.

    Raises:
        KeyError: Если колонка, содержащая ни одно из указанных ключевых слов, не найдена.
    """
    for keyword in keywords:
        for col in df.columns:
            if keyword.lower() in str(col).lower():
                return col
    raise KeyError(f"Колонка с ключевыми словами '{keywords}' не найдена в данных.")