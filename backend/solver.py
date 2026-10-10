"""Xếp tàu vào hợp đồng thuê bến = tô màu đồ thị (góc nhìn hãng tàu).

Mỗi màu = một hợp đồng thuê bến. Chi phí hợp đồng = F + r × (giờ rời cuối − giờ đến đầu),
kể cả giờ trống ở giữa. Hai tàu chồng thời gian (hoặc có ràng buộc thêm) không chung hợp đồng.
Mỗi thuật toán trả về danh sách bước (snapshot) để giao diện duyệt từng bước.
"""
from __future__ import annotations

import time
from typing import Any

EPS = 1e-9
STEP_CAP = 3000
BT_MAX_NODES = 400_000
BT_DEADLINE_S = 1.5


def fm(v: float) -> str:
    v = round(v * 100) / 100
    return str(int(v)) if v == int(v) else str(v)


def ft(v: float) -> str:
    """Giờ thập phân -> HH:MM (thêm +Nd nếu qua ngày)."""
    total = round(v * 60)
    day, rem = divmod(total, 1440)
    out = f"{rem // 60:02d}:{rem % 60:02d}"
    return out + (f"+{day}d" if day else "")


def list_contracts(ks) -> str:
    return ", ".join(f"HĐ {k + 1}" for k in sorted(ks))


