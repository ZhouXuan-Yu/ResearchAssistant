"""
Playwright 自动化回归测试 — 票据 OCR 服务
验证: API健康检查、票据识别、异常处理、批量处理
"""
import asyncio
import json
import os
import sys

# 添加 playwright 检查
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("正在安装 playwright...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    from playwright.async_api import async_playwright

OCR_URL = "http://localhost:8001"
TEST_IMAGE = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\receipt-ocr-service\test_receipt.png"

async def test_health_check(page):
    """测试1: 健康检查"""
    print("\n[TEST 1] 健康检查 /health")
    response = await page.request.get(f"{OCR_URL}/health")
    assert response.status == 200, f"Health check failed: {response.status}"
    data = await response.json()
    assert data["status"] == "healthy"
    assert "ocr_lang" in data
    print(f"  ✓ 服务健康: {data}")

async def test_api_docs(page):
    """测试2: API文档可访问"""
    print("\n[TEST 2] API 文档 /docs")
    response = await page.request.get(f"{OCR_URL}/docs")
    assert response.status == 200, f"Docs failed: {response.status}"
    text = await response.text()
    assert "Swagger" in text or "FastAPI" in text or "openapi" in text.lower()
    print(f"  ✓ API 文档可访问")

async def test_extract_vat_invoice(page):
    """测试3: 增值税发票识别"""
    print("\n[TEST 3] 增值税发票识别 POST /api/extract")
    
    with open(TEST_IMAGE, 'rb') as f:
        file_content = f.read()
    
    response = await page.request.post(
        f"{OCR_URL}/api/extract",
        multipart={
            'file': {
                'name': 'test_receipt.png',
                'mimeType': 'image/png',
                'buffer': file_content
            }
        },
        params={'enable_preprocess': 'true'}
    )
    
    assert response.status == 200, f"Extract failed: {response.status}"
    result = await response.json()
    
    # 验证关键字段
    assert result["success"] == True
    assert result["receipt_type"] in ["vat_invoice", "general", "receipt"]
    assert result["date"] is not None, "日期未提取"
    assert result["total_amount"] is not None, "总金额未提取"
    assert result["processing_time"] > 0
    assert 0 <= result["confidence"] <= 1
    
    print(f"  ✓ 票据类型: {result['receipt_type']}")
    print(f"  ✓ 日期: {result['date']}")
    print(f"  ✓ 总金额: ¥{result['total_amount']}")
    print(f"  ✓ 商户: {result['vendor_name']}")
    print(f"  ✓ 置信度: {result['confidence']:.2%}")
    print(f"  ✓ 耗时: {result['processing_time']:.2f}s")

async def test_invalid_file_type(page):
    """测试4: 无效文件类型处理"""
    print("\n[TEST 4] 异常处理 - 无效文件类型")
    
    response = await page.request.post(
        f"{OCR_URL}/api/extract",
        multipart={
            'file': {
                'name': 'test.txt',
                'mimeType': 'text/plain',
                'buffer': b'This is not an image'
            }
        }
    )
    
    assert response.status == 400, f"Should reject text file, got {response.status}"
    data = await response.json()
    assert data["success"] == False
    print(f"  ✓ 正确拒绝非图片文件: {data['error'][:50]}")

async def test_empty_file(page):
    """测试5: 空文件处理"""
    print("\n[TEST 5] 异常处理 - 空文件")
    
    response = await page.request.post(
        f"{OCR_URL}/api/extract",
        multipart={
            'file': {
                'name': 'empty.png',
                'mimeType': 'image/png',
                'buffer': b''
            }
        }
    )
    
    # 空文件应该返回错误
    assert response.status in [400, 413], f"Should reject empty file, got {response.status}"
    print(f"  ✓ 正确拒绝空文件 (status={response.status})")

async def test_classify_api(page):
    """测试6: 票据分类接口"""
    print("\n[TEST 6] 票据分类 GET /api/classify")
    
    test_text = "增值税普通发票 发票代码 110023456789 开票日期 2026年06月15日"
    response = await page.request.get(
        f"{OCR_URL}/api/classify",
        params={'raw_text': test_text}
    )
    
    assert response.status == 200
    data = await response.json()
    assert data["receipt_type"] == "vat_invoice"
    print(f"  ✓ 正确分类为增值税发票: {data}")

async def test_concurrent_requests(page):
    """测试7: 并发请求鲁棒性"""
    print("\n[TEST 7] 鲁棒性 - 并发请求")
    
    # EasyOCR不是线程安全的，但FastAPI的async endpoint会排队
    async def send_request(i):
        with open(TEST_IMAGE, 'rb') as f:
            content = f.read()
        response = await page.request.post(
            f"{OCR_URL}/api/extract",
            multipart={
                'file': {
                    'name': f'test_{i}.png',
                    'mimeType': 'image/png',
                    'buffer': content
                }
            },
            timeout=120000
        )
        return response.status
    
    tasks = [send_request(i) for i in range(3)]
    results = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in results if r == 200)
    print(f"  ✓ 并发3请求: {success_count}/3 成功 (results: {results})")
    assert success_count >= 1, f"并发请求全部失败: {results}"

async def test_preprocessing_toggle(page):
    """测试8: 预处理开关"""
    print("\n[TEST 8] 功能 - 预处理开关")
    
    with open(TEST_IMAGE, 'rb') as f:
        content = f.read()
    
    # 禁用预处理
    response1 = await page.request.post(
        f"{OCR_URL}/api/extract",
        multipart={
            'file': {
                'name': 'test.png',
                'mimeType': 'image/png',
                'buffer': content
            }
        },
        params={'enable_preprocess': 'false'}
    )
    
    # 启用预处理
    response2 = await page.request.post(
        f"{OCR_URL}/api/extract",
        multipart={
            'file': {
                'name': 'test.png',
                'mimeType': 'image/png',
                'buffer': content
            }
        },
        params={'enable_preprocess': 'true'}
    )
    
    assert response1.status == 200
    assert response2.status == 200
    
    r1 = await response1.json()
    r2 = await response2.json()
    
    print(f"  ✓ 无预处理: 置信度={r1['confidence']:.2%}, 文本行={len(r1.get('raw_text','').splitlines())}")
    print(f"  ✓ 有预处理: 置信度={r2['confidence']:.2%}, 文本行={len(r2.get('raw_text','').splitlines())}")

async def main():
    print("=" * 60)
    print("Playwright 自动化回归测试 — 票据 OCR 服务")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        tests = [
            ("健康检查", test_health_check),
            ("API文档", test_api_docs),
            ("增值税发票识别", test_extract_vat_invoice),
            ("无效文件类型", test_invalid_file_type),
            ("空文件处理", test_empty_file),
            ("票据分类", test_classify_api),
            ("预处理开关", test_preprocessing_toggle),
            ("并发请求", test_concurrent_requests),
        ]
        
        passed = 0
        failed = 0
        
        for name, test_fn in tests:
            try:
                await test_fn(page)
                passed += 1
            except AssertionError as e:
                failed += 1
                print(f"  ✗ 失败: {e}")
            except Exception as e:
                failed += 1
                print(f"  ✗ 异常: {type(e).__name__}: {e}")
        
        await browser.close()
    
    print(f"\n{'=' * 60}")
    print(f"测试结果: {passed} 通过, {failed} 失败, 共 {len(tests)} 项")
    print(f"{'=' * 60}")
    
    return failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
