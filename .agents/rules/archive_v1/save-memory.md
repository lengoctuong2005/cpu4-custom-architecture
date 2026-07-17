---
trigger: model_decision
description: "Workflow: Lưu lại bộ nhớ và tổng kết phiên làm việc hiện tại"
---

# Lệnh: Lưu Bộ Nhớ (/save-memory)

**Mục tiêu:** Kích hoạt lệnh này để lưu trữ kiến thức và tổng kết phiên làm việc hiện tại vào bộ nhớ hệ thống.

**Hành động AI cần thực hiện khi thấy lệnh này:**
1. Đọc lại các thay đổi, quyết định quan trọng, và các bài học trong phiên làm việc hiện tại.
2. Cập nhật vào `.gemini/memory/session-state.md` và ghi nhận một `observation` hoặc `summarize` thông qua `memory_observer.py` nếu có cấu hình.
3. Đề xuất cập nhật preferences hoặc knowledge base nếu có điều gì mới đáng lưu ý.
4. Thông báo tổng kết cho người dùng.
