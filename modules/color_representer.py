import cv2
import numpy as np
import webcolors
from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtGui import QColor
import pyttsx3


class ColorRepresenter(QObject):
    colorChanged = Signal()
    _named_lab = []
    speak_engine = pyttsx3.init()
    speak_engine.setProperty("rate",150)

    def __init__(self, color: QColor = QColor(0, 0, 0), parent: QObject = None):
        super().__init__(parent)
        self.color = color
        self._current_name = ""
        if not self._named_lab:
            self.generate_names()

    @Property(QColor, notify=colorChanged)
    def color(self):
        return self._color

    @color.setter
    def color(self, value: QColor):
        self._color = value
        self.colorChanged.emit()

    @Property(list, notify=colorChanged)
    def rgb(self):
        return [self._color.red(), self._color.green(), self._color.blue()]

    @Property(str, notify=colorChanged)
    def hex(self):
        return self._color.name().upper()

    @Property(list, notify=colorChanged)
    def hsv(self):
        return self._color.hue(), self._color.saturation(), self._color.value()

    @Property(list, notify=colorChanged)
    def bgr(self):
        return self._color.blue(), self._color.green(), self._color.red()

    @Property(list, notify=colorChanged)
    def bgra(self):
        return self._color.blue(), self._color.green(), self._color.red(), 255

    @Property(list, notify=colorChanged)
    def lab(self):
        bgr = np.uint8([[self.bgr]])
        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2Lab)[0, 0]
        return lab.tolist()

    @staticmethod
    def generate_names():
        for name in webcolors.names("css3"):
            rgb = webcolors.name_to_rgb(name)
            lab = ColorRepresenter.rgb_to_lab(rgb)
            ColorRepresenter._named_lab.append((name, lab))

    @staticmethod
    def rgb_to_lab(rgb):
        rgb = np.uint8([[rgb]])
        lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
        return lab[0][0]

    @staticmethod
    def lab_distance(lab1, lab2):
        return np.sqrt(np.sum((lab1 - lab2) ** 2))

    @staticmethod
    def closest_color(lab_input):
        min_distance = 1000000000
        closest_name = ""
        for name, lab in ColorRepresenter._named_lab:
            distance = ColorRepresenter.lab_distance(lab, lab_input)

            if distance < min_distance:
                min_distance = distance
                closest_name = name

        return closest_name

    @Property(str, notify=colorChanged)
    def name(self):
        self._current_name = self.closest_color(self.lab)
        return self._current_name

    @Slot()
    def speak(self):
        self.speak_engine.say(self._current_name)
        self.speak_engine.runAndWait()
