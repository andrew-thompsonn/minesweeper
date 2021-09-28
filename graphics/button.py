from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal, Qt

class Button(QPushButton):
    """ A class used to override the signals emitted by a QPushButton
    """
    # Left click signal
    leftClick = pyqtSignal()
    # Right click signal
    rightClick = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, QMouseEvent):
        """ A method to override a mouse press event

            Inputs:     QMouseEvent <event>
            Outputs:    None
        """
        if QMouseEvent.button() == Qt.RightButton:
            self.rightClick.emit()
        if QMouseEvent.button() == Qt.LeftButton:
            self.leftClick.emit()
