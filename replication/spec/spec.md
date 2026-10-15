# Đặc tả: Demo điều phối cảng cho hãng tàu

## 1. Vì sao
Người dùng là bên hãng tàu (góc nhìn chủ tàu thuê bến, gần với công việc ở ONE). Một hãng có n tàu cần cập cảng trong khoảng giờ [đến, rời]. Hãng không sở hữu bến mà **thuê theo hợp đồng**. Câu hỏi: nên ký bao nhiêu hợp đồng và xếp tàu nào vào hợp đồng nào để tổng tiền thuê nhỏ nhất. Quanh bài toán đó có ba việc nhỏ hơn của cùng một cảng: phân công đội phục vụ, chọn việc tăng ca trong quỹ giờ công, xếp container lên tàu.

## 2. Bốn module
Mọi module có cùng khung: nhập dữ liệu, chọn thuật toán, xem từng bước, xem kết quả, so sánh các thuật toán.

### Module 1. Thuê bến (tô màu đồ thị khoảng)
- **Input:** n tàu (tên, giờ đến s, giờ rời e, s < e), danh sách cặp tàu cấm chung hợp đồng (ràng buộc phụ), phí cố định F ≥ 0, đơn giá giờ r ≥ 0.
- **Mô hình:** tàu là đỉnh, hợp đồng là màu. Hai tàu trùng giờ (s_i < e_j và s_j < e_i) hoặc nằm trong cặp cấm thì không chung hợp đồng.
- **Chi phí một hợp đồng:** F + r × (giờ rời cuối − giờ đến đầu), tính cả giờ trống giữa các tàu.
- **Output:** gán tàu → hợp đồng, tổng chi phí nhỏ nhất.
- **Cận dưới:** ω·F + r·Σ(e − s), với ω là số tàu cùng neo nhiều nhất.
- **Thuật toán:** tham lam theo giờ đến, tham lam chọn hợp đồng tăng ít tiền nhất, DSATUR, quay lui có bỏ nhánh.
- **Giới hạn:** 1 đến 200 tàu.

### Module 2. Phân công đội phục vụ
- **Input:** n tàu (tên, s, e, danh sách kỹ năng cần), m đội (tên, kỹ năng, đơn giá giờ), cặp tàu cấm chung đội.
- **Ràng buộc:** mỗi tàu một đội có đủ kỹ năng; hai tàu trùng giờ hoặc bị cấm không chung đội.
- **Chi phí:** Σ đơn giá đội × (e − s).
- **Output:** gán tàu → đội, hoặc kết luận vô nghiệm kèm lý do.
- **Thuật toán:** tham lam theo giờ đến, tham lam tàu khó trước (ít đội đủ kỹ năng nhất), quay lui có bỏ nhánh. Có bước kiểm tra trước điều kiện cần (khớp hai phía theo từng thời điểm) để chứng minh vô nghiệm nhanh.
- **Giới hạn:** 1 đến 60 tàu, 1 đến 12 đội.

### Module 3. Quỹ giờ công (cái túi 0/1)
- **Input:** n yêu cầu tăng ca (tên, số giờ w nguyên ≥ 1, giá trị v ≥ 0), quỹ giờ W nguyên.
- **Output:** tập yêu cầu được nhận có tổng giờ ≤ W và tổng giá trị lớn nhất.
- **Thuật toán:** tham lam theo giá trị/giờ (cố ý để thấy nó sai), quy hoạch động có truy vết, quay lui với cận trên nới lỏng phân số.
- **Giới hạn:** 1 đến 25 yêu cầu, 0 ≤ W ≤ 200, n·(W+1) ≤ 2500.

### Module 4. Xếp container
- **Input:** n lô (tên, khối lượng w), tải trọng một tàu C, 0 < w ≤ C.
- **Output:** gán lô → tàu sao cho mỗi tàu không quá C, số tàu ít nhất.
- **Cận dưới:** ⌈Σw / C⌉.
- **Thuật toán:** First-Fit, First-Fit giảm dần, Best-Fit giảm dần, quay lui có bỏ nhánh.
- **Giới hạn:** 1 đến 60 lô.

## 3. Hợp đồng bước (chung)
Mỗi thuật toán trả `{key, name, steps[], cost|value|bins, optimal, nodes, truncated, ms}`. Mỗi bước có `kind` (info, assign, back, prune, found, done, ...), `msg` tiếng Việt, và trạng thái đủ để vẽ lại màn hình. Quay lui có thêm `best` (phương án tốt nhất hiện có) và `depth`.

## 4. Tiêu chí chấp nhận
- A1. Với mọi testcase có đáp án tham chiếu, kết quả quay lui không tệ hơn đáp án và nếu chạy hết thì bằng đáp án.
- A2. Không thuật toán nào trả phương án vi phạm ràng buộc (kiểm bằng checker độc lập).
- A3. Chạy hai lần cùng đầu vào ra đúng cùng kết quả (kể cả quay lui).
- A4. Người dùng bấm Tiếp/Lùi/Tự động/kéo thanh trượt và thấy trạng thái khớp với `msg`.
- A5. Mỗi module có mẫu cơ bản bấm một lần là chạy.
