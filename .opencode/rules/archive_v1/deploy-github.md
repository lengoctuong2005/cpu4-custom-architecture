---
trigger: model_decision
description: "Workflow: Kiểm tra an toàn và push code lên Github"
---

# Lệnh: Deploy Github (/deploy-github)

**Mục tiêu:** Kích hoạt lệnh này để AI tự động kiểm tra an toàn và đẩy code lên Github.

**Hành động AI cần thực hiện khi thấy lệnh này:**
1. Chạy kiểm tra an toàn: `python %USERPROFILE%/.gemini/scripts/safety_guard.py --scan-file .` để đảm bảo không có key, token bị lộ.
2. Kiểm tra `git status` để xem các file thay đổi.
3. Tạo commit message chuẩn mực (dựa trên convention của dự án).
4. Thực hiện `git add`, `git commit` và `git push`.
5. Báo cáo trạng thái thành công cho người dùng.
