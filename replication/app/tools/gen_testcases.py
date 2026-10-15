"""Sinh bộ testcase (cố định seed). Mỗi file: id, module, group, title, desc, input, expect.
expect.opt là đáp án tham chiếu từ vét cạn / công thức / instance dựng sẵn, KHÔNG lấy từ solver."""
import json, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tests"))
sys.path.insert(0, str(HERE))
from oracles import assign_opt, berth_opt, bins_opt, knap_opt  # noqa: E402
from checker import knap_dp_1d  # noqa: E402
sys.path.insert(0, str(HERE.parent / "backend"))
import assign as A, berth as B1, binpack as B4  # noqa: E402  (chỉ để TÌM instance có tính chất mong muốn; đáp án vẫn từ vét cạn)

OUT = HERE.parent / "testcases"
G = {"thuong": "Thông thường", "nho": "Dữ liệu nhỏ", "bien": "Biên", "dacbiet": "Đặc biệt", "lon": "Dữ liệu lớn"}
cases = []


def add(mod, gid, group, title, desc, inp, opt=None, src=None, **extra):
    cases.append({"id": f"{mod}-{gid}", "module": mod, "group": group, "title": title, "desc": desc,
                  "input": inp, "expect": {"opt": opt, "opt_source": src, **extra}})


def ships_rand(rng, n, horizon, maxd=8):
    out = []
    for i in range(n):
        s = rng.randint(0, int(horizon * 2)) / 2
        out.append({"name": f"Tàu {i+1}", "s": s, "e": s + rng.randint(1, maxd * 2) / 2})
    return out


