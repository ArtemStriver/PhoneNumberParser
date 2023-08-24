#!/usr/bin/env python3
from pprint import pprint


class PhoneNumberParser:

    def __init__(self, path_from, path_out):
        self.path_from = path_from
        self.path_out = path_out
        self.index = ['-', '+', '(', ')', "'", "\n", ' ', ',']
        self.numbers = []
        self.correct_numbers = []
        self.incorrect_numbers = []
        self.incorrect_numbers_log = []  # TODO почистить количество списков, а то их многовато стало!

        self.correct_numbers_kz = []
        self.correct_numbers_belarus = []
        self.correct_numbers_uzbeckistan = []
        self.correct_numbers_kirgistan = []
        self.correct_numbers_tadgikistan = []
        self.correct_numbers_azerbaidgan = []
        self.correct_numbers_italy = []
        self.correct_numbers_germany = []
        self.correct_numbers_turky = []
        self.correct_numbers_izrail = []
        self.correct_numbers_greatbritan = []

        self.correct_number_count = 0

    def read_file(self):
        """Чтение списка номеров из файла"""
        with open(file='original_file.txt', mode='r', encoding='utf8') as file:
            for line in file:
                self.numbers.append(line)

    def file_correction(self):
        """Форматирование номеров и отсев на русские/казахские/абхазские и иностранные (СНГ и другие)"""
        for odd_numb in self.numbers:
            clear_numb = odd_numb.translate({ord(i): None for i in self.index})
            clear_numb = ''.join(i for i in clear_numb if not i.isalpha())
            if len(clear_numb) == 22:  # два русских номера, но есть варианты номеров русский+иностранный (или наоборот)
                self.correct_number_count += 2
                self.correct_numbers.append('+7' + clear_numb[1:11] + '\n' + '+7' + clear_numb[12:])
            elif self.sorting_foreign_numbers(clear_numb):
                pass
            elif len(clear_numb) != 11:
                self.incorrect_numbers_log.append(odd_numb)
                self.incorrect_numbers.append(clear_numb)
            elif clear_numb[1] != '9' and len(clear_numb) == 11:
                self.correct_numbers_kz.append('+7' + clear_numb[1:])
            else:
                self.correct_number_count += 1
                self.correct_numbers.append('+7' + clear_numb[1:])

    def sorting_foreign_numbers(self, numb):  # TODO перевести в вмодуль отдельный
        """Функция сортировки списка иностранных номеров по странам"""
        all_foreign_codes = {'375': self.correct_numbers_belarus,
                             '998': self.correct_numbers_uzbeckistan,
                             '996': self.correct_numbers_kirgistan,
                             '992': self.correct_numbers_tadgikistan,
                             '994': self.correct_numbers_azerbaidgan,
                             '39': self.correct_numbers_italy,
                             '49': self.correct_numbers_germany,
                             '90': self.correct_numbers_turky,
                             '972': self.correct_numbers_izrail,
                             '44': self.correct_numbers_greatbritan}
        for key in all_foreign_codes.keys():
            if numb[0:3] == key:
                all_foreign_codes[key].append(numb)
                return True
            elif numb[0:2] == key:
                all_foreign_codes[key].append(numb)
                return True
        else:
            return False

    def write_file(self):
        """Запись правильных номеров в файл"""
        all_foreign_numbers = {'Беларусь': self.correct_numbers_belarus,
                               'Узбекистан': self.correct_numbers_uzbeckistan,
                               'Киргизстан': self.correct_numbers_kirgistan,
                               'Таджикистан': self.correct_numbers_tadgikistan,
                               'Азербайджан': self.correct_numbers_azerbaidgan,
                               'Италия': self.correct_numbers_italy,
                               'Германия': self.correct_numbers_germany,
                               'Турция': self.correct_numbers_turky,
                               'Израйль': self.correct_numbers_izrail,
                               'Великобритания': self.correct_numbers_greatbritan}
        with open(file=f'{self.path_out}result_RU_KZ.txt', mode='w', encoding='utf8') as out_file:
            for numb in self.correct_numbers:
                out_file.write(numb + '\n')
            for numb in self.correct_numbers_kz:
                out_file.write(numb + '\n')

        with open(file=f'{self.path_out}result_other.txt', mode='w', encoding='utf8') as out_file:
            for value in all_foreign_numbers.values():
                for numb in value:
                    out_file.write('+' + str(numb) + '\n')

        with open(file=f'{self.path_out}result_other_with_explanations.txt', mode='w', encoding='utf8') as out_file:
            for key, value in all_foreign_numbers.items():
                out_file.write(key + '\n')
                for numb in value:
                    out_file.write(numb + '\n')

        with open(file=f'{self.path_out}incorrect_numbers.txt', mode='w', encoding='utf8') as out_file:
            for numb in self.incorrect_numbers:
                out_file.write('+' + str(numb) + '\n')

        # TODO организовать запись в таблицу с нумерацией номеров

    def run(self):
        self.read_file()
        self.file_correction()
        self.write_file()
        # pprint(self.correct_numbers)
        # print(self.correct_number_count)
        # pprint(self.correct_numbers_kz)
        # print()
        # pprint(self.incorrect_numbers)
        # print(self.correct_numbers_belarus,
        #       self.correct_numbers_uzbeckistan,
        #       self.correct_numbers_kirgistan,
        #       self.correct_numbers_tadgikistan,
        #       self.correct_numbers_italy,
        #       self.correct_numbers_germany,
        #       self.correct_numbers_turky,
        #       self.correct_numbers_azerbaidgan,
        #       self.correct_numbers_izrail,
        #       self.correct_numbers_greatbritan,
        #       )


def run():
    """Консольный интерфейс"""
    try:
        while True:
            # TODO сделать нормальный дружественный интерфейс
            path_from = input('Введите путь по которому расположен файл для парсинга с именем самого файла: \n >>> ')
            path_out = input('Введите путь по которому вы хотите сохранить файл с результатом парсинга: \n >>> ')
            print(path_from, path_out)
            parser = PhoneNumberParser(path_from=path_from, path_out=path_out)
            parser.run()
    except Exception as exc:
        print(exc)


if __name__ == '__main__':
    run()
