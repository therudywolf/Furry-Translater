"""
Главный модуль UWU Translator - GUI приложение.

Содержит графический интерфейс на Tkinter для трансформации текста
в милый UWU-стиль с волчьей тематикой и кибер-эстетикой.

Зависимости:
    - tkinter: для GUI
    - pyperclip: для работы с буфером обмена (pip install pyperclip)
    - uwu_translator: модуль трансформации текста
    - config: модуль конфигурации
    - settings: модуль работы с настройками
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import pyperclip

from uwu_translator import UwuTranslator
from config import (
    WINDOW_TITLE, WINDOW_SIZE, WINDOW_BG,
    COLORS, FONTS, TEXT_FIELD_CONFIG, BUTTON_CONFIG,
    UI_TEXTS, AUTO_CONVERT_DELAY, COPY_NOTIFICATION_DURATION
)
from settings import load_settings, save_settings, get_setting, set_setting
from history import load_history, add_to_history, clear_history, get_history_count
from themes import get_theme, get_theme_names, get_theme_info


# ═══════════════════════════════════════════════════════════════
# КЛАСС ОКНА НАСТРОЕК
# ═══════════════════════════════════════════════════════════════

class SettingsWindow:
    """
    Окно настроек приложения.
    
    Позволяет пользователю настраивать:
    - Интенсивность трансформации
    - Автоконверт и его задержку
    - Вероятности звуков
    - Тему оформления
    """
    
    def __init__(self, parent, main_app):
        """
        Инициализация окна настроек.
        
        Args:
            parent: Родительское окно
            main_app: Экземпляр главного приложения (для применения настроек)
        """
        self.parent = parent
        self.main_app = main_app
        self.settings = load_settings()
        
        # Получаем цвета из текущей темы главного приложения
        self.colors = main_app.current_colors
        
        # Создаем окно настроек
        self.window = tk.Toplevel(parent)
        self.window.title("⚙️ Настройки")
        self.window.geometry("500x600")
        self.window.configure(bg=self.colors['background'])
        self.window.transient(parent)  # Модальное окно
        self.window.grab_set()  # Захватываем фокус
        
        # Переменные для виджетов
        self.intensity_var = tk.IntVar(value=self.settings.get('intensity', 5))
        self.auto_convert_var = tk.BooleanVar(value=self.settings.get('auto_convert', True))
        self.auto_convert_delay_var = tk.IntVar(value=self.settings.get('auto_convert_delay', 500))
        self.noise_prob_var = tk.DoubleVar(value=self.settings.get('noise_probability', 0.6))
        self.cyber_vibe_prob_var = tk.DoubleVar(value=self.settings.get('cyber_vibe_probability', 0.3))
        self.theme_var = tk.StringVar(value=self.settings.get('theme', 'nocturne'))
        
        # Ссылки на виджеты для обновления цветов
        self.widgets_to_update = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создание виджетов окна настроек."""
        # Заголовок
        title = tk.Label(
            self.window,
            text="⚙️ НАСТРОЙКИ",
            bg=self.colors['background'],
            fg=self.colors['accent'],
            font=('Courier', 16, 'bold')
        )
        title.pack(pady=20)
        
        # Фрейм для настроек с прокруткой
        canvas = tk.Canvas(self.window, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Интенсивность трансформации
        self._create_section(scrollable_frame, "Интенсивность трансформации")
        intensity_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        intensity_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            intensity_frame,
            text="Уровень милоты (1-10):",
            bg=self.colors['background'],
            fg=self.colors['text_primary'],
            font=FONTS['label']
        ).pack(side=tk.LEFT)
        
        intensity_scale = tk.Scale(
            intensity_frame,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.intensity_var,
            bg=self.colors['background'],
            fg=self.colors['accent'],
            highlightthickness=0,
            troughcolor=self.colors['secondary_bg'],
            activebackground=self.colors['accent']
        )
        intensity_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        intensity_label = tk.Label(
            intensity_frame,
            textvariable=self.intensity_var,
            bg=self.colors['background'],
            fg=self.colors['accent'],
            font=('Consolas', 12, 'bold'),
            width=3
        )
        intensity_label.pack(side=tk.LEFT)
        
        # Автоконверт
        self._create_section(scrollable_frame, "Автоматическая трансформация")
        auto_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        auto_frame.pack(fill=tk.X, padx=20, pady=5)
        
        auto_check = tk.Checkbutton(
            auto_frame,
            text="Включить автоконверт при вводе",
            variable=self.auto_convert_var,
            bg=self.colors['background'],
            fg=self.colors['text_primary'],
            selectcolor=self.colors['secondary_bg'],
            activebackground=self.colors['background'],
            activeforeground=self.colors['accent'],
            font=FONTS['label']
        )
        auto_check.pack(anchor=tk.W)
        
        delay_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        delay_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            delay_frame,
            text="Задержка автоконверта (мс):",
            bg=self.colors['background'],
            fg=self.colors['text_primary'],
            font=FONTS['label']
        ).pack(side=tk.LEFT)
        
        delay_scale = tk.Scale(
            delay_frame,
            from_=100,
            to=2000,
            orient=tk.HORIZONTAL,
            variable=self.auto_convert_delay_var,
            bg=self.colors['background'],
            fg=self.colors['accent'],
            highlightthickness=0,
            troughcolor=self.colors['secondary_bg'],
            activebackground=self.colors['accent'],
            resolution=50
        )
        delay_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        delay_label = tk.Label(
            delay_frame,
            textvariable=self.auto_convert_delay_var,
            bg=self.colors['background'],
            fg=self.colors['accent'],
            font=('Consolas', 10),
            width=5
        )
        delay_label.pack(side=tk.LEFT)
        
        # Вероятности звуков
        self._create_section(scrollable_frame, "Вероятности звуков")
        
        noise_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        noise_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            noise_frame,
            text="Волчьи звуки:",
            bg=self.colors['background'],
            fg=self.colors['text_primary'],
            font=FONTS['label']
        ).pack(side=tk.LEFT)
        
        noise_scale = tk.Scale(
            noise_frame,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.noise_prob_var,
            bg=self.colors['background'],
            fg=self.colors['accent'],
            highlightthickness=0,
            troughcolor=self.colors['secondary_bg'],
            activebackground=self.colors['accent'],
            resolution=0.1
        )
        noise_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        noise_label = tk.Label(
            noise_frame,
            textvariable=self.noise_prob_var,
            bg=self.colors['background'],
            fg=self.colors['accent'],
            font=('Consolas', 10),
            width=5
        )
        noise_label.pack(side=tk.LEFT)
        
        cyber_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        cyber_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            cyber_frame,
            text="Кибер-символы:",
            bg=self.colors['background'],
            fg=self.colors['text_primary'],
            font=FONTS['label']
        ).pack(side=tk.LEFT)
        
        cyber_scale = tk.Scale(
            cyber_frame,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.cyber_vibe_prob_var,
            bg=self.colors['background'],
            fg=self.colors['accent'],
            highlightthickness=0,
            troughcolor=self.colors['secondary_bg'],
            activebackground=self.colors['accent'],
            resolution=0.1
        )
        cyber_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        cyber_label = tk.Label(
            cyber_frame,
            textvariable=self.cyber_vibe_prob_var,
            bg=self.colors['background'],
            fg=self.colors['accent'],
            font=('Consolas', 10),
            width=5
        )
        cyber_label.pack(side=tk.LEFT)
        
        # Тема оформления
        self._create_section(scrollable_frame, "Тема оформления")
        theme_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        theme_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            theme_frame,
            text="Выберите тему:",
            bg=self.colors['background'],
            fg=self.colors['text_primary'],
            font=FONTS['label']
        ).pack(anchor=tk.W, pady=5)
        
        theme_listbox = tk.Listbox(
            theme_frame,
            listvariable=tk.StringVar(value=get_theme_names()),
            height=5,
            bg=self.colors['secondary_bg'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['background'],
            font=FONTS['label'],
            relief=tk.FLAT,
            borderwidth=2
        )
        theme_listbox.pack(fill=tk.X, pady=5)
        
        # Выбираем текущую тему
        current_theme = self.theme_var.get()
        if current_theme in get_theme_names():
            theme_listbox.selection_set(get_theme_names().index(current_theme))
        
        # Привязка выбора темы
        def on_theme_select(event):
            selection = theme_listbox.curselection()
            if selection:
                selected_theme = get_theme_names()[selection[0]]
                self.theme_var.set(selected_theme)
                # Показываем описание темы
                theme_info = get_theme_info(selected_theme)
                theme_desc_label.config(text=theme_info['description'])
        
        theme_listbox.bind('<<ListboxSelect>>', on_theme_select)
        
        theme_desc_label = tk.Label(
            theme_frame,
            text=get_theme_info(self.theme_var.get())['description'],
            bg=self.colors['background'],
            fg=self.colors['text_muted'],
            font=('Consolas', 9, 'italic'),
            wraplength=400
        )
        theme_desc_label.pack(anchor=tk.W, pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        btn_frame.pack(pady=30)
        
        save_btn = tk.Button(
            btn_frame,
            text="💾 СОХРАНИТЬ",
            command=self.save_and_close,
            **BUTTON_CONFIG['action']
        )
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ ОТМЕНА",
            command=self.window.destroy,
            **BUTTON_CONFIG['clear']
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Упаковка canvas и scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_section(self, parent, title):
        """Создание секции с заголовком."""
        section = tk.Label(
            parent,
            text=f"▼ {title}",
            bg=self.colors['background'],
            fg=self.colors['text_secondary'],
            font=('Consolas', 11, 'bold'),
            anchor=tk.W
        )
        section.pack(fill=tk.X, padx=20, pady=(15, 5))
    
    def save_and_close(self):
        """Сохранение настроек и закрытие окна."""
        # Собираем настройки
        new_settings = {
            'intensity': self.intensity_var.get(),
            'auto_convert': self.auto_convert_var.get(),
            'auto_convert_delay': self.auto_convert_delay_var.get(),
            'noise_probability': round(self.noise_prob_var.get(), 2),
            'cyber_vibe_probability': round(self.cyber_vibe_prob_var.get(), 2),
            'theme': self.theme_var.get()
        }
        
        # Сохраняем
        if save_settings(new_settings):
            # Применяем настройки в главном приложении
            self.main_app.apply_settings(new_settings)
            messagebox.showinfo("Успех", "Настройки сохранены! *одобрительно рычит*")
            self.window.destroy()
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить настройки")


# ═══════════════════════════════════════════════════════════════
# КЛАСС ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
# ═══════════════════════════════════════════════════════════════

class WolfTranslatorGUI:
    """
    Главный класс GUI приложения для UWU трансформации.
    
    Предоставляет интерфейс с двумя текстовыми полями:
    - Input: для ввода исходного текста
    - Output: для отображения трансформированного текста
    
    Функциональность:
    - Автоматическая трансформация при вводе (с задержкой)
    - Копирование результата в буфер обмена
    - Выделение и копирование части текста
    - Очистка полей ввода/вывода
    - Настройки приложения
    """
    
    def __init__(self, root: tk.Tk):
        """
        Инициализация GUI приложения.
        
        Создает все элементы интерфейса: заголовок, поля ввода/вывода,
        кнопки управления и футер.
        
        Args:
            root: Корневое окно Tkinter
        """
        self.root = root
        self.settings = load_settings()
        
        # Загружаем текущую тему
        self.current_theme = get_theme(self.settings.get('theme', 'nocturne'))
        self.current_colors = self.current_theme['colors']
        
        # Создаем трансформатор с настройками
        self.translator = UwuTranslator(
            noise_probability=self.settings.get('noise_probability', 0.6),
            cyber_vibe_probability=self.settings.get('cyber_vibe_probability', 0.3)
        )
        
        self._setup_window()
        self._create_menu()
        self._create_widgets()
        
        # Переменная для хранения задачи автоконверта
        self.convert_job = None
        
        # Применяем настройки
        self.apply_settings(self.settings)
    
    def _setup_window(self):
        """Настройка основного окна приложения."""
        self.root.title(WINDOW_TITLE)
        
        # Размер окна из настроек
        width = self.settings.get('window_width', 700)
        height = self.settings.get('window_height', 600)
        self.root.geometry(f"{width}x{height}")
        
        self.root.configure(bg=self.current_colors['background'])
    
    def _create_menu(self):
        """Создание меню-бара."""
        menubar = tk.Menu(self.root, bg=COLORS['secondary_bg'], fg=COLORS['text_primary'])
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.current_colors['secondary_bg'], fg=self.current_colors['text_primary'])
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Очистить всё", command=self.clear_all, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Меню "Правка"
        edit_menu = tk.Menu(menubar, tearoff=0, bg=self.current_colors['secondary_bg'], fg=self.current_colors['text_primary'])
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Копировать результат", command=self.copy_output, accelerator="Ctrl+C")
        edit_menu.add_command(label="Трансформировать", command=self.convert, accelerator="Ctrl+Enter")
        edit_menu.add_separator()
        edit_menu.add_command(label="📜 История", command=self.open_history, accelerator="Ctrl+H")
        
        # Меню "Настройки"
        settings_menu = tk.Menu(menubar, tearoff=0, bg=self.current_colors['secondary_bg'], fg=self.current_colors['text_primary'])
        menubar.add_cascade(label="Настройки", menu=settings_menu)
        settings_menu.add_command(label="⚙️ Настройки...", command=self.open_settings, accelerator="Ctrl+,")
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.current_colors['secondary_bg'], fg=self.current_colors['text_primary'])
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        
        # Горячие клавиши
        self.root.bind('<Control-n>', lambda e: self.clear_all())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-comma>', lambda e: self.open_settings())
        self.root.bind('<Control-Return>', lambda e: self.convert())
        self.root.bind('<Control-h>', lambda e: self.open_history())
    
    def _create_widgets(self):
        """Создание всех виджетов интерфейса."""
        self._create_title()
        self._create_input_section()
        self._create_buttons()
        self._create_output_section()
        self._create_footer()
    
    def _create_title(self):
        """Создание заголовка приложения."""
        self.title_label = tk.Label(
            self.root,
            text=UI_TEXTS['title'],
            bg=self.current_colors['background'],
            fg=self.current_colors['accent'],
            font=FONTS['title']
        )
        self.title_label.pack(pady=10)
        
    def _create_input_section(self):
        """Создание секции ввода текста."""
        # Метка для поля ввода
        self.input_label = tk.Label(
            self.root,
            text=UI_TEXTS['input_label'],
            bg=self.current_colors['background'],
            fg=self.current_colors['text_secondary'],
            font=FONTS['label']
        )
        self.input_label.pack(pady=(10, 5))
        
        # Текстовое поле ввода с прокруткой
        self.input_box = scrolledtext.ScrolledText(
            self.root,
            width=TEXT_FIELD_CONFIG['width'],
            height=TEXT_FIELD_CONFIG['height'],
            bg=self.current_colors['secondary_bg'],
            fg=self.current_colors['text_primary'],
            insertbackground=self.current_colors['accent'],
            font=FONTS['text'],
            relief=tk.FLAT,
            borderwidth=2
        )
        self.input_box.pack(padx=15, pady=5)
        
        # Привязка событий для автоконверта (если включен)
        self.input_box.bind('<Control-v>', lambda e: self.root.after(10, self.convert))
        self.input_box.bind('<Command-v>', lambda e: self.root.after(10, self.convert))
        self.input_box.bind('<KeyRelease>', lambda e: self.auto_convert_delayed())
        
    def _create_buttons(self):
        """Создание панели кнопок управления."""
        self.btn_frame = tk.Frame(self.root, bg=self.current_colors['background'])
        self.btn_frame.pack(pady=10)
        
        # Кнопка трансформации
        self.convert_btn = tk.Button(
            self.btn_frame,
            text="⚡ TRANSFORM ⚡", 
            command=self.convert,
            bg=self.current_colors['border'],
            fg=self.current_colors['accent'],
            activebackground=self.current_colors['accent'],
            activeforeground=self.current_colors['background'],
            font=('Consolas', 11, 'bold'),
            relief=tk.RAISED,
            borderwidth=3,
            padx=20
        )
        self.convert_btn.grid(row=0, column=0, padx=10)
        
        # Кнопка копирования
        self.copy_btn = tk.Button(
            self.btn_frame,
            text="📋 COPY OUTPUT",
            command=self.copy_output,
            bg=self.current_colors['secondary_bg'],
            fg=self.current_colors['accent'],
            font=('Consolas', 10),
            relief=tk.RAISED,
            borderwidth=2,
            padx=15
        )
        self.copy_btn.grid(row=0, column=1, padx=10)
        
        # Кнопка очистки
        self.clear_btn = tk.Button(
            self.btn_frame,
            text="🗑 CLEAR",
            command=self.clear_all,
            bg=self.current_colors['secondary_bg'],
            fg=self.current_colors['error'],
            font=('Consolas', 10),
            relief=tk.RAISED,
            borderwidth=2,
            padx=15
        )
        self.clear_btn.grid(row=0, column=2, padx=10)
        
        # Кнопка настроек
        self.settings_btn = tk.Button(
            self.btn_frame,
            text="⚙️ SETTINGS",
            command=self.open_settings,
            bg=self.current_colors['secondary_bg'],
            fg=self.current_colors['accent'],
            font=('Consolas', 10),
            relief=tk.RAISED,
            borderwidth=2,
            padx=15
        )
        self.settings_btn.grid(row=0, column=3, padx=10)
    
    def _create_output_section(self):
        """Создание секции вывода трансформированного текста."""
        # Метка для поля вывода
        self.output_label = tk.Label(
            self.root,
            text=UI_TEXTS['output_label'],
            bg=self.current_colors['background'],
            fg=self.current_colors['text_secondary'],
            font=FONTS['label']
        )
        self.output_label.pack(pady=(10, 5))
        
        # Текстовое поле вывода с прокруткой
        self.output_box = scrolledtext.ScrolledText(
            self.root,
            width=TEXT_FIELD_CONFIG['width'],
            height=TEXT_FIELD_CONFIG['height'],
            bg=self.current_colors['secondary_bg'],
            fg=self.current_colors['text_primary'],
            insertbackground=self.current_colors['accent'],
            font=FONTS['text'],
            relief=tk.FLAT,
            borderwidth=2
        )
        self.output_box.pack(padx=15, pady=5)
        
        # Привязка событий для работы с выделенным текстом
        self.output_box.bind('<Control-c>', self.copy_selection)
        self.output_box.bind('<Command-c>', self.copy_selection)
        self.output_box.bind('<Control-a>', self.select_all_output)
        self.output_box.bind('<Button-1>', lambda e: 'break')
        
    def _create_footer(self):
        """Создание футера приложения."""
        self.footer_label = tk.Label(
            self.root,
            text=UI_TEXTS['footer'],
            bg=self.current_colors['background'],
            fg=self.current_colors['text_muted'],
            font=FONTS['footer']
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=10)
        
    # ═══════════════════════════════════════════════════════════
    # МЕТОДЫ ТРАНСФОРМАЦИИ
    # ═══════════════════════════════════════════════════════════
    
    def convert(self):
        """
        Основная функция трансформации текста.
        
        Получает текст из поля ввода, трансформирует его через
        uwu_translate() и выводит результат в поле вывода.
        Если поле ввода пустое, показывает сообщение об этом.
        """
        input_text = self.input_box.get("1.0", tk.END).strip()
        
        if not input_text:
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, UI_TEXTS['empty_message'])
            return
        
        # Трансформация текста через экземпляр трансформатора
        output = self.translator.translate(input_text)
        
        # Сохраняем в историю
        add_to_history(input_text, output)
        
        # Вывод результата
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, output)
    
    def auto_convert_delayed(self):
        """
        Автоматическая трансформация с задержкой.
        
        Отменяет предыдущую запланированную трансформацию и
        планирует новую через заданную задержку.
        Работает только если автоконверт включен в настройках.
        """
        # Проверяем, включен ли автоконверт
        if not self.settings.get('auto_convert', True):
            return
        
        # Отменяем предыдущую задачу, если она есть
        if self.convert_job:
            self.root.after_cancel(self.convert_job)
        
        # Получаем задержку из настроек
        delay = self.settings.get('auto_convert_delay', AUTO_CONVERT_DELAY)
        
        # Планируем новую трансформацию
        self.convert_job = self.root.after(delay, self.convert)
    
    # ═══════════════════════════════════════════════════════════
    # МЕТОДЫ РАБОТЫ С БУФЕРОМ ОБМЕНА
    # ═══════════════════════════════════════════════════════════
    
    def copy_output(self):
        """
        Копирование всего содержимого поля вывода в буфер обмена.
        
        После копирования временно показывает уведомление
        в поле вывода, затем восстанавливает исходный текст.
        """
        output_text = self.output_box.get("1.0", tk.END).strip()
        
        if not output_text:
            return
        
        try:
            pyperclip.copy(output_text)
            
            original_text = self.output_box.get("1.0", tk.END)
            
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, UI_TEXTS['copied_message'])
            
            self.root.after(
                COPY_NOTIFICATION_DURATION,
                lambda: self.restore_output(original_text)
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Не удалось скопировать *скулит*\n{str(e)}"
            )
    
    def restore_output(self, text: str):
        """
        Восстановление текста в поле вывода после уведомления.
        
        Args:
            text: Текст для восстановления
        """
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, text.strip())
    
    def copy_selection(self, event=None):
        """
        Копирование выделенного текста из поля вывода.
        
        Обработчик события Ctrl+C / Cmd+C для копирования
        выделенного фрагмента текста.
        
        Args:
            event: Событие клавиатуры (необязательно)
            
        Returns:
            'break' для предотвращения стандартной обработки
        """
        try:
            # Получаем выделенный текст
            selected = self.output_box.get(tk.SEL_FIRST, tk.SEL_LAST)
            pyperclip.copy(selected)
        except tk.TclError:
            # Если ничего не выделено, просто игнорируем
            pass
        
        return 'break'
    
    def select_all_output(self, event=None):
        """
        Выделение всего текста в поле вывода.
        
        Обработчик события Ctrl+A для выделения всего содержимого.
        
        Args:
            event: Событие клавиатуры (необязательно)
            
        Returns:
            'break' для предотвращения стандартной обработки
        """
        self.output_box.tag_add(tk.SEL, "1.0", tk.END)
        self.output_box.mark_set(tk.INSERT, "1.0")
        self.output_box.see(tk.INSERT)
        return 'break'
    
    # ═══════════════════════════════════════════════════════════
    # МЕТОДЫ УПРАВЛЕНИЯ И НАСТРОЕК
    # ═══════════════════════════════════════════════════════════
    
    def clear_all(self):
        """Очистка всех полей ввода и вывода."""
        self.input_box.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)

    def open_settings(self):
        """Открытие окна настроек."""
        SettingsWindow(self.root, self)
    
    def open_history(self):
        """Открытие окна истории трансформаций."""
        HistoryWindow(self.root)
    
    def apply_settings(self, settings: dict):
        """
        Применение настроек к приложению.
        
        Args:
            settings: Словарь с настройками
        """
        self.settings = settings
        
        # Обновляем трансформатор с новыми вероятностями
        self.translator.noise_probability = settings.get('noise_probability', 0.6)
        self.translator.cyber_vibe_probability = settings.get('cyber_vibe_probability', 0.3)
        
        # Обновляем размер окна, если изменился
        width = settings.get('window_width', 700)
        height = settings.get('window_height', 600)
        self.root.geometry(f"{width}x{height}")
        
        # Применяем тему, если изменилась
        new_theme_name = settings.get('theme', 'nocturne')
        current_theme_name = self.settings.get('theme', 'nocturne')
        if new_theme_name != current_theme_name:
            self.apply_theme(new_theme_name)
    
    def apply_theme(self, theme_name: str):
        """
        Применение темы оформления.
        
        Args:
            theme_name: Имя темы
        """
        self.current_theme = get_theme(theme_name)
        self.current_colors = self.current_theme['colors']
        
        # Обновляем цвета всех виджетов
        self.root.configure(bg=self.current_colors['background'])
        
        if hasattr(self, 'title_label'):
            self.title_label.configure(
                bg=self.current_colors['background'],
                fg=self.current_colors['accent']
            )
        
        if hasattr(self, 'input_label'):
            self.input_label.configure(
                bg=self.current_colors['background'],
                fg=self.current_colors['text_secondary']
            )
        
        if hasattr(self, 'output_label'):
            self.output_label.configure(
                bg=self.current_colors['background'],
                fg=self.current_colors['text_secondary']
            )
        
        if hasattr(self, 'footer_label'):
            self.footer_label.configure(
                bg=self.current_colors['background'],
                fg=self.current_colors['text_muted']
            )
        
        if hasattr(self, 'btn_frame'):
            self.btn_frame.configure(bg=self.current_colors['background'])
        
        if hasattr(self, 'input_box'):
            self.input_box.configure(
                bg=self.current_colors['secondary_bg'],
                fg=self.current_colors['text_primary'],
                insertbackground=self.current_colors['accent']
            )
        
        if hasattr(self, 'output_box'):
            self.output_box.configure(
                bg=self.current_colors['secondary_bg'],
                fg=self.current_colors['text_primary'],
                insertbackground=self.current_colors['accent']
            )
        
        if hasattr(self, 'convert_btn'):
            self.convert_btn.configure(
                bg=self.current_colors['border'],
                fg=self.current_colors['accent'],
                activebackground=self.current_colors['accent'],
                activeforeground=self.current_colors['background']
            )
        
        if hasattr(self, 'copy_btn'):
            self.copy_btn.configure(
                bg=self.current_colors['secondary_bg'],
                fg=self.current_colors['accent']
            )
        
        if hasattr(self, 'clear_btn'):
            self.clear_btn.configure(
                bg=self.current_colors['secondary_bg'],
                fg=self.current_colors['error']
            )
        
        if hasattr(self, 'settings_btn'):
            self.settings_btn.configure(
                bg=self.current_colors['secondary_bg'],
                fg=self.current_colors['accent']
            )
    
    def show_about(self):
        """Показ окна 'О программе'."""
        about_text = f"""
🐺 UWU Furry Translator v2.0

Проект для трансформации текста в милый "uwu" стиль
с волчьей тематикой и кибер-эстетикой.

Автор: contributors
Repository: community maintained

Версия: 2.0
Python: {__import__('sys').version.split()[0]}

*клацает когтями* | Nocturne Protocol
        """
        messagebox.showinfo("О программе", about_text.strip())


