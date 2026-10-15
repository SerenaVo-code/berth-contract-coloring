# Nhật ký kỹ thuật của lần dựng lại

Tác giả: Claude. Ghi những gì thật sự xảy ra khi dựng lại, theo thứ tự.

1. **Hiến pháp và đặc tả** (`spec/`). Hai thay đổi so với bản gốc, đều xuất phát từ hạn chế đã biết: quay lui giới hạn theo số lần thử chứ không theo đồng hồ (cùng đầu vào luôn cùng kết quả); bảng quy hoạch động tối đa 2500 ô để mỗi ô là một bước.
2. **Backend** (`app/backend/`): bốn module và hạ tầng ghi bước dùng chung `core.py`. Quay lui khởi tạo từ kết quả tham lam tốt nhất; module 2 có kiểm tra điều kiện cần (khớp hai phía) để chứng minh vô nghiệm.
3. **Kiểm thử** (`app/tests/`): so với vét cạn trên dữ liệu ngẫu nhiên nhỏ, kiểm tính xác định, kiểm số tự báo bằng số tính lại. Đáp án tham chiếu nằm trong `oracles.py`, độc lập với solver.
4. **Bộ testcase** (79 ca, 5 nhóm x 4 module) sinh bằng `tools/gen_testcases.py`; `tools/checker.py` tính lại độc lập.
5. **Giao diện React**: phát lại bước, Gantt, đồ thị xung đột, bảng quy hoạch động, cột tàu; nhập/xuất JSON theo đúng định dạng testcase. Dữ liệu mẫu trên giao diện lấy từ testcase (`tools/make_samples.py`).

## Lỗi thật gặp phải và cách sửa
- `Timer.ms` chưa có khi `return` giữa khối `with` → 24 test module 2 hỏng. Sửa: `ms` thành thuộc tính tính tại chỗ.
- Mô tả vài testcase không khớp kết quả thật (FF "kém hơn" FFD nhưng bằng nhau; tham lam "bị kẹt" nhưng không kẹt). Sửa: sinh bằng cách tìm instance thật có tính chất đó (đáp án vẫn từ vét cạn).
- Quay lui module 1 với 200 tàu mất 17 giây cho 150 nghìn nút. Sửa: tính ngân sách theo lần thử gán, 60 nghìn đơn vị, còn khoảng 0,4 giây.
- Giao diện sập khi xóa tên tàu: kết quả cũ còn, dữ liệu mới là `null`. Sửa: hook trả kèm đúng dữ liệu đã dùng để ra kết quả (`solved`).
- Chỉ số bước vượt số bước khi đổi thuật toán. Sửa: kẹp trong `usePlayer`.
- Sau đối chiếu với bản gốc: bản dựng lại kém ở 3 ca lớn. Nguyên nhân: module 4 cần ngân sách 400 nghìn nút (rẻ mỗi nút); module 2 duyệt theo "tàu khó trước" kém hơn duyệt theo giờ đến. Sau sửa: m4-L01 đạt tối ưu 6; m2-L01 1100 bằng bản gốc; m2-L02 2467,5 (bản gốc 2471,5).

## Kết quả
- 79/79 testcase dựng lại đạt; 237 pytest đạt; e2e Playwright đạt.
- Đối chiếu: 88/88 testcase của bản gốc đạt trên solver dựng lại; 78/79 testcase dựng lại cho cùng kết quả tốt nhất, ca còn lại bản dựng lại tốt hơn.

## Hạn chế còn lại
- Quay lui vẫn hết ngân sách ở các ca lớn module 1 và 2 (không chứng minh được tối ưu).
- m4-L02 hết ngân sách trước khi chạm tối ưu.
- Chưa thử trên Codespaces; chưa đẩy lên GitHub (token đăng nhập của phiên làm việc đang lỗi).
