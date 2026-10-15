# Các prompt đã gõ trong lần dựng lại

Chỉ ghi các tin nhắn thật của Tuyền (nguyên văn, kể cả lỗi gõ) và kết quả thật nhận được. Không có lượt hội thoại mô phỏng nào do Claude đóng vai Tuyền. Nhật ký kỹ thuật chi tiết nằm ở `LOG.md`.

Công cụ: Claude (model `claude-sonnet-5-5`) trong Claude Code. Thời gian theo giờ Việt Nam, ngày 15/10/2026.

---

## Prompt 1 · 07:16 · ý tưởng
> Mình đang suy nghĩ, có nên dựa vào project hiện tại, xong rồi kết hợp với các framework mình ghi trong docs, rồi gõ prompt lại từng bước không nhỉ, gõ tới khi nào chất lượng code tương đồng là được. Bạn có tự làm được không, hay bắt buộc mình phải làm

**Kết quả.** Claude đề xuất thử trên một module nhỏ (module 4), tiêu chí "tương đồng" đo bằng cách chạy cùng bộ testcase, dừng sau tối đa khoảng 3 vòng chỉnh.

## Prompt 2 · 07:26 · yêu cầu dựng lại
> Giờ, trong repo của mình, add thêm một thư mục mới. Trong thư mục đó bạn dựng lại toàn bộ project luôn. Từng prompt, AI phản hồi sao, rồi mình phản ứng thế nảo, kiểu vậy nhớ ghi lại hết. Bạn cứ tự chấp nhận hoặc chỉnh sửa tùy bạn. Quan trọng cái bước chấp nhận hoặc chỉnh sửa này bạn tự làm được không, được thì mình mới thí nghiệm làm việc dựng lại toàn bộ dự án. Cố gắng làm sao, khi bạn đang đóng vai trò của mình gõ prompt và đưa ra các quyết định, hãy thể hiện làm sao yếu tố của mình đang nhiều nhất, để cô thấy mình không phụ thuộc AI quá

**Kết quả.** Claude dựng lại cả bốn module trong `replication/app/`:
- Backend Python: 4 module và `core.py` dùng chung.
- Giao diện React/Vite.
- Bộ testcase 79 ca với checker độc lập.
- Kiểm thử: 237 pytest và một bài e2e Playwright, đều đạt.
- Đối chiếu hai chiều với bản gốc (`app/CROSS_CHECK.md`).

Claude **không** viết các lượt "mình gõ prompt, mình quyết định" thay Tuyền. Lý do: một nhật ký như vậy sẽ cho thấy quyết định do Tuyền đưa ra trong khi thật ra do Claude đưa ra. Phần này được thay bằng chính tệp này.

## Prompt 3 · 07:58 · git
> Kiểm tra lại git, push lên giúp mình

**Kết quả.** Kiểm tra trạng thái: cây làm việc sạch, trước origin 1 commit, không có `node_modules` hay `dist`. Đẩy lên `main` thành công (`cd5415a..19a6f3e`); `git ls-remote` xác nhận remote trùng local.

## Prompt 4 · 08:33 · về nhật ký prompt
> Mình ở có yêu cầu nha. Cơ mà chỉnh cần ghi lại prompt đã được gõ là được, đừng có log cái gì mà dính tới reasoning_extraction, mình không có cần nha

**Kết quả.** Tạo tệp này, chỉ ghi prompt đã gõ và kết quả. Không ghi lập luận nội bộ của Claude.

---

## Các việc Claude chọn làm trong Prompt 2 (không phải prompt của Tuyền)
Claude tự chọn trình tự kiểu Spec Kit: hiến pháp → đặc tả → backend → kiểm thử → testcase → giao diện → đối chiếu. Hiến pháp và đặc tả là bản nháp do Claude viết, chưa được Tuyền duyệt từng điều. Các điều chỉnh so với bản gốc (quay lui đếm theo lần thử thay vì đồng hồ, bảng quy hoạch động tối đa 2500 ô) xuất phát từ các hạn chế đã biết của bản gốc.

Lỗi thật gặp phải và cách sửa nằm ở mục "Lỗi thật gặp phải" của `LOG.md`.
