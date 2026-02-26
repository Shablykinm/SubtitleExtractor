#!/usr/bin/env python3
"""
Audio to Subtitles Converter
Конвертирует аудио в оригинальные субтитры
"""

import argparse
import sys
from pathlib import Path

from src.config import VERSION, DEFAULT_MODEL, MODEL_CACHE_DIR
from src.audio_processor import AudioProcessor
from src.subtitle_generator import SubtitleGenerator
from src.utils import (
    check_ffmpeg,
    check_dependencies,
    validate_input_file,
    create_output_path,
    print_banner,
    print_summary
)


def main():
    parser = argparse.ArgumentParser(
        description='Конвертация аудио в оригинальные субтитры',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py audio.mp3
  python main.py video.mp4 -o subtitles -m tiny
  python main.py podcast.wav --model large
  python main.py audio.mp3 --model-path /custom/path/to/models
        """
    )
    
    parser.add_argument('input', help='Путь к аудио или видео файлу')
    parser.add_argument('-o', '--output', help='Путь для сохранения субтитров (без расширения)')
    parser.add_argument('-m', '--model', default=DEFAULT_MODEL,
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help=f'Размер модели Whisper (по умолчанию: {DEFAULT_MODEL})')
    parser.add_argument('--model-path', help='Путь к папке с моделями (переопределяет стандартный)')
    parser.add_argument('--no-ffmpeg-check', action='store_true',
                       help='Пропустить проверку FFmpeg')
    parser.add_argument('--version', action='version', 
                       version=f'Audio to Subtitles Converter v{VERSION}')
    
    args = parser.parse_args()
    
    # Проверка зависимостей
    if not check_dependencies():
        sys.exit(1)
    
    # Проверка FFmpeg (если не отключено)
    if not args.no_ffmpeg_check and not check_ffmpeg():
        print("\n⚠ Продолжаем без FFmpeg, но возможны проблемы с некоторыми форматами")
    
    # Проверка входного файла
    if not validate_input_file(args.input):
        sys.exit(1)
    
    # Определяем путь к моделям
    model_path = Path(args.model_path) if args.model_path else MODEL_CACHE_DIR
    print(f"📁 Используется папка моделей: {model_path}")
    
    # Создание пути для выходного файла
    output_path = create_output_path(args.input, args.output, suffix="_original")
    
    # Печать баннера
    print_banner(args.input, args.model)
    
    # Инициализация процессора с указанием пути к моделям
    try:
        processor = AudioProcessor(
            model_size=args.model,
            download_root=model_path
        )
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        sys.exit(1)
    
    # Обработка аудио
    try:
        result = processor.process_audio(args.input)
        detected_language = result['language']
        segments = result['segments']
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")
        sys.exit(1)
    
    # Генерация субтитров
    try:
        generator = SubtitleGenerator()
        subtitle_file = generator.generate_srt(segments, output_path)
    except Exception as e:
        print(f"❌ Ошибка создания субтитров: {e}")
        sys.exit(1)
    
    # Печать итогов
    print_summary(subtitle_file, detected_language, len(segments))


if __name__ == "__main__":
    main()