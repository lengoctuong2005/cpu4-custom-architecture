---
trigger: model_decision
description: "Core Rule: Diagnostic & Bayesian Reasoning (Chẩn đoán Bệnh) - Khi hệ thống có lỗi, cấm đổ lỗi cho 1 nguyên nhân duy nhất."
---
# Core Rule: Diagnostic & Bayesian Reasoning (Chẩn đoán Bệnh)

**Mục tiêu**: Bắt lỗi như một Bác sĩ Y khoa, không phải như một thợ sửa xe đoán mò.

## 1. Differential Diagnosis (Chẩn đoán Phân biệt)
Khi hệ thống có lỗi, cấm đổ lỗi cho 1 nguyên nhân duy nhất.
- Phải đưa ra 3-4 Root Causes khả dĩ nhất.
- Gắn xác suất (%). (VD: 45% do tràn Buffer, 30% do Clock, 25% do Nhiễu nguồn).

## 2. Bayesian Updating (Cập nhật Niềm tin)
- Khi User cung cấp thêm bằng chứng mới (VD: "Đã thay cáp nhưng vẫn lỗi").
- AI lập tức update lại xác suất: *"Cáp không lỗi -> Loại trừ nhiễu cứng -> Khả năng lỗi Software tăng lên 90%"*.

## 3. The Testing Protocol (Giao thức Thực nghiệm)
- Luôn đề xuất CÁCH TEST (Experiment) để xác nhận/loại trừ từng giả thuyết trước khi hối thúc User đập đi viết lại code.


