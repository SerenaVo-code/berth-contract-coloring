# Kịch bản prompt đề xuất để chạy lại (do Claude soạn thay Tuyền)

**Đây là kịch bản đề xuất, chưa phải prompt thật Tuyền đã gõ.** Claude soạn các lượt "người dùng" và các quyết định đi kèm theo yêu cầu của Tuyền (15/10, 08:39), để sau này Tuyền dùng làm đầu vào chạy lại thí nghiệm. Các prompt thật nằm ở `PROMPTS.md`.

Quy ước nguồn của từng quyết định:
- 🟢 **Gốc**: Tuyền đã thật sự quyết định như vậy khi xây bản gốc.
- 🔵 **Đề xuất**: Claude đề xuất, Tuyền chưa xác nhận. Khi chạy lại, Tuyền duyệt hoặc đổi.

Mỗi vòng có: prompt (tiếng Anh), kết quả khi chạy lần này (số thật, đo ngày 15/10/2026), quyết định, cách kiểm.

---

## Vòng 0 · Hiến pháp
**Prompt**
> Create a project constitution for a CS112 demo app. Principles: results are verified by an independent checker; every algorithm emits steps through one shared contract and the UI only replays them; tests target the algorithm functions only (no API or invalid-input groups), with reference answers that do not come from the solver; limits are honest and deterministic; plain-language Vietnamese terms; no auto-run scripts; sources cited.

**Kết quả lần này:** `spec/constitution.md`, 7 nguyên tắc.
**Quyết định:** 🟢 phạm vi testcase chỉ nhắm vào hàm thuật toán (Tuyền đã chốt ở bản gốc); 🟢 không có script tự chạy, chỉ `npm run`; 🟢 thuật ngữ dễ hiểu ("phương án tốt nhất hiện có", "bỏ nhánh"); 🔵 quay lui giới hạn theo số lần thử, không theo đồng hồ.
**Kiểm:** đọc từng nguyên tắc, mỗi nguyên tắc phải kiểm được bằng một lệnh hoặc một bài test.

## Vòng 1 · Đặc tả
**Prompt**
> Specify a demo for a shipping line (the shipowner's view, linked to ONE's industry context). Module 1: lease berth contracts for n ships with arrival/departure times; each contract costs F + r × (last departure − first arrival) including idle time; two ships overlapping in time or in a forbidden pair cannot share a contract; minimise total cost. Add three related port problems: assigning skilled service teams to ship calls, choosing overtime requests within a labour-hour budget (0/1 knapsack), and loading container lots onto ships (bin packing). Each module compares several algorithms step by step.

**Kết quả lần này:** `spec/spec.md` với 4 module, hợp đồng bước chung, 5 tiêu chí chấp nhận.
**Quyết định:** 🟢 góc nhìn chủ tàu thuê bến, mô hình chi phí F + r × khoảng thời gian; 🟢 thêm nhân viên phục vụ tàu và các bài toán quanh cảng; 🔵 giới hạn kích thước từng module.
**Kiểm:** mỗi module có Input, Output, ràng buộc, thuật toán, cận dưới.

## Vòng 2 · Làm rõ
**Prompt**
> List the ambiguities in the spec that would change the implementation, with your recommended answer for each. Do not start coding.

**Kết quả lần này:** các điểm cần chốt và câu trả lời đã dùng khi chạy:
1. Chi phí tính cả giờ trống? → có. 🟢
2. Hai tàu chạm đầu mút (rời = đến) có xung đột? → không. 🔵
3. Quay lui dừng theo gì? → số lần thử (60 nghìn đơn vị), không theo đồng hồ. 🔵
4. Bảng quy hoạch động tối đa bao nhiêu ô? → 2500, để mỗi ô là một bước. 🔵
5. Bài vô nghiệm ở module 2 xử lý ra sao? → kiểm tra điều kiện cần bằng khớp hai phía trước khi duyệt. 🔵
**Kiểm:** mỗi câu trả lời đi vào `spec.md` hoặc `constitution.md`.

## Vòng 3 · Kế hoạch
**Prompt**
> Plan the architecture: FastAPI backend with one POST endpoint per module that runs every algorithm and returns all steps; React + Vite frontend that replays steps from memory and never recomputes; Magenta Design System look. Environment is a Codespace; only `npm run setup`, `npm run dev`, `npm test`.

**Kết quả lần này:** `core.py` (ghi bước, ngân sách), `berth.py`, `assign.py`, `knapsack.py`, `binpack.py`, `server.py`; frontend React. 
**Quyết định:** 🟢 FastAPI, giao diện chỉ phát lại bước; 🟢 Magenta Design System; 🟢 Codespaces, không tự chạy gì.
**Kiểm:** `npm run dev` mở được cổng 5173, bốn tab hiện ra.

## Vòng 4 · Danh sách việc
**Prompt**
> Break the plan into small tasks in dependency order, each with a verification command.

**Kết quả lần này:** thứ tự đã làm: lõi và module 1 → module 2 → 3 → 4 → server → kiểm thử → testcase → giao diện → đối chiếu.

## Vòng 5 · Module 1 (thuê bến)
**Prompt**
> Implement module 1: greedy by arrival, greedy by cheapest contract, DSATUR, and backtracking with pruning that starts from the best greedy result. Every algorithm returns steps (kind, message, assignment snapshot, cost, candidate table with the reason each option is rejected). Lower bound = ω·F + r·Σ(departure − arrival). Add tests against brute force on random small inputs.

