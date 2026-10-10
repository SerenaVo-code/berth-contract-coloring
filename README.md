# Xếp bến tàu · Tô màu đồ thị (CS112)

Bài toán: hãng tàu có *n* tàu, mỗi tàu cần một bến trong khoảng [đến, rời]. Mỗi **hợp đồng thuê bến** (một màu) phục vụ nhiều tàu không trùng giờ, chi phí `F + r × (giờ rời cuối − giờ đến đầu)`, kể cả giờ trống. Hai tàu trùng giờ, hoặc có ràng buộc phụ, không được chung hợp đồng. Mục tiêu: tổng chi phí nhỏ nhất.

Bốn thuật toán: tham lam theo giờ đến, tham lam chọn hợp đồng rẻ nhất, DSatur, quay lui có cắt tỉa. Giao diện xem từng bước, đồ thị xung đột, bảng so sánh.

## Kiến trúc
React + Vite (`frontend/`) ⇄ FastAPI (`backend/`). Một endpoint `POST /api/solve` chạy cả 4 thuật toán và trả toàn bộ các bước; giao diện duyệt bước từ bộ nhớ, không gọi thêm.

```
backend/solver.py     thuật toán + sinh bước
backend/server.py     FastAPI
frontend/src/         giao diện
tests/                pytest (so với vét cạn) + e2e Playwright
testcases/*.json      dữ liệu mẫu
```

## Chạy bằng GitHub Codespaces (khuyên dùng)
Code → Codespaces → Create. Môi trường tự cài thư viện và chạy server; mở cổng **5173** (giao diện). Nếu cần chạy lại: `bash scripts/start.sh`.

## Chạy trên máy
```bash
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
bash scripts/start.sh          # 8000 (API) + 5173 (giao diện)
```
Chạy một cổng: `cd frontend && npm run build`, rồi `cd backend && uvicorn server:app --port 8000` và mở http://localhost:8000.

## Kiểm thử
```bash
python -m pytest tests          # thuật toán + API
python tests/e2e_smoke.py       # giao diện (cần playwright, backend và frontend đang chạy)
```

## Giới hạn
Tối đa 200 tàu; quay lui dừng sau 400.000 nút hoặc 1,5 giây (khi đó kết quả được đánh dấu *chưa chắc tối ưu*); tối đa 3000 bước được trả về cho mỗi thuật toán.
