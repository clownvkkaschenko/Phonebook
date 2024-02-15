import os
import time
from math import ceil
from typing import List

import pandas as pd
from colorama import Fore, Style, init
from progress.bar import FillingCirclesBar
from simple_term_menu import TerminalMenu
from terminaltables import SingleTable

init(autoreset=True)  # colorama


def table_with_phonebook(data_table: List[List], title: str = None) -> str:
    """Функция для получения данных виде таблицы.

    Args:
        - data_table (List[List]): Список списков с данными для таблицы.
        - title (str): Заголовок таблицы.

    Returns:
        - Строка, содержащая таблицу, в формате текста.
    """

    table_instance = SingleTable(data_table, title)
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = True
    return table_instance.table


def loading_effect(message: str) -> None:
    """Функция для отображения эффекта загрузки."""

    bar = FillingCirclesBar('Loading', max=20)
    for _ in [i for i in range(20)]:
        bar.next()
        time.sleep(0.1)
    bar.finish()
    print(message)


class Phonebook:
    """В классе реализованы шесть методов:

    - display_phonebook: Метод для постраничного вывода контактов.
    - add_contact: Метод для добавления нового контакта в тел.справочник.
    - contact_by_idx: Метод для поиска контакта в тел.справочнике, по индексу.
    - edit_contact: Метод для редактирования контакта в тел.справочнике.
    - search_contact: Метод для поиска контакта в тел.справочнике.
    - main_menu: Главное меню, со всем функционалом.
    """

    FILE_PHONEBOOK: str = 'phonebook_ex.csv'
    COLUMNS_COUNT: int = 6
    COLUMNS_NAME: List[str] = [
        'фамилия', 'имя', 'отчество', 'название организации',
        'телефон рабочий', 'телефон сотовый'
    ]
    PAGE_SIZE: int = 10

    def display_phonebook(self, message: str = None, current_page: int = 1) -> None:
        """Метод для постраничного вывода контактов.

        Args:
            - message (str):  Применяется для отображения: предупреждений, ошибок или
                              дополнительной информации.
            - current_page (int): Номер текущей страницы.
        """

        os.system('cls||clear')
        if message:
            print(message)

        df: pd.DataFrame = pd.read_csv(self.FILE_PHONEBOOK)
        cnt_rows: int = df.shape[0]

        if cnt_rows <= self.PAGE_SIZE:
            df_to_list: List[List] = [self.COLUMNS_NAME] + df.values.tolist()
            phonebook_table: str = table_with_phonebook(
                data_table=df_to_list, title='Вы находитесь на странице «1/1»')
            return self.main_menu(message=phonebook_table)

        start_idx: int = (current_page - 1) * self.PAGE_SIZE
        end_idx: int = start_idx + self.PAGE_SIZE
        last_page: int = ceil(cnt_rows / self.PAGE_SIZE)

        df_on_current_page: pd.DataFrame = df.iloc[start_idx:end_idx]
        df_to_list: List[List] = [self.COLUMNS_NAME] + df_on_current_page.values.tolist()
        phonebook_table: str = table_with_phonebook(
            data_table=df_to_list,
            title=f'Вы находитесь на странице «{current_page}/{last_page}»')

        print(phonebook_table)

        menu = TerminalMenu(
            [
                'Перейти на следующую страницу.',
                'Перейти на предыдущую страницу.',
                'Выход в главное меню.'
            ],
            title='«Display phonebook»'
        )
        selected_index = menu.show()

        if selected_index == 0:
            if last_page != current_page:
                return self.display_phonebook(current_page=current_page+1)

            return self.display_phonebook(
                current_page=current_page,
                message=(f'{Fore.RED}Вы уже находитесь на последней страничке.\n'
                         f'{Style.RESET_ALL}')
            )

        elif selected_index == 1:
            if current_page != 1:
                return self.display_phonebook(current_page=current_page-1)

            return self.display_phonebook(
                message=(f'{Fore.RED}Вы уже находитесь на первой страничке\n{Style.RESET_ALL}')
            )

        elif selected_index == 2:
            return self.main_menu()

    def add_contact(self, message: str = None) -> None:
        """Метод для добавления нового контакта в телефонный справочник.

        Args:
            - message (str):  Применяется для отображения: предупреждений, ошибок или
                              дополнительной информации.
        """

        os.system('cls||clear')
        if message:
            print(message)

        data_contact: List[str] = input(
            ('Для добавления новой записи введите данные в формате:\n'
             '«фамилия, имя, отчество, название организации, телефон рабочий, телефон сотовый»'
             '\n\nПример:\nИванов, Иван, Иванович, VK, 32999, 89999999999\n\n'
             'Введите данные или введите «m» для выхода в главное меню: ')
        ).split(', ')

        if data_contact == ['m']:
            return self.main_menu()

        if len(data_contact) != self.COLUMNS_COUNT:
            return self.add_contact(
                message=(f'{Fore.RED}Количество столбцов в справочнике не совпадает с '
                         'количеством переданных данных.\n')
            )

        try:
            new_contact: pd.DataFrame = pd.DataFrame([data_contact])
            new_contact.to_csv(self.FILE_PHONEBOOK, mode='a',
                               header=False, index=False)
        except UnicodeEncodeError:
            return self.add_contact(message=(f'{Fore.RED}Ошибка кодировки!\n'))

        loading_effect(message=f'{Fore.GREEN}Данные добавлены!!!\n')

        menu = TerminalMenu(
            [
                'Добавить ещё один контакт.',
                'Выйти в главное меню.'
            ],
            title='«Add contact»'
        )
        selected_index = menu.show()

        if selected_index == 0:
            return self.add_contact()
        elif selected_index == 1:
            return self.main_menu()

    def contact_by_idx(self, message: str = None, idx: int = None) -> None:
        """Метод для поиска контакта в телефонном справочнике, по индексу.

        Args:
            - message (str):  Применяется для отображения: предупреждений, ошибок или
                              дополнительной информации.
            - idx (int): Индекс строки.
        """

        os.system('cls||clear')
        if message:
            print(message)

        if idx is None:
            idx: str = input(
                'Введите индекс строки с контактом, который хотите изменить, '
                'или введите «m» для выхода в главное меню: ')

            if idx == 'm':
                return self.main_menu()

            try:
                idx = int(idx)
            except ValueError:
                return self.contact_by_idx(
                    message=f'{Fore.RED}Введите номер строки, а не символ.\n'
                )

        df: pd.DataFrame = pd.read_csv(self.FILE_PHONEBOOK)

        try:
            df_to_list: List = df.iloc[idx].values.tolist()
        except IndexError:
            return self.contact_by_idx(
                message=f'{Fore.RED}Строки с номером «{idx}» не существует\n'
            )

        return self.edit_contact(idx=idx, df_to_list=df_to_list, df=df)

    def edit_contact(
            self, idx: int, df_to_list: List, df: pd.DataFrame, message: str = None
    ) -> None:
        """Метод для редактирования контакта в справочнике.

        Args:
            - idx (int): Индекс строки.
            - df_to_list (List):
            - df (pd.DataFrame):
            - message (str):  Применяется для отображения: предупреждений, ошибок или
                              дополнительной информации.
        """

        os.system('cls||clear')
        if message:
            print(message)

        fields_to_change: List[str] = input(
            f'Вот выбранная вами строка с номером «{idx}»:\n{", ".join(df_to_list)}\n'
            f'{"-"*70}\n'
            'Какие столбцы вы хотите изменить? Напишите нужные столбцы в таком формате:\n'
            '«фамилия, имя, отчество, название организации, телефон рабочий, телефон сотовый»'
            f'\n\nПример:\nфамилия, название организации\n\n'
            'Введите столбцы или введите «m» для выхода в главное меню: '
        ).split(', ')

        if fields_to_change == ['m']:
            return self.main_menu()

        for column in fields_to_change:
            if column not in self.COLUMNS_NAME:
                return self.edit_contact(
                    idx=idx, df_to_list=df_to_list, df=df,
                    message=(f'{Fore.RED}Вы ввели несуществующий столбец: «{column}»\n')
                )

        data_to_update = {}
        for field in fields_to_change:
            data_to_update[field] = input(f'Введите новое значение для столбца «{field}»: ')

        try:
            for column, value in data_to_update.items():
                df.at[idx, column] = value
            df.to_csv(self.FILE_PHONEBOOK, index=False)
        except UnicodeEncodeError:
            return self.edit_contact(
                idx=idx, df_to_list=df_to_list, df=df,
                message=(f'{Fore.RED}Ошибка кодировки!\n')
            )

        loading_effect(message=f'{Fore.GREEN}Данные обновлены!!!\n')

        menu = TerminalMenu(
            [
                'Изменить ещё один контакт.',
                'Выйти в главное меню.'
            ],
            title='«Edit contact»'
        )
        selected_index = menu.show()

        if selected_index == 0:
            return self.contact_by_idx()
        elif selected_index == 1:
            return self.main_menu()

    def search_contact(self, message: str = None) -> None:
        """Метод для поиска контакта по одной или нескольким характеристикам.

        Args:
            - message (str):  Применяется для отображения: предупреждений, ошибок или
                              дополнительной информации.
        """

        os.system('cls||clear')
        if message:
            print(message)

        df: pd.DataFrame = pd.read_csv(self.FILE_PHONEBOOK)

        fields_to_search: List[str] = input(
            'По каким столбцам вы хотите найти контакт? Напишите нужные '
            'столбцы в таком формате:\n«фамилия, имя, отчество, '
            'название организации, телефон рабочий, телефон сотовый»\n\n'
            'Пример:\nфамилия, название организации\n\n'
            'Введите столбцы или введите «m» для выхода в главное меню: '
        ).split(', ')

        if fields_to_search == ['m']:
            return self.main_menu()

        for column in fields_to_search:
            if column not in self.COLUMNS_NAME:
                return self.search_contact(
                    message=(f'{Fore.RED}Вы ввели несуществующий столбец: «{column}»\n')
                )

        data_to_search = {}
        for field in fields_to_search:
            data_to_search[field] = input(f'Введите значение для поиска в столбце «{field}»: ')

        for column, value in data_to_search.items():
            df = df[df[column] == value]

        if df.empty:
            loading_effect(message=f'{Fore.RED}Контакты не найдены.\n')
        else:
            df_to_list: List[List] = [self.COLUMNS_NAME] + df.values.tolist()
            table = table_with_phonebook(data_table=df_to_list)
            loading_effect(message=f'{Fore.GREEN}Данные найдены!!!{Style.RESET_ALL}\n'
                                   f'{table}\n')

        menu = TerminalMenu(
            [
                'Найти ещё один контакт.',
                'Выйти в главное меню.'
            ],
            title='«Search contact»'
        )
        selected_index = menu.show()

        if selected_index == 0:
            return self.search_contact()
        elif selected_index == 1:
            return self.main_menu()

    def main_menu(self, message: str = None) -> None:
        """Главное меню, со всем функционалом."""

        os.system('cls||clear')
        if message:
            print(message)

        menu = TerminalMenu(
            ['Вывести список контактов.',
             'Добавить контакт.',
             'Редактировать контакт.',
             'Поиск контакта.',
             'Выйти из приложения.'],
            title='«Phonebook App»'
        )
        selected_index = menu.show()

        if selected_index == 0:
            self.display_phonebook()

        elif selected_index == 1:
            self.add_contact()

        elif selected_index == 2:
            self.contact_by_idx()

        elif selected_index == 3:
            self.search_contact()

        elif selected_index == 4:
            os.system('cls||clear')
            exit()


phonebook = Phonebook()
phonebook.main_menu()
