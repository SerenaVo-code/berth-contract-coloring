# Hiến pháp dự án (constitution)

Bảy nguyên tắc này áp dụng cho mọi vòng sau. Nếu một vòng vi phạm, phải sửa hoặc ghi rõ ngoại lệ.

1. **Đúng trước, đẹp sau.** Mọi kết quả của thuật toán đều được một hàm kiểm tra độc lập tính lại (chi phí, tính hợp lệ). Không tin số mà chính thuật toán tự báo.
2. **Một hợp đồng bước duy nhất.** Mỗi thuật toán trả về danh sách bước theo cùng một cấu trúc. Giao diện chỉ phát lại các bước, không tự chạy lại thuật toán.
3. **Kiểm thử chỉ nhắm vào hàm thuật toán.** Không có nhóm "dữ liệu không hợp lệ" hay kiểm thử API trong bộ testcase. Đáp án tham chiếu đến từ vét cạn, công thức hoặc instance dựng sẵn, không lấy từ chính solver.
4. **Giới hạn phải trung thực và xác định.** Thuật toán quay lui dừng theo số nút duyệt, không theo đồng hồ, để cùng một đầu vào luôn ra cùng một kết quả. Khi bị cắt, giao diện ghi "chưa chắc tối ưu".
5. **Thuật ngữ dễ hiểu.** Giao diện dùng "phương án tốt nhất hiện có", "bỏ nhánh", không dùng "kỷ lục", "cắt tỉa". Thuật ngữ khác phải có chú thích trong ngoặc.
6. **Không tự chạy gì.** Môi trường không có script tự khởi động. Chỉ có lệnh `npm run ...` do người dùng gõ.
7. **Nguồn rõ ràng.** Mọi thuật toán lấy từ tài liệu phải có số tham chiếu trong docstring. Phần tự thiết kế phải được ghi là tự thiết kế.
