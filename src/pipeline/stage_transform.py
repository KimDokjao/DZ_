import pandas as pd
import numpy as np
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from .base import Handler

class FeatureTransformHandler(Handler):
    """
    Обработчик для TF-IDF векторизации текста и масштабирования чисел.
    Сохраняет веса векторизатора и скалера в папку resources.
    """
    RESOURCES_DIR = "resources"
    VECTORIZER_PATH = os.path.join(RESOURCES_DIR, "vectorizer.pkl")
    SCALER_PATH = os.path.join(RESOURCES_DIR, "scaler.pkl")

    def __init__(self):
        super().__init__()
        os.makedirs(self.RESOURCES_DIR, exist_ok=True)

    def _load_or_fit_vectorizer(self, text_data: pd.Series) -> TfidfVectorizer:
        if os.path.exists(self.VECTORIZER_PATH):
            return joblib.load(self.VECTORIZER_PATH)

        print(f"[{self.__class__.__name__}] Обучение TF-IDF...")
        vectorizer = TfidfVectorizer(max_features=500, min_df=2)
        vectorizer.fit(text_data)
        joblib.dump(vectorizer, self.VECTORIZER_PATH)
        return vectorizer

    def _load_or_fit_scaler(self, numeric_data: pd.DataFrame) -> StandardScaler:
        if os.path.exists(self.SCALER_PATH):
            return joblib.load(self.SCALER_PATH)

        print(f"[{self.__class__.__name__}] Обучение StandardScaler...")
        scaler = StandardScaler()
        scaler.fit(numeric_data)
        joblib.dump(scaler, self.SCALER_PATH)
        return scaler

    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Преобразует признаки, очищая их от строковых аномалий.
        """
        # 1. Очистка числовых признаков от строк
        numeric_cols = ['age', 'exp_total']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Заполняем NaN средним или нулем, чтобыScaler не упал
        df[numeric_cols] = df[numeric_cols].fillna(0)

        # 2. Обработка текста (TF-IDF)
        text_corpus = df['position_name'].fillna('') + " " + df['city_name'].fillna('')
        vectorizer = self._load_or_fit_vectorizer(text_corpus)
        text_features = vectorizer.transform(text_corpus).toarray()

        text_df = pd.DataFrame(
            text_features,
            columns=[f'tf_{i}' for i in range(text_features.shape[1])],
            index=df.index
        )

        # 3. Масштабирование чисел
        scaler = self._load_or_fit_scaler(df[numeric_cols])
        scaled_values = scaler.transform(df[numeric_cols])
        scaled_df = pd.DataFrame(
            scaled_values,
            columns=[f'{c}_scaled' for c in numeric_cols],
            index=df.index
        )

        # Сборка финального DF для следующей стадии
        # Сохраняем 'is_male' и исходную колонку с ЗП (для EncodingHandler)
        from utils.helpers import find_column_name
        col_salary = find_column_name(df, ['ЗП'])

        res_df = pd.concat([df[[col_salary, 'is_male']], scaled_df, text_df], axis=1)

        return super().handle(res_df)