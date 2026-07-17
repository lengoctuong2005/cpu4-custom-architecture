---
trigger: model_decision
description: "Core Rule: Surgical Edit Protocol (Kỷ luật Chỉnh sửa Phẫu thuật)"
---
# Core Rule: Surgical Edit Protocol (Kỷ luật Chỉnh sửa Phẫu thuật)

**TÔN CHỈ**: Không bao giờ Overwrite khi có thể Merge. Thay đổi ít nhất có thể.

## 1. Lệnh Cấm Đoán (Read Before Write)
- BẮT BUỘC phải dùng công cụ đọc (view_file) trước khi đưa ra lệnh sửa (replace_file_content).
- TUYỆT ĐỐI CẤM dùng công cụ tạo file (write_to_file với cờ Overwrite=true) đối với một file đã có sẵn nội dung, TRỪ KHI User yêu cầu "Viết lại toàn bộ từ đầu".

## 2. Các Cấp Độ Chỉnh Sửa
- **Word/Line-level**: Lỗi dòng nào, sửa chính xác dòng đó.
- **Block-level**: Sửa đúng logic của function/class bị lỗi. KHÔNG đụng đến các function khác trong cùng file.
- **Bảo toàn hiện trạng**: Phải giữ nguyên mọi comment, formatting, docstrings cũ của User nếu nó không liên quan đến Bug.

## 3. Regression Awareness (Kiểm soát Cải lùi)
- Trước khi đổi tên/đổi tham số của một hàm, BẮT BUỘC phải tự hỏi: *"Hàm này đang được gọi ở đâu? Đổi xong có làm sập component khác không?"*


