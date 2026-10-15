"""Kiểm tra giao diện bằng Playwright. Cần backend đang chạy (đã build frontend) tại URL (mặc định http://localhost:8000).
Ảnh chụp ghi vào thư mục tạm (hoặc đối số thứ 2), KHÔNG ghi vào repo."""
import sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(tempfile.mkdtemp(prefix="e2e-"))
TABS = ["1 · Thuê bến", "2 · Phân công đội", "3 · Quỹ giờ công", "4 · Xếp container"]


def main():
    errors = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1400, "height": 1200})
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(URL)
        for ti, name in enumerate(TABS):
            pg.get_by_role("tab", name=name).click()
            pg.wait_for_selector(".msg", timeout=8000)
            algos = pg.locator(".segm label").count()
            assert algos >= 3, f"{name}: thiếu thuật toán"
            msgs = set()
            for k in range(algos):
                pg.locator(".segm label").nth(k).click()
                pg.wait_for_selector(".msg")
                first = pg.locator(".msg").inner_text()
                for _ in range(4):
                    pg.get_by_role("button", name="Tiếp", exact=True).click()
                after = pg.locator(".msg").inner_text()
                assert pg.locator('.pseudo .pl.on').count() == 1, f'{name}/thuật toán {k}: mã giả không tô dòng nào'
                assert after != first, f"{name}/thuật toán {k}: bấm Tiếp không đổi thông điệp"
                msgs.add(after)
                pg.get_by_role("button", name="Về đầu").click()
            # lùi/tiến, thanh trượt
            pg.locator(".segm label").nth(0).click()
            pg.locator("input[type=range]").first.fill("3")
            assert "Bước 3/" in pg.locator(".card-h span", has_text="Bước").first.inner_text()
            # tự động chạy tới cuối
            pg.get_by_role("button", name="Tự động").click()
            pg.get_by_label("Tốc độ").select_option("200")
            pg.wait_for_function("document.querySelector('.tag.done')", timeout=20000)
            pg.screenshot(path=str(OUT / f"module{ti+1}.png"), full_page=True)
            # bảng so sánh các thuật toán (module 1 để trong tab "So sánh")
            if pg.get_by_role("tab", name="So sánh").count():
                pg.get_by_role("tab", name="So sánh").click()
            assert pg.get_by_text("So sánh các thuật toán").count() or pg.locator("table.tbl thead", has_text="Đánh giá").count()
            assert pg.locator("table.tbl thead", has_text="Độ phức tạp").count() == 1
            assert pg.locator("table.tbl thead", has_text="Đánh giá").count() == 1
            assert pg.locator("details.gloss").count() == 1
            # nhập sai: xóa tên của dòng đầu -> thông báo lỗi
            pg.locator(".edit-row input").first.fill("")
            pg.wait_for_selector(".alert", timeout=3000)
        b.close()
    assert not errors, errors
    print("e2e OK; ảnh ở", OUT)


main()
