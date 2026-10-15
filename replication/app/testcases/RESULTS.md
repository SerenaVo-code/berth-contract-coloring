# Kết quả chạy bộ testcase (bản dựng lại)

Tổng: **79/79** testcase đạt. Sinh bởi `tools/run_testcases.py`.

Đáp án tham chiếu đến từ vét cạn, công thức, instance dựng sẵn hoặc DP một chiều viết riêng, không lấy từ solver. Kết quả mỗi thuật toán đã được `tools/checker.py` tính lại độc lập.


## Thuê bến

| Nhóm | Số ca | Đạt |
|---|---|---|
| Thông thường | 5 | 5 |
| Dữ liệu nhỏ | 3 | 3 |
| Biên | 8 | 8 |
| Đặc biệt | 6 | 6 |
| Dữ liệu lớn | 5 | 5 |

| ID | Nhóm | Cỡ | Tiêu đề | Tham chiếu | Kết quả từng thuật toán | ms | Đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| m1-B01 | Biên | 1 tàu | Chỉ 1 tàu | 170 (vét cạn) | Tham lam theo giờ đến 170; Tham lam chọn hợp đồng rẻ nhất 170; DSATUR 170; Quay lui 170 | 0.06 | ✔ |  |
| m1-B02 | Biên | 2 tàu | Hai tàu chạm đầu mút | 140 (vét cạn) | Tham lam theo giờ đến 140; Tham lam chọn hợp đồng rẻ nhất 140; DSATUR 140; Quay lui 140 | 0.03 | ✔ |  |
| m1-B03 | Biên | 2 tàu | Hai tàu chồng 0,5 giờ | 245 (vét cạn) | Tham lam theo giờ đến 245; Tham lam chọn hợp đồng rẻ nhất 245; DSATUR 245; Quay lui 245 | 0.04 | ✔ |  |
| m1-B04 | Biên | 9 tàu | F = 0 | 295 (công thức) | Tham lam theo giờ đến 365; Tham lam chọn hợp đồng rẻ nhất 295; DSATUR 360; Quay lui 295 | 0.12 | ✔ |  |
| m1-B05 | Biên | 12 tàu | r = 0 | 1200 (công thức) | Tham lam theo giờ đến 1200; Tham lam chọn hợp đồng rẻ nhất 1200; DSATUR 1200; Quay lui 1200 | 0.17 | ✔ |  |
| m1-B06 | Biên | 2 tàu | F = 0 và r = 0 | 0 (công thức) | Tham lam theo giờ đến 0; Tham lam chọn hợp đồng rẻ nhất 0; DSATUR 0; Quay lui 0 | 0.02 | ✔ |  |
| m1-B07 | Biên | 4 tàu | Tàu qua đêm (giờ > 24) | 750 (vét cạn) | Tham lam theo giờ đến 774; Tham lam chọn hợp đồng rẻ nhất 750; DSATUR 774; Quay lui 750 | 0.09 | ✔ |  |
| m1-B08 | Biên | 3 tàu | Giờ lẻ 0,25 | 230 (vét cạn) | Tham lam theo giờ đến 230; Tham lam chọn hợp đồng rẻ nhất 230; DSATUR 230; Quay lui 230 | 0.03 | ✔ |  |
| m1-D01 | Đặc biệt | 6 tàu | 6 tàu trùng giờ hoàn toàn | 960 (vét cạn) | Tham lam theo giờ đến 960; Tham lam chọn hợp đồng rẻ nhất 960; DSATUR 960; Quay lui 960 | 0.07 | ✔ |  |
| m1-D02 | Đặc biệt | 9 tàu | 9 tàu nối đuôi | 480 (công thức) | Tham lam theo giờ đến 480; Tham lam chọn hợp đồng rẻ nhất 480; DSATUR 480; Quay lui 480 | 0.1 | ✔ |  |
| m1-D03 | Đặc biệt | 5 tàu | Chu trình lẻ C5 do ràng buộc phụ | 550 (vét cạn) | Tham lam theo giờ đến 550; Tham lam chọn hợp đồng rẻ nhất 550; DSATUR 550; Quay lui 550 | 0.05 | ✔ |  |
| m1-D04 | Đặc biệt | 4 tàu | Cặp cấm lặp, đảo chiều và tự thân | 300 (vét cạn) | Tham lam theo giờ đến 330; Tham lam chọn hợp đồng rẻ nhất 300; DSATUR 330; Quay lui 300 | 0.07 | ✔ |  |
| m1-D05 | Đặc biệt | 6 tàu | Mọi cặp bị cấm (K6) | 660 (vét cạn) | Tham lam theo giờ đến 660; Tham lam chọn hợp đồng rẻ nhất 660; DSATUR 660; Quay lui 660 | 0.08 | ✔ |  |
| m1-D06 | Đặc biệt | 5 tàu | Cùng giờ đến, khác giờ rời | 740 (vét cạn) | Tham lam theo giờ đến 740; Tham lam chọn hợp đồng rẻ nhất 740; DSATUR 740; Quay lui 740 | 0.05 | ✔ |  |
| m1-L01 | Dữ liệu lớn | 30 tàu | 30 tàu ngẫu nhiên | — | Tham lam theo giờ đến 8275; Tham lam chọn hợp đồng rẻ nhất 7945; DSATUR 8245; Quay lui 7945 | 362.49 | ✔ | quay lui hết ngân sách (không có đáp án tham chiếu) |
| m1-L02 | Dữ liệu lớn | 100 tàu | 100 tàu, F = 0 | 9975 (công thức) | Tham lam theo giờ đến 14737.5; Tham lam chọn hợp đồng rẻ nhất 9975; DSATUR 14562.5; Quay lui 9975 | 4.96 | ✔ |  |
| m1-L03 | Dữ liệu lớn | 100 tàu | 100 tàu, r = 0 | 3300 (công thức) | Tham lam theo giờ đến 3300; Tham lam chọn hợp đồng rẻ nhất 3300; DSATUR 3300; Quay lui 3300 | 5.55 | ✔ |  |
| m1-L04 | Dữ liệu lớn | 200 tàu | 200 tàu (tối đa), ngẫu nhiên | — | Tham lam theo giờ đến 46965; Tham lam chọn hợp đồng rẻ nhất 41900; DSATUR 47115; Quay lui 41900 | 378.82 | ✔ | quay lui hết ngân sách (không có đáp án tham chiếu) |
| m1-L05 | Dữ liệu lớn | 200 tàu | 200 tàu nối đuôi | 6200 (công thức) | Tham lam theo giờ đến 6200; Tham lam chọn hợp đồng rẻ nhất 6200; DSATUR 6200; Quay lui 6200 | 6.38 | ✔ |  |
| m1-N01 | Dữ liệu nhỏ | 2 tàu | 2 tàu rời nhau | 190 (vét cạn) | Tham lam theo giờ đến 190; Tham lam chọn hợp đồng rẻ nhất 190; DSATUR 190; Quay lui 190 | 0.07 | ✔ |  |
| m1-N02 | Dữ liệu nhỏ | 3 tàu | 3 tàu chồng nhau | 450 (vét cạn) | Tham lam theo giờ đến 450; Tham lam chọn hợp đồng rẻ nhất 450; DSATUR 450; Quay lui 450 | 0.04 | ✔ |  |
| m1-N03 | Dữ liệu nhỏ | 4 tàu | Hai cụm tàu cách xa | 390 (vét cạn) | Tham lam theo giờ đến 420; Tham lam chọn hợp đồng rẻ nhất 390; DSATUR 420; Quay lui 390 | 0.13 | ✔ |  |
| m1-T01 | Thông thường | 8 tàu | 8 tàu ngẫu nhiên #1 | 5000 (vét cạn) | Tham lam theo giờ đến 5000; Tham lam chọn hợp đồng rẻ nhất 5000; DSATUR 5020; Quay lui 5000 | 0.47 | ✔ |  |
| m1-T02 | Thông thường | 8 tàu | 8 tàu ngẫu nhiên #2 | 4440 (vét cạn) | Tham lam theo giờ đến 4560; Tham lam chọn hợp đồng rẻ nhất 4440; DSATUR 4520; Quay lui 4440 | 0.67 | ✔ |  |
| m1-T03 | Thông thường | 8 tàu | 8 tàu ngẫu nhiên #3 | 4380 (vét cạn) | Tham lam theo giờ đến 4500; Tham lam chọn hợp đồng rẻ nhất 4380; DSATUR 4420; Quay lui 4380 | 0.29 | ✔ |  |
| m1-T04 | Thông thường | 8 tàu | 8 tàu ngẫu nhiên #4 | 3600 (vét cạn) | Tham lam theo giờ đến 3660; Tham lam chọn hợp đồng rẻ nhất 3600; DSATUR 3600; Quay lui 3600 | 0.42 | ✔ |  |
| m1-T05 | Thông thường | 8 tàu | Bốn thuật toán cho bốn chi phí khác nhau | 3780 (vét cạn) | Tham lam theo giờ đến 3960; Tham lam chọn hợp đồng rẻ nhất 3800; DSATUR 3840; Quay lui 3780 | 0.69 | ✔ |  |

