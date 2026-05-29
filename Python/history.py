"""
Модуль для работы с историей трансформаций.

Обеспечивает сохранение и загрузку истории трансформаций
в JSON файл history.json.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


# Путь к файлу истории (в директории скрипта)
HISTORY_FILE = Path(__file__).parent / 'history.json'

# Максимальное количество записей в истории
MAX_HISTORY_ITEMS = 50


def load_history() -> List[Dict[str, Any]]:
    """
    Загрузка истории трансформаций из файла.
    
    Returns:
        Список записей истории (последние MAX_HISTORY_ITEMS)
    """
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        # Ограничиваем количество записей
        return history[-MAX_HISTORY_ITEMS:]
    
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка загрузки истории: {e}")
        return []


def save_history(history: List[Dict[str, Any]]) -> bool:
    """
    Сохранение истории трансформаций в файл.
    
    Args:
        history: Список записей истории
        
    Returns:
        True если успешно, False в случае ошибки
    """
    try:
        # Ограничиваем количество записей
        limited_history = history[-MAX_HISTORY_ITEMS:]
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(limited_history, f, indent=2, ensure_ascii=False)
        
        return True
    
    except IOError as e:
        print(f"Ошибка сохранения истории: {e}")
        return False


def add_to_history(original: str, transformed: str) -> bool:
    """
    Добавление новой записи в историю.
    
    Args:
        original: Исходный текст
        transformed: Трансформированный текст
        
    Returns:
        True если успешно
    """
    history = load_history()
    
    # Создаем новую запись
    new_entry = {
        'timestamp': datetime.now().isoformat(),
        'original': original,
        'transformed': transformed
    }
    
    # Добавляем в конец
    history.append(new_entry)
    
    return save_history(history)


def clear_history() -> bool:
    """
    Очистка всей истории.
    
    Returns:
        True если успешно
    """
    return save_history([])


def get_history_count() -> int:
    """
    Получение количества записей в истории.
    
    Returns:
        Количество записей
    """
    return len(load_history())

