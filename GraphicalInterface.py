import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QFileDialog

from PhoneNumberParser import run_parsing

"""
GraphicalInterface - модуль, запускающий графический интерфейс программы.
"""

print(os.path.realpath(__file__))
dirname, filename = os.path.split(os.path.realpath(__file__))
print(dirname)
Form, Window = uic.loadUiType(dirname + "\\graphical_interface_template.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

file_from = ''
dir_out = ''


def on_click_select_file():
    """Кнопка для выбора файла, который необходимо обработать."""
    global file_from
    print("'Select file' clicked!")
    dialog = QFileDialog()
    file_from = dialog.getOpenFileName(window, 'Select file')
    print(file_from[0])
    form.label.setText(file_from[0])


def on_click_select_folder():
    """Кнопка для выбора директории, в которой будут созданы файлы с результатом обработки."""
    global dir_out
    print("'Select directory' clicked!")
    dialog = QFileDialog()
    dir_out = dialog.getExistingDirectory(window, 'Select directory')
    print(dir_out)
    form.label_2.setText(dir_out)


def on_click_run_parsing():
    """Кнопка запуска обработки. И выбор стиля обработки."""
    line_for_size = int(form.spinBox.text())
    line_for_cells = form.lineEdit.text().split()
    print(line_for_cells)
    run_parsing(path_from=file_from[0], path_out=dir_out + '/', style_mode=line_for_size, cells=line_for_cells)
    QMessageBox.information(window, "Парсинг выполнен.", "Проверьте указанную папку.", QMessageBox.Ok)


form.pushButton.clicked.connect(on_click_select_file)
form.pushButton_2.clicked.connect(on_click_select_folder)
form.pushButton_3.clicked.connect(on_click_run_parsing)

if __name__ == '__main__':
    app.exec_()
