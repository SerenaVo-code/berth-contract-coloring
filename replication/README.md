# Thí nghiệm dựng lại dự án (replication)

**Đây là một thí nghiệm làm sau khi dự án gốc đã xong, không phải lịch sử thật của dự án gốc.** Toàn bộ mã trong `app/` được Claude viết lại từ đầu theo đặc tả trong `spec/` (quy trình kiểu Spec Kit: hiến pháp → đặc tả → kế hoạch → cài đặt → đối chiếu). Không có lượt thoại nào của sinh viên được ghi ở đây: các quyết định thiết kế và thông số do Claude đưa ra, chờ Tuyền duyệt.

Mục đích: kiểm tra xem đặc tả và bộ testcase có đủ chặt để dựng lại một hệ thống cho kết quả tương đương bản gốc hay không.

| Thư mục | Nội dung |
|---|---|
| `spec/` | hiến pháp và đặc tả |
| `app/` | bản dựng lại: backend, giao diện React, testcase, kiểm thử |
| `LOG.md` | nhật ký kỹ thuật: đã làm gì, lỗi thật gặp phải, số đo thật |
| `app/CROSS_CHECK.md` | đối chiếu hai chiều với bản gốc, sinh bởi `app/tools/cross_check.py` |

Chạy: `cd app && npm run setup && npm run dev` (giao diện :5173); kiểm thử: `npm test`; testcase: `npm run testcases`.
