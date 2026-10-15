// Độ phức tạp, giải thích thuật ngữ và mã giả của từng thuật toán (hiện trên giao diện).
// n = số phần tử, k = số hợp đồng/tàu, m = số đội, d = số xung đột trung bình, E = số cạnh xung đột, W = quỹ giờ.

export const CX = {
  berth: { greedy: 'O(n log n + n·k + E)', greedy_cost: 'O(n log n + n·k + E)', dsatur: 'O(n·(n + E))', bt: 'O(kⁿ) xấu nhất, bỏ nhánh giúp giảm nhiều' },
  assign: { greedy: 'O(n log n + n·m·d)', greedy_hard: 'O(n log n + n·m·d)', bt: 'O(mⁿ) xấu nhất; kiểm tra Hall: O(n·(n+m)·m) mỗi mốc giờ' },
  knap: { greedy: 'O(n log n)', dp: 'O(n·W) thời gian và bộ nhớ', bt: 'O(2ⁿ) xấu nhất' },
  bins: { ff: 'O(n²) cài thô, O(n log n) với cây', ffd: 'O(n log n + n²)', bfd: 'O(n²)', bt: 'O(nⁿ) xấu nhất' },
}

export const GLOSS = [
  ['Phương án tốt nhất hiện có', 'Lời giải rẻ nhất (hoặc nhiều giá trị nhất) mà thuật toán đã tìm được tới lúc này. Một nhánh chỉ được nhận nếu hơn nó. Trong tài liệu thường gọi là "kỷ lục".'],
  ['Bỏ nhánh', 'Dừng không duyệt tiếp một hướng vì chắc chắn nó không thể hơn phương án tốt nhất hiện có. Trong tài liệu thường gọi là "cắt tỉa".'],
  ['Cận dưới / cận trên', 'Con số mà lời giải tối ưu chắc chắn không thể vượt qua (không thể rẻ hơn cận dưới, không thể giá trị hơn cận trên). Dùng để biết một kết quả đã tối ưu chưa và để bỏ nhánh.'],
  ['Quay lui', 'Thử từng lựa chọn cho phần tử hiện tại; đi tiếp được thì đi, gặp ngõ cụt thì lùi lại và thử lựa chọn khác.'],
  ['Tham lam', 'Mỗi bước chọn cái tốt nhất ngay lúc đó và không bao giờ đổi lại. Nhanh nhưng có thể không tối ưu.'],
  ['DSATUR', 'Cách tô màu đồ thị: luôn xử lý trước đỉnh đang bị nhiều màu khác nhau chặn nhất (Brélaz, 1979).'],
  ['ω (omega)', 'Số tàu neo cùng một lúc nhiều nhất. Với đồ thị khoảng, cần ít nhất ω hợp đồng.'],
  ['Hall / khớp hai phía', 'Kiểm tra điều kiện cần cho module 2: tại một thời điểm, các tàu đang neo phải xếp được vào các đội khác nhau đủ kỹ năng. Không qua thì chắc chắn vô nghiệm.'],
  ['Quy hoạch động', 'Chia bài toán thành các bài con nhỏ hơn, lưu lời giải mỗi bài con vào một bảng để không tính lại.'],
  ['First-Fit / Best-Fit', 'Xếp lô vào tàu đầu tiên còn đủ chỗ (First-Fit) hoặc vào tàu vừa khít nhất (Best-Fit). "Giảm dần" nghĩa là xếp lô nặng trước.'],
]

const BEST = 'best ← kết quả tham lam tốt nhất'

