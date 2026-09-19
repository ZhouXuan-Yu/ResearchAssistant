"""票据字段提取器 — 正则规则为主，支持扩展 LLM 兜底"""

import re
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from app.schemas import ExtractionResult, ReceiptItem

logger = logging.getLogger(__name__)


class FieldExtractor:
    """
    基于正则 + 位置启发式的票据关键字段提取器。

    设计原则:
    1. 正则优先 —— 零成本、可解释、快速
    2. 位置辅助 —— 利用 OCR 返回的坐标信息做区域裁剪
    3. 预留 LLM 兜底接口 —— 正则命不中的字段交给 LLM
    """

    # ==================== 正则模式库 ====================

    DATE_PATTERNS = [
        # 标准日期格式
        (r'(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})[日号]?', 'standard'),
        # 前导关键词
        (r'(?:开票日期|发票日期|日期|时间|Date)[：:\s]*(\d{4}[-/年]?\d{1,2}[-/月]?\d{1,2})', 'keyword'),
        (r'(?:开票日期|发票日期|日期|时间|Date)[：:\s]*(\d{4}[-/年]?\d{1,2}[-/月]?\d{1,2})', 'keyword'),
    ]

    AMOUNT_PATTERNS = [
        # 价税合计（增值税发票特有）
        (r'(?:价税合计|大写.*小写)[^\d]*[¥￥]?(\d{1,3}(?:,\d{3})*\.?\d{0,2})', 'total'),
        # 合计/总计
        (r'(?:合\s*计|总\s*计|应\s*付|实\s*付|金\s*额|消费金额|小计)[^\d]*[¥￥]?\s*(\d{1,3}(?:,\d{3})*\.?\d{0,2})', 'total'),
        # ¥符号
        (r'[¥￥]\s*(\d{1,3}(?:,\d{3})*\.?\d{0,2})', 'currency'),
        # 元结尾
        (r'(\d{1,3}(?:,\d{3})*\.?\d{0,2})\s*元', 'yuan'),
        # 税额
        (r'(?:税\s*额|税\s*金)[^\d]*[¥￥]?\s*(\d{1,3}(?:,\d{3})*\.?\d{0,2})', 'tax'),
    ]

    TAX_PATTERNS = [
        (r'(?:税\s*额|税\s*金|税率)[^\d]*[¥￥]?\s*(\d{1,3}(?:,\d{3})*\.?\d{0,2})', 'tax_amount'),
        (r'(?:税\s*率)[^\d]*(\d{1,2}(?:\.\d+)?)\s*%?', 'tax_rate'),
    ]

    NUMBER_PATTERNS = [
        # 发票号码
        (r'(?:发票号码|发票号|No\.?|编号)[：:\s]*([A-Z0-9]{6,20})', 'invoice_no'),
        # 发票代码
        (r'(?:发票代码)[：:\s]*([0-9]{10,12})', 'invoice_code'),
        # 订单号/流水号
        (r'(?:订单号|流水号|单号|交易号)[：:\s]*([A-Za-z0-9\-_]{6,40})', 'order_no'),
    ]

    VENDOR_PATTERNS = [
        # 销售方/开票方
        (r'(?:销[售受]方|开票方|收款方|商户)\s*(?:名称)?[：:\s]*([\u4e00-\u9fa5()（）a-zA-Z\w·]{4,50})', 'vendor'),
        # 名称（在"名 称"关键字的行中）
        (r'名\s*称[：:\s]*([\u4e00-\u9fa5()（）a-zA-Z\w·]{4,50})', 'vendor_alt'),
    ]

    ITEM_LINE_PATTERN = re.compile(
        r'^(.+?)\s*[×xX\*]?\s*(\d+\.?\d*)?\s*[×xX\*]?\s*(\d+\.?\d*)?\s*(\d+\.?\d{1,2})$'
    )

    # ==================== 类型分类 ====================

    def _classify_receipt(self, text: str) -> str:
        """根据关键词判断票据类型"""
        kw_map = [
            ("vat_invoice", ["增值税", "发票联", "抵扣联", "记账联", "发票代码"]),
            ("taxi", ["出租车", "的士", "燃油附加费", "TAXI"]),
            ("train", ["火车票", "车次", "席别", "中国铁路"]),
            ("receipt", ["小票", "收银", "POS", "购物清单", "流水单", "收据"]),
        ]
        scores = {}
        for rtype, kws in kw_map:
            scores[rtype] = sum(1 for kw in kws if kw in text)

        best = max(scores, key=scores.get)
        if scores[best] >= 2:
            return best
        return "general"

    # ==================== 核心提取 ====================

    def extract(self, text_lines: List[Dict], raw_text: str,
                use_position: bool = True) -> ExtractionResult:
        """
        主提取入口。

        Args:
            text_lines: OCR 返回的结构化文本行（含坐标）
            raw_text: 拼接后的纯文本
            use_position: 是否使用位置信息辅助提取

        Returns:
            ExtractionResult
        """
        result = ExtractionResult(
            success=True,
            raw_text=raw_text,
            receipt_type=self._classify_receipt(raw_text),
        )
        warnings = []

        # 1. 日期
        date_str = self._extract_date(raw_text)
        if date_str:
            result.date = date_str
        else:
            warnings.append("未能提取日期")

        # 2. 编号
        number = self._extract_number(raw_text)
        if number:
            result.receipt_number = number
        else:
            warnings.append("未能提取票据编号")

        # 3. 商户名称
        vendor = self._extract_vendor(raw_text, text_lines)
        if vendor:
            result.vendor_name = vendor
        else:
            warnings.append("未能提取商户名称")

        # 4. 金额（总金额 + 税额）
        amounts = self._extract_amounts(raw_text)
        if amounts:
            result.total_amount = amounts.get("total")
            result.tax_amount = amounts.get("tax")
            if result.total_amount is None:
                warnings.append("未能提取总金额")
        else:
            warnings.append("未能提取金额信息")

        # 5. 行项目
        if text_lines:
            result.items = self._extract_line_items(text_lines)

        # 6. 整体置信度
        if text_lines:
            result.confidence = round(
                sum(l["confidence"] for l in text_lines) / len(text_lines), 4
            )

        result.warnings = warnings
        if len(warnings) >= 3:
            # 3 个以上关键字段缺失，标记为部分成功
            result.success = len(warnings) < 5

        return result

    # ==================== 字段提取子方法 ====================

    def _extract_date(self, text: str) -> Optional[str]:
        """提取日期，标准化为 YYYY-MM-DD"""
        for pattern, _ in self.DATE_PATTERNS:
            m = re.search(pattern, text)
            if m:
                groups = m.groups()
                if len(groups) == 3:
                    y, mo, d = groups
                    try:
                        year = int(y)
                        month = int(mo) if len(mo) <= 2 else int(mo) if int(mo) <= 12 else None
                        day = int(d) if d and int(d) <= 31 else None
                        if year and month and day:
                            return f"{year:04d}-{month:02d}-{day:02d}"
                    except (ValueError, TypeError):
                        pass
                elif len(groups) == 1:
                    raw = groups[0]
                    # 尝试直接解析
                    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日", "%Y%m%d"]:
                        try:
                            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
                        except ValueError:
                            continue
        return None

    def _extract_number(self, text: str) -> Optional[str]:
        """提取票据编号"""
        for pattern, _ in self.NUMBER_PATTERNS:
            m = re.search(pattern, text)
            if m:
                return m.group(1).strip()
        return None

    def _extract_vendor(self, text: str, lines: List[Dict]) -> Optional[str]:
        """提取商户名称"""
        # 正则优先
        for pattern, _ in self.VENDOR_PATTERNS:
            m = re.search(pattern, text)
            if m:
                name = m.group(1).strip()
                # 过滤掉纯数字或过短的
                if len(name) >= 2 and not name.isdigit():
                    return name

        # 位置启发：票据顶部通常有商户名（取前 15% 区域内最长中文文本行）
        if lines:
            ys = [l["y"] for l in lines]
            y_min, y_max = min(ys), max(ys)
            top_threshold = y_min + (y_max - y_min) * 0.15
            top_lines = [l for l in lines if l["y"] <= top_threshold]
            if top_lines:
                # 找最长的中文行
                best = max(top_lines, key=lambda l: len(l["text"]))
                if len(best["text"]) >= 4:
                    return best["text"]
        return None

    def _extract_amounts(self, text: str) -> Dict[str, Optional[float]]:
        """提取金额信息，返回 {total, tax}"""
        result = {"total": None, "tax": None}
        all_amounts = []

        for pattern, ptype in self.AMOUNT_PATTERNS:
            for m in re.finditer(pattern, text):
                try:
                    val = float(m.group(1).replace(",", ""))
                    all_amounts.append((val, ptype))
                except (ValueError, TypeError):
                    continue

        if not all_amounts:
            return result

        # 分类
        tax_values = [v for v, t in all_amounts if t == "tax"]
        total_values = [v for v, t in all_amounts if t == "total"]
        currency_values = [v for v, t in all_amounts if t == "currency"]
        yuan_values = [v for v, t in all_amounts if t == "yuan"]

        # 总金额：优先取 total 类别的最大值
        candidates = total_values + currency_values + yuan_values
        if candidates:
            result["total"] = round(max(candidates), 2)

        # 税额：取 tax 类别的最大值
        if tax_values:
            result["tax"] = round(max(tax_values), 2)

        return result

    def _extract_line_items(self, text_lines: List[Dict]) -> List[ReceiptItem]:
        """提取行项目列表"""
        items = []
        for line in text_lines:
            txt = line["text"]
            m = self.ITEM_LINE_PATTERN.match(txt)
            if m:
                name = m.group(1).strip()
                # 去掉名字中的纯数字和符号前缀
                name = re.sub(r'^[\d\.\s×xX\*]+', '', name).strip()
                if len(name) >= 2:
                    amount = None
                    g2, g3, g4 = m.group(2), m.group(3), m.group(4)
                    try:
                        amount = float(g4) if g4 else (float(g3) if g3 else None)
                    except (ValueError, TypeError):
                        pass

                    if amount is not None and amount >= 0.01:
                        item = ReceiptItem(name=name, amount=round(amount, 2))
                        try:
                            item.quantity = float(g2) if g2 else 1.0
                        except (ValueError, TypeError):
                            pass
                        items.append(item)

        return items

    # ==================== LLM 兜底接口（预留） ====================

    def needs_llm_fallback(self, result: ExtractionResult) -> List[str]:
        """
        判断哪些字段需要 LLM 二次提取。
        返回需要 LLM 兜底的字段名列表。
        """
        missing = []
        if not result.vendor_name:
            missing.append("vendor_name")
        if not result.receipt_number:
            missing.append("receipt_number")
        if not result.date:
            missing.append("date")
        if not result.total_amount:
            missing.append("total_amount")
        return missing
