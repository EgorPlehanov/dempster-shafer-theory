# Инструкция по установке и запуску

## Предварительные требования

- Python 3.8 или выше
- pip (пакетный менеджер Python)

## Установка на Windows

1. **Скачайте Python** с [официального сайта](https://python.org) если еще не установлен

2. **Клонируйте репозиторий:**
```cmd
git clone https://github.com/your-username/dempster-shafer-theory.git
cd dempster-shafer-theory
```

3. **Создайте виртуальное окружение:**
```cmd
python -m venv dempster_venv
```

4. **Активируйте окружение:**
```cmd
dempster_venv\Scripts\activate
```

5. **Установите зависимости:**
```cmd
pip install -r requirements.txt
```

6. **Запустите программу:**
```cmd
python main.py
```

## Установка на Linux/Mac

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/dempster-shafer-theory.git
cd dempster-shafer-theory
```

2. **Создайте виртуальное окружение:**
```bash
python3 -m venv dempster_venv
```

3. **Активируйте окружение:**
```bash
source dempster_venv/bin/activate
```

4. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

5. **Запустите программу:**
```bash
python main.py
```

## Решение возможных проблем

### Ошибка: "python не является внутренней или внешней командой"
- Убедитесь, что Python установлен и добавлен в PATH
- Попробуйте использовать `python3` вместо `python`

### Ошибка при активации виртуального окружения
- На Windows PowerShell может потребоваться:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Ошибки с библиотеками
- Обновите pip: `python -m pip install --upgrade pip`
- Переустановите зависимости: `pip install -r requirements.txt --force-reinstall`

## Использование

После запуска `main.py` откроется консольное меню:

```
Теория Демпстера-Шейфера - реализация примеров из книги
==================================================

Выберите пример для запуска:
1. Пример 2.1 - Кандидаты на должность
2. Пример 2.2 - Прогноз цен акций
3. Пример 2.6 - Комбинирование свидетельств (Демпстер)
4. Пример 2.8 - Правило комбинирования Ягера
5. Сравнение Демпстера и Ягера
6. Все примеры последовательно
0. Выход
```

Выберите нужный вариант и следуйте инструкциям.