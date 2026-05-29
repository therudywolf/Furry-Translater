"""
Модуль для работы с темами оформления.

Содержит определения различных цветовых схем для приложения.
"""

from typing import Dict, Any


# ═══════════════════════════════════════════════════════════════
# ОПРЕДЕЛЕНИЯ ТЕМ
# ═══════════════════════════════════════════════════════════════

THEMES: Dict[str, Dict[str, Any]] = {
    'nocturne': {
        'name': 'Nocturne',
        'description': 'Кибер-эстетика с неоновыми акцентами',
        'colors': {
            'background': '#1a1a2e',
            'secondary_bg': '#16213e',
            'accent': '#00ff41',
            'border': '#0f3460',
            'text_primary': '#00ff41',
            'text_secondary': '#0f3460',
            'text_muted': '#636e72',
            'error': '#ff4757'
        }
    },
    'dark': {
        'name': 'Dark',
        'description': 'Классическая темная тема',
        'colors': {
            'background': '#1e1e1e',
            'secondary_bg': '#252526',
            'accent': '#007acc',
            'border': '#3e3e42',
            'text_primary': '#cccccc',
            'text_secondary': '#858585',
            'text_muted': '#6a6a6a',
            'error': '#f48771'
        }
    },
    'light': {
        'name': 'Light',
        'description': 'Светлая тема для дневного использования',
        'colors': {
            'background': '#ffffff',
            'secondary_bg': '#f5f5f5',
            'accent': '#0078d4',
            'border': '#e1e1e1',
            'text_primary': '#1e1e1e',
            'text_secondary': '#666666',
            'text_muted': '#999999',
            'error': '#d13438'
        }
    },
    'purple': {
        'name': 'Purple',
        'description': 'Фиолетовая тема с мягкими оттенками',
        'colors': {
            'background': '#2d1b3d',
            'secondary_bg': '#3d2b4d',
            'accent': '#b794f6',
            'border': '#5a4a6a',
            'text_primary': '#b794f6',
            'text_secondary': '#8b7a9b',
            'text_muted': '#6a5a7a',
            'error': '#f56565'
        }
    },
    'ocean': {
        'name': 'Ocean',
        'description': 'Морская тема с голубыми оттенками',
        'colors': {
            'background': '#0a1929',
            'secondary_bg': '#132f4c',
            'accent': '#64b5f6',
            'border': '#1e3a5f',
            'text_primary': '#64b5f6',
            'text_secondary': '#4a90a4',
            'text_muted': '#3a7080',
            'error': '#ef5350'
        }
    }
}


def get_theme(theme_name: str) -> Dict[str, Any]:
    """
    Получение темы по имени.
    
    Args:
        theme_name: Имя темы
        
    Returns:
        Словарь с определением темы или тема по умолчанию
    """
    return THEMES.get(theme_name, THEMES['nocturne'])


def get_theme_names() -> list:
    """
    Получение списка всех доступных тем.
    
    Returns:
        Список имен тем
    """
    return list(THEMES.keys())


def get_theme_info(theme_name: str) -> Dict[str, str]:
    """
    Получение информации о теме (имя и описание).
    
    Args:
        theme_name: Имя темы
        
    Returns:
        Словарь с информацией о теме
    """
    theme = get_theme(theme_name)
    return {
        'name': theme['name'],
        'description': theme['description']
    }

