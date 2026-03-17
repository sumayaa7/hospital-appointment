# Как запустить 4everCare (каждый раз, чтобы даты совпадали)

Делай эти шаги **в день презентации** (или когда хочешь свежие даты).

---

## Шаг 1. Открой PowerShell

- Нажми `Win + X` → выбери **Windows PowerShell** (или **Terminal**).
- Либо в поиске Windows введи `PowerShell` и открой.

---

## Шаг 2. Перейди в папку проекта

Скопируй и вставь в PowerShell, нажми Enter:

```powershell
cd C:\Users\Administrator\hospital-appointment
```

---

## Шаг 3. Обнови базу под сегодняшний день

Эта команда создаёт/пересоздаёт слоты на **сегодня + следующие 5 дней**.  
Скопируй и вставь, нажми Enter:

```powershell
.\.venv\Scripts\python.exe app.py init-db
```

Должно появиться: `Initialized database with demo data.`

- Если вместо этого ошибка **"cannot be loaded because running scripts is disabled"** — переходи к **Варианту Б** внизу.
- Если ошибка **"No module named 'dotenv'"** — значит, ты вызвала `py app.py ...` без пути к `.venv`. Всегда используй **полный путь** `.\.venv\Scripts\python.exe app.py ...`.

---

## Шаг 4. Запусти сервер

Скопируй и вставь, нажми Enter:

```powershell
.\.venv\Scripts\python.exe app.py run
```

Должно появиться что‑то вроде:
```
* Running on http://127.0.0.1:5000
```

Окно PowerShell **не закрывай** — пока оно открыто, сайт работает.

---

## Шаг 5. Открой сайт в браузере

- Открой браузер (Chrome, Edge и т.д.).
- В адресной строке введи: **http://127.0.0.1:5000/**
- Нажми Enter.

Сверху увидишь кнопки дней (например Mar 16, Mar 17, …) — это и есть актуальные даты на сегодня.

---

## Кратко: порядок каждый раз

1. `cd C:\Users\Administrator\hospital-appointment`
2. `.\.venv\Scripts\python.exe app.py init-db`   ← обновляет даты
3. `.\.venv\Scripts\python.exe app.py run`      ← запускает сервер
4. В браузере открыть **http://127.0.0.1:5000/**

Чтобы остановить сервер: в окне PowerShell нажми **Ctrl+C**.

---

## Вариант Б: если PowerShell пишет "running scripts is disabled"

Тогда команду активации `.\.venv\Scripts\Activate.ps1` выполнить нельзя. Разрешить скрипты **один раз** (только для твоего пользователя):

1. Открой PowerShell **от имени администратора** (правый клик → «Запуск от имени администратора»).
2. Выполни:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. На вопрос ответь `Y` и Enter.
4. Закрой этот PowerShell. Дальше в обычном PowerShell можно использовать либо:
   - `.\.venv\Scripts\Activate.ps1` а потом `py app.py init-db` и `py app.py run`,
   - либо по‑прежнему **без активации**: `.\.venv\Scripts\python.exe app.py init-db` и `.\.venv\Scripts\python.exe app.py run`.

Лучше запомнить путь `.\.venv\Scripts\python.exe` — так всё будет работать даже без активации.
