---
trigger: model_decision
description: "Workflow: Khởi tạo hệ thống thư mục và cấu trúc .gemini cho dự án mới"
---

# Lệnh: Khởi tạo Dự án (/init)

**Mục tiêu:** Kích hoạt lệnh này để khởi tạo cấu trúc `.gemini` cho dự án hiện tại.

**Hành động AI cần thực hiện khi thấy lệnh này:**
1. Chạy script khởi tạo dự án: `python %USERPROFILE%/.gemini/scripts/auto_init_project.py`
2. Nếu script không tồn tại hoặc lỗi, tự động tạo các thư mục cơ bản: `.gemini/rules/`, `.gemini/workflows/`, `.gemini/memory/`.
3. Tạo file `.gemini/memory/session-state.md` cơ bản.
4. Thông báo cho người dùng rằng dự án đã được khởi tạo thành công và sẵn sàng để sử dụng.
