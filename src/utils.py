"""
Вспомогательные функции
"""

import os
import sys
import shutil
from pathlib import Path


def check_dependencies():
    """Проверка наличия необходимых зависимостей"""
    missing = []
    
    try:
        import whisper
    except ImportError:
        missing.append("openai-whisper")
    
    try:
        import torch
    except ImportError:
        missing.append("torch")
    
    if missing:
        print("❌ Отсутствуют необходимые зависимости:")
        for dep in missing:
            print(f"  - {dep}")
        print("\nУстановите их командой:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True


def check_ffmpeg():
    """Проверка наличия FFmpeg"""
    ffmpeg_path = shutil.which('ffmpeg')
    
    if ffmpeg_path:
        return True
    else:
        print("⚠ FFmpeg не найден")
        print("  Для работы со всеми форматами установите FFmpeg:")
        print("  Windows: https://ffmpeg.org/download.html")
        print("  Mac: brew install ffmpeg")
        print("  Linux: sudo apt-get install ffmpeg")
        return False


def get_device(torch_available):
    """
    Определение доступного устройства
    
    Args:
        torch_available: доступен ли torch
        
    Returns:
        str: устройство ('cuda' или 'cpu')
    """
    if torch_available:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    return "cpu"


def format_file_size(size_bytes):
    """
    Форматирование размера файла
    
    Args:
        size_bytes: размер в байтах
        
    Returns:
        str: отформатированный размер
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def validate_input_file(file_path):
    """
    Проверка входного файла
    
    Args:
        file_path: путь к файлу
        
    Returns:
        bool: валидный ли файл
    """
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return False
    
    if os.path.getsize(file_path) == 0:
        print(f"❌ Файл пустой: {file_path}")
        return False
    
    return True


def create_output_path(input_path, output_arg=None, suffix=""):
    """
    Создание пути для выходного файла
    
    Args:
        input_path: путь к входному файлу
        output_arg: аргумент выходного пути
        suffix: суффикс для имени файла
        
    Returns:
        Path: путь для сохранения
    """
    input_path = Path(input_path)
    
    if output_arg:
        output_path = Path(output_arg)
        if output_path.suffix:
            return output_path
        else:
            return output_path.with_suffix('.srt')
    else:
        return input_path.parent / f"{input_path.stem}{suffix}.srt"


def print_banner(input_file, model):
    """Печать баннера программы"""
    print("\n" + "="*60)
    print("🎬 AUDIO TO SUBTITLES CONVERTER (оригинальные субтитры)")
    print("="*60)
    print(f"Входной файл: {input_file}")
    print(f"Модель: {model}")
    print("="*60)


def print_summary(output_file, language, segments_count):
    """Печать итогов работы"""
    print("\n" + "="*60)
    print("✅ ГОТОВО!")
    print("="*60)
    print(f"📁 Файл сохранен: {output_file}")
    print(f"🌐 Язык: {language.upper()}")
    print(f"📝 Сегментов: {segments_count}")
    print("="*60)