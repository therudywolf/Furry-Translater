"""
Модуль для работы с настройками приложения.

Обеспечивает сохранение и загрузку пользовательских настроек
в JSON файл settings.json.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


# Путь к файлу настроек (в директории скрипта)
SETTINGS_FILE = Path(__file__).parent / 'settings.json'


# Настройки по умолчанию
DEFAULT_SETTINGS = {
    'intensity': 5,              # Интенсивность трансформации (1-10)
    'auto_convert': True,         # Включен ли автоконверт
    'auto_convert_delay': 500,    # Задержка автоконверта (мс)
    'noise_probability': 0.6,     # Вероятность волчьих звуков (0.0-1.0)
    'cyber_vibe_probability': 0.3, # Вероятность кибер-символов (0.0-1.0)
    'theme': 'nocturne',          # Тема оформления
    'font_size': 11,              # Размер шрифта
    'window_width': 700,          # Ширина окна
    'window_height': 600           # Высота окна
}


def load_settings() -> Dict[str, Any]:
    """
    Загрузка настроек из файла.
    
    Если файл не существует, возвращаются настройки по умолчанию.
    
    Returns:
        Словарь с настройками
    """
    if not SETTINGS_FILE.exists():
        return DEFAULT_SETTINGS.copy()
    
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # Объединяем с настройками по умолчанию (на случай новых полей)
        result = DEFAULT_SETTINGS.copy()
        result.update(settings)
        return result
    
    except (json.JSONDecodeError, IOError) as e:
        # Если ошибка чтения, возвращаем настройки по умолчанию
        print(f"Ошибка загрузки настроек: {e}")
        return DEFAULT_SETTINGS.copy()


def save_settings(settings: Dict[str, Any]) -> bool:
    """
    Сохранение настроек в файл.
    
    Args:
        settings: Словарь с настройками для сохранения
        
    Returns:
        True если успешно, False в случае ошибки
    """
    try:
        # Объединяем с настройками по умолчанию для валидации
        validated = DEFAULT_SETTINGS.copy()
        validated.update(settings)
        
        # Валидация значений
        validated['intensity'] = max(1, min(10, validated.get('intensity', 5)))
        validated['auto_convert_delay'] = max(100, min(5000, validated.get('auto_convert_delay', 500)))
        validated['noise_probability'] = max(0.0, min(1.0, validated.get('noise_probability', 0.6)))
        validated['cyber_vibe_probability'] = max(0.0, min(1.0, validated.get('cyber_vibe_probability', 0.3)))
        
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(validated, f, indent=2, ensure_ascii=False)
        
        return True
    
    except IOError as e:
        print(f"Ошибка сохранения настроек: {e}")
        return False


def get_setting(key: str, default: Any = None) -> Any:
    """
    Получение значения конкретной настройки.
    
    Args:
        key: Ключ настройки
        default: Значение по умолчанию, если настройка не найдена
        
    Returns:
        Значение настройки или default
    """
    settings = load_settings()
    return settings.get(key, default)


def set_setting(key: str, value: Any) -> bool:
    """
    Установка значения конкретной настройки.
    
    Args:
        key: Ключ настройки
        value: Новое значение
        
    Returns:
        True если успешно
    """
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)

