---
trigger: model_decision
description: "Core Rule: Reliability Pipeline (Kiến trúc Đảm bảo Chất lượng)"
---
# Core Rule: Reliability Pipeline (Kiến trúc Đảm bảo Chất lượng)

**Tôn chỉ**: CẤM Agent xuất đáp án hoặc sinh code ngay ở lần suy nghĩ đầu tiên (Single-pass). Mọi câu trả lời BẮT BUỘC phải đi qua đường ống 4 bước (Multi-Pass Reasoning).

## Pipeline 4 Bước Bắt Buộc:

**1. Pass 1: Generate & Assume (Sinh nháp & Ghi nhận Giả định)**
- Xây dựng giải pháp thô trong bộ nhớ tạm.
- Liệt kê rõ ràng mọi [ASSUMPTION]. Ví dụ: `[Assumption: User đang dùng Linux]`, `[Assumption: Mạng IoT luôn ổn định]`.

**2. Pass 2: Self-Critique & Contradiction Check (Tự phản biện & Kiểm tra mâu thuẫn)**
- Gọi `failure-database.yaml` và `causal-graph.yaml`.
- Bẻ gãy các Giả định: "Nếu mạng IoT rớt thì sao?" -> Buộc phải đổi kiến trúc.
- Đóng vai Critic Agent: Cố gắng tìm lỗi bảo mật, lỗi bộ nhớ, lỗi logic trong bản nháp.

**3. Pass 3: Reality Check & Failure Prediction (Rủi ro & Thực tế)**
- Dự đoán: "Điều gì có thể khiến giải pháp này sụp đổ?" (Ví dụ: Chết RAM, Khó deploy).
- Đánh giá: Có phù hợp với nguồn lực và Deadline hiện tại của User không?

**4. Pass 4: Final Polish & Confidence (Hoàn thiện & Độ tin cậy)**
- Xuất đáp án cuối cùng.
- **BẮT BUỘC** gắn nhãn Độ tin cậy. 
- *Ví dụ:* `[Confidence: 90% - Đã kiểm chứng qua Datasheet]` hoặc `[Confidence: 40% - Cần User cung cấp thêm schematic phần cứng]`.


