<div id="header" align="center">
  <h1>Phonebook</h1>
  <img src="https://img.shields.io/badge/Python-3.8.10-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/Pandas-2.0.3-F8F8FF?style=for-the-badge&logo=pandas&logoColor=150458">
  <img src="https://img.shields.io/badge/Numpy-1.24.4-F8F8FF?style=for-the-badge&logo=numpy&logoColor=013243">
</div>

# Запуск проекта:

- В проекте используется библиотека **simple-term-menu**, которая не работает на Windows. Если вы используете Windows, то проект можно запустить, например, в WSL-Ubuntu.
- Клонируйте репозиторий и перейдите в него.
- Установите и активируйте виртуальное окружение.
    ```
    python3 -m venv env
    source env/bin/activate
    ```
- Установите зависимости из файла requirements.txt
    ```
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ``` 
- Запустите код:
    ```
    python code_phonebook.py
    ```

# Техническое задание проекта:

Реализовать телефонный справочник со следующими возможностями:
- Вывод постранично записей из справочника на экран.
- Добавление новой записи в справочник.
- Возможность редактирования записей в справочнике.
- Поиск записей по одной или нескольким характеристикам.

Требования к программе:
- Реализация интерфейса через консоль (без web или графического интерфейса).
- Хранение данных должно быть организовано в виде текстового файла, формат которого придумывает сам программист.
- В справочнике хранится следующая информация: фамилия, имя, отчество, название организации, телефон рабочий, телефон личный (сотовый).
