import numpy as np
import cv2
from modules.cvd_machado_matrices import CVD_MACHADO_MATRICES


class CVD:
    def __init__(self):
        self.matrices = CVD_MACHADO_MATRICES

    def linearize_srgb(self, x):
        """sRGB -> linear RGB"""
        mask = x <= 0.04045
        return np.where(mask, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)

    def gamma_correct(self, x):
        """linear RGB -> sRGB"""
        mask = x <= 0.0031308
        return np.where(mask, x * 12.92, 1.055 * (x ** (1 / 2.4)) - 0.055)

    def apply_color_simulation(self, image_bgr: np.ndarray, cb_type: str, severity: float) -> np.ndarray:
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) / 255.0
        image_linear = self.linearize_srgb(image_rgb)
        idx = int(severity * 10)
        mat = self.matrices[cb_type][idx]
        transformed = np.clip(image_linear @ mat.T, 0.0, 1.0)
        corrected_srgb = self.gamma_correct(transformed)
        corrected_uint8 = (corrected_srgb * 255).astype(np.uint8)
        return cv2.cvtColor(corrected_uint8, cv2.COLOR_RGB2BGR)

    def apply_color_daltonization(self, image_bgr: np.ndarray, cb_type: str, severity: float = 1.0,
                                  correction_factor: float = 1.0) -> np.ndarray:
        img_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) / 255.0
        img_linear = self.linearize_srgb(img_rgb)

        idx = int(severity * 10)
        mat = self.matrices[cb_type][idx]

        sim_linear = np.clip(img_linear @ mat.T, 0.0, 1.0)
        error = img_linear - sim_linear
        correction_matrix = np.array([
            [0, 0, 0],
            [0.7, 1, 0],
            [0.7, 0, 1]
        ])

        correction = error @ correction_matrix.T
        corrected_linear = np.clip(img_linear + correction_factor * correction, 0.0, 1.0)

        corrected_srgb = self.gamma_correct(corrected_linear)
        corrected_uint8 = (corrected_srgb * 255).astype(np.uint8)
        return cv2.cvtColor(corrected_uint8, cv2.COLOR_RGB2BGR)
