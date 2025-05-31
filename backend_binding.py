import os
from typing import Any

from PySide6.QtQml import QQmlApplicationEngine


class Engine:
    def __init__(self):
        self.engine = QQmlApplicationEngine()

    def bind(self, obj: Any, name: str):
        self.engine.rootContext().setContextProperty(name, obj)

    def bind_provider(self, obj:Any, name: str):
        self.engine.addImageProvider(name, obj)
        self.bind(obj, name)

    def load(self):
        qml_file = os.path.join(os.path.dirname(__file__), "qml\\main.qml")
        self.engine.load(qml_file)

    @property
    def is_loaded(self) -> bool:
        return bool(self.engine.rootObjects())


