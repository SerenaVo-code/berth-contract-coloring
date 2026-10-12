# Kết quả chạy bộ testcase

Tổng: **122/122** testcase đạt. Sinh tự động bởi `tools/run_testcases.py` từ các file trong `testcases/`.

Cách đọc: *Kết quả* là chi phí (module 1, 2), giá trị (module 3) hoặc số thùng (module 4) mà mỗi thuật toán trả về, đã được tính lại độc lập. *Tối ưu tham chiếu* lấy từ vét cạn, công thức hoặc instance dựng sẵn, không lấy từ solver.

## Thuê bến (tô màu đồ thị)

| Nhóm | Số testcase | Đạt |
|---|---|---|
| Thông thường | 5 | 5 |
| Dữ liệu nhỏ | 4 | 4 |
| Biên | 9 | 9 |
| Đặc biệt | 6 | 6 |
| Dữ liệu lớn | 5 | 5 |
| Không hợp lệ | 10 | 10 |

| ID | Nhóm | Cỡ | Tiêu đề | Tối ưu tham chiếu | Kết quả từng thuật toán | Thời gian lớn nhất (ms) | Đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| m1-B01 | Biên | 1 tàu | Chỉ 1 tàu | 140 (vét cạn) | Tham lam 140; Tham lam chi phí 140; DSATUR 140; Quay lui 140 | 0.06 | ✔ |  |
| m1-B02 | Biên | 2 tàu | Hai tàu chạm đầu mút (rời = đến) | 180 (vét cạn) | Tham lam 180; Tham lam chi phí 180; DSATUR 180; Quay lui 180 | 0.07 | ✔ |  |
| m1-B03 | Biên | 2 tàu | Hai tàu chồng sát 0,5 giờ | 285 (vét cạn) | Tham lam 285; Tham lam chi phí 285; DSATUR 285; Quay lui 285 | 0.05 | ✔ |  |
| m1-B04 | Biên | 12 tàu | F = 0 | 269.5 (công thức) | Tham lam 374.5; Tham lam chi phí 269.5; DSATUR 392; Quay lui 269.5 | 0.51 | ✔ |  |
| m1-B05 | Biên | 15 tàu | r = 0 | 200 (công thức) | Tham lam 200; Tham lam chi phí 200; DSATUR 200; Quay lui 200 | 0.56 | ✔ |  |
| m1-B06 | Biên | 6 tàu | F = 0 và r = 0 | 0 (công thức) | Tham lam 0; Tham lam chi phí 0; DSATUR 0; Quay lui 0 | 0.19 | ✔ |  |
| m1-B07 | Biên | 4 tàu | Tàu qua đêm (giờ > 24) | 530 (vét cạn) | Tham lam 600; Tham lam chi phí 530; DSATUR 600; Quay lui 530 | 0.13 | ✔ |  |
| m1-B08 | Biên | 4 tàu | Giờ lẻ 0,25 | 256.25 (vét cạn) | Tham lam 256.25; Tham lam chi phí 256.25; DSATUR 265.625; Quay lui 256.25 | 0.16 | ✔ |  |
| m1-B09 | Biên | 9 tàu | F rất lớn so với r | 40037.5 (vét cạn) | Tham lam 40040; Tham lam chi phí 40037.5; DSATUR 40042; Quay lui 40037.5 | 2.97 | ✔ |  |
| m1-D01 | Đặc biệt | 10 tàu | 10 tàu trùng giờ hoàn toàn | 1400 (vét cạn) | Tham lam 1400; Tham lam chi phí 1400; DSATUR 1400; Quay lui 1400 | 0.38 | ✔ |  |
| m1-D02 | Đặc biệt | 10 tàu | 10 tàu nối đuôi không chồng | 560 (vét cạn) | Tham lam 560; Tham lam chi phí 560; DSATUR 560; Quay lui 560 | 0.35 | ✔ |  |
| m1-D03 | Đặc biệt | 5 tàu | Chu trình lẻ C5 do ràng buộc thêm | 390 (vét cạn) | Tham lam 390; Tham lam chi phí 390; DSATUR 390; Quay lui 390 | 0.21 | ✔ |  |
| m1-D04 | Đặc biệt | 4 tàu | Cặp ràng buộc lặp, đảo chiều và tự thân | 250 (vét cạn) | Tham lam 265; Tham lam chi phí 250; DSATUR 265; Quay lui 250 | 0.09 | ✔ |  |
| m1-D05 | Đặc biệt | 6 tàu | Mọi cặp bị cấm (K6 do ràng buộc) | 660 (vét cạn) | Tham lam 660; Tham lam chi phí 660; DSATUR 660; Quay lui 660 | 0.11 | ✔ |  |
| m1-D06 | Đặc biệt | 5 tàu | Cùng giờ đến, khác giờ rời | 520 (vét cạn) | Tham lam 550; Tham lam chi phí 520; DSATUR 550; Quay lui 520 | 0.11 | ✔ |  |
| m1-L01 | Dữ liệu lớn | 30 tàu | 30 tàu ngẫu nhiên | — | Tham lam 3640; Tham lam chi phí 3095; DSATUR 3540; Quay lui 3095 | 1505.37 | ✔ | BT chạm giới hạn thời gian (không có đáp án tham chiếu) |
| m1-L02 | Dữ liệu lớn | 100 tàu | 100 tàu, r = 0 | 1020 (công thức) | Tham lam 1020; Tham lam chi phí 1020; DSATUR 1020; Quay lui 1020 | 44.49 | ✔ |  |
| m1-L03 | Dữ liệu lớn | 100 tàu | 100 tàu, F = 0 | 2262 (công thức) | Tham lam 3082; Tham lam chi phí 2262; DSATUR 3078; Quay lui 2262 | 145.53 | ✔ |  |
| m1-L04 | Dữ liệu lớn | 200 tàu | 200 tàu (tối đa), ngẫu nhiên | — | Tham lam 27936; Tham lam chi phí 23556; DSATUR 27870; Quay lui 23556 | 1508.85 | ✔ | BT chạm giới hạn thời gian (không có đáp án tham chiếu) |
| m1-L05 | Dữ liệu lớn | 200 tàu | 200 tàu nối đuôi, F lớn | 5599 (công thức) | Tham lam 5599; Tham lam chi phí 5599; DSATUR 5599; Quay lui 5599 | 51.71 | ✔ |  |
| m1-N01 | Dữ liệu nhỏ | 2 tàu | 2 tàu rời nhau | 135 (vét cạn) | Tham lam 135; Tham lam chi phí 135; DSATUR 135; Quay lui 135 | 0.06 | ✔ |  |
| m1-N02 | Dữ liệu nhỏ | 3 tàu | 3 tàu chồng giờ hoàn toàn | 270 (vét cạn) | Tham lam 270; Tham lam chi phí 270; DSATUR 270; Quay lui 270 | 0.06 | ✔ |  |
| m1-N03 | Dữ liệu nhỏ | 4 tàu | 4 tàu nối chuỗi | 320 (vét cạn) | Tham lam 320; Tham lam chi phí 320; DSATUR 320; Quay lui 320 | 0.08 | ✔ |  |
| m1-N04 | Dữ liệu nhỏ | 5 tàu | 5 tàu hỗn hợp | 384 (vét cạn) | Tham lam 420; Tham lam chi phí 384; DSATUR 420; Quay lui 384 | 0.16 | ✔ |  |
| m1-T01 | Thông thường | 7 tàu | Mẫu cơ bản (7 tàu, 1 cặp ràng buộc) | 2580 (vét cạn) | Tham lam 2700; Tham lam chi phí 2580; DSATUR 2840; Quay lui 2580 | 0.24 | ✔ |  |
| m1-T02 | Thông thường | 8 tàu | Bốn thuật toán cho bốn kết quả khác nhau | 2900 (vét cạn) | Tham lam 3400; Tham lam chi phí 3340; DSATUR 3000; Quay lui 2900 | 0.25 | ✔ |  |
| m1-T03 | Thông thường | 6 tàu | 6 tàu ngẫu nhiên, không ràng buộc thêm | 1360 (vét cạn) | Tham lam 1360; Tham lam chi phí 1360; DSATUR 1370; Quay lui 1360 | 0.17 | ✔ |  |
| m1-T04 | Thông thường | 8 tàu | 8 tàu ngẫu nhiên, 3 cặp ràng buộc | 1022.5 (vét cạn) | Tham lam 1155; Tham lam chi phí 1155; DSATUR 1022.5; Quay lui 1022.5 | 0.43 | ✔ |  |
| m1-T05 | Thông thường | 10 tàu | 10 tàu ngẫu nhiên | 990 (vét cạn) | Tham lam 1005; Tham lam chi phí 990; DSATUR 1005; Quay lui 990 | 2.31 | ✔ |  |
| m1-X01 | Không hợp lệ | 0 tàu | Danh sách tàu rỗng | HTTP 422 | — | 0 | ✔ | bị từ chối: Số tàu phải từ 1 đến 200. |
| m1-X02 | Không hợp lệ | 1 tàu | Giờ rời trước giờ đến | HTTP 422 | — | 0 | ✔ | bị từ chối: Tàu 1: giờ rời phải sau giờ đến. |
| m1-X03 | Không hợp lệ | 1 tàu | Giờ rời bằng giờ đến | HTTP 422 | — | 0 | ✔ | bị từ chối: Tàu 1: giờ rời phải sau giờ đến. |
| m1-X04 | Không hợp lệ | 2 tàu | F âm | HTTP 422 | — | 0 | ✔ | bị từ chối: F và r phải không âm. |
| m1-X05 | Không hợp lệ | 2 tàu | r âm | HTTP 422 | — | 0 | ✔ | bị từ chối: F và r phải không âm. |
| m1-X06 | Không hợp lệ | 2 tàu | Cặp ràng buộc ngoài phạm vi | HTTP 422 | — | 0 | ✔ | bị từ chối: Cặp ràng buộc không hợp lệ. |
| m1-X07 | Không hợp lệ | 2 tàu | Cặp ràng buộc sai dạng | HTTP 422 | — | 0 | ✔ | bị từ chối: Cặp ràng buộc không hợp lệ. |
| m1-X08 | Không hợp lệ | 201 tàu | 201 tàu (vượt giới hạn 200) | HTTP 422 | — | 0 | ✔ | bị từ chối: Số tàu phải từ 1 đến 200. |
| m1-X09 | Không hợp lệ | 1 tàu | Thiếu trường giờ đến | HTTP 422 | — | 0 | ✔ | bị từ chối: [{'type': 'missing', 'loc': ['body', 'ships', 0, 's'], 'msg': 'Field required', 'input': { |
| m1-X10 | Không hợp lệ | 1 tàu | Giờ là chữ | HTTP 422 | — | 0 | ✔ | bị từ chối: [{'type': 'float_parsing', 'loc': ['body', 'ships', 0, 's'], 'msg': 'Input should be a val |

## Phân công đội (gán việc)

| Nhóm | Số testcase | Đạt |
|---|---|---|
| Thông thường | 4 | 4 |
| Dữ liệu nhỏ | 3 | 3 |
| Biên | 5 | 5 |
| Đặc biệt | 5 | 5 |
| Dữ liệu lớn | 4 | 4 |
| Không hợp lệ | 8 | 8 |

| ID | Nhóm | Cỡ | Tiêu đề | Tối ưu tham chiếu | Kết quả từng thuật toán | Thời gian lớn nhất (ms) | Đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| m2-B01 | Biên | 2 tàu × 2 đội | Tàu nối đuôi (rời = đến) | 800 (vét cạn) | Tham lam 800; Khó trước 800; Quay lui 800 | 0.1 | ✔ |  |
| m2-B02 | Biên | 2 tàu × 2 đội | Chồng sát 0,5 giờ | 1650 (vét cạn) | Tham lam 1750; Khó trước 1750; Quay lui 1650 | 0.08 | ✔ |  |
| m2-B03 | Biên | 2 tàu × 2 đội | Đơn giá bằng 0 | 0 (vét cạn) | Tham lam 0; Khó trước 0; Quay lui 0 | 0.05 | ✔ |  |
| m2-B04 | Biên | 3 tàu × 3 đội | Các đội cùng đơn giá | 1200 (vét cạn) | Tham lam 1200; Khó trước 1200; Quay lui 1200 | 0.06 | ✔ |  |
| m2-B05 | Biên | 3 tàu × 3 đội | Số đội đúng bằng số tàu chồng nhau | 1200 (vét cạn) | Tham lam 1200; Khó trước 1200; Quay lui 1200 | 0.07 | ✔ |  |
| m2-D01 | Đặc biệt | 2 tàu × 2 đội | Vô nghiệm: thiếu kỹ năng | vô nghiệm | Tham lam —; Khó trước —; Quay lui — | 0.07 | ✔ | vô nghiệm, đã phát hiện đúng |
| m2-D02 | Đặc biệt | 3 tàu × 2 đội | Vô nghiệm: thiếu đội | vô nghiệm | Tham lam —; Khó trước —; Quay lui — | 0.05 | ✔ | vô nghiệm, đã phát hiện đúng |
| m2-D03 | Đặc biệt | 4 tàu × 3 đội | Đội rẻ nhất bị tranh nhiều | 2080 (vét cạn) | Tham lam 2080; Khó trước 2080; Quay lui 2080 | 0.2 | ✔ |  |
| m2-D04 | Đặc biệt | 2 tàu × 2 đội | Tham lam theo giờ đến bị trượt nghiệm | 1000 (vét cạn) | Tham lam —; Khó trước 1000; Quay lui 1000 | 0.07 | ✔ | Tham lam không gán được hết |
| m2-D05 | Đặc biệt | 3 tàu × 2 đội | Đội 'lạnh' rẻ hơn đội thường | 660 (vét cạn) | Tham lam —; Khó trước 660; Quay lui 660 | 0.08 | ✔ | Tham lam không gán được hết |
| m2-L01 | Dữ liệu lớn | 20 tàu × 6 đội | 20 tàu, 6 đội | — | Tham lam 6780; Khó trước 6780; Quay lui 6740 | 1500.22 | ✔ | BT chạm giới hạn thời gian (không có đáp án tham chiếu) |
| m2-L02 | Dữ liệu lớn | 60 tàu × 4 đội | 60 tàu nối đuôi (tối đa) | 19800 (công thức) | Tham lam 19800; Khó trước 19800; Quay lui 19800 | 3.01 | ✔ |  |
| m2-L03 | Dữ liệu lớn | 40 tàu × 12 đội | 40 tàu, 12 đội | — | Tham lam 12160; Khó trước 12040; Quay lui 12040 | 1500.48 | ✔ | BT chạm giới hạn thời gian (không có đáp án tham chiếu) |
| m2-L04 | Dữ liệu lớn | 32 tàu × 6 đội | 32 tàu, vô nghiệm do 7 tàu cùng cập, chỉ 6 đội | vô nghiệm | Tham lam —; Khó trước —; Quay lui — | 0.97 | ✔ | vô nghiệm, đã phát hiện đúng |
| m2-N01 | Dữ liệu nhỏ | 1 tàu × 1 đội | 1 tàu, 1 đội | 400 (vét cạn) | Tham lam 400; Khó trước 400; Quay lui 400 | 0.04 | ✔ |  |
| m2-N02 | Dữ liệu nhỏ | 2 tàu × 2 đội | 2 tàu trùng giờ, 2 đội | 880 (vét cạn) | Tham lam 880; Khó trước 880; Quay lui 880 | 0.13 | ✔ |  |
| m2-N03 | Dữ liệu nhỏ | 3 tàu × 1 đội | 3 tàu rời nhau, 1 đội | 350 (vét cạn) | Tham lam 350; Khó trước 350; Quay lui 350 | 0.07 | ✔ |  |
| m2-T01 | Thông thường | 6 tàu × 4 đội | Mẫu chính (6 tàu, 4 đội) | 3060 (vét cạn) | Tham lam 3060; Khó trước 3060; Quay lui 3060 | 0.31 | ✔ |  |
| m2-T02 | Thông thường | 6 tàu × 4 đội | Có cặp ràng buộc thêm | 3100 (vét cạn) | Tham lam 3110; Khó trước 3110; Quay lui 3100 | 0.26 | ✔ |  |
| m2-T03 | Thông thường | 7 tàu × 4 đội | 7 tàu ngẫu nhiên, 4 đội | 2460 (vét cạn) | Tham lam 2550; Khó trước 2490; Quay lui 2460 | 0.67 | ✔ |  |
| m2-T04 | Thông thường | 8 tàu × 5 đội | 8 tàu ngẫu nhiên, 5 đội | 2620 (vét cạn) | Tham lam 2630; Khó trước 2630; Quay lui 2620 | 0.5 | ✔ |  |
| m2-X01 | Không hợp lệ | 0 tàu × 1 đội | Không có tàu | HTTP 422 | — | 0 | ✔ | bị từ chối: Cần 1–60 tàu và 1–12 đội. |
| m2-X02 | Không hợp lệ | 1 tàu × 0 đội | Không có đội | HTTP 422 | — | 0 | ✔ | bị từ chối: Cần 1–60 tàu và 1–12 đội. |
| m2-X03 | Không hợp lệ | 1 tàu × 13 đội | 13 đội (vượt giới hạn 12) | HTTP 422 | — | 0 | ✔ | bị từ chối: Cần 1–60 tàu và 1–12 đội. |
| m2-X04 | Không hợp lệ | 61 tàu × 1 đội | 61 tàu (vượt giới hạn 60) | HTTP 422 | — | 0 | ✔ | bị từ chối: Cần 1–60 tàu và 1–12 đội. |
| m2-X05 | Không hợp lệ | 1 tàu × 1 đội | Giờ rời không sau giờ đến | HTTP 422 | — | 0 | ✔ | bị từ chối: T1: giờ rời phải sau giờ đến. |
| m2-X06 | Không hợp lệ | 1 tàu × 1 đội | Đơn giá âm | HTTP 422 | — | 0 | ✔ | bị từ chối: Đơn giá phải không âm. |
| m2-X07 | Không hợp lệ | 1 tàu × 1 đội | Cặp ràng buộc ngoài phạm vi | HTTP 422 | — | 0 | ✔ | bị từ chối: Cặp ràng buộc không hợp lệ. |
| m2-X08 | Không hợp lệ | 1 tàu × 1 đội | Thiếu đơn giá của đội | HTTP 422 | — | 0 | ✔ | bị từ chối: [{'type': 'missing', 'loc': ['body', 'teams', 0, 'rate'], 'msg': 'Field required', 'input' |

## Quỹ giờ công (cái túi 0/1)

| Nhóm | Số testcase | Đạt |
|---|---|---|
| Thông thường | 4 | 4 |
| Dữ liệu nhỏ | 3 | 3 |
| Biên | 5 | 5 |
| Đặc biệt | 4 | 4 |
| Dữ liệu lớn | 3 | 3 |
| Không hợp lệ | 8 | 8 |

| ID | Nhóm | Cỡ | Tiêu đề | Tối ưu tham chiếu | Kết quả từng thuật toán | Thời gian lớn nhất (ms) | Đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| m3-B01 | Biên | 2 yêu cầu, W=0 | Quỹ = 0 | 0 (vét cạn) | Tham lam 0; QHĐ 0; Quay lui 0 | 0.03 | ✔ |  |
| m3-B02 | Biên | 3 yêu cầu, W=10 | Yêu cầu có w đúng bằng quỹ | 100 (vét cạn) | Tham lam 100; QHĐ 100; Quay lui 100 | 0.12 | ✔ |  |
| m3-B03 | Biên | 3 yêu cầu, W=8 | Mọi yêu cầu đều quá nặng | 0 (vét cạn) | Tham lam 0; QHĐ 0; Quay lui 0 | 0.07 | ✔ |  |
| m3-B04 | Biên | 3 yêu cầu, W=6 | Giá trị bằng 0 | 25 (vét cạn) | Tham lam 25; QHĐ 25; Quay lui 25 | 0.06 | ✔ |  |
| m3-B05 | Biên | 20 yêu cầu, W=199 | Số ô DP đúng bằng giới hạn 4000 | 1172 (DP độc lập) | Tham lam 1170; QHĐ 1172; Quay lui 1172 | 10.32 | ✔ | tham lam thiếu 2 |
| m3-D01 | Đặc biệt | 4 yêu cầu, W=7 | Cùng giá trị/giờ (hoà) | 70 (vét cạn) | Tham lam 50; QHĐ 70; Quay lui 70 | 0.15 | ✔ | tham lam thiếu 20 |
| m3-D02 | Đặc biệt | 3 yêu cầu, W=12 | Bẫy tham lam | 66 (vét cạn) | Tham lam 43; QHĐ 66; Quay lui 66 | 0.15 | ✔ | tham lam thiếu 23 |
| m3-D03 | Đặc biệt | 4 yêu cầu, W=8 | Giá trị lẻ (số thập phân) | 11.35 (vét cạn) | Tham lam 10.25; QHĐ 11.35; Quay lui 11.35 | 0.22 | ✔ | tham lam thiếu 1.1 |
| m3-D04 | Đặc biệt | 6 yêu cầu, W=12 | Nhiều yêu cầu trùng hệt nhau | 30 (vét cạn) | Tham lam 30; QHĐ 30; Quay lui 30 | 0.37 | ✔ |  |
| m3-L01 | Dữ liệu lớn | 20 yêu cầu, W=120 | 20 yêu cầu, quỹ 120 | 1567 (DP độc lập) | Tham lam 1562; QHĐ 1567; Quay lui 1567 | 10.89 | ✔ | tham lam thiếu 5 |
| m3-L02 | Dữ liệu lớn | 25 yêu cầu, W=150 | 25 yêu cầu (tối đa), quỹ 150 | 2169 (DP độc lập) | Tham lam 2167; QHĐ 2169; Quay lui 2169 | 13.79 | ✔ | tham lam thiếu 2 |
| m3-L03 | Dữ liệu lớn | 25 yêu cầu, W=150 | 25 yêu cầu tương quan mạnh (khó cho cận trên) | 1519 (DP độc lập) | Tham lam 1499; QHĐ 1519; Quay lui 1519 | 10.36 | ✔ | tham lam thiếu 20 |
| m3-N01 | Dữ liệu nhỏ | 1 yêu cầu, W=8 | 1 yêu cầu vừa quỹ | 40 (vét cạn) | Tham lam 40; QHĐ 40; Quay lui 40 | 0.03 | ✔ |  |
| m3-N02 | Dữ liệu nhỏ | 2 yêu cầu, W=8 | 2 yêu cầu, chỉ lấy được một | 50 (vét cạn) | Tham lam 50; QHĐ 50; Quay lui 50 | 0.05 | ✔ |  |
| m3-N03 | Dữ liệu nhỏ | 3 yêu cầu, W=10 | 3 yêu cầu lấy hết | 35 (vét cạn) | Tham lam 35; QHĐ 35; Quay lui 35 | 0.1 | ✔ |  |
| m3-T01 | Thông thường | 4 yêu cầu, W=8 | Mẫu chính (4 yêu cầu, quỹ 8 giờ) | 110 (vét cạn) | Tham lam 100; QHĐ 110; Quay lui 110 | 0.11 | ✔ | tham lam thiếu 10 |
| m3-T02 | Thông thường | 3 yêu cầu, W=50 | Mẫu kinh điển 3 vật | 220 (vét cạn) | Tham lam 160; QHĐ 220; Quay lui 220 | 0.31 | ✔ | tham lam thiếu 60 |
| m3-T03 | Thông thường | 10 yêu cầu, W=30 | 10 yêu cầu ngẫu nhiên | 263 (vét cạn) | Tham lam 263; QHĐ 263; Quay lui 263 | 0.69 | ✔ |  |
| m3-T04 | Thông thường | 14 yêu cầu, W=40 | 14 yêu cầu ngẫu nhiên | 516 (vét cạn) | Tham lam 516; QHĐ 516; Quay lui 516 | 2.53 | ✔ |  |
| m3-X01 | Không hợp lệ | 0 yêu cầu, W=10 | Không có yêu cầu | HTTP 422 | — | 0 | ✔ | bị từ chối: Cần 1–25 yêu cầu. |
| m3-X02 | Không hợp lệ | 26 yêu cầu, W=10 | 26 yêu cầu (vượt giới hạn 25) | HTTP 422 | — | 0 | ✔ | bị từ chối: Cần 1–25 yêu cầu. |
| m3-X03 | Không hợp lệ | 1 yêu cầu, W=-1 | Quỹ âm | HTTP 422 | — | 0 | ✔ | bị từ chối: Quỹ giờ công từ 0 đến 200 và (số yêu cầu × quỹ) tối đa khoảng 4000 ô. |
| m3-X04 | Không hợp lệ | 1 yêu cầu, W=201 | Quỹ 201 (vượt 200) | HTTP 422 | — | 0 | ✔ | bị từ chối: Quỹ giờ công từ 0 đến 200 và (số yêu cầu × quỹ) tối đa khoảng 4000 ô. |
| m3-X05 | Không hợp lệ | 20 yêu cầu, W=200 | Vượt 4000 ô DP | HTTP 422 | — | 0 | ✔ | bị từ chối: Quỹ giờ công từ 0 đến 200 và (số yêu cầu × quỹ) tối đa khoảng 4000 ô. |
| m3-X06 | Không hợp lệ | 1 yêu cầu, W=10 | Số giờ bằng 0 | HTTP 422 | — | 0 | ✔ | bị từ chối: Y1: số giờ phải là số nguyên ≥ 1 và giá trị ≥ 0. |
| m3-X07 | Không hợp lệ | 1 yêu cầu, W=10 | Số giờ không nguyên | HTTP 422 | — | 0 | ✔ | bị từ chối: [{'type': 'int_from_float', 'loc': ['body', 'items', 0, 'w'], 'msg': 'Input should be a va |
| m3-X08 | Không hợp lệ | 1 yêu cầu, W=10 | Giá trị âm | HTTP 422 | — | 0 | ✔ | bị từ chối: Y1: số giờ phải là số nguyên ≥ 1 và giá trị ≥ 0. |

## Xếp container (bin packing)

| Nhóm | Số testcase | Đạt |
|---|---|---|
| Thông thường | 3 | 3 |
| Dữ liệu nhỏ | 3 | 3 |
| Biên | 5 | 5 |
| Đặc biệt | 4 | 4 |
| Dữ liệu lớn | 4 | 4 |
| Không hợp lệ | 8 | 8 |

| ID | Nhóm | Cỡ | Tiêu đề | Tối ưu tham chiếu | Kết quả từng thuật toán | Thời gian lớn nhất (ms) | Đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| m4-B01 | Biên | 4 lô, C=10 | Mọi lô đúng bằng tải trọng | 4 (vét cạn) | FF 4; FFD 4; BFD 4; Quay lui 4 | 0.92 | ✔ |  |
| m4-B02 | Biên | 6 lô, C=10 | Hai lô cộng đúng bằng tải trọng | 3 (vét cạn) | FF 3; FFD 3; BFD 3; Quay lui 3 | 0.07 | ✔ |  |
| m4-B03 | Biên | 9 lô, C=10 | Mọi lô rất nhỏ | 1 (vét cạn) | FF 1; FFD 1; BFD 1; Quay lui 1 | 0.05 | ✔ |  |
| m4-B04 | Biên | 3 lô, C=0.6 | Số thập phân gây sai số (0,1 + 0,2 + 0,3) | 1 (vét cạn) | FF 1; FFD 1; BFD 1; Quay lui 1 | 0.05 | ✔ |  |
| m4-B05 | Biên | 8 lô, C=1 | Khối lượng bằng 0,01 (rất nhỏ) | 1 (vét cạn) | FF 1; FFD 1; BFD 1; Quay lui 1 | 0.1 | ✔ |  |
| m4-D01 | Đặc biệt | 8 lô, C=10 | Bẫy First-Fit | 4 (vét cạn) | FF 5; FFD 4; BFD 4; Quay lui 4 | 0.08 | ✔ |  |
| m4-D02 | Đặc biệt | 8 lô, C=12 | Lô nhỏ xen kẽ, tổng khít tải trọng | 3 (vét cạn) | FF 3; FFD 3; BFD 3; Quay lui 3 | 0.06 | ✔ |  |
| m4-D03 | Đặc biệt | 9 lô, C=12 | Nhiều lô cùng khối lượng | 5 (vét cạn) | FF 5; FFD 5; BFD 5; Quay lui 5 | 0.61 | ✔ |  |
| m4-D04 | Đặc biệt | 8 lô, C=10 | Hai nhóm kích thước | 4 (vét cạn) | FF 4; FFD 4; BFD 4; Quay lui 4 | 0.07 | ✔ |  |
| m4-L01 | Dữ liệu lớn | 18 lô, C=30 | 18 lô dựng sẵn (tối ưu = 6) | 6 (dựng sẵn) | FF 7; FFD 7; BFD 7; Quay lui 6 | 37.7 | ✔ |  |
| m4-L02 | Dữ liệu lớn | 60 lô, C=100 | 60 lô dựng sẵn (tối ưu = 15) | 15 (dựng sẵn) | FF 16; FFD 16; BFD 16; Quay lui 16 | 1500.09 | ✔ | BT chạm giới hạn thời gian, hơn tối ưu 1 thùng |
| m4-L03 | Dữ liệu lớn | 60 lô, C=100 | 60 lô ngẫu nhiên | — | FF 20; FFD 19; BFD 19; Quay lui 19 | 2.04 | ✔ |  |
| m4-L04 | Dữ liệu lớn | 40 lô, C=100 | 40 lô, mỗi lô > C/3 | — | FF 25; FFD 23; BFD 23; Quay lui 23 | 1500.07 | ✔ | BT chạm giới hạn thời gian (không có đáp án tham chiếu) |
| m4-N01 | Dữ liệu nhỏ | 1 lô, C=10 | 1 lô | 1 (vét cạn) | FF 1; FFD 1; BFD 1; Quay lui 1 | 0.03 | ✔ |  |
| m4-N02 | Dữ liệu nhỏ | 2 lô, C=10 | 2 lô vừa một thùng | 1 (vét cạn) | FF 1; FFD 1; BFD 1; Quay lui 1 | 0.03 | ✔ |  |
| m4-N03 | Dữ liệu nhỏ | 3 lô, C=10 | 3 lô, mỗi lô hơn nửa thùng | 3 (vét cạn) | FF 3; FFD 3; BFD 3; Quay lui 3 | 0.04 | ✔ |  |
| m4-T01 | Thông thường | 8 lô, C=30 | Mẫu chính (8 lô, tải 30) | 3 (vét cạn) | FF 3; FFD 3; BFD 3; Quay lui 3 | 0.09 | ✔ |  |
| m4-T02 | Thông thường | 8 lô, C=25 | 8 lô ngẫu nhiên | 3 (vét cạn) | FF 3; FFD 3; BFD 3; Quay lui 3 | 0.07 | ✔ |  |
| m4-T03 | Thông thường | 10 lô, C=30 | 10 lô ngẫu nhiên | 6 (vét cạn) | FF 6; FFD 6; BFD 6; Quay lui 6 | 1.71 | ✔ |  |
| m4-X01 | Không hợp lệ | 0 lô, C=10 | Không có lô | HTTP 422 | — | 0 | ✔ | bị từ chối: Cần 1–60 lô container. |
| m4-X02 | Không hợp lệ | 61 lô, C=10 | 61 lô (vượt giới hạn 60) | HTTP 422 | — | 0 | ✔ | bị từ chối: Cần 1–60 lô container. |
| m4-X03 | Không hợp lệ | 1 lô, C=0 | Tải trọng bằng 0 | HTTP 422 | — | 0 | ✔ | bị từ chối: Tải trọng phải dương. |
| m4-X04 | Không hợp lệ | 1 lô, C=-5 | Tải trọng âm | HTTP 422 | — | 0 | ✔ | bị từ chối: Tải trọng phải dương. |
| m4-X05 | Không hợp lệ | 1 lô, C=10 | Lô nặng hơn tải trọng | HTTP 422 | — | 0 | ✔ | bị từ chối: C1: khối lượng phải trong (0, 10.0]. |
| m4-X06 | Không hợp lệ | 1 lô, C=10 | Khối lượng bằng 0 | HTTP 422 | — | 0 | ✔ | bị từ chối: C1: khối lượng phải trong (0, 10.0]. |
| m4-X07 | Không hợp lệ | 1 lô, C=10 | Khối lượng âm | HTTP 422 | — | 0 | ✔ | bị từ chối: C1: khối lượng phải trong (0, 10.0]. |
| m4-X08 | Không hợp lệ | 1 lô, C=10 | Khối lượng là chữ | HTTP 422 | — | 0 | ✔ | bị từ chối: [{'type': 'float_parsing', 'loc': ['body', 'items', 0, 'w'], 'msg': 'Input should be a val |