class Graph:
    def __init__(self, ships, pairs, F, r):
        self.ships = ships
        self.n = n = len(ships)
        self.F, self.r = F, r
        self.adj: list[set[int]] = [set() for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if ships[i]["s"] < ships[j]["e"] and ships[j]["s"] < ships[i]["e"]:
                    self.adj[i].add(j)
                    self.adj[j].add(i)
        for a, b in pairs:
            if a != b:
                self.adj[a].add(b)
                self.adj[b].add(a)
        ev = []
        for x in ships:
            ev.append((x["s"], 1))
            ev.append((x["e"], -1))
        ev.sort()
        cur = lb = 0
        for _, d in ev:
            cur += d
            lb = max(lb, cur)
        self.lb = lb
        self.sum_dur = sum(x["e"] - x["s"] for x in ships)
        self.lb_cost = lb * F + r * self.sum_dur
        self.order = sorted(range(n), key=lambda i: (ships[i]["s"], ships[i]["e"], i))

    def forb(self, col, v):
        return {col[u] for u in self.adj[v] if col[u] >= 0}

    def stats(self, col):
        st: dict[int, list[float]] = {}
        for i, c in enumerate(col):
            if c < 0:
                continue
            s, e = self.ships[i]["s"], self.ships[i]["e"]
            q = st.setdefault(c, [s, e])
            q[0] = min(q[0], s)
            q[1] = max(q[1], e)
        return st

    def cost(self, col):
        return sum(self.F + self.r * (e - s) for s, e in self.stats(col).values())


def _finish(G, col, steps, extra=""):
    k = (max(col) + 1) if col else 0
    cost = G.cost(col)
    steps.append(dict(col=list(col), cur=-1, row=-1, kind="done",
                      msg=f"Hoàn tất: dùng {k} hợp đồng, tổng chi phí {fm(cost)}.{extra}"))
    return cost


def _result(G, steps, col, cost, optimal=None, exhausted=False):
    return dict(steps=steps, col=list(col), nBerths=(max(col) + 1) if col else 0,
                cost=cost, optimal=cost <= G.lb_cost + EPS if optimal is None else optimal,
                exhausted=exhausted)


def run_greedy(G):
    col = [-1] * G.n
    names = ", ".join(G.ships[v]["name"] for v in G.order)
    steps = [dict(col=list(col), cur=-1, row=-1, kind="info",
                  msg=f"Sắp xếp tàu theo giờ đến: {names}. Mỗi tàu được xếp vào hợp đồng có số nhỏ nhất còn dùng được, không xét chi phí.")]
    for v in G.order:
        forb = G.forb(col, v)
        c0 = G.cost(col)
        k = 0
        while k in forb:
            k += 1
        col[v] = k
        s = G.ships[v]
        c1 = G.cost(col)
        steps.append(dict(col=list(col), cur=v, row=k, kind="assign",
                          msg=f"Xét {s['name']} (đến {ft(s['s'])}, rời {ft(s['e'])}). Hợp đồng bị chặn bởi tàu xung đột: {list_contracts(forb) if forb else 'không có'}. Chọn HĐ {k + 1}, chi phí tăng thêm {fm(c1 - c0)}."))
    return _result(G, steps, col, _finish(G, col, steps))


def run_best(G):
    F, r = G.F, G.r
    col = [-1] * G.n
    cend: list[float] = []
    steps = [dict(col=list(col), cur=-1, row=-1, kind="info",
                  msg="Tham lam chọn hợp đồng rẻ nhất: duyệt tàu theo giờ đến. Với mỗi tàu, so chi phí nối vào một hợp đồng đang có (trả thêm r × số giờ kéo dài, kể cả giờ trống) với chi phí mở hợp đồng mới (F + r × số giờ của tàu), rồi chọn cách rẻ hơn.")]
    for v in G.order:
        s = G.ships[v]
        dur = s["e"] - s["s"]
        forb = G.forb(col, v)
        best_k, best_d = -1, float("inf")
        for k in range(len(cend)):
            if k in forb:
                continue
            d = r * (s["e"] - cend[k])
            if d < best_d - EPS:
                best_d, best_k = d, k
        new_d = F + r * dur
        head = f"Xét {s['name']} (đến {ft(s['s'])}, rời {ft(s['e'])}). "
        if best_k >= 0 and best_d <= new_d + EPS:
            pick = best_k
            txt = (f"{head}Nối vào HĐ {best_k + 1} (rảnh từ {ft(cend[best_k])}, trống {fm(s['s'] - cend[best_k])} giờ) "
                   f"tốn thêm {fm(r)}×{fm(s['e'] - cend[best_k])} = {fm(best_d)}, không đắt hơn mở hợp đồng mới "
                   f"({fm(F)} + {fm(r)}×{fm(dur)} = {fm(new_d)}).")
            cend[pick] = s["e"]
        else:
            pick = len(cend)
            cend.append(s["e"])
            if best_k >= 0:
                txt = (f"{head}Nối vào HĐ {best_k + 1} tốn {fm(best_d)}, đắt hơn mở hợp đồng mới "
                       f"({fm(F)} + {fm(r)}×{fm(dur)} = {fm(new_d)}). Mở HĐ {pick + 1}.")
            else:
                why = f"bị chặn: {list_contracts(forb)}" if forb else "chưa có hợp đồng nào"
                txt = (f"{head}Không hợp đồng nào dùng được ({why}). Mở HĐ {pick + 1}, "
                       f"tốn {fm(F)} + {fm(r)}×{fm(dur)} = {fm(new_d)}.")
        col[v] = pick
        steps.append(dict(col=list(col), cur=v, row=pick, kind="assign", msg=txt))
    return _result(G, steps, col, _finish(G, col, steps))


def run_dsatur(G):
    n = G.n
    col = [-1] * n
    steps = [dict(col=list(col), cur=-1, row=-1, kind="info",
                  msg="DSatur: mỗi lượt chọn tàu có nhiều hợp đồng khác nhau bị chặn nhất. Nếu hòa thì chọn tàu có nhiều xung đột nhất, rồi đến tàu đứng trước trong danh sách. Thuật toán chỉ tìm cách dùng ít hợp đồng, không xét chi phí.")]
    for _ in range(n):
        bv, bsat, bdeg, bforb = -1, -1, -1, set()
        for v in range(n):
            if col[v] >= 0:
                continue
            f = G.forb(col, v)
            deg = len(G.adj[v])
            if len(f) > bsat or (len(f) == bsat and deg > bdeg):
                bv, bsat, bdeg, bforb = v, len(f), deg, f
        c0 = G.cost(col)
        k = 0
        while k in bforb:
            k += 1
        col[bv] = k
        c1 = G.cost(col)
        steps.append(dict(col=list(col), cur=bv, row=k, kind="assign",
                          msg=f"Chọn {G.ships[bv]['name']} ({bsat} hợp đồng bị chặn, {bdeg} xung đột). Bị chặn: {list_contracts(bforb) if bforb else 'không có'}. Chọn HĐ {k + 1}, chi phí tăng thêm {fm(c1 - c0)}."))
    return _result(G, steps, col, _finish(G, col, steps))


def run_bt(G):
    n, lb, F, r = G.n, G.lb, G.F, G.r
    order = G.order
    col = [-1] * n
    cend: list[float] = []
    rem_lb = [0.0] * (n + 1)
    for i in range(n - 1, -1, -1):
        sh = G.ships[order[i]]
        rem_lb[i] = rem_lb[i + 1] + r * (sh["e"] - sh["s"])
    t0 = time.monotonic()
    steps: list[dict[str, Any]] = []
    st = dict(best=float("inf"), best_col=None, stop=False, timed_out=False, truncated=False, nodes=0)

    def push(o):
        if len(steps) < STEP_CAP:
            o["col"] = list(col)
            steps.append(o)
        else:
            st["truncated"] = True

    names = ", ".join(G.ships[v]["name"] for v in order)
    steps.append(dict(col=list(col), cur=-1, row=-1, kind="info",
                      msg=f"Quay lui: duyệt tàu theo giờ đến ({names}). Mỗi tàu thử lần lượt các lựa chọn từ rẻ đến đắt: nối vào một hợp đồng đang có hoặc mở hợp đồng mới. Nhánh nào có chi phí đã tiêu cộng cận dưới phần còn lại không thấp hơn kỷ lục thì bị cắt."))

    def rec(idx, used, cost):
        if st["stop"]:
            return
        st["nodes"] += 1
        if st["nodes"] > BT_MAX_NODES or (st["nodes"] % 256 == 0 and time.monotonic() - t0 > BT_DEADLINE_S):
            st["stop"] = st["timed_out"] = True
            return
        if idx == n:
            st["best"], st["best_col"] = cost, list(col)
            hit = cost <= G.lb_cost + EPS
            push(dict(cur=-1, row=-1, kind="found",
                      msg=f"Tìm được phương án dùng {used} hợp đồng, tổng chi phí {fm(cost)}, ghi nhận làm kỷ lục."
                          + (f" Bằng cận dưới {fm(G.lb_cost)} nên chắc chắn tối ưu, dừng tìm." if hit else " Tiếp tục tìm phương án rẻ hơn.")))
            if hit:
                st["stop"] = True
            return
        v = order[idx]
        s = G.ships[v]
        dur = s["e"] - s["s"]
        forb = G.forb(col, v)
        opts = [(r * (s["e"] - cend[k]), k, False) for k in range(used) if k not in forb]
        opts.append((F + r * dur, used, True))
        opts.sort(key=lambda o: (o[0], o[1]))
        tried = 0
        for d, k, nw in opts:
            used2 = used + 1 if nw else used
            bound = cost + d + rem_lb[idx + 1] + F * max(0, lb - used2)
            if bound >= st["best"] - EPS:
                continue
            tried += 1
            old_end = cend[k] if not nw else None
            if nw:
                cend.append(s["e"])
            else:
                cend[k] = s["e"]
            col[v] = k
            what = (f"Thử mở HĐ {k + 1} cho {s['name']} (tốn {fm(F)} + {fm(r)}×{fm(dur)} = {fm(d)})" if nw
                    else f"Thử nối {s['name']} vào HĐ {k + 1} (tốn thêm {fm(d)})")
            push(dict(cur=v, row=k, kind="assign", msg=f"{what}, tổng chi phí {fm(cost + d)}."))
            rec(idx + 1, used2, cost + d)
            if st["stop"]:
                return
            col[v] = -1
            if nw:
                cend.pop()
            else:
                cend[k] = old_end
            push(dict(cur=v, row=k, kind="back",
                      msg=f"Quay lui: bỏ {s['name']} khỏi HĐ {k + 1}, thử lựa chọn tiếp theo."))
        if not tried:
            push(dict(cur=v, row=-1, kind="dead",
                      msg=f"Cắt tỉa: mọi lựa chọn cho {s['name']} đều làm chi phí đã tiêu cộng cận dưới phần còn lại không thấp hơn kỷ lục {fm(st['best'])}. Quay lui."))

    rec(0, 0, 0.0)
    best_col = st["best_col"] or run_best(G)["col"]
    cost = G.cost(best_col)
    note = ""
    if st["timed_out"]:
        note += " Dừng vì chạm giới hạn thời gian hoặc số nút duyệt, đây là kết quả tốt nhất tìm được."
    if st["truncated"]:
        note += f" Demo chỉ hiển thị {STEP_CAP} bước đầu."
    # col trong bước cuối phải là lời giải tốt nhất, không phải trạng thái đang duyệt dở
    _finish(G, best_col, steps, note)
    return _result(G, steps, best_col, cost,
                   optimal=cost <= G.lb_cost + EPS or not st["timed_out"],
                   exhausted=not st["timed_out"])


ALGOS = dict(greedy=run_greedy, best=run_best, dsatur=run_dsatur, bt=run_bt)


def solve_all(ships, pairs, F, r):
    G = Graph(ships, pairs, F, r)
    out = {}
    for key, fn in ALGOS.items():
        t = time.perf_counter()
        res = fn(G)
        res["ms"] = round((time.perf_counter() - t) * 1000, 2)
        out[key] = res
    return dict(results=out, lb=G.lb, lbCost=G.lb_cost, sumDur=G.sum_dur)
