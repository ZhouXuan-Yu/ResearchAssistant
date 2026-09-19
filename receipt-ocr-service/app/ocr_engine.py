"""EasyOCR 引擎封装 — 轻量级方案，构建速度快"""

import numpy as np
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class OCREngine:
    """
    EasyOCR 封装，统一 OCR 识别接口。
    支持 CPU/GPU、多语言、文字方向检测。
    """

    def __init__(
        self,
        lang_list: list = None,
        use_gpu: bool = False,
        gpu_id: int = 0,
    ):
        """
        Args:
            lang_list: 语言列表，默认 ['ch_sim', 'en'] 简体中文+英文
            use_gpu: 是否使用 GPU
            gpu_id: GPU 设备 ID
        """
        if lang_list is None:
            lang_list = ['ch_sim', 'en']
        self.lang_list = lang_list
        self.use_gpu = use_gpu
        self.gpu_id = gpu_id
        self._reader = None

    @property
    def reader(self):
        """懒加载 EasyOCR Reader"""
        if self._reader is None:
            import easyocr
            logger.info(
                f"Initializing EasyOCR: langs={self.lang_list}, gpu={self.use_gpu}"
            )
            kwargs = {
                'lang_list': self.lang_list,
                'gpu': self.use_gpu,
                'verbose': False,
            }
            if self.use_gpu:
                kwargs['gpu_id'] = self.gpu_id
            self._reader = easyocr.Reader(**kwargs)
            logger.info("EasyOCR initialized successfully")
        return self._reader

    def recognize(self, image: np.ndarray) -> list:
        """
        原始 OCR 识别。

        Args:
            image: numpy 数组 (BGR 格式)

        Returns:
            [[bbox, text, confidence], ...]
            bbox: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
        """
        result = self.reader.readtext(image, detail=1, paragraph=False)
        return result

    def extract_text_lines(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        提取结构化的文本行列表，按阅读顺序排序。

        Returns:
            [
                {
                    "text": "合计",
                    "confidence": 0.987,
                    "x": 450.5,
                    "y": 120.3,
                    "width": 80.2,
                    "height": 24.6,
                    "bbox": [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
                },
                ...
            ]
        """
        items = self.recognize(image)
        lines = []
        for bbox, text, conf in items:
            if not text or not text.strip():
                continue

            # 计算几何属性
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            x_center = sum(xs) / len(xs)
            y_center = sum(ys) / len(ys)
            width = max(xs) - min(xs)
            height = max(ys) - min(ys)

            lines.append({
                "text": text.strip(),
                "confidence": round(conf, 4),
                "x": round(x_center, 1),
                "y": round(y_center, 1),
                "width": round(width, 1),
                "height": round(height, 1),
                "bbox": [[round(p[0], 1), round(p[1], 1)] for p in bbox],
            })

        # 按阅读顺序排序：先按 y 分组（行），再按 x 排
        if lines:
            lines.sort(key=lambda l: (round(l["y"] / 25), l["x"]))

        return lines

    def get_raw_text(self, lines: List[Dict]) -> str:
        """将文本行列表拼接为纯文本"""
        return "\n".join(l["text"] for l in lines)

    def warm_up(self):
        """预热引擎（用空白图触发初始化）"""
        dummy = np.zeros((100, 100, 3), dtype=np.uint8)
        self.recognize(dummy)
        logger.info("OCREngine warm-up complete")
