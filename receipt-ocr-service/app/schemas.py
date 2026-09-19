"""数据模型定义"""

from pydantic import BaseModel, Field
from typing import Optional, List


class ReceiptItem(BaseModel):
    """票据行项目"""
    name: str = Field(description="商品/服务名称")
    quantity: float = Field(default=1.0, ge=0, description="数量")
    unit_price: Optional[float] = Field(default=None, ge=0, description="单价")
    amount: Optional[float] = Field(default=None, ge=0, description="金额")


class ExtractionResult(BaseModel):
    """票据提取完整结果"""
    success: bool = Field(description="是否成功")
    receipt_type: Optional[str] = Field(
        default=None,
        description="票据类型: vat_invoice(增值税发票) / receipt(小票) / taxi(的士票) / train(火车票) / general(通用)"
    )
    vendor_name: Optional[str] = Field(default=None, description="商户/开票方名称")
    receipt_number: Optional[str] = Field(default=None, description="票据编号/发票号码")
    date: Optional[str] = Field(default=None, description="日期 YYYY-MM-DD")
    total_amount: Optional[float] = Field(default=None, ge=0, description="总金额")
    tax_amount: Optional[float] = Field(default=None, ge=0, description="税额")
    currency: str = Field(default="CNY", description="货币")
    items: List[ReceiptItem] = Field(default_factory=list, description="行项目列表")
    raw_text: str = Field(default="", description="OCR全量文本")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="整体置信度")
    processing_time: float = Field(default=0.0, ge=0, description="处理耗时/秒")
    warnings: List[str] = Field(default_factory=list, description="警告信息")


class HealthResponse(BaseModel):
    status: str
    version: str
    ocr_lang: str
    gpu_available: bool
