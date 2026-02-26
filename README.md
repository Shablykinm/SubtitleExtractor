# Subtitles Converter

Конвертер аудио в оригинальные субтитры с использованием Whisper от OpenAI.

## Возможности

- Автоматическое определение языка аудио
- Создание SRT субтитров
- Поддержка различных моделей Whisper (tiny, base, small, medium, large)
- Работает с любыми аудио/видео форматами (через FFmpeg)

## Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/Shablykinm/SubtitleExtractor.git
cd subtitles_converter
pip install -r requirements.txt
```

# Базовое использование
```
python main.py audio.mp3
```
## С указанием модели
```
python main.py audio.mp3 -m tiny
```

## С указанием выходного файла
```
python main.py audio.wav -o my_subtitles
```

## Справка
```
python main.py -h
```

## В случае проблем со скачиванием моделей

```
Убедитесь, что в папке проекта есть директория models
```
## Выполнить в терминале перед запуском
```
set WHISPER_MODEL_URL=https://openaipublic.azureedge.net/main/whisper/models
```

Для тестирования работы приложен audio.mp3 и полученный результат - audio_original.srt
