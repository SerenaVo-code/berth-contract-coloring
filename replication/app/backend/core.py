"""Hạ tầng dùng chung cho cả bốn module: ghi bước và ngân sách nút duyệt.

Ngân sách tính theo SỐ NÚT, không theo đồng hồ, để cùng đầu vào luôn ra cùng kết quả
(hiến pháp, nguyên tắc 4).
"""
import time

EPS = 1e-9
MAX_NODES = 60_000       # ngân sách của một lần quay lui (module 1 tính theo lần thử gán một tàu)
MAX_STEPS = 3000         # số bước tối đa trả về cho mỗi thuật toán
MAX_STEP_CELLS = 400_000  # n * số bước: giữ kích thước JSON trong tầm kiểm soát


def step_cap(n: int) -> int:
    return max(300, min(MAX_STEPS, MAX_STEP_CELLS // max(1, n)))


class Recorder:
    """Gom các bước. Quá giới hạn thì bỏ bước, nhưng bước 'done' luôn được giữ."""

    def __init__(self, cap: int):
        self.steps: list[dict] = []
        self.cap = cap
        self.truncated = False

    def add(self, kind: str, msg: str, **data) -> None:
        if kind == "done" or len(self.steps) < self.cap:
            self.steps.append({"kind": kind, "msg": msg, **data})
        else:
            self.truncated = True


class Budget:
    def __init__(self, max_nodes: int = MAX_NODES):
        self.max_nodes = max_nodes
        self.nodes = 0
        self.exhausted = False

    def tick(self) -> bool:
        """Đếm một nút. Trả False khi đã hết ngân sách."""
        self.nodes += 1
        if self.nodes > self.max_nodes:
            self.exhausted = True
        return not self.exhausted


class Timer:
    """Đo thời gian chạy (chỉ để hiển thị, không dùng để cắt thuật toán)."""

    def __enter__(self):
        self.t0 = time.perf_counter()
        self._end = None
        return self

    def __exit__(self, *a):
        self._end = time.perf_counter()

    @property
    def ms(self):  # đọc được cả khi `return` giữa khối with
        return ((self._end or time.perf_counter()) - self.t0) * 1000


def fmt(x: float) -> str:
    """Số gọn cho thông điệp: bỏ .0 thừa."""
    return str(int(x)) if float(x).is_integer() else f"{x:.2f}".rstrip("0").rstrip(".")

MAX_NODES_BIN = 400_000  # nút của đóng thùng rất rẻ nên ngân sách lớn hơn
