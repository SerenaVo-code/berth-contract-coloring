"""Module 1: thuê bến theo hợp đồng = tô màu đồ thị khoảng với hàm chi phí.

Tham chiếu (xem README):
  [1] bài giảng CS112 (khung tham lam, khung quay lui try(i))   [2] Brélaz 1979 (DSATUR)
  [3] Kleinberg-Tardos §4.1 (interval partitioning)             [11] Golumbic 1980 (số màu = ω)
Tự thiết kế: chi phí hợp đồng F + r·(giờ rời cuối − giờ đến đầu), cận dưới ω·F + r·Σ(e−s).
"""
from core import EPS, Budget, Recorder, Timer, fmt, step_cap, MAX_NODES


def prepare(ships, pairs, F, r):
    n = len(ships)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if ships[i]["s"] < ships[j]["e"] and ships[j]["s"] < ships[i]["e"]:
                adj[i].add(j)
                adj[j].add(i)
    for a, b in pairs:
        if a != b:
            adj[a].add(b)
            adj[b].add(a)
    ev = []
    for sh in ships:
        ev.append((sh["s"], 1))
        ev.append((sh["e"], -1))
    ev.sort(key=lambda t: (t[0], t[1]))  # rời trước đến khi cùng giờ
    cur = omega = 0
    for _, d in ev:
        cur += d
        omega = max(omega, cur)
    lb = omega * F + r * sum(sh["e"] - sh["s"] for sh in ships)
    return {"n": n, "ships": ships, "adj": adj, "F": F, "r": r, "omega": omega, "lb": lb}


def total_cost(P, col):
    """Chi phí tính lại từ gán `col` (checker dùng hàm này)."""
    span = {}
    for i, k in enumerate(col):
        s, e = P["ships"][i]["s"], P["ships"][i]["e"]
        lo, hi = span.get(k, (s, e))
        span[k] = (min(lo, s), max(hi, e))
    return sum(P["F"] + P["r"] * (hi - lo) for lo, hi in span.values())


def is_valid(P, col):
    return all(col[i] >= 0 and all(col[i] != col[j] for j in P["adj"][i]) for i in range(P["n"]))


class State:
    """Trạng thái hợp đồng: giờ đến đầu, giờ rời cuối, số tàu, chi phí hiện tại."""

    def __init__(self, P):
        self.P = P
        self.col = [-1] * P["n"]
        self.lo, self.hi, self.cnt = [], [], []
        self.cost = 0.0

    def contracts(self):
        return len(self.lo)

    def blockers(self, v, k):
        return [u for u in self.P["adj"][v] if self.col[u] == k]

    def delta(self, v, k):
        s, e = self.P["ships"][v]["s"], self.P["ships"][v]["e"]
        if k == len(self.lo):
            return self.P["F"] + self.P["r"] * (e - s)
        return self.P["r"] * ((max(self.hi[k], e) - min(self.lo[k], s)) - (self.hi[k] - self.lo[k]))

    def put(self, v, k):
        """Gán v vào hợp đồng k; trả thông tin để hoàn tác."""
        s, e = self.P["ships"][v]["s"], self.P["ships"][v]["e"]
        d = self.delta(v, k)
        if k == len(self.lo):
            self.lo.append(s); self.hi.append(e); self.cnt.append(1)
            undo = (k, None, None)
        else:
            undo = (k, self.lo[k], self.hi[k])
            self.lo[k] = min(self.lo[k], s); self.hi[k] = max(self.hi[k], e); self.cnt[k] += 1
        self.col[v] = k
        self.cost += d
        return undo, d

    def remove(self, v, undo, d):
        k, lo, hi = undo
        self.col[v] = -1
        self.cost -= d
        if lo is None:
            self.lo.pop(); self.hi.pop(); self.cnt.pop()
        else:
            self.lo[k], self.hi[k] = lo, hi
            self.cnt[k] -= 1


def cands(P, st, v, new_only=False):
    """Bảng ứng viên cho tàu v: mỗi hợp đồng đã có (hợp lệ hay lý do bị loại) và hợp đồng mới."""
    out = []
    for k in range(st.contracts()):
        bl = st.blockers(v, k)
        if bl:
            names = ", ".join(P["ships"][u]["name"] for u in sorted(bl)[:3]) + ("…" if len(bl) > 3 else "")
            out.append({"k": k, "ok": False, "why": f"xung đột với {names}", "delta": None})
        else:
            out.append({"k": k, "ok": True, "why": "", "delta": st.delta(v, k)})
    out.append({"k": st.contracts(), "ok": True, "why": "mở hợp đồng mới", "delta": st.delta(v, st.contracts())})
    return out


