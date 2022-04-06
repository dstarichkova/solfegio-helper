import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QFileDialog
from PyQt5 import QtCore, QtMultimedia, uic
import sqlite3
import os
from PyQt5.QtGui import QPixmap

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class Solfegio(QMainWindow):  # Главный экран
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/home_screen.ui', self)
        self.pushButton_2.clicked.connect(self.open_intervals)
        self.pushButton.clicked.connect(self.open_triades)
        self.pixmap1 = QPixmap('img/int_icon.PNG')
        self.pixmap2 = QPixmap('img/tri_icon.PNG')
        self.pixmap3 = QPixmap('img/home_image.jpg')
        self.icon_1.setPixmap(self.pixmap1)
        self.icon_2.setPixmap(self.pixmap2)
        self.main_image.setPixmap(self.pixmap3)

    def open_intervals(self):
        self.screen_2 = Intervals(self, '')
        self.screen_2.show()

    def open_triades(self):
        self.screen_3 = Triades(self, '')
        self.screen_3.show()


class Intervals(QWidget):  # Работа с интервалами
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('ui/intervals.ui', self)

        self.connection = sqlite3.connect("db/solfegio.db")

        self.c.clicked.connect(self.play_note)
        self.cx.clicked.connect(self.play_note)
        self.d.clicked.connect(self.play_note)
        self.dx.clicked.connect(self.play_note)
        self.e.clicked.connect(self.play_note)
        self.f.clicked.connect(self.play_note)
        self.fx.clicked.connect(self.play_note)
        self.g.clicked.connect(self.play_note)
        self.gx.clicked.connect(self.play_note)
        self.a.clicked.connect(self.play_note)
        self.ax.clicked.connect(self.play_note)
        self.b.clicked.connect(self.play_note)
        self.c1.clicked.connect(self.play_note)
        self.c1x.clicked.connect(self.play_note)
        self.d1.clicked.connect(self.play_note)
        self.d1x.clicked.connect(self.play_note)
        self.e1.clicked.connect(self.play_note)
        self.f1.clicked.connect(self.play_note)
        self.f1x.clicked.connect(self.play_note)
        self.g1.clicked.connect(self.play_note)
        self.g1x.clicked.connect(self.play_note)
        self.a1.clicked.connect(self.play_note)
        self.a1x.clicked.connect(self.play_note)
        self.b1.clicked.connect(self.play_note)

        self.play_int.clicked.connect(self.play_interval)
        self.build_int.clicked.connect(self.find_interval)
        self.load_int.clicked.connect(self.load_interval)
        self.change_int.clicked.connect(self.change_interval)

        self.play1.clicked.connect(self.play_note)
        self.play2.clicked.connect(self.play_note)
        self.play1.hide()
        self.play2.hide()

        self.play_on_keys.hide()

    def play_note(self):  # Игра на клваишах
        path = os.path.join(CURRENT_DIR, f"mp3 Notes/{self.sender().text()}.mp3")
        self.load_mp3(path)
        self.player.play()

    def load_mp3(self, filename):  # Игра на клваишах
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

    def play_interval(self):  # Проиграть интервал
        result = (i[0] for i in self.connection.cursor().execute(
            "SELECT intshort FROM intervals_length").fetchall())
        interval, ok_pressed = QInputDialog.getItem(
            self, "Выберите интервал", "Выберите интервал, который хотите проиграть:",
            result, 1, False)
        limit = self.connection.cursor().execute(f"SELECT length FROM intervals_length WHERE "
                                                 f"intshort = '{interval}'").fetchall()[0][0]
        if ok_pressed:
            result = (i[0] for i in self.connection.cursor().execute(
                f"SELECT notename FROM notes WHERE notevalue + {limit} < 25").fetchall())
            note, ok_pressed = QInputDialog.getItem(
                self, "Выберите ноту", "Выберите ноту, с которой начинается интервал:",
                result, 1, False)
            if ok_pressed:
                self.int_name.setText([i[0] for i in self.connection.cursor().execute(f"SELECT"
                    f" intname FROM intervals_length WHERE intshort = '{interval}'").fetchall()][0])
                self.int_label.setText(interval)
                note1_value = [i[0] for i in self.connection.cursor().execute(f"SELECT"
                    f" notevalue FROM notes WHERE notename = '{note}'").fetchall()][0]
                interval_value = limit
                note2 = [i[0] for i in self.connection.cursor().execute(f"SELECT"
                    f" notename FROM notes WHERE notevalue = '{note1_value + interval_value}'"
                                                                        f"").fetchall()][0]
                self.show_image(interval)
                self.play1.setText(note)
                self.play2.setText(note2)
                self.play1.show()
                self.play2.show()

    def find_interval(self):  # Определить интервал
        self.play1.hide()
        self.play2.hide()
        self.play_on_keys.show()
        self.notes = []

        def get_interval_notes():  # После того как сыграли 2 ноты
            if len(self.notes) < 2:
                self.notes.append(self.sender().text())
            if len(self.notes) >= 2:
                self.play_on_keys.hide()
                note1, note2 = self.notes
                a = [[i[0] for i in self.connection.cursor().execute(f"SELECT"
                    f" notevalue FROM notes WHERE notename = '{note1}'").fetchall()][0],
                [i[0] for i in self.connection.cursor().execute(f"SELECT"
                    f" notevalue FROM notes WHERE notename = '{note2}'").fetchall()][
                    0]]
                a.sort()
                note1_value, note2_value = a
                int_value = note2_value - note1_value
                interval = [i[0] for i in self.connection.cursor().execute(f"SELECT"
                    f" intshort FROM intervals_length WHERE length = '{int_value}'").fetchall()][0]
                self.int_name.setText([i[0] for i in self.connection.cursor().execute(f"SELECT"
                    f" intname FROM intervals_length WHERE length = '{int_value}'").fetchall()][0])
                self.int_label.setText(interval)
                self.show_image(interval)

                self.c.clicked.disconnect(get_interval_notes)
                self.cx.clicked.disconnect(get_interval_notes)
                self.d.clicked.disconnect(get_interval_notes)
                self.dx.clicked.disconnect(get_interval_notes)
                self.e.clicked.disconnect(get_interval_notes)
                self.f.clicked.disconnect(get_interval_notes)
                self.fx.clicked.disconnect(get_interval_notes)
                self.g.clicked.disconnect(get_interval_notes)
                self.gx.clicked.disconnect(get_interval_notes)
                self.a.clicked.disconnect(get_interval_notes)
                self.ax.clicked.disconnect(get_interval_notes)
                self.b.clicked.disconnect(get_interval_notes)
                self.c1.clicked.disconnect(get_interval_notes)
                self.c1x.clicked.disconnect(get_interval_notes)
                self.d1.clicked.disconnect(get_interval_notes)
                self.d1x.clicked.disconnect(get_interval_notes)
                self.e1.clicked.disconnect(get_interval_notes)
                self.f1.clicked.disconnect(get_interval_notes)
                self.f1x.clicked.disconnect(get_interval_notes)
                self.g1.clicked.disconnect(get_interval_notes)
                self.g1x.clicked.disconnect(get_interval_notes)
                self.a1.clicked.disconnect(get_interval_notes)
                self.a1x.clicked.disconnect(get_interval_notes)
                self.b1.clicked.disconnect(get_interval_notes)

        self.c.clicked.connect(get_interval_notes)
        self.cx.clicked.connect(get_interval_notes)
        self.d.clicked.connect(get_interval_notes)
        self.dx.clicked.connect(get_interval_notes)
        self.e.clicked.connect(get_interval_notes)
        self.f.clicked.connect(get_interval_notes)
        self.fx.clicked.connect(get_interval_notes)
        self.g.clicked.connect(get_interval_notes)
        self.gx.clicked.connect(get_interval_notes)
        self.a.clicked.connect(get_interval_notes)
        self.ax.clicked.connect(get_interval_notes)
        self.b.clicked.connect(get_interval_notes)
        self.c1.clicked.connect(get_interval_notes)
        self.c1x.clicked.connect(get_interval_notes)
        self.d1.clicked.connect(get_interval_notes)
        self.d1x.clicked.connect(get_interval_notes)
        self.e1.clicked.connect(get_interval_notes)
        self.f1.clicked.connect(get_interval_notes)
        self.f1x.clicked.connect(get_interval_notes)
        self.g1.clicked.connect(get_interval_notes)
        self.g1x.clicked.connect(get_interval_notes)
        self.a1.clicked.connect(get_interval_notes)
        self.a1x.clicked.connect(get_interval_notes)
        self.b1.clicked.connect(get_interval_notes)

    def load_interval(self):  # txt файл с интервалом
        self.finterval = QFileDialog.getOpenFileName(
            self, 'Выберите txt файл с названием интервала и его первую ноту, разделенные знаком ;',
            '', 'Текстовый файл (*.txt);;Все файлы (*)')[0]
        if self.finterval:
            f = open(self.finterval, encoding="utf8", mode='r')
            lines = f.readlines()
            interval, note = lines[0].split(';')
            self.int_name.setText(interval)
            self.int_label.setText([i[0] for i in self.connection.cursor().execute(
                f"SELECT intshort FROM intervals_length WHERE intname ="
                f" '{interval}'").fetchall()][0])
            note1_value = [i[0] for i in self.connection.cursor().execute(
                f"SELECT notevalue FROM notes WHERE notename = '{note}'").fetchall()][0]
            interval_value = [i[0] for i in self.connection.cursor().execute(
                f"SELECT length FROM intervals_length WHERE "
                f"intname = '{interval}'").fetchall()][0]
            note2 = [i[0] for i in self.connection.cursor().execute(
                f"SELECT notename FROM notes WHERE notevalue = '{note1_value + interval_value}'"
                                                                f"").fetchall()][0]
            self.play1.setText(note)
            self.play2.setText(note2)
            self.play1.show()
            self.play2.show()
            self.show_image(interval)

    def change_interval(self):  # Изменить название
        result = (i[0] for i in self.connection.cursor().execute(
            "SELECT intshort FROM intervals_length").fetchall())
        interval, ok_pressed = QInputDialog.getItem(
            self, "Выберите интервал", "Выберите интервал, которому хотите поменять название:",
            result, 1, False)
        if ok_pressed:
            new_name, ok_pressed = QInputDialog.getText(
                self, "Введите название", "Введите новое название интервала:")
            if ok_pressed:
                self.connection.cursor().execute(
                    f"UPDATE intervals_length SET intname = '{new_name}' WHERE intshort"
                    f" = '{interval}'")
                self.connection.commit()

    def show_image(self, name):  # Вид на нотном стане
        self.pixmap = QPixmap(f'img/{name}.png')
        self.image_file.setPixmap(self.pixmap)

    def closeEvent(self, event):
        self.connection.close()


