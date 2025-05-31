import numpy as np
from PySide6.QtCore import QObject, Signal, QPointF, Property, QPoint, Slot
from PySide6.QtGui import QColor, QImage, QImageReader, QPainter
from modules.color_representer import ColorRepresenter
from modules.cvd_matrices import CVD
from modules.flood_filler import FloodFiller


class ImageContainer(QObject):
    presenterChanged = Signal()
    imageChanged = Signal()
    cursorChanged = Signal()

    def __init__(self, name: str = "original_image"):
        super().__init__()
        self.image = QImage()
        self._presenter = ColorRepresenter()
        self.offset = [0, 0, 1]
        self._image_params = [1, 1]
        self._cursor_pos = []
        self.name = name
        self.counter = 0
        self.imageChanged.connect(self.update_size)

    @Property(list, notify=cursorChanged)
    def cursor_pos(self):
        return self._cursor_pos

    @Property(str, notify=imageChanged)
    def provider_source(self):
        self.counter += 1
        return f"image://image_provider/{self.name}?" + str(self.counter)

    @Property(ColorRepresenter, notify=presenterChanged)
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, value):
        self._presenter = value
        self.presenterChanged.emit()

    @Slot(int, int)
    def color_at(self, x, y):
        if self.image and not self.image.isNull() and 0 <= x < self.image.width() and 0 <= y < self.image.height():
            self._presenter.color = self.image.pixelColor(x, y)

    @Slot()
    def update_size(self):
        if self.image.width() == 0:
            return
        img_aspect = self.image.width() / self.image.height()
        item_aspect = self._image_params[0] / self._image_params[1]
        offset_x, offset_y, scale = 0.0, 0.0, 1.0

        if img_aspect > item_aspect:
            scale = self._image_params[0] / self.image.width()
            offset_y = (self._image_params[1] - self.image.height() * scale) / 2
        else:
            scale = self._image_params[1] / self.image.height()
            offset_x = (self._image_params[0] - self.image.width() * scale) / 2

        self.offset = [offset_x, offset_y, scale]

    @Slot(float, float)
    def on_size_changed(self, width, height):
        self._image_params = width, height
        self.update_size()

    @Slot(float, float)
    def on_cursor_pos(self, x, y):
        self._cursor_pos = [
            (x - self.offset[0]) / self.offset[2],
            (y - self.offset[1]) / self.offset[2],
        ]
        self.cursorChanged.emit()

    @Slot()
    def color_update(self):
        self.color_at(self.cursor_pos[0], self.cursor_pos[1])


class ImageFloodContainer(ImageContainer):
    toleranceChanged = Signal()

    def __init__(self, name: str = "flood_image"):
        super().__init__(name=name)
        self.flood_filler = FloodFiller()
        self.original_image = QImage()

    @Property(int, notify=toleranceChanged)
    def tolerance(self):
        return self.flood_filler.tolerance

    @tolerance.setter
    def tolerance(self, value):
        self.flood_filler.tolerance = value
        self.toleranceChanged.emit()

    @Slot(int, int)
    def paint_at(self, x, y):
        if self.image and not self.image.isNull() and 0 <= x < self.image.width() and 0 <= y < self.image.height():
            self._presenter.color = self.image.pixelColor(x, y)
            mask = self.flood_filler.get_flood_fill_mask(self.image, x, y)
            self.flood_filler.fill_mask(self.image, mask, self._presenter.bgra)
            self.imageChanged.emit()

    @Slot()
    def paint(self):
        self.paint_at(int(self.cursor_pos[0]), int(self.cursor_pos[1]))

    @Slot()
    def reset(self):
        self.image = self.original_image.copy()
        self.imageChanged.emit()


class ImageShiftContainer(ImageContainer):
    severityChanged = Signal()
    cvdChanged = Signal()

    def __init__(self, name: str = "shift_image"):
        super().__init__(name=name)
        self._severity: float = 0
        self._cvd_type: str = "protanopia"
        self._cvd = CVD()
        self.original_container: ImageContainer = ImageContainer()

    def color_at(self, x, y):
        super().color_at(x, y)
        self.original_container.color_at(x, y)

    @Property(float, notify=severityChanged)
    def severity(self):
        return self._severity

    @severity.setter
    def severity(self, value):
        self._severity = value
        self.apply_shift()
        self.severityChanged.emit()

    @Property(str, notify=cvdChanged)
    def cvd_type(self):
        return self._cvd_type

    @cvd_type.setter
    def cvd_type(self, value):
        self._cvd_type = value
        self.apply_shift()
        self.cvdChanged.emit()

    def qimage_to_bgr(self, image: QImage) -> np.ndarray:
        if image.format() != QImage.Format.Format_ARGB32:
            image = image.convertToFormat(QImage.Format.Format_ARGB32)

        w, h = image.width(), image.height()
        ptr = image.bits()
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((h, w, 4))
        return arr[:, :, :3]


    @Slot()
    def apply_shift(self):
        bgr = self.qimage_to_bgr(self.original_container.image)
        corrected_bgr = self._cvd.apply_color_simulation(bgr, self.cvd_type, self.severity)
        ptr = self.image.bits()
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((self.image.height(), self.image.width(), 4))
        arr[:, :, 0:3] = corrected_bgr
        self.imageChanged.emit()


class ImageDaltonizeContainer(ImageShiftContainer):
    def __init__(self, name: str = "daltonize_image"):
        super().__init__(name)

    def apply_shift(self):
        bgr = self.qimage_to_bgr(self.original_container.image)
        corrected_bgr = self._cvd.apply_color_daltonization(bgr, self.cvd_type, self.severity)
        ptr = self.image.bits()
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((self.image.height(), self.image.width(), 4))
        arr[:, :, 0:3] = corrected_bgr
        self.imageChanged.emit()
