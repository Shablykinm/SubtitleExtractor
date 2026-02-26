"""Конфигурационный файл"""

import os
from pathlib import Path

# Версия программы
VERSION = "1.0.0"

# Модель по умолчанию
DEFAULT_MODEL = "medium"

# Доступные модели Whisper
AVAILABLE_MODELS = ['tiny', 'base', 'small', 'medium', 'large']

# Настройки транскрибации
TRANSCRIBE_CONFIG = {
    'verbose': False,
    'fp16': False,
    'task': 'transcribe'
}

# Путь для кэша моделей (абсолютный или относительный путь)
# По умолчанию модели сохраняются в папку models/whisper рядом с проектом
BASE_DIR = Path(__file__).parent.parent  # Корневая папка проекта
MODEL_CACHE_DIR = BASE_DIR / 'models' / 'whisper'

# Создаем папку для моделей, если её нет
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Переменная окружения для Whisper (чтобы использовать наш путь)
os.environ['WHISPER_CACHE_DIR'] = str(MODEL_CACHE_DIR)
os.environ['WHISPER_MODELS_DIR'] = str(MODEL_CACHE_DIR)

print(f"📁 Модели будут сохраняться в: {MODEL_CACHE_DIR}")