def snap(st):
    return {"col": st.col[:], "cost": round(st.cost, 6), "n_contracts": st.contracts()}


def finish(P, name, key, rec, st_col, optimal, ms, nodes=0, extra=None):
    cost = total_cost(P, st_col)
    out = {"key": key, "name": name, "steps": rec.steps, "col": st_col, "cost": cost,
           "n_contracts": len(set(st_col)), "optimal": optimal, "nodes": nodes,
           "truncated": rec.truncated, "ms": ms}
    if extra:
        out.update(extra)
    return out


# --------------------------------------------------------------------------- tham lam
def order_arrival(P):
    return sorted(range(P["n"]), key=lambda i: (P["ships"][i]["s"], P["ships"][i]["e"], i))


def run_greedy(P, cheapest=False):
    key = "greedy_cost" if cheapest else "greedy"
    name = "Tham lam chọn hợp đồng rẻ nhất" if cheapest else "Tham lam theo giờ đến"
    rec = Recorder(step_cap(P["n"]))
    with Timer() as t:
        st = State(P)
        order = order_arrival(P)
        rec.add("info", ("Sắp tàu theo giờ đến. Mỗi tàu vào hợp đồng " +
                         ("làm tổng tiền tăng ít nhất (kể cả mở hợp đồng mới)." if cheapest
                          else "có số thứ tự nhỏ nhất mà không xung đột.")),
                order=order, **snap(st))
        for v in order:
            cs = cands(P, st, v)
            ok = [c for c in cs if c["ok"]]
            pick = min(ok, key=lambda c: (c["delta"], c["k"])) if cheapest else ok[0]
            _, d = st.put(v, pick["k"])
            sh = P["ships"][v]
            rec.add("assign",
                    f"Xét {sh['name']} ({fmt(sh['s'])}h–{fmt(sh['e'])}h). Chọn hợp đồng {pick['k'] + 1}"
                    f"{' (mới)' if pick['why'] == 'mở hợp đồng mới' else ''}, tăng {fmt(d)}.",
                    cur=v, to=pick["k"], cands=cs, **snap(st))
        rec.add("done", f"Hoàn tất: {st.contracts()} hợp đồng, tổng {fmt(st.cost)}.", cur=-1, **snap(st))
    return finish(P, name, key, rec, st.col, st.cost <= P["lb"] + EPS, t.ms)


def run_dsatur(P):
    rec = Recorder(step_cap(P["n"]))
    with Timer() as t:
        st = State(P)
        rec.add("info", "DSATUR: mỗi lượt chọn tàu bị chặn bởi nhiều hợp đồng khác nhau nhất; hòa thì chọn tàu nhiều xung đột hơn, rồi tàu đứng trước. Tàu vào hợp đồng nhỏ nhất còn hợp lệ.", **snap(st))
        for _ in range(P["n"]):
            best = None
            for v in range(P["n"]):
                if st.col[v] >= 0:
                    continue
                sat = len({st.col[u] for u in P["adj"][v] if st.col[u] >= 0})
                key = (-sat, -len(P["adj"][v]), v)
                if best is None or key < best[0]:
                    best = (key, v, sat)
            _, v, sat = best
            cs = cands(P, st, v)
            pick = next(c for c in cs if c["ok"])
            _, d = st.put(v, pick["k"])
            sh = P["ships"][v]
            rec.add("assign",
                    f"Chọn {sh['name']} ({sat} hợp đồng bị chặn, {len(P['adj'][v])} xung đột). "
                    f"Vào hợp đồng {pick['k'] + 1}{' (mới)' if pick['why'] else ''}, tăng {fmt(d)}.",
                    cur=v, to=pick["k"], cands=cs, **snap(st))
        rec.add("done", f"Hoàn tất: {st.contracts()} hợp đồng, tổng {fmt(st.cost)}.", cur=-1, **snap(st))
    return finish(P, "DSATUR", "dsatur", rec, st.col, st.cost <= P["lb"] + EPS, t.ms)