class Triades(QWidget):  # Работа с трезвучиями
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('ui/triades.ui', self)

        self.connection = sqlite3.connect("db/solfegio.db")

        self.c.clicked.connect(self.play_note)
        self.cx.clicked.connect(self.play_note)
        self.d.clicked.connect(self.play_note)
        self.dx.clicked.connect(self.play_note)
        self.e.clicked.connect(self.play_note)
        self.f.clicked.connect(self.play_note)
        self.fx.clicked.connect(self.play_note)
        self.g.clicked.connect(self.play_note)
        self.gx.clicked.connect(self.play_note)
        self.a.clicked.connect(self.play_note)
        self.ax.clicked.connect(self.play_note)
        self.b.clicked.connect(self.play_note)
        self.c1.clicked.connect(self.play_note)
        self.c1x.clicked.connect(self.play_note)
        self.d1.clicked.connect(self.play_note)
        self.d1x.clicked.connect(self.play_note)
        self.e1.clicked.connect(self.play_note)
        self.f1.clicked.connect(self.play_note)
        self.f1x.clicked.connect(self.play_note)
        self.g1.clicked.connect(self.play_note)
        self.g1x.clicked.connect(self.play_note)
        self.a1.clicked.connect(self.play_note)
        self.a1x.clicked.connect(self.play_note)
        self.b1.clicked.connect(self.play_note)

        self.play_tri.clicked.connect(self.play_triade)
        self.build_tri.clicked.connect(self.find_triade)
        self.load_tri.clicked.connect(self.load_triade)
        self.change_tri.clicked.connect(self.change_triade)
        self.make_tri.clicked.connect(self.make_triade)

        self.play1.clicked.connect(self.play_note)
        self.play2.clicked.connect(self.play_note)
        self.play3.clicked.connect(self.play_note)
        self.play1.hide()
        self.play2.hide()
        self.play3.hide()

        self.play_on_keys.hide()

    def play_note(self):
        path = os.path.join(CURRENT_DIR, f"mp3 Notes/{self.sender().text()}.mp3")
        self.load_mp3(path)
        self.player.play()

    def load_mp3(self, filename):
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

    def play_triade(self):
        result = (i[0] for i in self.connection.cursor().execute(
            "SELECT trishort FROM triades").fetchall())
        triade, ok_pressed = QInputDialog.getItem(
            self, "Выберите трезвучие", "Выберите трезвучие, который хотите проиграть:",
            result, 1, False)
        one, two = self.connection.cursor().execute(
            f"SELECT length1, length2 FROM triades WHERE trishort = '{triade}'").fetchall()[0]
        limit = one + two
        if ok_pressed:
            result = (i[0] for i in self.connection.cursor().execute(
                f"SELECT notename FROM notes WHERE notevalue + {limit} < 25").fetchall())
            note, ok_pressed = QInputDialog.getItem(
                self, "Выберите ноту", "Выберите ноту, с которой начинается трезвучие:",
                result, 1, False)
            if ok_pressed:
                self.tri_name.setText([i[0] for i in self.connection.cursor().execute(
                    f"SELECT"
                    f" triname FROM triades WHERE trishort = '{triade}'").fetchall()][0])
                self.tri_label.setText(triade)
                note1_value = [i[0] for i in self.connection.cursor().execute(
                    f"SELECT notevalue FROM notes WHERE notename = '{note}'").fetchall()][0]
                note2 = [i[0] for i in self.connection.cursor().execute(
                    f"SELECT notename FROM notes WHERE notevalue = '{note1_value + one}'"
                    f"").fetchall()][0]
                note3 = [i[0] for i in self.connection.cursor().execute(
                    f"SELECT notename FROM notes WHERE "
                    f"notevalue = '{note1_value + one + two}'"
                    f"").fetchall()][0]
                self.play1.setText(note)
                self.play2.setText(note2)
                self.play3.setText(note3)
                self.play1.show()
                self.play2.show()
                self.play3.show()

    def find_triade(self):
        self.play1.hide()
        self.play2.hide()
        self.play3.hide()
        self.play_on_keys.show()
        self.play_on_keys.setText('Сыграйте трезвучие на клавиатуре')
        self.notes = []

        def get_triade_notes():
            if len(self.notes) < 3:
                self.notes.append(self.sender().text())
            if len(self.notes) >= 3:
                self.play_on_keys.hide()
                note1, note2, note3 = self.notes
                a = [[i[0] for i in self.connection.cursor().execute(
                    f"SELECT notevalue FROM notes WHERE notename = '{note1}'").fetchall()][0],
                     [i[0] for i in self.connection.cursor().execute(
                         f"SELECT notevalue FROM notes WHERE notename = '{note2}'").fetchall()][0],
                     [i[0] for i in self.connection.cursor().execute(
                         f"SELECT notevalue FROM notes WHERE notename = '{note3}'").fetchall()][0]]

                a.sort()
                note1_value, note2_value, note3_value = a
                tri_value1 = note2_value - note1_value
                tri_value2 = note3_value - note2_value

                tri_n = [i[0] for i in self.connection.cursor().execute(
                    f"SELECT triname FROM triades WHERE length1"
                    f" = '{tri_value1}' AND length2 ="
                    f" '{tri_value2}'").fetchall()]
                tri_short = [i[0] for i in self.connection.cursor().execute(
                    f"SELECT trishort FROM triades WHERE length1 = '{tri_value1}' AND length2 ="
                    f" '{tri_value2}'").fetchall()]
                if tri_n and tri_short:
                    self.tri_name.setText(tri_n[0])
                    self.tri_label.setText(tri_short[0])
                else:
                    self.play_on_keys.show()
                    self.play_on_keys.setText('Ошибка! Такого трезвучия нет.')
                self.c.clicked.disconnect(get_triade_notes)
                self.cx.clicked.disconnect(get_triade_notes)
                self.d.clicked.disconnect(get_triade_notes)
                self.dx.clicked.disconnect(get_triade_notes)
                self.e.clicked.disconnect(get_triade_notes)
                self.f.clicked.disconnect(get_triade_notes)
                self.fx.clicked.disconnect(get_triade_notes)
                self.g.clicked.disconnect(get_triade_notes)
                self.gx.clicked.disconnect(get_triade_notes)
                self.a.clicked.disconnect(get_triade_notes)
                self.ax.clicked.disconnect(get_triade_notes)
                self.b.clicked.disconnect(get_triade_notes)
                self.c1.clicked.disconnect(get_triade_notes)
                self.c1x.clicked.disconnect(get_triade_notes)
                self.d1.clicked.disconnect(get_triade_notes)
                self.d1x.clicked.disconnect(get_triade_notes)
                self.e1.clicked.disconnect(get_triade_notes)
                self.f1.clicked.disconnect(get_triade_notes)
                self.f1x.clicked.disconnect(get_triade_notes)
                self.g1.clicked.disconnect(get_triade_notes)
                self.g1x.clicked.disconnect(get_triade_notes)
                self.a1.clicked.disconnect(get_triade_notes)
                self.a1x.clicked.disconnect(get_triade_notes)
                self.b1.clicked.disconnect(get_triade_notes)
        self.c.clicked.connect(get_triade_notes)
        self.cx.clicked.connect(get_triade_notes)
        self.d.clicked.connect(get_triade_notes)
        self.dx.clicked.connect(get_triade_notes)
        self.e.clicked.connect(get_triade_notes)
        self.f.clicked.connect(get_triade_notes)
        self.fx.clicked.connect(get_triade_notes)
        self.g.clicked.connect(get_triade_notes)
        self.gx.clicked.connect(get_triade_notes)
        self.a.clicked.connect(get_triade_notes)
        self.ax.clicked.connect(get_triade_notes)
        self.b.clicked.connect(get_triade_notes)
        self.c1.clicked.connect(get_triade_notes)
        self.c1x.clicked.connect(get_triade_notes)
        self.d1.clicked.connect(get_triade_notes)
        self.d1x.clicked.connect(get_triade_notes)
        self.e1.clicked.connect(get_triade_notes)
        self.f1.clicked.connect(get_triade_notes)
        self.f1x.clicked.connect(get_triade_notes)
        self.g1.clicked.connect(get_triade_notes)
        self.g1x.clicked.connect(get_triade_notes)
        self.a1.clicked.connect(get_triade_notes)
        self.a1x.clicked.connect(get_triade_notes)
        self.b1.clicked.connect(get_triade_notes)

    def load_triade(self):
        self.ftriade = QFileDialog.getOpenFileName(
            self, 'Выберите txt файл с названием интервала и его первую ноту, разделенные знаком ;',
            '', 'Текстовый файл (*.txt);;Все файлы (*)')[0]
        if self.ftriade:
            f = open(self.ftriade, encoding="utf8", mode='r')
            lines = f.readlines()
            triade, note = lines[0].split(';')
            self.tri_name.setText(triade)
            self.tri_label.setText([i[0] for i in self.connection.cursor().execute(
                f"SELECT trishort FROM triades WHERE triname = '{triade}'").fetchall()][0])
            one, two = self.connection.cursor().execute(
                f"SELECT length1, length2 FROM triades WHERE triname = '{triade}'").fetchall()[0]
            note1_value = [i[0] for i in self.connection.cursor().execute(
                f"SELECT notevalue FROM notes WHERE notename = '{note}'").fetchall()][0]
            note2 = [i[0] for i in self.connection.cursor().execute(
                f"SELECT notename FROM notes WHERE notevalue = '{note1_value + one}'"
                f"").fetchall()][0]
            note3 = [i[0] for i in self.connection.cursor().execute(
                f"SELECT notename FROM notes WHERE notevalue = '{note1_value + one + two}'"
                f"").fetchall()][0]
            self.play1.setText(note)
            self.play2.setText(note2)
            self.play3.setText(note3)
            self.play1.show()
            self.play2.show()
            self.play3.show()

    def change_triade(self):
        result = (i[0] for i in self.connection.cursor().execute(
            "SELECT trishort FROM triades").fetchall())
        triade, ok_pressed = QInputDialog.getItem(
            self, "Выберите интервал", "Выберите трезвучие, которому хотите поменять название:",
            result, 1, False)
        if ok_pressed:
            new_name, ok_pressed = QInputDialog.getText(
                self, "Введите название", "Введите новое название трезвучия:")
            if ok_pressed:
                self.connection.cursor().execute(
                    f"UPDATE triades SET triname = '{new_name}' WHERE trishort"
                    f" = '{triade}'")
                self.connection.commit()

    def make_triade(self):  # Создать свое трезвучие
        triade_name, ok_pressed = QInputDialog.getText(
            self, "Введите название", "Введите полное название вашего трезвучия:")
        if ok_pressed:
            triade_short, ok_pressed = QInputDialog.getText(
                self, "Введите название", "Введите короткое название вашего трезвучия:")
            if ok_pressed:
                triade_length1, ok_pressed = QInputDialog.getInt(
                    self, "Введите длину", "Введите длину первого интервала трезвучия "
                                           "(в полутонах):", 1, 1, 25)
                if ok_pressed:
                    triade_length2, ok_pressed = QInputDialog.getInt(
                        self, "Введите длину", "Введите длину второго интервала трезвучия "
                                               "(в полутонах):", 1, 1, 25 - triade_length1)
                    self.connection.cursor().execute(
                        f"INSERT INTO triades(triname, trishort, length1, length2) VALUES"
                        f"('{triade_name}', '{triade_short}', {triade_length1}, {triade_length2})")
                    self.connection.commit()

    def show_image(self, name):
        self.pixmap = QPixmap(f'img/{name}.png')
        self.image_file.setPixmap(self.pixmap)

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Solfegio()
    ex.show()
    sys.exit(app.exec_())