# =============================================================== MODULE 1
def m1():
    rng = random.Random(101)
    B = lambda sh, pr, F, r: {"ships": sh, "pairs": pr, "F": F, "r": r}
    sh = lambda *t: [{"name": f"Tàu {i+1}", "s": a, "e": b} for i, (a, b) in enumerate(t)]
    # thông thường
    for k in range(1, 5):
        s = ships_rand(rng, 8, 14)
        inp = B(s, [[0, 5]] if k % 2 else [], 500, 40)
        add("m1", f"T0{k}", "thuong", f"8 tàu ngẫu nhiên #{k}", "Dữ liệu cỡ vừa, vét cạn được.", inp, berth_opt(s, inp["pairs"], 500, 40), "vét cạn")
    # T05: tìm instance 8 tàu mà bốn thuật toán cho bốn chi phí khác nhau
    r5 = random.Random(55)
    while True:
        s = ships_rand(r5, 8, 14); pr = [[r5.randrange(8), r5.randrange(8)] for _ in range(2)]
        res = B1.solve_all(s, pr, 500, 40)
        if len({round(a["cost"], 6) for a in res["algos"]}) == 4:
            break
    add("m1", "T05", "thuong", "Bốn thuật toán cho bốn chi phí khác nhau", "Tìm bằng cách thử nhiều bộ ngẫu nhiên; làm lộ khác biệt giữa các thuật toán.", B(s, pr, 500, 40), berth_opt(s, pr, 500, 40), "vét cạn")
    # nhỏ
    s = sh((0, 5), (7, 9)); add("m1", "N01", "nho", "2 tàu rời nhau", "Dùng một hợp đồng hay hai tùy F và r.", B(s, [], 100, 10), berth_opt(s, [], 100, 10), "vét cạn")
    s = sh((0, 5), (3, 8), (4, 9)); add("m1", "N02", "nho", "3 tàu chồng nhau", "Cần ít nhất 3 hợp đồng.", B(s, [], 100, 10), berth_opt(s, [], 100, 10), "vét cạn")
    s = sh((0, 3), (1, 4), (6, 8), (7, 9)); add("m1", "N03", "nho", "Hai cụm tàu cách xa", "Giờ trống giữa hai cụm khiến gộp hợp đồng tốn tiền.", B(s, [], 50, 20), berth_opt(s, [], 50, 20), "vét cạn")
    # biên
    s = sh((0, 3)); add("m1", "B01", "bien", "Chỉ 1 tàu", "n = 1.", B(s, [], 140, 0.0 + 10), berth_opt(s, [], 140, 10), "vét cạn")
    s = sh((0, 2), (2, 4)); add("m1", "B02", "bien", "Hai tàu chạm đầu mút", "rời = đến thì không xung đột.", B(s, [], 100, 10), berth_opt(s, [], 100, 10), "vét cạn")
    s = sh((0, 2), (1.5, 4)); add("m1", "B03", "bien", "Hai tàu chồng 0,5 giờ", "Chồng rất ít vẫn là xung đột.", B(s, [], 100, 10), berth_opt(s, [], 100, 10), "vét cạn")
    s = ships_rand(random.Random(7), 9, 12); add("m1", "B04", "bien", "F = 0", "Mỗi tàu một hợp đồng là tối ưu: r × Σ thời gian cập.", B(s, [], 0, 10), 10 * sum(x["e"] - x["s"] for x in s), "công thức")
    s = ships_rand(random.Random(8), 12, 12); P = B(s, [], 200, 0)
    om = 0
    for t in {x["s"] for x in s}: om = max(om, sum(1 for x in s if x["s"] <= t < x["e"]))
    add("m1", "B05", "bien", "r = 0", "Chỉ còn phí F: tối ưu = F × ω.", P, 200 * om, "công thức")
    s = sh((0, 1), (0.5, 2)); add("m1", "B06", "bien", "F = 0 và r = 0", "Mọi phương án đều 0.", B(s, [], 0, 0), 0, "công thức")
    s = sh((20, 26), (23, 28), (30, 36), (25, 31)); add("m1", "B07", "bien", "Tàu qua đêm (giờ > 24)", "Giờ vượt 24 vẫn bình thường.", B(s, [], 150, 12), berth_opt(s, [], 150, 12), "vét cạn")
    s = sh((0, 1.25), (1.25, 2.5), (0.25, 1.5)); add("m1", "B08", "bien", "Giờ lẻ 0,25", "Số thực lẻ.", B(s, [], 100, 8), berth_opt(s, [], 100, 8), "vét cạn")
    # đặc biệt
    s = sh(*[(0, 6)] * 6); add("m1", "D01", "dacbiet", "6 tàu trùng giờ hoàn toàn", "Cần đúng 6 hợp đồng.", B(s, [], 100, 10), berth_opt(s, [], 100, 10), "vét cạn")
    s = sh(*[(i * 2, i * 2 + 2) for i in range(9)]); add("m1", "D02", "dacbiet", "9 tàu nối đuôi", "Không giờ trống: một hợp đồng là tối ưu, F + r×Σd.", B(s, [], 300, 10), 300 + 10 * 18, "công thức")
    s = sh(*[(0, 1)] * 5); add("m1", "D03", "dacbiet", "Chu trình lẻ C5 do ràng buộc phụ", "Tàu không chồng giờ nhưng cấm theo vòng 5.", B(s, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]], 100, 10), berth_opt(s, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]], 100, 10), "vét cạn")
    s = sh((0, 2), (3, 5), (6, 8), (9, 11)); pr = [[0, 1], [1, 0], [2, 2], [0, 1]]; add("m1", "D04", "dacbiet", "Cặp cấm lặp, đảo chiều và tự thân", "Phải được xử lý như một cặp.", B(s, pr, 100, 10), berth_opt(s, pr, 100, 10), "vét cạn")
    s = sh(*[(i * 3, i * 3 + 1) for i in range(6)]); pr = [[i, j] for i in range(6) for j in range(i + 1, 6)]; add("m1", "D05", "dacbiet", "Mọi cặp bị cấm (K6)", "Cần 6 hợp đồng dù giờ không chồng.", B(s, pr, 100, 10), berth_opt(s, pr, 100, 10), "vét cạn")
    s = sh((0, 8), (0, 2), (0, 5), (0, 3), (0, 6)); add("m1", "D06", "dacbiet", "Cùng giờ đến, khác giờ rời", "Thứ tự hòa cần quy tắc phụ.", B(s, [], 100, 10), berth_opt(s, [], 100, 10), "vét cạn")
    # lớn
    add("m1", "L01", "lon", "30 tàu ngẫu nhiên", "Không có đáp án tham chiếu, quay lui có thể hết ngân sách.", B(ships_rand(random.Random(31), 30, 40), [], 400, 30))
    s = ships_rand(random.Random(32), 100, 80); add("m1", "L02", "lon", "100 tàu, F = 0", "Công thức cho đáp án.", B(s, [], 0, 25), 25 * sum(x["e"] - x["s"] for x in s), "công thức")
    s = ships_rand(random.Random(33), 100, 80); om = max(sum(1 for x in s if x["s"] <= t < x["e"]) for t in {x["s"] for x in s}); add("m1", "L03", "lon", "100 tàu, r = 0", "Tối ưu = F × ω.", B(s, [], 300, 0), 300 * om, "công thức")
    add("m1", "L04", "lon", "200 tàu (tối đa), ngẫu nhiên", "Biên trên của giới hạn.", B(ships_rand(random.Random(34), 200, 160), [], 400, 30))
    s = sh(*[(i * 1.5, i * 1.5 + 1.5) for i in range(200)]); add("m1", "L05", "lon", "200 tàu nối đuôi", "Một hợp đồng là tối ưu.", B(s, [], 5000, 4), 5000 + 4 * 300, "công thức")


