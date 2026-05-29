"""
Конфигурационный модуль для UWU Translator.

Содержит все настройки приложения: цвета, размеры, шрифты,
словари трансформации и другие константы.
"""

# ═══════════════════════════════════════════════════════════════
# НАСТРОЙКИ GUI
# ═══════════════════════════════════════════════════════════════

# Настройки окна
WINDOW_TITLE = "🐺 Nocturne UWU Translator | Cyber Wolf Protocol"
WINDOW_SIZE = "700x600"
WINDOW_BG = '#1a1a2e'

# Цветовая схема (кибер-эстетика)
COLORS = {
    'background': '#1a1a2e',          # Основной фон
    'secondary_bg': '#16213e',         # Фон текстовых полей
    'accent': '#00ff41',               # Акцентный цвет (зеленый кибер)
    'border': '#0f3460',               # Цвет границ
    'text_primary': '#00ff41',         # Основной текст
    'text_secondary': '#0f3460',       # Вторичный текст
    'text_muted': '#636e72',           # Приглушенный текст
    'error': '#ff4757'                 # Цвет ошибок
}

# Шрифты
FONTS = {
    'title': ('Courier', 14, 'bold'),
    'label': ('Consolas', 10),
    'text': ('Consolas', 11),
    'footer': ('Courier', 9, 'italic')
}

# Настройки текстовых полей
TEXT_FIELD_CONFIG = {
    'width': 80,
    'height': 10,
    'bg': COLORS['secondary_bg'],
    'fg': COLORS['text_primary'],
    'insertbackground': COLORS['accent'],
    'font': FONTS['text'],
    'relief': 'flat',
    'borderwidth': 2
}

# Настройки кнопок
BUTTON_CONFIG = {
    'convert': {
        'bg': COLORS['border'],
        'fg': COLORS['accent'],
        'activebackground': COLORS['accent'],
        'activeforeground': COLORS['background'],
        'font': ('Consolas', 11, 'bold'),
        'relief': 'raised',
        'borderwidth': 3,
        'padx': 20
    },
    'action': {
        'bg': COLORS['secondary_bg'],
        'fg': COLORS['accent'],
        'font': ('Consolas', 10),
        'relief': 'raised',
        'borderwidth': 2,
        'padx': 15
    },
    'clear': {
        'bg': COLORS['secondary_bg'],
        'fg': COLORS['error'],
        'font': ('Consolas', 10),
        'relief': 'raised',
        'borderwidth': 2,
        'padx': 15
    }
}

# Тексты интерфейса
UI_TEXTS = {
    'title': "━━━━━ 🐺 NOCTURNE PROTOCOL: UWU MODE ━━━━━",
    'input_label': "▼ INPUT [normal text] *принюхивается*",
    'output_label': "▼ OUTPUT [uwu translated] *хвост вильнул*",
    'footer': "*клацает когтями* | Nocturne v2.0 | *неоновый отблеск*",
    'empty_message': "*принюхивается* Пусто... *уши прижал*",
    'copied_message': "✓ COPIED! *одобрительно рычит*"
}

# ═══════════════════════════════════════════════════════════════
# НАСТРОЙКИ ТРАНСФОРМАЦИИ
# ═══════════════════════════════════════════════════════════════

# Задержка автоконверта (в миллисекундах)
AUTO_CONVERT_DELAY = 500

# Вероятности добавления звуков
NOISE_PROBABILITY = 0.6      # 60% вероятность волчьих звуков
CYBER_VIBE_PROBABILITY = 0.3  # 30% вероятность кибер-символов

# Время отображения уведомления о копировании (в миллисекундах)
COPY_NOTIFICATION_DURATION = 800

