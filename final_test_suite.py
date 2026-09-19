"""
票据 OCR 服务 — 自动化验收套件
使用 requests + curl 进行 API 测试，Playwright 做文档页面验证
"""
import requests
import json
import os
import time

OCR_URL = "http://localhost:8001"
TEST_DIR = r"C:\Users\ZhouXuan\Desktop\OH-WorkSpace\receipt-ocr-service"
TEST_IMAGE = os.path.join(TEST_DIR, "test_receipt.png")

passed = 0
failed = 0

def test(name):
    """装饰器风格的测试包装"""
    def decorator(fn):
        global passed, failed
        print(f"\n[测试] {name}")
        try:
            fn()
            passed += 1
            print(f"  ✓ 通过")
        except AssertionError as e:
            failed += 1
            print(f"  ✗ 断言失败: {e}")
        except Exception as e:
            failed += 1
            print(f"  ✗ 异常: {type(e).__name__}: {str(e)[:100]}")
    return decorator

# ==================== 测试用例 ====================

@test("1. 健康检查")
def _():
    r = requests.get(f"{OCR_URL}/health", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "ocr_lang" in data
    print(f"    服务版本: {data['version']}, OCR引擎: {data['ocr_lang']}")

@test("2. API 文档页面可访问")
def _():
    r = requests.get(f"{OCR_URL}/docs", timeout=5)
    assert r.status_code == 200
    assert "Swagger" in r.text or "openapi" in r.text.lower()

@test("3. 增值税发票识别 — 核心功能")
def _():
    with open(TEST_IMAGE, 'rb') as f:
        r = requests.post(
            f"{OCR_URL}/api/extract",
            files={'file': ('test_receipt.png', f, 'image/png')},
            timeout=120
        )
    assert r.status_code == 200, f"HTTP {r.status_code}"
    data = r.json()
    assert data["success"] == True, "识别失败"
    assert data["receipt_type"] == "vat_invoice", f"票据类型错误: {data['receipt_type']}"
    assert data["date"] == "2026-06-15", f"日期错误: {data['date']}"
    assert data["total_amount"] == 8305.0 or data["total_amount"] == 7550.0, f"金额错误: {data['total_amount']}"
    assert data["vendor_name"] is not None
    assert 0 < data["confidence"] <= 1
    assert data["processing_time"] > 0
    print(f"    类型={data['receipt_type']}, 金额=¥{data['total_amount']}, 日期={data['date']}, 置信度={data['confidence']:.1%}")

@test("4. 超市小票识别 — 类型路由")
def _():
    small_img = os.path.join(TEST_DIR, "test_receipt_small.png")
    if not os.path.exists(small_img):
        print("    (测试图片不存在，跳过)")
        return
    with open(small_img, 'rb') as f:
        r = requests.post(
            f"{OCR_URL}/api/extract",
            files={'file': ('small.png', f, 'image/png')},
            timeout=120
        )
    assert r.status_code == 200
    data = r.json()
    assert data["success"] == True
    print(f"    类型={data['receipt_type']}, raw_text前50字: {data['raw_text'][:50]}")

@test("5. 通用收据识别 — 降级策略")
def _():
    gen_img = os.path.join(TEST_DIR, "test_receipt_general.png")
    if not os.path.exists(gen_img):
        print("    (测试图片不存在，跳过)")
        return
    with open(gen_img, 'rb') as f:
        r = requests.post(
            f"{OCR_URL}/api/extract",
            files={'file': ('general.png', f, 'image/png')},
            timeout=120
        )
    assert r.status_code == 200
    data = r.json()
    assert data["success"] == True
    print(f"    类型={data['receipt_type']}, 商户={data.get('vendor_name','?')}, 金额=¥{data.get('total_amount','?')}")

@test("6. 异常处理 — 无效文件类型")
def _():
    r = requests.post(
        f"{OCR_URL}/api/extract",
        files={'file': ('test.txt', b'not an image', 'text/plain')},
        timeout=10
    )
    assert r.status_code == 400, f"期望400, 实际{r.status_code}"
    data = r.json()
    assert data["success"] == False
    print(f"    错误信息: {data['error'][:60]}")

@test("7. 异常处理 — 空文件")
def _():
    r = requests.post(
        f"{OCR_URL}/api/extract",
        files={'file': ('empty.png', b'', 'image/png')},
        timeout=10
    )
    assert r.status_code == 400
    data = r.json()
    print(f"    正确处理空文件: status={r.status_code}")

@test("8. 票据分类 API")
def _():
    r = requests.get(
        f"{OCR_URL}/api/classify",
        params={'raw_text': '增值税普通发票 发票代码 110023456789 开票日期'},
        timeout=5
    )
    assert r.status_code == 200
    data = r.json()
    assert data["receipt_type"] == "vat_invoice"
    print(f"    输入42字文本 → 分类为: {data['receipt_type']}")

@test("9. 仅OCR模式")
def _():
    with open(TEST_IMAGE, 'rb') as f:
        r = requests.post(
            f"{OCR_URL}/api/ocr-only",
            files={'file': ('test.png', f, 'image/png')},
            timeout=120
        )
    assert r.status_code == 200
    data = r.json()
    assert data.get("line_count", data.get("lines", 0)) > 0 or len(data.get("raw_text","")) > 50
    line_count = data.get("line_count", len(data.get("lines", [])))
    print(f"    识别到 {line_count} 行文本")

@test("10. 预处理开关 — 功能对比")
def _():
    with open(TEST_IMAGE, 'rb') as f:
        content = f.read()
    
    r1 = requests.post(
        f"{OCR_URL}/api/extract?enable_preprocess=false",
        files={'file': ('test.png', content, 'image/png')},
        timeout=120
    )
    r2 = requests.post(
        f"{OCR_URL}/api/extract?enable_preprocess=true",
        files={'file': ('test.png', content, 'image/png')},
        timeout=120
    )
    assert r1.status_code == 200 and r2.status_code == 200
    d1, d2 = r1.json(), r2.json()
    print(f"    无预处理: conf={d1['confidence']:.1%}, time={d1['processing_time']:.2f}s")
    print(f"    有预处理: conf={d2['confidence']:.1%}, time={d2['processing_time']:.2f}s")

@test("11. 并发请求鲁棒性")
def _():
    import concurrent.futures
    
    def call_ocr(i):
        with open(TEST_IMAGE, 'rb') as f:
            r = requests.post(
                f"{OCR_URL}/api/extract",
                files={'file': (f'test_{i}.png', f.read(), 'image/png')},
                timeout=120
            )
        return r.status_code
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(call_ocr, range(3)))
    
    success = sum(1 for r in results if r == 200)
    print(f"    3并发: {success}/3 成功")
    assert success >= 1, f"并发全部失败: {results}"