// lines: các dòng mã giả; map: loại bước -> chỉ số dòng được tô sáng
export const PSEUDO = {
  berth: {
    greedy: { lines: ['sắp tàu theo giờ đến', 'với mỗi tàu v theo thứ tự:', '    bỏ các hợp đồng có tàu xung đột với v', '    cho v vào hợp đồng nhỏ nhất còn lại (hết thì mở mới)', 'trả về phân bổ và tổng chi phí'], map: { info: 0, assign: 3, done: 4 } },
    greedy_cost: { lines: ['sắp tàu theo giờ đến', 'với mỗi tàu v theo thứ tự:', '    bỏ các hợp đồng có tàu xung đột với v', '    cho v vào hợp đồng làm tổng tiền tăng ít nhất', '        (mở hợp đồng mới tốn F + r·thời gian cập)', 'trả về phân bổ và tổng chi phí'], map: { info: 0, assign: 3, done: 5 } },
    dsatur: { lines: ['lặp n lần:', '    chọn tàu chưa xếp bị chặn bởi nhiều hợp đồng khác nhau nhất', '        (hòa: nhiều xung đột hơn, rồi tàu đứng trước)', '    cho tàu đó vào hợp đồng nhỏ nhất còn hợp lệ', 'trả về phân bổ và tổng chi phí'], map: { info: 0, assign: 3, done: 4 } },
    bt: { lines: [BEST, 'thử(i):', '    nếu i = n: nếu tổng < best thì best ← tổng', '    với mỗi hợp đồng k hợp lệ cho tàu i (rẻ trước, rồi mở mới):', '        gán tàu i vào k', '        nếu tổng tạm + F·(ω − số hợp đồng) ≥ best: bỏ nhánh', '        ngược lại: thử(i + 1)', '        bỏ gán tàu i'], map: { info: 0, found: 2, assign: 6, prune: 5, back: 7, done: 0 } },
  },
  assign: {
    greedy: { lines: ['sắp tàu theo giờ đến', 'với mỗi tàu v:', '    lọc đội đủ kỹ năng và không trùng giờ / không bị cấm', '    nếu không còn đội nào: kẹt, dừng', '    giao v cho đội làm chi phí tăng ít nhất', 'trả về phân công'], map: { info: 0, dead: 3, assign: 4, done: 5 } },
    greedy_hard: { lines: ['sắp tàu theo số đội đủ kỹ năng tăng dần', 'với mỗi tàu v:', '    lọc đội đủ kỹ năng và không trùng giờ / không bị cấm', '    nếu không còn đội nào: kẹt, dừng', '    giao v cho đội làm chi phí tăng ít nhất', 'trả về phân công'], map: { info: 0, dead: 3, assign: 4, done: 5 } },
    bt: { lines: ['nếu có thời điểm mà tàu đang neo không khớp được với đội khác nhau: vô nghiệm', 'thử(i):', '    nếu i = n: ghi nhận nếu rẻ hơn best', '    với mỗi đội hợp lệ cho tàu i (rẻ trước):', '        giao tàu i cho đội', '        nếu tổng tạm + chi phí rẻ nhất của các tàu còn lại ≥ best: bỏ nhánh', '        ngược lại: thử(i + 1)', '    không đội nào: ngõ cụt, quay lui'], map: { info: 0, dead: 7, found: 2, assign: 6, prune: 5, done: 0 } },
  },
  knap: {
    greedy: { lines: ['sắp yêu cầu theo giá trị/giờ giảm dần', 'với mỗi yêu cầu:', '    nếu còn đủ giờ: nhận', '    ngược lại: bỏ qua', 'trả về tập đã nhận'], map: { info: 0, assign: 2, skip: 3, done: 4 } },
    dp: { lines: ['f[0][j] = 0 với mọi j', 'với i = 1..n, j = 0..W:', '    f[i][j] = max(f[i-1][j], f[i-1][j-wᵢ] + vᵢ)', 'truy vết từ f[n][W]:', '    f[i][j] ≠ f[i-1][j] thì nhận yêu cầu i, j ← j − wᵢ'], map: { info: 0, cell: 2, trace: 4, done: 4 } },
    bt: { lines: ['best ← giá trị của tham lam', 'thử(i):', '    nếu giá trị hiện tại > best thì best ← giá trị hiện tại', '    nếu cận trên (nhận tiếp theo tỉ lệ) ≤ best: bỏ nhánh', '    nếu còn đủ giờ: nhận yêu cầu i, thử(i + 1), rồi bỏ nhận', '    không nhận yêu cầu i, thử(i + 1)'], map: { info: 0, found: 2, prune: 3, assign: 4, back: 5, done: 0 } },
  },
  bins: {
    ff: { lines: ['với mỗi lô theo thứ tự nhập:', '    xếp vào tàu đầu tiên còn đủ chỗ', '    không có thì mở tàu mới', 'trả về số tàu'], map: { info: 0, assign: 1, done: 3 } },
    ffd: { lines: ['sắp lô theo khối lượng giảm dần', 'với mỗi lô:', '    xếp vào tàu đầu tiên còn đủ chỗ (không có thì mở tàu mới)', 'trả về số tàu'], map: { info: 0, assign: 2, done: 3 } },
    bfd: { lines: ['sắp lô theo khối lượng giảm dần', 'với mỗi lô:', '    xếp vào tàu vừa khít nhất (còn trống ít nhất nhưng đủ chỗ)', '    không có thì mở tàu mới', 'trả về số tàu'], map: { info: 0, assign: 2, done: 4 } },
    bt: { lines: ['best ← kết quả First-Fit giảm dần tốt nhất', 'thử(i): (lô nặng trước)', '    nếu i = n: ghi nhận nếu ít tàu hơn best', '    với mỗi tàu đang mở đủ chỗ (bỏ qua tàu có cùng mức tải đã thử) và tàu mới:', '        xếp lô i vào đó', '        nếu cận (số tàu + ⌈phần chưa xếp còn thiếu / C⌉) ≥ best: bỏ nhánh', '        ngược lại: thử(i + 1)'], map: { info: 0, found: 2, assign: 6, prune: 5, done: 0 } },
  },
}
