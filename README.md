# Điều phối cảng cho hãng tàu (CS112)

Một demo, bốn bài toán, cùng một khung giao diện (chọn thuật toán bên trái, xem từng bước bên phải):

| Module | Bài toán | Thuật toán |
|---|---|---|
| 1 Thuê bến | Tô màu đồ thị khoảng: thuê ít tiền nhất | Tham lam, best-fit, DSatur, quay lui |
| 2 Phân công đội | Gán đội đủ kỹ năng cho từng lượt tàu, không trùng giờ | Tham lam (2 kiểu), quay lui + nhánh cận |
| 3 Quỹ giờ công | Cái túi 0/1: chọn yêu cầu tăng ca giá trị lớn nhất | Tham lam giá trị/giờ, quy hoạch động, quay lui + nhánh cận |
| 4 Xếp container | Đóng thùng: dùng ít tàu nhất | First-fit, first-fit giảm dần, best-fit giảm dần, quay lui + nhánh cận |

Module 2 có nút lấy danh sách tàu từ module 1.

## Module 1: Xếp bến tàu · Tô màu đồ thị

Bài toán: hãng tàu có *n* tàu, mỗi tàu cần một bến trong khoảng [đến, rời]. Mỗi **hợp đồng thuê bến** (một màu) phục vụ nhiều tàu không trùng giờ, chi phí `F + r × (giờ rời cuối − giờ đến đầu)`, kể cả giờ trống. Hai tàu trùng giờ, hoặc có ràng buộc phụ, không được chung hợp đồng. Mục tiêu: tổng chi phí nhỏ nhất.

Bốn thuật toán: tham lam theo giờ đến, tham lam chọn hợp đồng rẻ nhất, DSatur, quay lui (lùi lại thử cách khác, có bỏ nhánh). Tab "Từng bước" hiện mã giả đang chạy, bảng ứng viên kèm lý do bị loại, biểu đồ so với phương án tốt nhất hiện có; ngoài ra có dòng thời gian, đồ thị xung đột và bảng so sánh.

## Kiến trúc
React + Vite (`frontend/`) ⇄ FastAPI (`backend/`). Mỗi module có một endpoint (`/api/solve`, `/api/assign`, `/api/knapsack`, `/api/binpack`) chạy mọi thuật toán và trả toàn bộ các bước; giao diện duyệt bước từ bộ nhớ, không gọi thêm.

```
backend/solver.py     module 1: thuật toán + sinh bước
backend/assign.py     module 2: phân công đội
backend/knapsack.py   module 3: quỹ giờ công (cái túi)
backend/binpack.py    module 4: xếp container (đóng thùng)
backend/server.py     FastAPI
frontend/src/         giao diện
tests/                pytest (so với vét cạn) + e2e Playwright
testcases/*.json      dữ liệu mẫu ban đầu của module 1
testcases/m*/         bộ testcase file (4 module × 5 nhóm), chỉ kiểm hàm thuật toán; `input` dán thẳng vào giao diện/API
testcases/RESULTS.md  bảng kết quả chạy bộ testcase (sinh tự động)
tools/gen_testcases.py   sinh lại bộ testcase (cố định seed)
tools/run_testcases.py   chạy bộ testcase, kiểm tra độc lập, ghi RESULTS.md
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
python tests/e2e_smoke.py    # giao diện module 1 (cần playwright, backend và frontend đang chạy)
python tests/e2e_modules.py  # giao diện module 2, 3, 4 (đối số: URL, mặc định http://localhost:8000)
```

## Giới hạn
Module 1: tối đa 200 tàu. Module 2: 60 tàu, 12 đội. Module 3: 25 yêu cầu, quỹ tối đa 200 giờ, số ô bảng tối đa 4000, giờ là số nguyên. Module 4: 60 lô. Các thuật toán quay lui dừng sau 400.000 nút hoặc 1,5 giây (khi đó kết quả được đánh dấu *chưa chắc tối ưu*); tối đa 3000 bước được trả về cho mỗi thuật toán.


## Bộ testcase

