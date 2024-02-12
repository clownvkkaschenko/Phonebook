from math import ceil
from typing import List

import pandas as pd
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)  # colorama


class Phonebook:
    """В классе реализованы пять методов:

    - display_phonebook: Метод для постраничного вывода контактов.
    - add_contact: Метод для добавления нового контакта в справочник.
    - edit_contact: Метод для редактирования контакта в справочнике.
    - search_contact: Метод для поиска контакта в справочнике.
    - main: Главное меню, со всем функционалом.
    """

    FILE_PHONEBOOK: str = 'phonebook.csv'
    COLUMNS_COUNT: int = 6
    COLUMNS_NAME: List[str] = [
        'фамилия', 'имя', 'отчество', 'название организации',
        'телефон рабочий', 'телефон сотовый'
    ]
    PAGE_SIZE = 10

    def display_phonebook(
            self, page_number=1,
            message: str = None
    ) -> None:
        """Метод для постраничного вывода контактов."""

        if message:
            print(message)

        df: pd.DataFrame = pd.read_csv(self.FILE_PHONEBOOK)
        cnt_rows: int = df.shape[0]

        if cnt_rows <= self.PAGE_SIZE:
            df_str: str = tabulate(df, showindex=True, headers=df.columns)
            return self.main(message=('Вы находитесь на странице «1/'
                                      f'1»\n{df_str}\n'))

        start_idx = (page_number - 1) * self.PAGE_SIZE
        end_idx = start_idx + self.PAGE_SIZE
        df_on_page = df.iloc[start_idx:end_idx]
        last_page = ceil(cnt_rows / self.PAGE_SIZE)

        switch: str = input(
            f'Вы находитесь на странице «{page_number}/{last_page}»\n'
            f'{tabulate(df_on_page, showindex=True, headers=df.columns)}\n'
            f'{"-"*70}\n'
            f'{Fore.GREEN}Для перехода на следующую страницу отправьте «n»\n'
            'Для перехода на предыдущую страницу отправьте «e»\n'
            f'Для выхода в главное меню отправьте «m»{Style.RESET_ALL}\n'
        )

        if switch == 'n' and last_page == page_number:
            return self.display_phonebook(
                page_number=page_number,
                message=(f'{Fore.RED}Вы уже находитесь на '
                         'последней страничке.')
            )
        elif switch == 'n':
            return self.display_phonebook(page_number=page_number+1)
        elif switch == 'e' and page_number == 1:
            return self.display_phonebook(
                message=(f'{Fore.RED}Вы уже находитесь '
                         'на первой страничке.')
            )
        elif switch == 'e':
            return self.display_phonebook(page_number=page_number-1)
        elif switch == 'm':
            return self.main()
        else:
            return self.display_phonebook(
                page_number=page_number,
                message=f'{Fore.RED}Такого варианта нет.')

    def add_contact(self, message: str = None) -> None:
        """Метод для добавления нового контакта в справочник."""

        if message:
            print(message)

        data: List[str] = input(
            ('Для добавления новой записи введите данные в формате:\n'
             '«фамилия, имя, отчество, название организации, '
             'телефон рабочий, телефон сотовый»\n\n'
             'Пример:\nИванов, Иван, Иванович, VK, 32999, 89999999999\n\n'
             'Введите данные или введите «m» для выхода в главное меню: ')
        ).split(', ')

        if data == ['m']:
            return self.main()

        if len(data) != self.COLUMNS_COUNT:
            message = (f'{"-"*70}\n{Fore.RED}'
                       'Количество столбцов в справочнике не совпадает с '
                       'количеством переданных данных.\n')
            self.add_contact(message=message)

        new_contact: pd.DataFrame = pd.DataFrame([data])
        new_contact.to_csv(self.FILE_PHONEBOOK, mode='a',
                           header=False, index=False)

        return self.main(message=f'{Fore.GREEN}Данные добавлены!\n')

    def edit_contact(self, number: int = None, message: str = None) -> str:
        """Метод для редактирования контакта в справочнике."""

        if message:
            print(message)

        if not number:
            number: str = input(
                'Введите номер строки с контактом, который хотите изменить, '
                'или введите «m» для выхода в главное меню: ')

            if number == 'm':
                return self.main()

            try:
                number = int(number)
            except ValueError:
                return self.edit_contact(
                    message=f'{Fore.RED}Введите номер строки, а не символ.'
                )

        df: pd.DataFrame = pd.read_csv(self.FILE_PHONEBOOK)

        try:
            df_to_list: List = df.iloc[number].values.tolist()
        except IndexError:
            return self.edit_contact(
                message=f'{Fore.RED}Строки с номером «{number}» не существует'
            )

        fields_to_change: List[str] = input(
            f'\nВот выбранная вами строка:\n{", ".join(df_to_list)}\n'
            f'{"-"*70}\n'
            'Какие столбцы вы хотите изменить? Напишите нужные столбцы в '
            'таком формате:\n«фамилия, имя, отчество, название организации, '
            'телефон рабочий, телефон сотовый»\n\n'
            f'Пример:\nфамилия, название организации\n\n'
            'Введите столбцы или введите «m» для выхода в главное меню: '
        ).split(', ')

        if fields_to_change == ['m']:
            return self.main()

        for column in fields_to_change:
            if column not in self.COLUMNS_NAME:
                return self.edit_contact(
                    number=number,
                    message=(f'{Fore.RED}Вы ввели несуществующий '
                             f'столбец: «{column}»')
                )

        data_to_update = {}
        for field in fields_to_change:
            data_to_update[field] = input('Введите новое значение для '
                                          f'столбца «{field}»: ')

        for column, value in data_to_update.items():
            df.at[number, column] = value
        df.to_csv(self.FILE_PHONEBOOK, index=False)

        return self.main(message=f'{Fore.GREEN}Спасибо, данные обновлены!\n')

    def search_contact(self, message: str = None) -> str:
        """
        Метод для поиска контакта по одной или нескольким характеристикам.
        """

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
            return self.main()

        for column in fields_to_search:
            if column not in self.COLUMNS_NAME:
                return self.search_contact(
                    message=(f'\n{Fore.RED}Вы ввели несуществующий '
                             f'столбец: «{column}»')
                )

        data_to_search = {}
        for field in fields_to_search:
            data_to_search[field] = input('Введите значение для поиска в '
                                          f'столбце «{field}»: ')

        for column, value in data_to_search.items():
            df = df[df[column] == value]

        if df.empty:
            return self.main(message=f'{Fore.RED}Контакты не найдены.\n')

        result: str = tabulate(df, showindex=False, headers=df.columns)
        return self.main(message=(f'\n{Fore.GREEN}Найденные контакты:'
                                  f'{Style.RESET_ALL}\n{result}\n'))

    def main(self, message: str = None):
        """Главное меню, со всем функционалом."""

        if message:
            print(message)

        option = input(
            ('Главное меню\n'
             f'{"-"*70}\n'
             'Введите «1», для вывода всех записей из справочника на экран.\n'
             'Введите «2», для добавления новой записи в справочник.\n'
             'Введите «3», для редактирования записи.\n'
             'Введите «4», для поиска записей.\n'
             'Введите «0», для выхода.\n'
             f'{"-"*70}\n')
        )

        if option == '1':
            self.display_phonebook()

        elif option == '2':
            self.add_contact()

        elif option == '3':
            self.edit_contact()

        elif option == '4':
            self.search_contact()

        elif option == '0':
            print('Вы вышли из программы.')
            exit()

        else:
            self.main(message=f'{Fore.RED}Такого варианта нет')


phonebook = Phonebook()
phonebook.main()
