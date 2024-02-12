<div id="header" align="center">
  <h1>Phonebook</h1>
  <img src="https://img.shields.io/badge/Python-3.10.11-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/Pandas-2.2.0-F8F8FF?style=for-the-badge&logo=pandas&logoColor=150458">
  <img src="https://img.shields.io/badge/Numpy-1.26.4-F8F8FF?style=for-the-badge&logo=numpy&logoColor=013243">
</div>

# Запуск проекта:

- Клонируйте репозиторий и перейдите в него.
- Установите и активируйте виртуальное окружение.
    ```
    python3.10 -m venv venv
    source venv/Scripts/activate
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

- Пример работы можно увидеть на скринах, в папке [example](./example/)

# Описание проекта:

Реализовать телефонный справочник со следующими возможностями:
- Вывод постранично записей из справочника на экран.
- Добавление новой записи в справочник.
- Возможность редактирования записей в справочнике.
- Поиск записей по одной или нескольким характеристикам.

Требования к программе:
- Реализация интерфейса через консоль (без web или графического интерфейса).
- Хранение данных должно быть организовано в виде текстового файла, формат которого придумывает сам программист.
- В справочнике хранится следующая информация: фамилия, имя, отчество, название организации, телефон рабочий, телефон личный (сотовый).