Năm nhóm cho mỗi module: thông thường, dữ liệu nhỏ, biên, đặc biệt, dữ liệu lớn. Chỉ kiểm các hàm giải, không kiểm lớp API.
Đáp án tối ưu tham chiếu đến từ vét cạn, công thức lý thuyết hoặc instance dựng sẵn, không lấy từ solver.

    python3 tools/gen_testcases.py      # sinh lại testcases/m*/
    python3 tools/run_testcases.py      # chạy, ghi testcases/RESULTS.md và results.json
    python3 -m pytest -q                # gồm cả 88 testcase


## Nguồn tham khảo

Đánh số để dẫn trong docstring của `backend/*.py` và trong report.

| # | Nguồn | Dùng cho |
|---|---|---|
| [1] | Huỳnh Thị Thanh Thương, bài giảng CS112 (Phân tích và thiết kế thuật toán), UIT: quy trình giải quyết vấn đề và các chiến lược thiết kế, khung tham lam, khung quay lui `try(i)`, quy hoạch động, ví dụ tô màu đồ thị | Khung tham lam, quay lui, quy hoạch động; cách mô hình hoá tô màu đồ thị |
| [2] | D. Brélaz, "New methods to color the vertices of a graph", Communications of the ACM 22(4), 1979, tr. 251–256 | DSATUR (module 1) |
| [3] | J. Kleinberg, É. Tardos, *Algorithm Design*, Addison-Wesley, 2006: §4.1 (Interval Scheduling, Interval Partitioning), §6.4 (Subset Sums and Knapsacks) | Tô màu đồ thị khoảng; quy hoạch động cái túi |
| [4] | T. Cormen, C. Leiserson, R. Rivest, C. Stein, *Introduction to Algorithms*, 3rd ed., MIT Press, 2009: §16.2 | Cái túi phân số (tham lam đúng) so với 0/1 (tham lam sai) |
| [5] | G. B. Dantzig, "Discrete-variable extremum problems", Operations Research 5(2), 1957, tr. 266–288 | Cận trên bằng nới lỏng phân số (module 3) |
| [6] | S. Martello, P. Toth, "Lower bounds and reduction procedures for the bin packing problem", Discrete Applied Mathematics 28, 1990, tr. 59–70 | Cận dưới ⌈Σw / C⌉ (module 4) |
| [7] | D. S. Johnson, A. Demers, J. D. Ullman, M. R. Garey, R. L. Graham, "Worst-case performance bounds for simple one-dimensional packing algorithms", SIAM Journal on Computing 3(4), 1974, tr. 299–325 | First-Fit, First-Fit Decreasing (module 4) |
| [8] | M. R. Garey, D. S. Johnson, *Computers and Intractability*, W. H. Freeman, 1979 | Bin packing, k-tô màu, cái túi đều là bài toán NP-khó |
| [9] | P. Hall, "On representatives of subsets", Journal of the London Mathematical Society 10(1), 1935, tr. 26–30 | Điều kiện cần để module 2 có nghiệm |
| [10] | H. W. Kuhn, "The Hungarian method for the assignment problem", Naval Research Logistics Quarterly 2, 1955, tr. 83–97 | Khớp hai phía bằng đường tăng (hàm `hall_violation`) |
| [11] | M. C. Golumbic, *Algorithmic Graph Theory and Perfect Graphs*, Academic Press, 1980 | Đồ thị khoảng: số màu = số tàu chồng nhau nhiều nhất |

**Phần tự thiết kế:** mô hình chi phí hợp đồng `F + r × (giờ rời cuối − giờ đến đầu)`, cận dưới `ω·F + r·Σ thời gian cập`, mô hình hai bài toán thực tế quanh cảng (phân công đội, quỹ giờ công), cách sinh và hiển thị từng bước, bộ testcase và bộ kiểm tra độc lập.

**Công nghệ:** Python (FastAPI, uvicorn, pydantic, pytest, Playwright), React 18.3 và Vite 5.4, font JetBrains Mono và Noto Sans qua Fontsource. Tên và phiên bản thật nằm trong `backend/requirements.txt` và `frontend/package.json`.