# =============================================================== MODULE 2
SK = ["cẩu", "buộc dây", "hàng lạnh", "hóa chất"]


def m2():
    rng = random.Random(202)

    def mk(n, m, hor, extra=0):
        sh = []
        for s in ships_rand(rng, n, hor, 5):
            sh.append({**s, "need": rng.sample(SK, rng.randint(0, 2))})
        tm = [{"name": f"Đội {i+1}", "skills": rng.sample(SK, rng.randint(1, 4)), "rate": rng.randint(8, 40)} for i in range(m)]
        return {"ships": sh, "teams": tm, "pairs": [[rng.randrange(n), rng.randrange(n)] for _ in range(extra)]}

    def full_team(i, rate): return {"name": f"Đội {i}", "skills": list(SK), "rate": rate}
    for k in range(1, 4):
        inp = mk(6, 4, 10, k % 2)
        add("m2", f"T0{k}", "thuong", f"6 tàu, 4 đội #{k}", "Ngẫu nhiên cỡ vừa.", inp, assign_opt(inp["ships"], inp["teams"], inp["pairs"]), "vét cạn")
    inp = {"ships": [{"name": "A", "s": 0, "e": 4, "need": ["cẩu"]}], "teams": [full_team(1, 10)], "pairs": []}
    add("m2", "N01", "nho", "1 tàu, 1 đội", "Nhỏ nhất.", inp, 40, "công thức")
    inp = {"ships": [{"name": "A", "s": 0, "e": 4, "need": []}, {"name": "B", "s": 5, "e": 8, "need": []}], "teams": [full_team(1, 10), full_team(2, 6)], "pairs": []}
    add("m2", "N02", "nho", "2 tàu rời nhau, 2 đội", "Cùng giao đội rẻ.", inp, assign_opt(inp["ships"], inp["teams"], []), "vét cạn")
    inp = mk(4, 2, 6); add("m2", "N03", "nho", "4 tàu, 2 đội", "Cỡ nhỏ.", inp, assign_opt(inp["ships"], inp["teams"], inp["pairs"]), "vét cạn")
    inp = {"ships": [{"name": "A", "s": 0, "e": 2, "need": []}, {"name": "B", "s": 2, "e": 4, "need": []}], "teams": [full_team(1, 10)], "pairs": []}
    add("m2", "B01", "bien", "Hai tàu chạm đầu mút, một đội", "rời = đến, dùng chung được.", inp, 40, "công thức")
    inp = {"ships": [{"name": "A", "s": 0, "e": 2, "need": []}, {"name": "B", "s": 1.5, "e": 4, "need": []}], "teams": [full_team(1, 10)], "pairs": []}
    add("m2", "B02", "bien", "Hai tàu chồng, chỉ một đội", "Vô nghiệm.", inp, None, "vét cạn", feasible=False)
    inp = {"ships": [{"name": "A", "s": 0, "e": 2, "need": SK[:2]}], "teams": [{"name": "Đội 1", "skills": [SK[0]], "rate": 10}], "pairs": []}
    add("m2", "B03", "bien", "Thiếu một kỹ năng", "Không đội nào đủ.", inp, None, "vét cạn", feasible=False)
    inp = {"ships": [{"name": "A", "s": 0, "e": 2, "need": []}], "teams": [{"name": "Đội 1", "skills": [], "rate": 0}], "pairs": []}
    add("m2", "B04", "bien", "Đơn giá 0, không cần kỹ năng", "Chi phí 0.", inp, 0, "công thức")
    inp = {"ships": [{"name": "A", "s": 0, "e": 2, "need": []}, {"name": "B", "s": 3, "e": 4, "need": []}], "teams": [full_team(1, 10)], "pairs": [[0, 1]]}
    add("m2", "B05", "bien", "Cặp cấm ép hai tàu rời nhau vào hai đội", "Chỉ một đội nên vô nghiệm.", inp, None, "vét cạn", feasible=False)
    inp = {"ships": [{"name": f"S{i}", "s": 0, "e": 5, "need": ["cẩu"]} for i in range(3)], "teams": [full_team(1, 10), full_team(2, 12)], "pairs": []}
    add("m2", "D01", "dacbiet", "3 tàu cùng giờ, 2 đội đủ kỹ năng (vi phạm Hall)", "Phải kết luận vô nghiệm ngay, không cần duyệt.", inp, None, "vét cạn", feasible=False, hall=True)
    r2 = random.Random(22)
    while True:  # tìm instance có nghiệm mà tham lam theo giờ đến bị kẹt
        inp = mk(6, 4, 9, 1)
        opt = assign_opt(inp["ships"], inp["teams"], inp["pairs"])
        if opt is not None and A.solve_all(inp["ships"], inp["teams"], inp["pairs"])["algos"][0]["status"] == "fail":
            break
    add("m2", "D02", "dacbiet", "Có nghiệm nhưng tham lam theo giờ đến bị kẹt", "Tham lam giao đội rẻ cho tàu đến sớm rồi hết đội cho tàu đến sau; quay lui vẫn tìm được.", inp, opt, "vét cạn")
    inp = {"ships": [{"name": f"S{i}", "s": i, "e": i + 1, "need": []} for i in range(5)], "teams": [full_team(1, 10), full_team(2, 10)], "pairs": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]]}
    add("m2", "D03", "dacbiet", "Chu trình lẻ cấm với 2 đội", "Không thể 2-tô màu chu trình 5.", inp, None, "vét cạn", feasible=False)
    inp = mk(5, 3, 8); inp["teams"] = [{**t, "rate": 10, "skills": list(SK)} for t in inp["teams"]]
    add("m2", "D04", "dacbiet", "Các đội giống hệt nhau", "Kiểm tra bỏ qua đối xứng.", inp, assign_opt(inp["ships"], inp["teams"], inp["pairs"]), "vét cạn")
    inp = mk(30, 8, 40); add("m2", "L01", "lon", "30 tàu, 8 đội", "Không đáp án tham chiếu.", inp)
    inp = mk(60, 12, 80); add("m2", "L02", "lon", "60 tàu, 12 đội (tối đa)", "Biên trên.", inp)
    inp = {"ships": [{"name": f"S{i}", "s": i * 2, "e": i * 2 + 2, "need": []} for i in range(40)], "teams": [full_team(1, 7), full_team(2, 9)], "pairs": []}
    add("m2", "L03", "lon", "40 tàu nối đuôi, 2 đội", "Mọi tàu giao đội rẻ nhất: 7 × 80.", inp, 7 * 80, "công thức")