## Phân công đội

| Nhóm | Số ca | Đạt |
|---|---|---|
| Thông thường | 3 | 3 |
| Dữ liệu nhỏ | 3 | 3 |
| Biên | 5 | 5 |
| Đặc biệt | 4 | 4 |
| Dữ liệu lớn | 3 | 3 |

| ID | Nhóm | Cỡ | Tiêu đề | Tham chiếu | Kết quả từng thuật toán | ms | Đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| m2-B01 | Biên | 2 tàu | Hai tàu chạm đầu mút, một đội | 40 (công thức) | Tham lam theo giờ đến 40; Tham lam tàu khó trước 40; Quay lui 40 | 0.04 | ✔ |  |
| m2-B02 | Biên | 2 tàu | Hai tàu chồng, chỉ một đội | — | Tham lam theo giờ đến fail; Tham lam tàu khó trước fail; Quay lui infeasible | 0.02 | ✔ |  |
| m2-B03 | Biên | 1 tàu | Thiếu một kỹ năng | — | Tham lam theo giờ đến fail; Tham lam tàu khó trước fail; Quay lui infeasible | 0.01 | ✔ |  |
| m2-B04 | Biên | 1 tàu | Đơn giá 0, không cần kỹ năng | 0 (công thức) | Tham lam theo giờ đến 0; Tham lam tàu khó trước 0; Quay lui 0 | 0.04 | ✔ |  |
| m2-B05 | Biên | 2 tàu | Cặp cấm ép hai tàu rời nhau vào hai đội | — | Tham lam theo giờ đến fail; Tham lam tàu khó trước fail; Quay lui infeasible | 0.03 | ✔ |  |
| m2-D01 | Đặc biệt | 3 tàu | 3 tàu cùng giờ, 2 đội đủ kỹ năng (vi phạm Hall) | — | Tham lam theo giờ đến fail; Tham lam tàu khó trước fail; Quay lui infeasible | 0.02 | ✔ |  |
| m2-D02 | Đặc biệt | 6 tàu | Có nghiệm nhưng tham lam theo giờ đến bị kẹt | 198 (vét cạn) | Tham lam theo giờ đến fail; Tham lam tàu khó trước 243.5; Quay lui 198 | 0.14 | ✔ |  |
| m2-D03 | Đặc biệt | 5 tàu | Chu trình lẻ cấm với 2 đội | — | Tham lam theo giờ đến fail; Tham lam tàu khó trước fail; Quay lui infeasible | 0.08 | ✔ |  |
| m2-D04 | Đặc biệt | 5 tàu | Các đội giống hệt nhau | 145 (vét cạn) | Tham lam theo giờ đến 145; Tham lam tàu khó trước 145; Quay lui 145 | 0.04 | ✔ |  |
| m2-L01 | Dữ liệu lớn | 30 tàu | 30 tàu, 8 đội | — | Tham lam theo giờ đến 1119; Tham lam tàu khó trước 1166.5; Quay lui 1100 | 1189.67 | ✔ | quay lui hết ngân sách (không có đáp án tham chiếu) |
| m2-L02 | Dữ liệu lớn | 60 tàu | 60 tàu, 12 đội (tối đa) | — | Tham lam theo giờ đến 2495.5; Tham lam tàu khó trước 2526; Quay lui 2467.5 | 2314.05 | ✔ | quay lui hết ngân sách (không có đáp án tham chiếu) |
| m2-L03 | Dữ liệu lớn | 40 tàu | 40 tàu nối đuôi, 2 đội | 560 (công thức) | Tham lam theo giờ đến 560; Tham lam tàu khó trước 560; Quay lui 560 | 0.18 | ✔ |  |
| m2-N01 | Dữ liệu nhỏ | 1 tàu | 1 tàu, 1 đội | 40 (công thức) | Tham lam theo giờ đến 40; Tham lam tàu khó trước 40; Quay lui 40 | 0.03 | ✔ |  |
| m2-N02 | Dữ liệu nhỏ | 2 tàu | 2 tàu rời nhau, 2 đội | 42 (vét cạn) | Tham lam theo giờ đến 42; Tham lam tàu khó trước 42; Quay lui 42 | 0.03 | ✔ |  |
| m2-N03 | Dữ liệu nhỏ | 4 tàu | 4 tàu, 2 đội | — | Tham lam theo giờ đến fail; Tham lam tàu khó trước fail; Quay lui infeasible | 0.02 | ✔ |  |
| m2-T01 | Thông thường | 6 tàu | 6 tàu, 4 đội #1 | 451.5 (vét cạn) | Tham lam theo giờ đến 452.5; Tham lam tàu khó trước 452.5; Quay lui 451.5 | 0.22 | ✔ |  |
| m2-T02 | Thông thường | 6 tàu | 6 tàu, 4 đội #2 | 248 (vét cạn) | Tham lam theo giờ đến 248; Tham lam tàu khó trước 248; Quay lui 248 | 0.09 | ✔ |  |
| m2-T03 | Thông thường | 6 tàu | 6 tàu, 4 đội #3 | 481 (vét cạn) | Tham lam theo giờ đến 485; Tham lam tàu khó trước 485; Quay lui 481 | 1.17 | ✔ |  |

