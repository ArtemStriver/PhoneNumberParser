#!/usr/bin/env python3
from pprint import pprint


# Программа принимает на вход txt файл с номерами телефонов,
# расположенных построчно и имеющих разный формат.

# Необходимо переписать все номера в новый файл в едином стиле,
# попутно убирая все не прошедшие отбор в лог для последующей обработки,
# также добавить нумерацию столбцов. Выходной файл должен быть тхт или эксель.

# Из дополнительных фич ввести подсчет номеров и сколько из них РФ.

# TODO из лога вытянуть еще номера с буквами, номера через запятую, иностранные номера,
#  русские стандартизовать под формат +7, разделить номера по разным файлам по странам

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
        # TODO иностранные и русские вывести отдельно в файлы, + определение страны по коду и в разные файлы

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
        if numb[0:3] == '375':
            self.correct_numbers_belarus.append(numb)
            return True
        elif numb[0:3] == '998':
            self.correct_numbers_uzbeckistan.append(numb)
            return True
        elif numb[0:3] == '996':
            self.correct_numbers_kirgistan.append(numb)
            return True
        elif numb[0:3] == '994':
            self.correct_numbers_azerbaidgan.append(numb)
            return True
        elif numb[0:3] == '992':
            self.correct_numbers_tadgikistan.append(numb)
            return True
        elif numb[0:3] == '972':
            self.correct_numbers_izrail.append(numb)
            return True
        elif numb[0:2] == '39':
            self.correct_numbers_italy.append(numb)
            return True
        elif numb[0:2] == '49':
            self.correct_numbers_germany.append(numb)
            return True
        elif numb[0:2] == '90':
            self.correct_numbers_turky.append(numb)
            return True
        elif numb[0:2] == '44':
            self.correct_numbers_greatbritan.append(numb)
            return True
        else:
            return False

    def write_file(self):  # TODO оптимизировать код записи в файлы
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
            # all_foreign_numbers = [*self.correct_numbers_belarus, *self.correct_numbers_uzbeckistan,
            #                        *self.correct_numbers_kirgistan, *self.correct_numbers_tadgikistan,
            #                        *self.correct_numbers_azerbaidgan, *self.correct_numbers_italy,
            #                        *self.correct_numbers_germany, *self.correct_numbers_turky,
            #                        *self.correct_numbers_izrail, *self.correct_numbers_greatbritan]
            # for numb in all_foreign_numbers:
            #     out_file.write('+' + str(numb) + '\n')
            for value in all_foreign_numbers.values():
                for numb in value:
                    out_file.write('+' + str(numb) + '\n')

        with open(file=f'{self.path_out}result_other_with_explanations.txt', mode='w', encoding='utf8') as out_file:
            for key, value in all_foreign_numbers.items():
                out_file.write(key + '\n')
                for numb in value:
                    out_file.write(numb + '\n')
            # out_file.write('Беларусь' + '\n')
            # for numb in self.correct_numbers_belarus:
            #     out_file.write(numb + '\n')
            # out_file.write('Узбекистан' + '\n')
            # for numb in self.correct_numbers_uzbeckistan:
            #     out_file.write(numb + '\n')
            # out_file.write('Киргизстан' + '\n')
            # for numb in self.correct_numbers_kirgistan:
            #     out_file.write(numb + '\n')
            # out_file.write('Таджикистан' + '\n')
            # for numb in self.correct_numbers_tadgikistan:
            #     out_file.write(numb + '\n')
            # out_file.write('Азербайджан' + '\n')
            # for numb in self.correct_numbers_azerbaidgan:
            #     out_file.write(numb + '\n')
            # out_file.write('Италия' + '\n')
            # for numb in self.correct_numbers_italy:
            #     out_file.write(numb + '\n')
            # out_file.write('Турция' + '\n')
            # for numb in self.correct_numbers_turky:
            #     out_file.write(numb + '\n')
            # out_file.write('Германия' + '\n')
            # for numb in self.correct_numbers_germany:
            #     out_file.write(numb + '\n')
            # out_file.write('Израйль' + '\n')
            # for numb in self.correct_numbers_izrail:
            #     out_file.write(numb + '\n')
            # out_file.write('Великобритания' + '\n')
            # for numb in self.correct_numbers_greatbritan:
            #     out_file.write(numb + '\n')

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



parser = PhoneNumberParser(path_from='', path_out='')
parser.run()

# def run():
#     """Консольный интерфейс"""
#     try:
#         while True:
#             # TODO сделать нормальный дружественный интерфейс
#             path_from = input('Введите путь по которому расположен файл для парсинга с именем самого файла: \n >>> ')
#             path_out = input('Введите путь по которому вы хотите сохранить файл с результатом парсинга: \n >>> ')
#             print(path_from, path_out)
#             parser = PhoneNumberParser(path_from=path_from, path_out=path_out)
#             parser.run()
#     except Exception as exc:
#         print(exc)
#
#
# if __name__ == '__main__':
#     run()
