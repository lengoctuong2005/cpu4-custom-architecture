---
trigger: model_decision
description: "The Deep Thinking Pipeline (Động Cơ Tư Duy Sâu 12 Lớp) - 1. **[SURFACE]**: Nghĩa đen của yêu cầu là gì?"
---
# The Deep Thinking Pipeline (Động Cơ Tư Duy Sâu 12 Lớp)
# Mọi luồng suy nghĩ phải đi qua lưới lọc 12 lớp này.

1. **[SURFACE]**: Nghĩa đen của yêu cầu là gì?
2. **[INTENT]**: Vấn đề THẬT SỰ User muốn giải quyết?
3. **[ASSUMPTION]**: Đào xới các giả định ẩn (VD: Optimize "nhanh hơn" là cần giảm Latency hay tăng Throughput?).
4. **[INFORMATION]**: Check lỗ hổng thông tin.
5. **[HYPOTHESIS]**: Buộc sinh ra ít nhất 3 giả thuyết (Tuyệt đối cấm Tunnel Vision - chỉ đâm đầu 1 hướng).
6. **[EVIDENCE]**: Lọc bằng chứng (Chỉ tin Measurement/Logs, không tin cảm giác).
7. **[FALSIFICATION]**: Cố gắng BÁC BỎ giả thuyết của chính mình. (Nếu A đúng thì B phải đúng. Nếu B không xảy ra trên log -> A sai).
8. **[RECURSIVE (5 Whys)]**: Liên tục hỏi tại sao. (Tại sao crash? -> Tràn stack. Tại sao tràn? -> Đệ quy vô hạn).
9. **[SOLUTION]**: Đề xuất giải pháp.
10. **[CASCADE]**: Đánh giá Hệ quả bậc 1, 2, 3 (VD: Tăng Baud rate -> Tăng Nhiễu -> Đòi hỏi Cáp xịn -> Tăng Cost).
11. **[UNCERTAINTY]**: Định lượng rủi ro.
12. **[META]**: Tự vấn: "Mình có đang thiên kiến (Bias) để chốt nhanh cho xong task không?".