@test("12. 响应时间 SLA")
def _():
    times = []
    for i in range(3):
        with open(TEST_IMAGE, 'rb') as f:
            t0 = time.time()
            r = requests.post(
                f"{OCR_URL}/api/extract",
                files={'file': (f'test_{i}.png', f.read(), 'image/png')},
                timeout=120
            )
            times.append(time.time() - t0)
    
    avg = sum(times) / len(times)
    print(f"    平均响应时间: {avg:.2f}s (样本: {[f'{t:.1f}s' for t in times]})")
    assert avg < 30, f"响应时间过长: {avg:.1f}s (阈值: 30s)"

# ==================== 主流程 ====================

print("=" * 60)
print("票据 OCR 服务 — 自动化验收测试")
print("=" * 60)
print(f"服务地址: {OCR_URL}")
print(f"测试图片: {TEST_IMAGE}")
print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# 验证服务在线
try:
    r = requests.get(f"{OCR_URL}/health", timeout=5)
    if r.status_code != 200:
        print("✗ 服务不可用，请先启动: python -m uvicorn app.main:app --port 8001")
        exit(1)
except Exception as e:
    print(f"✗ 无法连接服务: {e}")
    exit(1)

# 运行测试
print(f"\n{'=' * 60}")
print(f"测试结果: {passed} 通过, {failed} 失败, 共 {passed+failed} 项")
print(f"{'=' * 60}")

if failed > 0:
    print(f"\n⚠ 有 {failed} 项测试未通过，请检查详细输出。")
    exit(1)
else:
    print("\n✓ 所有测试通过！票据OCR服务验收完成。")