# =============================================================== MODULE 3
def m3():
    rng = random.Random(303)

    def items(n, wmax, vmax): return [{"name": f"Yêu cầu {i+1}", "w": rng.randint(1, wmax), "v": rng.randint(0, vmax)} for i in range(n)]
    for k in range(1, 4):
        it = items(10, 12, 50); W = 30 + k * 5; add("m3", f"T0{k}", "thuong", f"10 yêu cầu #{k}", "Ngẫu nhiên.", {"items": it, "W": W}, knap_opt(it, W), "vét cạn")
    it = [{"name": "A", "w": 10, "v": 60}, {"name": "B", "w": 20, "v": 100}, {"name": "C", "w": 30, "v": 120}]
    add("m3", "T04", "thuong", "Ví dụ kinh điển: tham lam sai", "Tham lam 160, tối ưu 220.", {"items": it, "W": 50}, 220, "instance dựng sẵn")
    add("m3", "N01", "nho", "1 yêu cầu vừa quỹ", "", {"items": [{"name": "A", "w": 5, "v": 7}], "W": 5}, 7, "công thức")
    add("m3", "N02", "nho", "2 yêu cầu, chỉ nhận được một", "", {"items": [{"name": "A", "w": 4, "v": 5}, {"name": "B", "w": 4, "v": 8}], "W": 5}, 8, "công thức")
    it = items(5, 6, 20); add("m3", "N03", "nho", "5 yêu cầu", "", {"items": it, "W": 12}, knap_opt(it, 12), "vét cạn")
    add("m3", "B01", "bien", "Quỹ 0 giờ", "Không nhận được gì.", {"items": [{"name": "A", "w": 1, "v": 9}], "W": 0}, 0, "công thức")
    add("m3", "B02", "bien", "Mọi yêu cầu vượt quỹ", "", {"items": [{"name": "A", "w": 9, "v": 9}, {"name": "B", "w": 8, "v": 4}], "W": 7}, 0, "công thức")
    add("m3", "B03", "bien", "Mọi yêu cầu có giá trị 0", "", {"items": [{"name": "A", "w": 1, "v": 0}, {"name": "B", "w": 2, "v": 0}], "W": 3}, 0, "công thức")
    it = items(8, 5, 30); add("m3", "B04", "bien", "Quỹ vừa đúng tổng giờ", "Nhận tất cả.", {"items": it, "W": sum(x["w"] for x in it)}, sum(x["v"] for x in it), "công thức")
    it = [{"name": f"Y{i}", "w": 3, "v": 10} for i in range(6)]; add("m3", "D01", "dacbiet", "Mọi yêu cầu giống nhau", "Nhiều nghiệm tối ưu.", {"items": it, "W": 10}, 30, "công thức")
    it = [{"name": "A", "w": 6, "v": 12}, {"name": "B", "w": 5, "v": 10}, {"name": "C", "w": 4, "v": 8}]; add("m3", "D02", "dacbiet", "Giá trị/giờ bằng nhau", "Mọi tỉ lệ = 2, tối ưu = 2 × giờ dùng được.", {"items": it, "W": 10}, 20, "công thức")
    it = [{"name": "Lớn", "w": 10, "v": 100}] + [{"name": f"Nhỏ{i}", "w": 1, "v": 11} for i in range(9)]; add("m3", "D03", "dacbiet", "Một yêu cầu lớn so với nhiều yêu cầu nhỏ", "", {"items": it, "W": 10}, knap_opt(it, 10), "vét cạn")
    it = items(25, 20, 100); add("m3", "L01", "lon", "25 yêu cầu (tối đa), quỹ 100", "Đáp án từ quy hoạch động một chiều viết riêng.", {"items": it, "W": 100}, knap_dp_1d(it, 100), "DP độc lập")
    it = items(12, 40, 100); add("m3", "L02", "lon", "12 yêu cầu, quỹ 200", "Khớp vét cạn.", {"items": it, "W": 200}, knap_opt(it, 200), "vét cạn")
    it = items(25, 8, 60); add("m3", "L03", "lon", "25 yêu cầu nhỏ, quỹ 98", "Sát giới hạn 2500 ô.", {"items": it, "W": 98}, knap_dp_1d(it, 98), "DP độc lập")


