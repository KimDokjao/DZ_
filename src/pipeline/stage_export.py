import os
import numpy as np
from .base import Handler

class SaveNumpyHandler(Handler):
    """
    Обработчик для сохранения массивов NumPy (X и y) в файлы .npy.
    """
    def __init__(self, original_path: str):
        """
        Инициализирует обработчик сохранения.

        Args:
            original_path: Оригинальный путь к CSV-файлу. Используется для определения
                           директории, куда будут сохранены выходные файлы.
        """
        super().__init__()
        self.directory = os.path.dirname(os.path.abspath(original_path))

    def handle(self, data: dict) -> str:
        """
        Сохраняет 'x_data.npy' и 'y_data.npy' в целевую директорию.

        Args:
            data: Словарь, содержащий ключи 'x' (матрица признаков)
                  и 'y' (вектор целевой переменной).

        Returns:
            Сообщение о завершении операции и пути к сохраненным файлам.
        """
        x_path = os.path.join(self.directory, 'x_data.npy')
        y_path = os.path.join(self.directory, 'y_data.npy')

        np.save(x_path, data['x'])
        np.save(y_path, data['y'])

        return f"Пайплайн завершен. Файлы x_data.npy и y_data.npy созданы в: {self.directory}"