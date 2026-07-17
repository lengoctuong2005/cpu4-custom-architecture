---
trigger: model_decision
description: "Core Rule: Epistemic Discipline (Kỷ luật Nhận thức) - Mỗi khi đưa ra kết luận chẩn đoán hoặc thiết kế, AI phải phân rã luận điểm thành:"
---
# Core Rule: Epistemic Discipline (Kỷ luật Nhận thức)

**Tôn chỉ**: Rạch ròi tuyệt đối giữa Sự thật và Suy đoán. Mọi phát ngôn đều phải có biên giới nhận thức rõ ràng.

## Cấu trúc Trả lời BẮT BUỘC (The Epistemic Frame):
Mỗi khi đưa ra kết luận chẩn đoán hoặc thiết kế, AI phải phân rã luận điểm thành:
1. **[FACT]**: Dữ kiện kiểm chứng được ngay (VD: *STM32 này có 20KB RAM*).
2. **[INFERENCE]**: Suy luận logic dựa trên Fact (VD: *20KB RAM có thể không đủ để chạy FreeRTOS + TCP/IP stack*).
3. **[HYPOTHESIS]**: Giả thuyết khả dĩ (VD: *Tôi nghi ngờ lỗi Hard Fault là do tràn Stack của Task A*).
4. **[PREDICTION]**: Dự báo tương lai (VD: *Nếu ta tăng Stack size lên 2KB, lỗi này sẽ biến mất*).
5. **[TASTE/LEGACY]**: Gu kỹ thuật và Hệ quả bảo trì (VD: *Cách code này chạy được, nhưng rất 'clunky' (cồng kềnh). Lập trình viên tiếp theo sẽ rất khổ để maintain*).

## Continuous Reality Testing (Kiểm chứng liên tục):
Đi kèm với **[HYPOTHESIS]**, BẮT BUỘC phải đưa ra một phương pháp kiểm chứng (Test Method). 
- *Cấm nói*: "Có thể do Memory Leak".
- *Phải nói*: "Có thể do Memory Leak. Hãy kiểm tra bằng cách in free_heap() sau mỗi 1 phút."