**Kết quả lần này:** ví dụ 8 tàu, F = 500, r = 40: tham lam 3400, tham lam chọn hợp đồng rẻ 3340, DSATUR 3000, quay lui 2900 (tối ưu), cận dưới 2800.
**Quyết định:** 🟢 so sánh bốn thuật toán trên cùng ví dụ; 🔵 bỏ bước "quay lui" thừa ngay sau bước "bỏ nhánh".
**Kiểm:** `python -m pytest tests/test_algorithms.py -k berth`; số tự báo phải bằng số tính lại.

## Vòng 6 · Module 2 (phân công đội)
**Prompt**
> Implement module 2: assign a team with all required skills to each ship call; overlapping or forbidden pairs cannot share a team; minimise Σ rate × duration. Algorithms: greedy by arrival, greedy hardest-first, backtracking with a remaining-cost bound. If no solution exists, prove it with a bipartite matching check at every time point instead of searching.

**Kết quả lần này:** thêm kiểm tra Hall (khớp hai phía). Lần chạy đầu 24 test hỏng vì `Timer.ms` chưa có khi `return` giữa khối `with`; đã sửa.
**Quyết định:** 🟢 "VÔ NGHIỆM" phải hiện rõ trên giao diện (Tuyền yêu cầu ở bản gốc sau khi thấy quay lui không chứng minh được); 🔵 khi tham lam kẹt chỉ ghi "chưa chứng minh vô nghiệm".
**Kiểm:** test so với vét cạn gồm cả ca vô nghiệm.

## Vòng 7 · Module 3 (quỹ giờ công)
**Prompt**
> Implement module 3 as 0/1 knapsack: greedy by value/hour (to show it can be wrong), DP with one step per table cell and a traceback, and backtracking with a fractional upper bound.

**Kết quả lần này:** ví dụ kinh điển (10h/60, 20h/100, 30h/120, quỹ 50h): tham lam 160, DP và quay lui 220.
**Kiểm:** DP đúng bằng vét cạn và bằng một DP một chiều viết riêng.

## Vòng 8 · Module 4 (xếp container)
**Prompt**
> Implement module 4 as bin packing: First-Fit, First-Fit Decreasing, Best-Fit Decreasing, and backtracking that skips bins with equal load and prunes with the lower bound ⌈Σw/C⌉.

**Kết quả lần này:** có ca First-Fit giảm dần không tối ưu (4 tàu so với tối ưu 3), quay lui sửa được.
**Kiểm:** so với vét cạn trên dữ liệu nhỏ.

## Vòng 9 · Giao diện
**Prompt**
> Build the React UI: one tab per module, a data editor, sample data taken from the testcases, JSON import/export in the testcase format, algorithm picker, Prev/Next/Auto/slider, the step message, KPIs including "best so far", a candidate table, and a comparison table. Module 1 also gets a Gantt chart and a conflict graph; module 3 shows the DP table; module 4 shows bins as columns.

**Kết quả lần này:** e2e Playwright chạy được bốn module. Hai lỗi giao diện tìm ra khi kiểm: sập khi xóa tên tàu (kết quả cũ còn, dữ liệu mới là null); chỉ số bước vượt số bước khi đổi thuật toán.
**Quyết định:** 🟢 thanh bước phải thể hiện rõ từng bước của thuật toán (Tuyền không hài lòng với bản đầu của bản gốc về điểm này); 🟢 thuật ngữ khó có chú thích; 🔵 thêm nhập/xuất JSON.
**Kiểm:** `python tests/e2e.py` và xem ảnh chụp.

## Vòng 10 · Bộ testcase
**Prompt**
> Generate a deterministic testcase suite: five groups per module (typical, small, boundary, special, large). Reference answers must come from brute force, closed formulas or constructed instances, never from the solver. A separate checker recomputes every algorithm's result. The runner calls the solver functions directly and writes RESULTS.md. Test descriptions must match what actually happens.

**Kết quả lần này:** 79 ca, đạt 79/79. Hai vấn đề tìm ra: mô tả vài ca không khớp kết quả thật (First-Fit "kém hơn" nhưng bằng nhau), sửa bằng cách tìm instance thật; và module 1 với 200 tàu chạy 17 giây, sửa bằng cách đếm ngân sách theo lần thử.
**Quyết định:** 🟢 không có nhóm dữ liệu không hợp lệ; 🟢 mô tả phải khớp kết quả đo thật.
**Kiểm:** `npm run testcases`.

## Vòng 11 · Đối chiếu (converge)
**Prompt**
> Cross-check against the original implementation in both directions: run the original testcases on the rebuilt solvers and the rebuilt testcases on the original solvers. Report differences and fix real regressions.

**Kết quả lần này:** testcase của bản gốc chạy trên solver dựng lại: 88/88. Testcase dựng lại chạy trên solver gốc: 78/79 cho cùng kết quả tốt nhất. Ban đầu bản dựng lại kém ở 3 ca lớn; sau khi chỉnh ngân sách module 4 và thứ tự duyệt module 2, chỉ còn `m2-L02` lệch (dựng lại 2467,5; bản gốc 2471,5).
**Kiểm:** `app/CROSS_CHECK.md`.

---

## Cách dùng khi chạy lại
1. Mở phiên mới, thư mục trống, gõ lần lượt các prompt ở trên.
2. Sau mỗi vòng, chạy lệnh ở mục "Kiểm". Nếu không đạt thì sửa prompt hoặc ghi lại phản hồi thật của bạn.
3. Ghi vào `PROMPTS.md` đúng những gì bạn đã gõ và nhận được. Quyết định 🔵 chỉ thành quyết định của bạn khi bạn duyệt.
