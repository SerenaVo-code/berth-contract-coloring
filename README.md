# Xếp bến tàu · Tô màu đồ thị (CS112)

Bài toán: hãng tàu có *n* tàu, mỗi tàu cần một bến trong khoảng [đến, rời]. Mỗi **hợp đồng thuê bến** (một màu) phục vụ nhiều tàu không trùng giờ, chi phí `F + r × (giờ rời cuối − giờ đến đầu)`, kể cả giờ trống. Hai tàu trùng giờ, hoặc có ràng buộc phụ, không được chung hợp đồng. Mục tiêu: tổng chi phí nhỏ nhất.

Bốn thuật toán: tham lam theo giờ đến, tham lam chọn hợp đồng rẻ nhất, DSatur, quay lui (lùi lại thử cách khác, có bỏ nhánh). Tab "Từng bước" hiện mã giả đang chạy, bảng ứng viên kèm lý do bị loại, biểu đồ so với phương án tốt nhất hiện có; ngoài ra có dòng thời gian, đồ thị xung đột và bảng so sánh.

## Kiến trúc
React + Vite (`frontend/`) ⇄ FastAPI (`backend/`). Một endpoint `POST /api/solve` chạy cả 4 thuật toán và trả toàn bộ các bước; giao diện duyệt bước từ bộ nhớ, không gọi thêm.

```
backend/solver.py     thuật toán + sinh bước
backend/server.py     FastAPI
frontend/src/         giao diện
tests/                pytest (so với vét cạn) + e2e Playwright
testcases/*.json      dữ liệu mẫu
```

## Chạy
Codespaces: Code → Codespaces → Create codespace on main. Môi trường chỉ có sẵn Python và Node, **không tự cài hay tự chạy gì**. Trong Terminal:

```bash
npm run setup    # cài thư viện (một lần)
npm run dev      # chạy backend :8000 + giao diện :5173 (Ctrl+C để dừng)
```
Mở tab Ports, bấm biểu tượng địa cầu ở cổng 5173. Trên máy cũng dùng đúng các lệnh này.

Chạy một cổng: `npm --prefix frontend run build`, rồi `cd backend && uvicorn server:app --port 8000` và mở http://localhost:8000.

## Kiểm thử
```bash
npm test                   # thuật toán + API
python tests/e2e_smoke.py  # giao diện (cần playwright, backend và frontend đang chạy)
```

## Giới hạn
Tối đa 200 tàu; quay lui dừng sau 400.000 nút hoặc 1,5 giây (khi đó kết quả được đánh dấu *chưa chắc tối ưu*); tối đa 3000 bước được trả về cho mỗi thuật toán.
