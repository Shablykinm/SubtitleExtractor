"""
Модуль для генерации субтитров в различных форматах
"""

from datetime import timedelta
from pathlib import Path


class SubtitleGenerator:
    """Класс для генерации субтитров"""
    
    def __init__(self):
        """Инициализация генератора субтитров"""
        pass
    
    def _format_timestamp(self, seconds):
        """
        Форматирование временной метки в формат SRT
        
        Args:
            seconds: время в секундах (float)
            
        Returns:
            str: отформатированное время (HH:MM:SS,mmm)
        """
        # Исправлено: правильно обрабатываем миллисекунды
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds_remainder = seconds % 60
        whole_seconds = int(seconds_remainder)
        milliseconds = int(round((seconds_remainder - whole_seconds) * 1000))
        
        # Гарантируем, что миллисекунды в диапазоне 0-999
        milliseconds = min(999, max(0, milliseconds))
        
        return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d},{milliseconds:03d}"
    
    def generate_srt(self, segments, output_path):
        """
        Генерация SRT файла из сегментов
        
        Args:
            segments: список сегментов транскрипции
            output_path: путь для сохранения
            
        Returns:
            Path: путь к созданному файлу
        """
        print("\n📝 Создание субтитров...")
        
        srt_content = []
        
        for i, segment in enumerate(segments, start=1):
            start_time = self._format_timestamp(segment['start'])
            end_time = self._format_timestamp(segment['end'])
            text = segment['text'].strip()
            
            srt_content.append(f"{i}")
            srt_content.append(f"{start_time} --> {end_time}")
            srt_content.append(text)
            srt_content.append("")  # Пустая строка между субтитрами
        
        # Сохранение файла
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_content))
        
        print(f"  ✓ Субтитры сохранены: {output_path.name}")
        print(f"  📄 Всего сегментов: {len(segments)}")
        
        return output_path
    
    def generate_vtt(self, segments, output_path):
        """
        Генерация WebVTT файла (альтернативный формат)
        
        Args:
            segments: список сегментов транскрипции
            output_path: путь для сохранения
        """
        vtt_content = ["WEBVTT", ""]
        
        for segment in segments:
            start_time = self._format_timestamp(segment['start']).replace(',', '.')
            end_time = self._format_timestamp(segment['end']).replace(',', '.')
            text = segment['text'].strip()
            
            vtt_content.append(f"{start_time} --> {end_time}")
            vtt_content.append(text)
            vtt_content.append("")
        
        output_path = Path(output_path).with_suffix('.vtt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(vtt_content))
        
        print(f"  ✓ VTT субтитры сохранены: {output_path.name}")
        
        return output_path