# ═══════════════════════════════════════════════════════════════
# КЛАСС ОКНА ИСТОРИИ
# ═══════════════════════════════════════════════════════════════

class HistoryWindow:
    """
    Окно истории трансформаций.
    
    Показывает последние 50 трансформаций с возможностью
    копирования и очистки истории.
    """
    
    def __init__(self, parent):
        """
        Инициализация окна истории.
        
        Args:
            parent: Родительское окно
        """
        self.parent = parent
        self.history = load_history()
        
        # Создаем окно истории
        self.window = tk.Toplevel(parent)
        self.window.title("📜 История трансформаций")
        self.window.geometry("800x600")
        self.window.configure(bg=WINDOW_BG)
        self.window.transient(parent)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создание виджетов окна истории."""
        # Заголовок
        header_frame = tk.Frame(self.window, bg=WINDOW_BG)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        title = tk.Label(
            header_frame,
            text="📜 ИСТОРИЯ ТРАНСФОРМАЦИЙ",
            bg=WINDOW_BG,
            fg=COLORS['accent'],
            font=('Courier', 14, 'bold')
        )
        title.pack(side=tk.LEFT)
        
        count_label = tk.Label(
            header_frame,
            text=f"({len(self.history)} записей)",
            bg=WINDOW_BG,
            fg=COLORS['text_muted'],
            font=FONTS['label']
        )
        count_label.pack(side=tk.LEFT, padx=10)
        
        # Кнопки управления
        btn_frame = tk.Frame(header_frame, bg=WINDOW_BG)
        btn_frame.pack(side=tk.RIGHT)
        
        clear_btn = tk.Button(
            btn_frame,
            text="🗑 Очистить",
            command=self.clear_history,
            **BUTTON_CONFIG['clear']
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            btn_frame,
            text="🔄 Обновить",
            command=self.refresh_history,
            **BUTTON_CONFIG['action']
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Список истории с прокруткой
        list_frame = tk.Frame(self.window, bg=WINDOW_BG)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            list_frame,
            bg=COLORS['secondary_bg'],
            fg=COLORS['text_primary'],
            selectbackground=COLORS['accent'],
            selectforeground=COLORS['background'],
            font=('Consolas', 9),
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            borderwidth=2
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Заполняем список
        self._populate_list()
        
        # Двойной клик для копирования
        self.history_listbox.bind('<Double-Button-1>', self.copy_selected)
        
        # Кнопки действий
        action_frame = tk.Frame(self.window, bg=WINDOW_BG)
        action_frame.pack(fill=tk.X, padx=15, pady=10)
        
        copy_btn = tk.Button(
            action_frame,
            text="📋 Копировать выделенное",
            command=self.copy_selected,
            **BUTTON_CONFIG['action']
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            action_frame,
            text="❌ Закрыть",
            command=self.window.destroy,
            **BUTTON_CONFIG['clear']
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    def _populate_list(self):
        """Заполнение списка истории."""
        self.history_listbox.delete(0, tk.END)
        
        if not self.history:
            self.history_listbox.insert(0, "История пуста *принюхивается*")
            return
        
        # Показываем в обратном порядке (новые сверху)
        for i, entry in enumerate(reversed(self.history)):
            timestamp = entry.get('timestamp', '')
            original = entry.get('original', '')[:50]  # Первые 50 символов
            if len(entry.get('original', '')) > 50:
                original += '...'
            
            # Форматируем дату
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M:%S")
            except:
                time_str = timestamp[:8] if len(timestamp) > 8 else timestamp
            
            display_text = f"[{time_str}] {original}"
            self.history_listbox.insert(0, display_text)
    
    def copy_selected(self, event=None):
        """Копирование выделенной записи в буфер обмена."""
        selection = self.history_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        # Инвертируем индекс (список в обратном порядке)
        real_index = len(self.history) - 1 - index
        
        if 0 <= real_index < len(self.history):
            entry = self.history[real_index]
            transformed = entry.get('transformed', '')
            
            try:
                pyperclip.copy(transformed)
                messagebox.showinfo("Успех", "Текст скопирован в буфер обмена! *виляет хвостиком*")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось скопировать: {e}")
    
    def clear_history(self):
        """Очистка истории."""
        if messagebox.askyesno("Подтверждение", "Очистить всю историю? *навострил уши*"):
            if clear_history():
                self.history = []
                self._populate_list()
                messagebox.showinfo("Успех", "История очищена! *одобрительно рычит*")
    
    def refresh_history(self):
        """Обновление истории из файла."""
        from history import load_history
        self.history = load_history()
        self._populate_list()


# ═══════════════════════════════════════════════════════════════
# ТОЧКА ВХОДА ПРИЛОЖЕНИЯ
# ═══════════════════════════════════════════════════════════════

def main():
    """
    Главная функция запуска приложения.
    
    Создает корневое окно Tkinter, инициализирует GUI
    и запускает главный цикл обработки событий.
    """
    root = tk.Tk()
    app = WolfTranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
