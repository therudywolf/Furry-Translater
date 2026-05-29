# 🐺 UWU Furry Translator

> Трансформация обычного текста в милый «uwu» стиль с волчьей тематикой. Три варианта: Python GUI, AutoHotkey и Web (с AI-чатом).

![Version](https://img.shields.io/badge/version-0.9.0-4c8bf5)
![Status](https://img.shields.io/badge/status-active-22c55e)
[![License](https://img.shields.io/badge/license-AGPL--3.0--or--later-22c55e)](LICENSE)
[![Secret scan](https://github.com/therudywolf/Furry-Translater/actions/workflows/gitleaks.yml/badge.svg)](.github/workflows/gitleaks.yml)

Доступно три варианта реализации: **Python GUI**, **AutoHotkey скрипт** и **Web-приложение** с пятью персонажами-волками и опциональным AI-чатом через локальную LLM (LM Studio / Ollama / любой OpenAI-совместимый сервер).

---

## 📋 Содержание

- [Возможности](#-возможности)
- [Варианты реализации](#-варианты-реализации)
- [Быстрый старт](#-быстрый-старт)
- [AI-чат и деплой Web](#-ai-чат-и-деплой-web)
- [Примеры работы](#-примеры-работы)
- [Архитектура](#-архитектура)
- [Безопасность](#-безопасность)
- [FAQ](#-faq)
- [Лицензия](#-лицензия)

---

## ✨ Возможности

**Общее для всех вариантов:**

- **Словарные замены**: сотни слов → милые версии (волчья тематика, кибер-сленг, и т.д.)
- **Фонетические мутации**: русский `р`→`ль`, `л`→`лью`; английский `r/l`→`w`, `n`→`ny`
- **Волчьи звуки**: случайные вставки (`*виляет хвостиком*`, `гав~`, `OwO`, `▓▒░`)

**Уникальное:**

- **Python**: GUI с автоконвертом, темами, историей и настройками
- **AutoHotkey**: горячие клавиши, трансформация в любом приложении Windows, регулировка интенсивности
- **Web**: 5 персонажей-волков, динамические темы/анимации, **AI-чат** с локальной LLM

---

## 🎯 Варианты реализации

| Функция                   | Python | AutoHotkey   | Web               |
| ------------------------- | ------ | ------------ | ----------------- |
| GUI интерфейс             | ✅     | ❌           | ✅                |
| Горячие клавиши           | ❌     | ✅           | ❌                |
| Автоконверт               | ✅     | ❌           | ✅                |
| Работа в любом приложении | ❌     | ✅           | ❌                |
| Несколько персонажей      | ❌     | ❌           | ✅ (5)            |
| AI-чат                    | ❌     | ❌           | ✅                |
| Кроссплатформенность      | ✅     | ❌ (Windows) | ✅                |

---

## 🚀 Быстрый старт

### Python GUI

```bash
cd Python
pip install -r requirements.txt   # pyperclip
python uwu.py
```

### AutoHotkey (Windows)

1. Установите [AutoHotkey v2.0](https://www.autohotkey.com/).
2. Запустите `Script/UwuConverter.ahk` (иконка появится в трее).
3. Выделите текст → **Ctrl+Shift+U**. Настройки — в `Script/config.ini`.

Горячие клавиши: `Ctrl+Shift+U` трансформировать · `Ctrl+Shift+I` интенсивность (1-10) · `Ctrl+Shift+P` пауза · `Ctrl+Shift+H` справка.

### Web (переводчик)

Переводчик работает без всякой настройки — просто откройте `Web/forestchat.html` в браузере. Для **AI-чата** нужен запущенный сервер — см. ниже.

---

## 🧠 AI-чат и деплой Web

AI-чат опционален. Без LLM персонажи отвечают заготовленными репликами; с LLM — генерируют ответы вживую. Поддерживается любой OpenAI-совместимый сервер: **LM Studio**, **Ollama**, и т.п.

### Рекомендуемый способ — обратный прокси (Docker)

В этом режиме nginx проксирует запросы к LLM и **сам добавляет API-ключ на сервере**. Ключ хранится только в `.env`, не попадает в браузер, и нет проблем с CORS.

```bash
cp .env.example .env        # затем впишите свои значения
docker compose up --build
# открыть http://localhost:8080
```

`.env`:

```ini
LLM_UPSTREAM=https://your-lmstudio-host.example   # без хвостового /v1
LLM_API_KEY=sk-...                                # уйдёт в Authorization: Bearer
LLM_MODEL=google/gemma-4-e2b                        # см. GET /v1/models
LLM_REASONING_EFFORT=                               # пусто для gemma; none для Qwen3 (см. ниже)
LLM_MAX_TOKENS=600
WEB_PORT=8080
```

> **`.env` в `.gitignore` и никогда не коммитится.** Это единственное место, где живёт ключ.

Фронтенд при этом обращается к относительному `/api/llm`, а `config.js` генерируется контейнером и **не содержит секретов**.

### Альтернатива — прямое подключение (только для локального теста)

Браузер ходит в LLM напрямую. Подходит для локального LM Studio без авторизации. ⚠️ Если указать `API_KEY` здесь, он будет виден любому посетителю страницы (DevTools) — **не используйте на публичном сервере**.

```bash
cd Web
cp config.js.example config.js     # затем отредактируйте
```

```javascript
window.API_BASE_URL = 'http://127.0.0.1:1234';  // локальный LM Studio
window.MODEL_NAME    = 'google/gemma-4-e2b';
window.API_KEY       = '';                        // Bearer-токен, если нужен
```

### Про reasoning-модели (важно)

Разные модели ведут себя по-разному:

- **gemma** (`google/gemma-4-e2b`, по умолчанию): держит рассуждения в отдельном поле `reasoning_content`, а в `content` отдаёт чистый ответ. `reasoning_effort` слать **не нужно** — оставьте `LLM_REASONING_EFFORT=` пустым.
- **Qwen3** (`qwen/qwen3.5-9b`, `qwen3.6-27b`): **всегда «думают»** и могут потратить весь лимит токенов на рассуждения, вернув пустой ответ. Для них обязательно `LLM_REASONING_EFFORT=none`.

Приложение в любом случае убирает теги `<think>…</think>`, читает только `content` и при пустом ответе мягко падает на заготовленную реплику.

### Персонажи

🐺 **Ноктюрн** (киберволк) · 🚗 **Руди** (уличный) · 🎸 **Ник** (музыкант) · ☠️ **Смерть** (жнец) · 💕 **Феликс** (милый волчонок). У каждого свой словарь, звуки, system-prompt и набор заготовок.

---

## 📝 Примеры работы

**Вход:** `Привет, волк! Как дела?`
**Выход (Web, Ноктюрн):** `Пльивветик~, уольчек! Как дела? *клацает когтями* ▓▒░`

**Вход:** `Hello friend! The wolf is running in the dark night.`
**Выход:** `Hewwo fwend! The wuffie is wunning in the dark nitey. *воет на луну* OwO`

---

## 🏗️ Архитектура

```
Furry-Translater/
├── Python/                  # Python GUI
│   ├── uwu.py               # GUI (Tkinter)
│   ├── uwu_translator.py    # логика трансформации
│   ├── config.py            # константы UI
│   ├── settings.py          # настройки (settings.json)
│   ├── history.py           # история (history.json)
│   ├── themes.py            # темы оформления
│   └── tests/               # pytest
├── Script/                  # AutoHotkey
│   ├── UwuConverter.ahk
│   └── config.ini
├── Web/                     # Web-приложение
│   ├── forestchat.html      # разметка
│   ├── styles.css           # стили/анимации
│   ├── js/
│   │   ├── wolves.js        # данные персонажей
│   │   ├── translator.js    # uwu-трансформация (+ Node-экспорт для тестов)
│   │   ├── api.js           # вызовы LLM (Bearer, reasoning_effort, <think>-очистка)
│   │   └── app.js           # связывание UI
│   ├── config.js.example    # шаблон конфигурации (коммитится)
│   ├── config.js            # локальные настройки (в .gitignore)
│   ├── Dockerfile           # nginx + рендер конфига
│   └── docker/
│       ├── default.conf.template   # nginx: статика + /api/llm прокси
│       └── 40-render-config.sh     # генерация config.js из env
├── docker-compose.yml
├── .env.example             # шаблон секретов (коммитится)
└── .env                     # реальные секреты (в .gitignore)
```

**Алгоритм трансформации** (общий для всех вариантов): словарные замены целых слов → русская фонетика → английская фонетика → случайные звуки/символы после пунктуации.

**Поток AI-чата (прокси):** браузер → `/api/llm/v1/chat/completions` → nginx (добавляет `Authorization: Bearer …` из `.env`) → LLM-сервер.

---

## 🔐 Безопасность

- Ключ LLM — только в `.env` (gitignored), добавляется прокси на сервере.
- `Web/config.js`, `Python/settings.json`, `Python/history.json` — в `.gitignore`.
- Секрет-сканирование: [gitleaks](.gitleaks.toml) в CI и pre-commit.
- Перед публикацией проверьте, что в трекаемых файлах и истории нет ключей/паролей.
- Подробнее — [SECURITY.md](SECURITY.md).

---

## ❓ FAQ

**Какой вариант выбрать?** Python — GUI и кроссплатформенность; AutoHotkey — быстрая трансформация в любом окне Windows; Web — персонажи и AI-чат.

**AI-чат обязателен?** Нет. Переводчик и чат с заготовками работают без сервера.

**Чат отвечает пусто/медленно.** Reasoning-модель — см. [раздел выше](#про-reasoning-модели-важно): для Qwen3 поставьте `LLM_REASONING_EFFORT=none`, для gemma оставьте пусто; при необходимости поднимите `LLM_MAX_TOKENS`.

**Как добавить слова/персонажа?** Python — `uwu_translator.py` (`UWU_DICT`); AutoHotkey — `LoadDictionary()`; Web — `Web/js/wolves.js`.

**Случайно закоммитил ключ.** Немедленно отзовите/смените ключ на сервере, затем вычистите историю (`git filter-repo` / BFG) и проверьте GitHub → Security → Secret scanning.

---

## 📄 Лицензия

**GNU AGPL v3.0-or-later** (Copyleft). См. [LICENSE](LICENSE). SPDX: `AGPL-3.0-or-later`.

**Вой-вой! 🌙**
