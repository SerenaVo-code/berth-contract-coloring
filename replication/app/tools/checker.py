"""Bộ kiểm tra độc lập: tự tính lại chi phí/giá trị từ đầu vào và gán, không gọi hàm của solver."""


def _overlap(a, b):
    return a["s"] < b["e"] and b["s"] < a["e"]


def check_berth(inp, col):
    ships, F, r = inp["ships"], inp["F"], inp["r"]
    n = len(ships)
    if len(col) != n or min(col) < 0:
        return None, "gán thiếu"
    banned = {(min(a, b), max(a, b)) for a, b in inp.get("pairs", []) if a != b}
    for i in range(n):
        for j in range(i + 1, n):
            if col[i] == col[j] and (_overlap(ships[i], ships[j]) or (i, j) in banned):
                return None, f"{ships[i]['name']} và {ships[j]['name']} xung đột nhưng chung hợp đồng"
    total = 0.0
    for k in set(col):
        mem = [ships[i] for i in range(n) if col[i] == k]
        total += F + r * (max(x["e"] for x in mem) - min(x["s"] for x in mem))
    return total, ""


def check_assign(inp, col):
    ships, teams = inp["ships"], inp["teams"]
    n = len(ships)
    banned = {(min(a, b), max(a, b)) for a, b in inp.get("pairs", []) if a != b}
    for i in range(n):
        t = col[i]
        if t < 0:
            return None, "chưa gán"
        if not set(ships[i]["need"]) <= set(teams[t]["skills"]):
            return None, f"{ships[i]['name']} giao đội thiếu kỹ năng"
        for j in range(i + 1, n):
            if col[j] == t and (_overlap(ships[i], ships[j]) or (i, j) in banned):
                return None, f"{ships[i]['name']} và {ships[j]['name']} xung đột nhưng chung đội"
    return sum(teams[col[i]]["rate"] * (ships[i]["e"] - ships[i]["s"]) for i in range(n)), ""


def check_knap(inp, take):
    its = inp["items"]
    w = sum(its[i]["w"] for i in range(len(its)) if take[i])
    if w > inp["W"]:
        return None, f"vượt quỹ giờ: {w} > {inp['W']}"
    return sum(its[i]["v"] for i in range(len(its)) if take[i]), ""


def check_bins(inp, assign):
    its, C = inp["items"], inp["C"]
    load = {}
    for i, b in enumerate(assign):
        if b < 0:
            return None, "chưa xếp"
        load[b] = load.get(b, 0) + its[i]["w"]
    over = [b for b, x in load.items() if x > C + 1e-9]
    if over:
        return None, f"tàu {over[0] + 1} quá tải"
    return len(load), ""


def knap_dp_1d(items, W):
    """Đáp án tham chiếu khác cách cài với solver: mảng một chiều, duyệt j giảm dần."""
    f = [0.0] * (W + 1)
    for it in items:
        for j in range(W, it["w"] - 1, -1):
            f[j] = max(f[j], f[j - it["w"]] + it["v"])
    return f[W]
