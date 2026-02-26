"""
Модуль для обработки аудио с использованием Whisper
"""
import os
from pathlib import Path
from datetime import timedelta

from src.utils import get_device, format_file_size
from src.config import TRANSCRIBE_CONFIG, MODEL_CACHE_DIR

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class AudioProcessor:
    """Класс для обработки аудио файлов"""
    
    def __init__(self, model_size="medium", device=None, download_root=None):
        """
        Инициализация процессора аудио
        
        Args:
            model_size: размер модели whisper
            device: устройство для вычислений
            download_root: путь для скачивания моделей
        """
        if not WHISPER_AVAILABLE:
            raise ImportError(
                "Whisper не установлен. Выполните: pip install openai-whisper"
            )
        
        self.model_size = model_size
        self.device = device or get_device(TORCH_AVAILABLE)
        self.download_root = download_root or MODEL_CACHE_DIR
        self.model = None
        
        # Показываем где будут храниться модели
        print(f"📁 Директория для моделей: {self.download_root}")
        
    def load_model(self):
        """Загрузка модели Whisper"""
        print(f"📥 Загрузка модели Whisper ({self.model_size})...")
        
        try:
            # Явно указываем путь для скачивания модели
            self.model = whisper.load_model(
                self.model_size,
                device=self.device,
                download_root=self.download_root  # Важно! указываем путь
            )
            print(f"  ✓ Модель загружена на устройство: {self.device}")
            
            # Проверяем где сохранилась модель
            model_path = self.download_root / f"{self.model_size}.pt"
            if model_path.exists():
                print(f"  📍 Модель сохранена в: {model_path}")
            
        except Exception as e:
            print(f"  ✗ Ошибка загрузки модели: {e}")
            
            # Если ошибка загрузки, пробуем другой метод
            try:
                print("  🔄 Пробуем альтернативный метод загрузки...")
                
                # Устанавливаем переменные окружения
                os.environ['WHISPER_CACHE_DIR'] = str(self.download_root)
                os.environ['XDG_CACHE_HOME'] = str(self.download_root.parent)
                
                self.model = whisper.load_model(
                    self.model_size,
                    device=self.device,
                    download_root=self.download_root
                )
                print(f"  ✓ Модель загружена альтернативным методом")
                
            except Exception as e2:
                print(f"  ✗ Ошибка альтернативной загрузки: {e2}")
                raise
    
    def process_audio(self, audio_path):
        print(f"\n📂 Анализ файла: {audio_path}")
        
        # Проверка файла
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Файл {audio_path} не найден")
        
        # Информация о файле
        file_size = os.path.getsize(audio_path)
        print(f"  📊 Размер: {format_file_size(file_size)}")
        
        # Загрузка модели (если еще не загружена)
        if not self.model:
            self.load_model()
        
        # Транскрибация
        print("\n🔄 Транскрибация аудио...")
        print("  ⏳ Это может занять несколько минут")
        
        try:
            result = self.model.transcribe(
                audio_path,
                language=None,  # Автоопределение языка
                **TRANSCRIBE_CONFIG
            )
            
            # Информация о результате
            detected_language = result['language']
            segments_count = len(result['segments'])
            duration = timedelta(seconds=result['segments'][-1]['end'])
            
            print(f"  ✓ Транскрибация завершена")
            print(f"  🌐 Определен язык: {detected_language.upper()}")
            print(f"  📝 Сегментов: {segments_count}")
            print(f"  ⏱ Длительность: {duration}")
            
            return result
            
        except Exception as e:
            print(f"  ✗ Ошибка транскрибации: {e}")
            raise