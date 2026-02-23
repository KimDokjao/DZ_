# DZ_

##  1. Структура Репозитория

├── app.py
├── parse_data.py
├── train_model.py
├── README.md
├── data/
│ ├── hh.csv
│ ├── x_data.npy
│ └── y_data.npy
├── resources/
│ ├── model.pkl
│ ├── scaler.pkl
│ └── vectorizer.pkl
├── pipeline/
│ ├── init.py
│ ├── base.py
│ ├── stage_load.py
│ ├── stage_features.py
│ ├── stage_transform.py
│ ├── stage_encode.py
│ └── stage_export.py
└── utils/
├── init.py
├── parsers.py
├── helpers.py      

##  Порядок Запуска Проекта
1.  Шаг 1: Парсинг данных (parse_data.py)
2.  Шаг 2: Обучение модели (train_model.py)
3.  Шаг 3: Предсказание зарплат (app.py)

## Пример полного цикла запуска в терминале:

### 1. Обработка исходного CSV-файла (должен находиться в data/hh.csv)
`python parse_data.py data/hh.csv`

### 2. Обучение модели Linear Regression
`python train_model.py`

### 3. Получение предсказаний зарплат из подготовленных данных
`python app.py data/x_data.npy`