# =============================================================== MODULE 4
def m4():
    rng = random.Random(404)

    def items(n, C, lo=1): return [{"name": f"Lô {i+1}", "w": rng.randint(lo, C)} for i in range(n)]
    for k in range(1, 4):
        it = items(9, 100, 10); add("m4", f"T0{k}", "thuong", f"9 lô #{k}", "Ngẫu nhiên.", {"items": it, "C": 100}, bins_opt(it, 100), "vét cạn")
    r4 = random.Random(44)
    while True:  # FF dùng nhiều tàu hơn FFD, FFD đạt tối ưu
        it = [{"name": f"Lô {i+1}", "w": r4.randint(1, 9)} for i in range(9)]
        res = B4.solve_all(it, 10)
        if res["algos"][0]["bins"] > res["algos"][1]["bins"] == bins_opt(it, 10):
            break
    add("m4", "T04", "thuong", "First-Fit tệ hơn First-Fit giảm dần", "Thứ tự nhập xấu làm FF mở thừa tàu; FFD đạt tối ưu.", {"items": it, "C": 10}, bins_opt(it, 10), "vét cạn")
    add("m4", "N01", "nho", "1 lô", "", {"items": [{"name": "A", "w": 4}], "C": 10}, 1, "công thức")
    add("m4", "N02", "nho", "2 lô vừa một tàu", "", {"items": [{"name": "A", "w": 4}, {"name": "B", "w": 6}], "C": 10}, 1, "công thức")
    add("m4", "N03", "nho", "2 lô không vừa chung", "", {"items": [{"name": "A", "w": 6}, {"name": "B", "w": 5}], "C": 10}, 2, "công thức")
    add("m4", "B01", "bien", "Lô nặng đúng bằng tải trọng", "w = C.", {"items": [{"name": "A", "w": 10}, {"name": "B", "w": 10}], "C": 10}, 2, "công thức")
    add("m4", "B02", "bien", "Mọi lô nặng 1 chen đủ một tàu", "Σw = C.", {"items": [{"name": f"L{i}", "w": 1} for i in range(10)], "C": 10}, 1, "công thức")
    add("m4", "B03", "bien", "Khối lượng lẻ 0,1", "Sai số số thực.", {"items": [{"name": f"L{i}", "w": 0.1} for i in range(10)], "C": 1}, 1, "công thức")
    it = [{"name": f"L{i}", "w": 6} for i in range(7)]; add("m4", "D01", "dacbiet", "Mọi lô quá nửa tải", "Mỗi lô một tàu.", {"items": it, "C": 10}, 7, "công thức")
    r4 = random.Random(45)
    while True:  # First-Fit giảm dần không tối ưu
        it = [{"name": f"Lô {i+1}", "w": r4.randint(20, 60)} for i in range(r4.randint(7, 10))]
        res = B4.solve_all(it, 100)
        if res["algos"][1]["bins"] > bins_opt(it, 100):
            break
    add("m4", "D02", "dacbiet", "First-Fit giảm dần không tối ưu", "Cả FFD lẫn BFD dùng nhiều tàu hơn tối ưu; quay lui phải sửa lại.", {"items": it, "C": 100}, bins_opt(it, 100), "vét cạn")
    it = [{"name": f"L{i}", "w": w} for i, w in enumerate([5, 5, 5, 5, 5, 5, 5, 5, 5])]; add("m4", "D03", "dacbiet", "Tổng lẻ so với tải trọng", "Σ = 45, C = 10: cần 5 tàu.", {"items": it, "C": 10}, 5, "công thức")
    # lớn: dựng sẵn nghiệm hoàn hảo bằng cách cắt từng tàu đầy
    def perfect(k, C, seed):
        r = random.Random(seed); out = []
        for b in range(k):
            left = C
            while left > 0:
                w = min(left, r.randint(1, max(1, C // 2)))
                out.append(w); left -= w
        r.shuffle(out)
        return [{"name": f"Lô {i+1}", "w": w} for i, w in enumerate(out)]
    it = perfect(8, 100, 1)[:60]; opt = None
    pf = perfect(6, 100, 2); add("m4", "L01", "lon", "Dựng sẵn: 6 tàu đầy tải", f"{len(pf)} lô, tối ưu 6 chắc chắn.", {"items": pf, "C": 100}, 6, "instance dựng sẵn")
    pf = perfect(10, 50, 3); pf = pf[:60]; add("m4", "L02", "lon", "Dựng sẵn: 10 tàu đầy tải (cắt ≤ 60 lô)", f"{len(pf)} lô.", {"items": pf, "C": 50}, None)
    it = items(60, 100, 5); add("m4", "L03", "lon", "60 lô ngẫu nhiên (tối đa)", "Không đáp án tham chiếu; có cận dưới.", {"items": it, "C": 100})
    it = [{"name": f"L{i}", "w": 51 + (i % 5)} for i in range(60)]; add("m4", "L04", "lon", "60 lô đều quá nửa tải", "Mỗi lô một tàu: 60.", {"items": it, "C": 100}, 60, "công thức")


for f in (m1, m2, m3, m4):
    f()
for old in OUT.glob("m*/*.json"):
    old.unlink()
for c in cases:
    d = OUT / c["module"]
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{c['id']}.json").write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(cases), "testcase")
