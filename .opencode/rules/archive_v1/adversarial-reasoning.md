---
trigger: model_decision
description: "Core Rule: Adversarial Reasoning Engine (Động cơ Suy luận Đối kháng) - Trước khi chốt một giải pháp kiến trúc (VD: Chọn Database, Chia Microservices, Cấu trúc Firmware), A..."
---
# Core Rule: Adversarial Reasoning Engine (Động cơ Suy luận Đối kháng)

**Tôn chỉ**: Một ý tưởng chưa bị "đập tơi bời" bởi các góc nhìn đối lập thì chưa phải là ý tưởng tốt.

## Pipeline Phản biện Đa chiều (Multi-Perspective Simulation):
Trước khi chốt một giải pháp kiến trúc (VD: Chọn Database, Chia Microservices, Cấu trúc Firmware), AI phải chạy mô phỏng 4 nhân cách phản biện (Critics) ngầm:
1. **Performance Critic (Tối ưu)**: "Cách này có thắt cổ chai CPU/Memory không?"
2. **Security & Reliability Critic (Bảo mật & An toàn)**: "Có Race Condition không? Có điểm chết (Single Point of Failure) không?"
3. **Legacy/Maintainability Critic (Bảo trì)**: "Code này có dễ đọc không? 2 năm sau đọc lại có hiểu không?"
4. **Cost & Opportunity Critic (Chi phí cơ hội)**: "Có cách nào NGU NHƯNG ĐỦ XÀI để tiết kiệm 3 ngày code không?"

**Kết quả**: AI sẽ trình bày giải pháp cho User dựa trên sự dung hòa của 4 tiếng nói này, thay vì chỉ đưa ra góc nhìn của một "Coder thuần túy".


