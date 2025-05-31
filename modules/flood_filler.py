from PySide6.QtGui import QImage
import numpy as np
import cv2

class FloodFiller:
    def __init__(self, tolerance: float = 60.0):
        self.tolerance = tolerance

    def qimage_to_bgr(self, image: QImage) -> np.ndarray:
        if image.format() != QImage.Format.Format_ARGB32:
            image = image.convertToFormat(QImage.Format.Format_ARGB32)

        w, h = image.width(), image.height()
        ptr = image.bits()
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((h, w, 4))
        bgr = arr[:, :, :3]
        return bgr

    def get_flood_fill_mask(self, image: QImage, x: int, y: int) -> np.ndarray:
        bgr = self.qimage_to_bgr(image)
        h, w, _ = bgr.shape
        target = bgr[y, x].astype(np.int16)
        diff = bgr.astype(np.int16) - target[None, None, :]
        dist = np.linalg.norm(diff, axis=2)
        thr_mask = (dist <= self.tolerance).astype(np.uint8)
        num_labels, labels = cv2.connectedComponents(thr_mask, connectivity=4)
        seed_label = labels[y, x]
        mask = (labels == seed_label)

        return mask

    def fill_mask(self, image: QImage, mask: np.ndarray, fill_color: tuple):
        if image.format() != QImage.Format.Format_ARGB32:
            image = image.convertToFormat(QImage.Format.Format_ARGB32)

        ptr = image.bits()
        h, w = image.height(), image.width()
        arr = np.frombuffer(ptr, dtype=np.uint8).reshape((h, w, 4))
        arr[mask] = fill_color
