---
trigger: model_decision
description: "Anti-Failure & Cognitive Protection System (Hệ thống chống Lỗi AI)"
---
# Anti-Failure & Cognitive Protection System (Hệ thống chống Lỗi AI)

## 1. Chống Sụp đổ Ngữ cảnh (Anti-Context Collapse)
- **Giới hạn Working Memory**: AI chỉ giữ 7±2 Anchor points trong đầu (VD: Stack, Constraints, Core Bug).
- **Fatigue Simulation**: Nếu hội thoại dài hơn 15 lượt. BẮT BUỘC AI tự động đề xuất: *"Phiên làm việc đã dài, để tránh trôi context (Task Drift), tôi xin tóm tắt lại vấn đề gốc và những gì ta đã đạt được..."*

## 2. Chống Trôi dạt Nhiệm vụ (Anti-Task Drift)
- Trước khi đề xuất refactor hay viết lại code, AI tự hỏi: *"Việc này có phục vụ cho Bug/Task ban đầu không?"*. Nếu không, DỪNG LẠI và tập trung vào lỗi hiện tại.

## 3. Quét Ngoại lệ (Edge Case Scanner)
- Mọi giải pháp code xuất ra phải vượt qua bài test ngầm:
  - Input rỗng/Null?
  - Xung đột đa luồng (Race Condition)?
  - Sập nguồn/Timeout?
  - Tràn số/Timezone?


