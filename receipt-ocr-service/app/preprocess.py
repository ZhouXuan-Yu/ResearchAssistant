"""图像预处理模块"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple


def load_image_from_bytes(data: bytes) -> np.ndarray:
    """从字节流加载图片为 numpy 数组 (BGR for OpenCV)"""
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("无法解码图片，请确认文件为有效图片格式")
    return img


def preprocess_for_ocr(img: np.ndarray) -> np.ndarray:
    """
    OCR 前预处理管道:
    1. 大图缩放到合理尺寸
    2. 灰度化 + CLAHE 增强对比度
    3. 双边滤波去噪保边
    4. 锐化增强文字边缘
    """
    h, w = img.shape[:2]

    # 1. 限制最大边 2000px, 保持宽高比
    max_size = 2000
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    # 2. 转灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. CLAHE 自适应直方图均衡化（提升低对比度票据的可读性）
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 4. 双边滤波（去噪同时保留边缘）
    denoised = cv2.bilateralFilter(enhanced, d=9, sigmaColor=75, sigmaSpace=75)

    # 5. 轻度锐化
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    # 转回 BGR 给 PaddleOCR（它也能直接吃灰度图，但 BGR 更稳）
    return cv2.cvtColor(sharpened, cv2.COLOR_GRAY2BGR)


def detect_skew_angle(img: np.ndarray) -> float:
    """检测图片倾斜角度（用于后续纠偏，可选功能）"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)
    if lines is None:
        return 0.0
    angles = []
    for line in lines:
        rho, theta = line[0]
        angle = theta * 180.0 / np.pi - 90
        if -45 < angle < 45:
            angles.append(angle)
    if not angles:
        return 0.0
    return np.median(angles)


def rotate_image(img: np.ndarray, angle: float) -> np.ndarray:
    """旋转图片以纠正倾斜"""
    if abs(angle) < 0.5:
        return img
    h, w = img.shape[:2]
    center = (w / 2, h / 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, matrix, (w, h),
                             borderMode=cv2.BORDER_REPLICATE)
    return rotated
