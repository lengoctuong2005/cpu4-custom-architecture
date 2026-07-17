---
trigger: model_decision
description: "Core Rule: Scientific Method & Reality Grounding Layer - 1. **Observation (Quan sát)**: Xác định 'Symptom' (Triệu chứng) và 'Weak Signal' (Tín hiệu yếu như C..."
---
# Core Rule: Scientific Method & Reality Grounding Layer

**Tôn chỉ**: Code có thể nói dối, giả định có thể sai, chỉ có Test/Log/Metrics là sự thật. Tuyệt đối không nhảy cóc từ Giả thuyết sang Kết luận.

## Quy trình Chẩn đoán (Diagnostic Pipeline):
1. **Observation (Quan sát)**: Xác định "Symptom" (Triệu chứng) và "Weak Signal" (Tín hiệu yếu như CPU tăng 3%).
2. **Hypothesis (Giả thuyết)**: Liệt kê ít nhất 3 giả thuyết (Causal Reasoning).
3. **Experiment Design (Thiết kế Thực nghiệm)**: Không đoán bừa. Hướng dẫn User thực hiện các bài test cô lập (Isolation tests) để loại trừ giả thuyết.
   *Ví dụ: "Hãy thử tắt ngắt UART xem CPU có giảm không?"*
4. **Evidence (Bằng chứng)**: Thu thập kết quả thực nghiệm.
5. **Conclusion (Kết luận)**: Chốt Root Cause. Giải thích bằng Mechanistic Understanding (Tại sao nó hoạt động như vậy ở tầng vật lý/logic).
6. **Solution**: Ra code fix.


