from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog, QMessageBox, \
    QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QFont

import sys
from datetime import datetime, time
from random import randint
import keyboard


class Controller(object):
    def __init__(self, view, model):
        self.view = view
        self.model = model
        pass

    def run(self):
        keyboard.on_press(self.on_press)
        keyboard.on_press_key('q', self.stop)

    def stop(self, key):
        print(f"press {key} to stop")
        self.view.stop_popping()

    def on_press(self, key):
        if self.model.is_sleep_time():
            print(f"press {key}")
            self.view.spank()
        else:
            self.view.stop_popping()


class View(QMainWindow):
    """Dialog."""

    def __init__(self, text, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.text = text
        current_time = datetime.now().time().strftime("%H:%M:%S")
        self.text_label = QLabel(f"It's {current_time} " + text)
        self.text_label.setFont(QFont('Arial', 40))
        self.text_label.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel()
        self.middle_label = QLabel()
        self.right_image_lebel = QLabel()
        # pixmap = QPixmap('resources/ferris.png')
        # self.image_label.setPixmap(pixmap)
        # self.image_label.setScaledContents(True)

        image_layout = QHBoxLayout()
        image_widget = QWidget()
        image_widget.setLayout(image_layout)
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.middle_label)
        image_layout.addWidget(self.right_image_lebel)

        dlgLayout = QVBoxLayout()
        dlgLayout.addWidget(self.text_label)
        dlgLayout.addWidget(image_widget)
        # self.setLayout(dlgLayout)

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(dlgLayout)
        # self._centralWidget.resize(pixmap.width(), pixmap.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_label)
        self.timer.start(3000)

    def set_invisable(self):
        self._centralWidget.resize(1, 2)
        self.show()

    def stop_popping(self):
        pass

    def update_label(self):
        current_time = datetime.now().time().strftime("%H:%M:%S")
        self.text_label.setText(f"It's {current_time} " + self.text)

    def spank(self):
        current_time = datetime.now().time().strftime("%H:%M:%S")
        self.text_label.setText(f"It's {current_time} " + self.text)
        pixmap = QPixmap('resources/spank1.jpg')
        self.image_label.setAlignment(Qt.AlignLeft)
        self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

        right_image = QPixmap('resources/spank2.jpeg')
        self.right_image_lebel.setAlignment(Qt.AlignRight)
        self.right_image_lebel.setPixmap(right_image.scaled(300, 300, Qt.KeepAspectRatio))

        middle_image = QPixmap('resources/spank3.jpeg')
        self.middle_label.setAlignment(Qt.AlignCenter)
        self.middle_label.setPixmap(middle_image.scaled(300, 300, Qt.KeepAspectRatio))
        # right_image.scaledToWidth(200)
        # right_image.scaledToHeight(200)
        # self._centralWidget.resize(pixmap.width() + right_image.width(), pixmap.height() + right_image.height())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, u'警告', u'确认退出?', QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Model(object):
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def get_text(self):
        now = datetime.now()
        return f"It's {now}, " + self.text

    def is_sleep_time(self):
        now = datetime.now()
        return self.is_between(now.time(), self.start_time, self.end_time)

    @staticmethod
    def is_between(now, start, end):
        if start <= end:
            return start <= now < end
        else:  # over midnight e.g., 23:30-04:15
            return start <= now or now < end


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = View("Time")
        self.setFixedSize(1, 2)
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.toggle_window)
        self.setCentralWidget(self.button)

    def toggle_window(self, checked):
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = MainWindow()
    # w.show()
    v = View("Your mom ask you to go to bed")
    v.set_invisable()
    # v.start_popping()
    model = Model(time(20), time(0))
    ctrl = Controller(view=v, model=model)
    ctrl.run()
    app.exec()
