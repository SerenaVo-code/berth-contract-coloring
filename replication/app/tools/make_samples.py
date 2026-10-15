"""Tạo frontend/src/samples.js từ vài testcase, để dữ liệu mẫu trên giao diện và testcase là MỘT nguồn."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PICK = {
    "berth": [("m1-T05", "Bốn kết quả khác nhau"), ("m1-D03", "Chu trình lẻ do ràng buộc phụ")],
    "assign": [("m2-D02", "Tham lam bị kẹt"), ("m2-D01", "Vô nghiệm (vi phạm Hall)")],
    "knapsack": [("m3-T04", "Tham lam sai"), ("m3-T01", "10 yêu cầu ngẫu nhiên")],
    "binpack": [("m4-D02", "First-Fit giảm dần không tối ưu"), ("m4-T04", "First-Fit tệ hơn FFD")],
}
out = {}
for mod, lst in PICK.items():
    out[mod] = []
    for tid, label in lst:
        f = next((ROOT / "testcases").glob(f"*/{tid}.json"))
        out[mod].append({"id": tid, "label": label, "input": json.loads(f.read_text(encoding="utf-8"))["input"]})
(ROOT / "frontend" / "src" / "samples.js").write_text(
    "// Sinh tự động bởi tools/make_samples.py từ testcases/, đừng sửa tay.\nexport const SAMPLES = " + json.dumps(out, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8")
print("ok")