## Quỹ giờ công

| Nhóm | Số ca | Đạt |
|---|---|---|
| Thông thường | 4 | 4 |
| Dữ liệu nhỏ | 3 | 3 |
| Biên | 4 | 4 |
| Đặc biệt | 3 | 3 |
| Dữ liệu lớn | 3 | 3 |

| ID | Nhóm | Cỡ | Tiêu đề | Tham chiếu | Kết quả từng thuật toán | ms | Đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| m3-B01 | Biên | 1 mục | Quỹ 0 giờ | 0 (công thức) | Tham lam giá trị/giờ 0; Quy hoạch động 0; Quay lui + cận trên 0 | 0.01 | ✔ |  |
| m3-B02 | Biên | 2 mục | Mọi yêu cầu vượt quỹ | 0 (công thức) | Tham lam giá trị/giờ 0; Quy hoạch động 0; Quay lui + cận trên 0 | 0.03 | ✔ |  |
| m3-B03 | Biên | 2 mục | Mọi yêu cầu có giá trị 0 | 0 (công thức) | Tham lam giá trị/giờ 0; Quy hoạch động 0; Quay lui + cận trên 0 | 0.02 | ✔ |  |
| m3-B04 | Biên | 8 mục | Quỹ vừa đúng tổng giờ | 154 (công thức) | Tham lam giá trị/giờ 154; Quy hoạch động 154; Quay lui + cận trên 154 | 0.28 | ✔ |  |
| m3-D01 | Đặc biệt | 6 mục | Mọi yêu cầu giống nhau | 30 (công thức) | Tham lam giá trị/giờ 30; Quy hoạch động 30; Quay lui + cận trên 30 | 0.14 | ✔ |  |
| m3-D02 | Đặc biệt | 3 mục | Giá trị/giờ bằng nhau | 20 (công thức) | Tham lam giá trị/giờ 20; Quy hoạch động 20; Quay lui + cận trên 20 | 0.06 | ✔ |  |
| m3-D03 | Đặc biệt | 10 mục | Một yêu cầu lớn so với nhiều yêu cầu nhỏ | 100 (vét cạn) | Tham lam giá trị/giờ 99; Quy hoạch động 100; Quay lui + cận trên 100 | 3.7 | ✔ |  |
| m3-L01 | Dữ liệu lớn | 25 mục | 25 yêu cầu (tối đa), quỹ 100 | 997 (DP độc lập) | Tham lam giá trị/giờ 970; Quy hoạch động 997; Quay lui + cận trên 997 | 3.76 | ✔ |  |
| m3-L02 | Dữ liệu lớn | 12 mục | 12 yêu cầu, quỹ 200 | 614 (vét cạn) | Tham lam giá trị/giờ 614; Quy hoạch động 614; Quay lui + cận trên 614 | 3.66 | ✔ |  |
| m3-L03 | Dữ liệu lớn | 25 mục | 25 yêu cầu nhỏ, quỹ 98 | 840 (DP độc lập) | Tham lam giá trị/giờ 835; Quy hoạch động 840; Quay lui + cận trên 840 | 4.21 | ✔ |  |
| m3-N01 | Dữ liệu nhỏ | 1 mục | 1 yêu cầu vừa quỹ | 7 (công thức) | Tham lam giá trị/giờ 7; Quy hoạch động 7; Quay lui + cận trên 7 | 0.02 | ✔ |  |
| m3-N02 | Dữ liệu nhỏ | 2 mục | 2 yêu cầu, chỉ nhận được một | 8 (công thức) | Tham lam giá trị/giờ 8; Quy hoạch động 8; Quay lui + cận trên 8 | 0.03 | ✔ |  |
| m3-N03 | Dữ liệu nhỏ | 5 mục | 5 yêu cầu | 48 (vét cạn) | Tham lam giá trị/giờ 48; Quy hoạch động 48; Quay lui + cận trên 48 | 0.11 | ✔ |  |
| m3-T01 | Thông thường | 10 mục | 10 yêu cầu #1 | 196 (vét cạn) | Tham lam giá trị/giờ 196; Quy hoạch động 196; Quay lui + cận trên 196 | 0.56 | ✔ |  |
| m3-T02 | Thông thường | 10 mục | 10 yêu cầu #2 | 129 (vét cạn) | Tham lam giá trị/giờ 129; Quy hoạch động 129; Quay lui + cận trên 129 | 0.6 | ✔ |  |
| m3-T03 | Thông thường | 10 mục | 10 yêu cầu #3 | 245 (vét cạn) | Tham lam giá trị/giờ 245; Quy hoạch động 245; Quay lui + cận trên 245 | 0.72 | ✔ |  |
| m3-T04 | Thông thường | 3 mục | Ví dụ kinh điển: tham lam sai | 220 (instance dựng sẵn) | Tham lam giá trị/giờ 160; Quy hoạch động 220; Quay lui + cận trên 220 | 0.24 | ✔ |  |

