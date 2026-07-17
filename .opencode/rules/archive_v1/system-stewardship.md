---
trigger: model_decision
description: "Core Rule: System Stewardship & Architectural Review Board (ARB) - Trước khi đưa ra bất cứ đề xuất THÊM MỚI nào (Cài package mới, tạo file cấu trúc mới, đẻ thêm module..."
---
# Core Rule: System Stewardship & Architectural Review Board (ARB)

**TÔN CHỈ**: Không thêm tính năng, thư viện, hoặc layer mới nếu chưa vượt qua sự kiểm duyệt khắt khe. Refactor luôn được ưu tiên hơn Expand.

## 1. Inventory First (Kiểm Kê Trước Khi Mở Rộng)
Trước khi đưa ra bất cứ đề xuất THÊM MỚI nào (Cài package mới, tạo file cấu trúc mới, đẻ thêm module):
- **BẮT BUỘC** kiểm kê hệ thống hiện tại.
- Có thứ gì đang làm nhiệm vụ tương đương không?
- Nếu có, tại sao nó không giải quyết được bài toán? Có thể tối ưu nó thay vì đẻ thêm cái mới không?

## 2. The 5 Justification Questions (5 Câu Hỏi Biện Minh)
Để được cấp phép THÊM MỚI, AI phải chứng minh được:
1. Vấn đề hiện tại là gì? (Phải có bằng chứng/Log).
2. Hệ thống cũ thực sự bất lực?
3. Giải pháp mới đưa vào có gây Overengineering (Phức tạp hóa vấn đề) không?
4. Chi phí bảo trì (Maintenance Cost) dài hạn là gì?
5. Lợi ích có lớn hơn đáng kể so với chi phí không? (Nếu chỉ ngang bằng -> BÁC BỎ).

## 3. Complexity Budget (Ngân Sách Phức Tạp)
- Hệ thống có giới hạn chịu đựng sự phức tạp. Thêm dependency là tạo thêm nợ kỹ thuật.
- **Quy tắc**: Vanilla/Standard Library > 3rd Party Library. Đơn giản > Thông minh.

## 4. System Health & Self-Evolution Loop
- Thay vì thêm tính năng khi gặp lỗi, AI phải: Quan sát -> Đo lường -> Tinh chỉnh cái cũ.
- Định kỳ tự review: Cái nào không dùng -> Đề xuất Xóa. Cái nào lặp lại -> Đề xuất Gộp (Merge).

**LUẬT VÀNG:** Mọi thứ mới phải chứng minh được giá trị. Mọi thứ cũ phải chứng minh được lý do tồn tại. Không chứng minh được -> Không thay đổi hoặc Xóa bỏ.


