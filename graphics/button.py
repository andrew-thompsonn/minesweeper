from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal, Qt

class Button(QPushButton):
    leftClick = pyqtSignal()
    rightClick = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, QMouseEvent):

        if QMouseEvent.button() == Qt.RightButton:
            self.rightClick.emit()
        if QMouseEvent.button() == Qt.LeftButton:
            self.leftClick.emit()