## Xếp container

| Nhóm | Số ca | Đạt |
|---|---|---|
| Thông thường | 4 | 4 |
| Dữ liệu nhỏ | 3 | 3 |
| Biên | 3 | 3 |
| Đặc biệt | 3 | 3 |
| Dữ liệu lớn | 4 | 4 |

| ID | Nhóm | Cỡ | Tiêu đề | Tham chiếu | Kết quả từng thuật toán | ms | Đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| m4-B01 | Biên | 2 mục | Lô nặng đúng bằng tải trọng | 2 (công thức) | First-Fit 2; First-Fit giảm dần 2; Best-Fit giảm dần 2; Quay lui + bỏ nhánh 2 | 0.03 | ✔ |  |
| m4-B02 | Biên | 10 mục | Mọi lô nặng 1 chen đủ một tàu | 1 (công thức) | First-Fit 1; First-Fit giảm dần 1; Best-Fit giảm dần 1; Quay lui + bỏ nhánh 1 | 0.05 | ✔ |  |
| m4-B03 | Biên | 10 mục | Khối lượng lẻ 0,1 | 1 (công thức) | First-Fit 1; First-Fit giảm dần 1; Best-Fit giảm dần 1; Quay lui + bỏ nhánh 1 | 0.06 | ✔ |  |
| m4-D01 | Đặc biệt | 7 mục | Mọi lô quá nửa tải | 7 (công thức) | First-Fit 7; First-Fit giảm dần 7; Best-Fit giảm dần 7; Quay lui + bỏ nhánh 7 | 0.07 | ✔ |  |
| m4-D02 | Đặc biệt | 8 mục | First-Fit giảm dần không tối ưu | 3 (vét cạn) | First-Fit 4; First-Fit giảm dần 4; Best-Fit giảm dần 4; Quay lui + bỏ nhánh 3 | 0.09 | ✔ |  |
| m4-D03 | Đặc biệt | 9 mục | Tổng lẻ so với tải trọng | 5 (công thức) | First-Fit 5; First-Fit giảm dần 5; Best-Fit giảm dần 5; Quay lui + bỏ nhánh 5 | 0.04 | ✔ |  |
| m4-L01 | Dữ liệu lớn | 30 mục | Dựng sẵn: 6 tàu đầy tải | 6 (instance dựng sẵn) | First-Fit 7; First-Fit giảm dần 7; Best-Fit giảm dần 7; Quay lui + bỏ nhánh 6 | 468.5 | ✔ |  |
| m4-L02 | Dữ liệu lớn | 41 mục | Dựng sẵn: 10 tàu đầy tải (cắt ≤ 60 lô) | — | First-Fit 11; First-Fit giảm dần 11; Best-Fit giảm dần 11; Quay lui + bỏ nhánh 10 | 0.48 | ✔ |  |
| m4-L03 | Dữ liệu lớn | 60 mục | 60 lô ngẫu nhiên (tối đa) | — | First-Fit 33; First-Fit giảm dần 30; Best-Fit giảm dần 30; Quay lui + bỏ nhánh 30 | 0.9 | ✔ |  |
| m4-L04 | Dữ liệu lớn | 60 mục | 60 lô đều quá nửa tải | 60 (công thức) | First-Fit 60; First-Fit giảm dần 60; Best-Fit giảm dần 60; Quay lui + bỏ nhánh 60 | 0.77 | ✔ |  |
| m4-N01 | Dữ liệu nhỏ | 1 mục | 1 lô | 1 (công thức) | First-Fit 1; First-Fit giảm dần 1; Best-Fit giảm dần 1; Quay lui + bỏ nhánh 1 | 0.01 | ✔ |  |
| m4-N02 | Dữ liệu nhỏ | 2 mục | 2 lô vừa một tàu | 1 (công thức) | First-Fit 1; First-Fit giảm dần 1; Best-Fit giảm dần 1; Quay lui + bỏ nhánh 1 | 0.01 | ✔ |  |
| m4-N03 | Dữ liệu nhỏ | 2 mục | 2 lô không vừa chung | 2 (công thức) | First-Fit 2; First-Fit giảm dần 2; Best-Fit giảm dần 2; Quay lui + bỏ nhánh 2 | 0.01 | ✔ |  |
| m4-T01 | Thông thường | 9 mục | 9 lô #1 | 5 (vét cạn) | First-Fit 5; First-Fit giảm dần 5; Best-Fit giảm dần 5; Quay lui + bỏ nhánh 5 | 0.05 | ✔ |  |
| m4-T02 | Thông thường | 9 mục | 9 lô #2 | 5 (vét cạn) | First-Fit 5; First-Fit giảm dần 5; Best-Fit giảm dần 5; Quay lui + bỏ nhánh 5 | 0.06 | ✔ |  |
| m4-T03 | Thông thường | 9 mục | 9 lô #3 | 6 (vét cạn) | First-Fit 6; First-Fit giảm dần 6; Best-Fit giảm dần 6; Quay lui + bỏ nhánh 6 | 0.06 | ✔ |  |
| m4-T04 | Thông thường | 9 mục | First-Fit tệ hơn First-Fit giảm dần | 4 (vét cạn) | First-Fit 5; First-Fit giảm dần 4; Best-Fit giảm dần 4; Quay lui + bỏ nhánh 4 | 0.06 | ✔ |  |
