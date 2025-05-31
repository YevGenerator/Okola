import sys

from PySide6.QtGui import QGuiApplication
from backend_binding import Engine
from modules.test import Test
from modules.image_provider import ImageProvider

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = Engine()

    test = Test()
    image_provider = ImageProvider()
    modified_image_provider = ImageProvider()

    engine.bind(test, "log")
    engine.bind_provider(image_provider, "image_provider")
    engine.bind(image_provider.original_image, "original_image")
    engine.bind(image_provider.shift_image, "shift_image")
    engine.bind(image_provider.flood_image, "flood_image")
    engine.bind(image_provider.daltonize_image, image_provider.daltonize_image.name)
    engine.load()

    if not engine.is_loaded:
        sys.exit(-1)

    sys.exit(app.exec())