# --------------------------------------------------------------------------- quay lui
def run_bt(P, seed_col, max_nodes=MAX_NODES):
    """Quay lui. Phương án tốt nhất hiện có khởi tạo từ `seed_col` (kết quả tham lam rẻ nhất)."""
    n, F = P["n"], P["F"]
    rec = Recorder(step_cap(n))
    bud = Budget(max_nodes)
    with Timer() as t:
        st = State(P)
        order = order_arrival(P)
        best_col = seed_col[:]
        best = total_cost(P, best_col)
        stop = [best <= P["lb"] + EPS]
        rec.add("info", f"Quay lui duyệt tàu theo giờ đến. Phương án tốt nhất hiện có bắt đầu từ kết quả tham lam: {fmt(best)}. "
                        f"Chỉ nhận phương án rẻ hơn. Cận dưới toàn bài: {fmt(P['lb'])}.",
                best=round(best, 6), depth=0, **snap(st))
        if stop[0]:
            rec.add("info", "Phương án tham lam đã bằng cận dưới nên chắc chắn tối ưu, không cần tìm tiếp.",
                    best=round(best, 6), depth=0, **snap(st))

        def rec_(idx):
            nonlocal best, best_col
            if stop[0]:
                return
            if idx == n:
                if st.cost < best - EPS:
                    best, best_col = st.cost, st.col[:]
                    rec.add("found", f"Tìm được phương án rẻ hơn: {fmt(best)}. Ghi nhận là phương án tốt nhất hiện có.",
                            best=round(best, 6), depth=idx, **snap(st))
                    if best <= P["lb"] + EPS:
                        rec.add("info", "Bằng cận dưới nên chắc chắn tối ưu, dừng.", best=round(best, 6), depth=idx, **snap(st))
                        stop[0] = True
                return
            v = order[idx]
            cs = cands(P, st, v)
            ok = sorted([c for c in cs if c["ok"]], key=lambda c: (c["delta"], c["k"]))
            for c in ok:
                if not bud.tick():  # mỗi lần thử gán một tàu tính một đơn vị ngân sách
                    stop[0] = True
                    return
                k = c["k"]
                undo, d = st.put(v, k)
                # cận: chi phí hiện tại + phí của các hợp đồng còn phải mở để đủ ω
                bound = st.cost + F * max(0, P["omega"] - st.contracts())
                sh = P["ships"][v]["name"]
                pruned = bound >= best - EPS
                if pruned:
                    rec.add("prune", f"Bỏ nhánh: {sh} vào hợp đồng {k + 1} cho cận {fmt(bound)} ≥ {fmt(best)} (phương án tốt nhất hiện có).",
                            cur=v, to=k, best=round(best, 6), depth=idx + 1, **snap(st))
                else:
                    rec.add("assign", f"Thử {sh} vào hợp đồng {k + 1}, tăng {fmt(d)}, tổng tạm {fmt(st.cost)}.",
                            cur=v, to=k, best=round(best, 6), depth=idx + 1, cands=cs, **snap(st))
                    rec_(idx + 1)
                st.remove(v, undo, d)
                if stop[0]:
                    return
                if not pruned:
                    rec.add("back", f"Quay lui: bỏ {sh} khỏi hợp đồng {k + 1}, thử lựa chọn kế tiếp.",
                            cur=v, to=k, best=round(best, 6), depth=idx, **snap(st))

        rec_(0)
        tail = ""
        if bud.exhausted:
            tail = f" Dừng vì hết ngân sách {bud.max_nodes} nút, chưa chắc tối ưu."
        if rec.truncated:
            tail += f" Chỉ hiển thị {len(rec.steps)} bước đầu."
        fin = State(P)
        fin.col = best_col[:]
        rec.add("done", f"Hoàn tất: tổng {fmt(best)}.{tail}", cur=-1, col=best_col[:], cost=round(best, 6),
                n_contracts=len(set(best_col)), best=round(best, 6))
    optimal = (not bud.exhausted) or best <= P["lb"] + EPS
    return finish(P, "Quay lui", "bt", rec, best_col, optimal, t.ms, nodes=bud.nodes)


def solve_all(ships, pairs, F, r, max_nodes=MAX_NODES):
    P = prepare(ships, pairs, F, r)
    g = run_greedy(P)
    gc = run_greedy(P, cheapest=True)
    d = run_dsatur(P)
    seed = min([g, gc, d], key=lambda x: x["cost"])["col"]
    b = run_bt(P, seed, max_nodes)
    return {"lb": P["lb"], "omega": P["omega"], "n": P["n"], "algos": [g, gc, d, b]}
