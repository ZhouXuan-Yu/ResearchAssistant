"""Receipt OCR Service — FastAPI 主入口"""

import io
import time
import logging
import traceback
from pathlib import Path
from typing import Optional

import yaml
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.ocr_engine import OCREngine
from app.extractor import FieldExtractor
from app.preprocess import load_image_from_bytes, preprocess_for_ocr
from app.schemas import ExtractionResult, HealthResponse

# ==================== 日志 ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("receipt-ocr")

# ==================== 配置加载 ====================
def load_config() -> dict:
    config_path = Path(__file__).parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

config = load_config()
ocr_config = config.get("ocr", {})
server_config = config.get("server", {})

# ==================== FastAPI 应用 ====================
app = FastAPI(
    title="Receipt OCR Service",
    version="1.0.0",
    description="票据识别微服务 — 基于 PaddleOCR + 规则提取",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 全局单例 ====================
ocr_engine = OCREngine(
    lang_list=ocr_config.get("lang_list", ["ch_sim", "en"]),
    use_gpu=ocr_config.get("use_gpu", False),
)

extractor = FieldExtractor()


@app.on_event("startup")
async def startup_event():
    """启动时预热 OCR 引擎"""
    logger.info("Warming up OCR engine...")
    try:
        ocr_engine.warm_up()
        logger.info("OCR engine ready")
    except Exception as e:
        logger.error(f"OCR engine warm-up failed: {e}")


# ==================== 端点 ====================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        ocr_lang=str(ocr_engine.lang_list),
        gpu_available=ocr_engine.use_gpu,
    )


@app.get("/")
async def root():
    return {
        "service": "Receipt OCR Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.post("/api/extract", response_model=ExtractionResult)
async def extract_receipt(
    file: UploadFile = File(..., description="票据图片文件 (JPEG/PNG/WEBP)"),
    enable_preprocess: bool = Query(True, description="是否启用图像预处理"),
    enable_position: bool = Query(True, description="是否使用位置信息辅助提取"),
):
    """
    票据识别主接口。

    接收票据图片，执行 OCR 识别 + 字段结构化提取，返回 JSON 结果。

    支持格式: JPEG, PNG, BMP, WEBP, TIFF
    """
    t_start = time.time()

    # --- 校验 ---
    if not file.content_type:
        raise HTTPException(400, "无法确定文件类型")
    allowed_types = {"image/jpeg", "image/png", "image/bmp", "image/webp", "image/tiff"}
    if file.content_type not in allowed_types:
        raise HTTPException(400, f"不支持的图片格式: {file.content_type}。支持: {', '.join(allowed_types)}")

    # --- 读取 ---
    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, "上传的文件为空")
        if len(contents) > 50 * 1024 * 1024:  # 50MB
            raise HTTPException(413, "文件过大，限制 50MB")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"读取文件失败: {str(e)}")

    # --- 预处理 ---
    try:
        img = load_image_from_bytes(contents)
        if enable_preprocess:
            img = preprocess_for_ocr(img)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        logger.error(f"Image preprocessing failed: {traceback.format_exc()}")
        raise HTTPException(500, f"图片预处理失败: {str(e)}")

    # --- OCR ---
    try:
        text_lines = ocr_engine.extract_text_lines(img)
        raw_text = ocr_engine.get_raw_text(text_lines)
    except Exception as e:
        logger.error(f"OCR failed: {traceback.format_exc()}")
        raise HTTPException(500, f"OCR识别失败: {str(e)}")

    if not text_lines:
        return ExtractionResult(
            success=False,
            raw_text="",
            warnings=["OCR 未能识别任何文字，请检查图片质量"],
            processing_time=round(time.time() - t_start, 3),
        )

    # --- 结构化提取 ---
    try:
        result = extractor.extract(text_lines, raw_text, use_position=enable_position)
    except Exception as e:
        logger.error(f"Field extraction failed: {traceback.format_exc()}")
        result = ExtractionResult(
            success=False,
            raw_text=raw_text,
            warnings=[f"字段提取异常: {str(e)}"],
        )

    result.processing_time = round(time.time() - t_start, 3)
    logger.info(
        f"Extraction complete: type={result.receipt_type}, "
        f"vendor={result.vendor_name}, total={result.total_amount}, "
        f"conf={result.confidence:.2f}, time={result.processing_time}s, "
        f"warnings={len(result.warnings)}"
    )

    return result


@app.post("/api/extract-batch")
async def extract_batch(
    files: list[UploadFile] = File(..., description="多张票据图片"),
    enable_preprocess: bool = Query(True),
):
    """
    批量识别接口（最多 10 张）。
    """
    if len(files) > 10:
        raise HTTPException(400, "批量上限为 10 张")
    if len(files) == 0:
        raise HTTPException(400, "至少上传一张图片")

    results = []
    for f in files:
        # 复用单张逻辑（简化版）
        try:
            contents = await f.read()
            img = load_image_from_bytes(contents)
            if enable_preprocess:
                img = preprocess_for_ocr(img)
            text_lines = ocr_engine.extract_text_lines(img)
            raw_text = ocr_engine.get_raw_text(text_lines)
            r = extractor.extract(text_lines, raw_text)
            results.append(r)
        except Exception as e:
            results.append(ExtractionResult(
                success=False,
                warnings=[f"{f.filename}: {str(e)}"],
            ))

    return {
        "total": len(results),
        "success_count": sum(1 for r in results if r.success),
        "results": results,
    }


@app.get("/api/classify")
async def classify_text(raw_text: str = Query(..., description="OCR 全量文本")):
    """仅做票据类型分类（无需图片）"""
    rtype = extractor._classify_receipt(raw_text)
    return {"receipt_type": rtype, "text_length": len(raw_text)}


@app.post("/api/ocr-only")
async def ocr_only(
    file: UploadFile = File(...),
    enable_preprocess: bool = Query(True),
):
    """仅 OCR 识别，不做结构化提取"""
    contents = await file.read()
    img = load_image_from_bytes(contents)
    if enable_preprocess:
        img = preprocess_for_ocr(img)
    text_lines = ocr_engine.extract_text_lines(img)
    return {
        "lines": text_lines,
        "raw_text": ocr_engine.get_raw_text(text_lines),
        "line_count": len(text_lines),
    }


# ==================== 全局异常处理 ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error", "detail": str(exc)},
    )
