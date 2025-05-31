from PySide6.QtCore import QObject, Signal, QPointF, Property, QPoint, Slot
from PySide6.QtGui import QColor, QImage, QImageReader


class Test(QObject):

    @Slot(str)
    def print(self, file_path):
        print(file_path)
