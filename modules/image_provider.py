from PySide6.QtCore import Slot
from PySide6.QtGui import QImage
from PySide6.QtQuick import QQuickImageProvider
from modules.image_containers import ImageContainer, ImageFloodContainer, ImageShiftContainer, ImageDaltonizeContainer


class ImageProvider(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.Image)
        self.original_image = ImageContainer()
        self.flood_image = ImageFloodContainer()
        self.shift_image = ImageShiftContainer()
        self.daltonize_image = ImageDaltonizeContainer()


    @Slot(str)
    def load_image(self, path):
        self.original_image.image = QImage(path)
        self.flood_image.image = self.original_image.image.copy()
        self.flood_image.original_image = self.original_image.image
        self.shift_image.image = self.original_image.image.copy()
        self.shift_image.original_container = self.original_image
        self.daltonize_image.image = self.original_image.image.copy()
        self.daltonize_image.original_container = self.original_image
        self.original_image.imageChanged.emit()
        self.flood_image.imageChanged.emit()
        self.shift_image.imageChanged.emit()
        self.daltonize_image.imageChanged.emit()

    def requestImage(self, id, size, requestedSize):
        id = id.split("?")[0]
        image = QImage()
        if id == self.original_image.name:
            image = self.original_image.image
        elif id == self.flood_image.name:
            image = self.flood_image.image
        elif id == self.shift_image.name:
            image =  self.shift_image.image
        elif id == self.daltonize_image.name:
            image = self.daltonize_image.image

        size.setWidth(image.width())
        size.setHeight(image.height())
        return image