---
trigger: model_decision
description: "Core Rule: Self-Audit & State Snapshot (Tự Kiểm Kê) - Trước khi báo cáo với User là 'Xong', tự chạy bảng hỏi:"
---
# Core Rule: Self-Audit & State Snapshot (Tự Kiểm Kê)

**TÔN CHỈ**: Không kết thúc Task nếu chưa tự Audit lại chính mình.

## 1. State Snapshot (Trạng thái trước khi sửa)
- Trước khi gõ code, AI phải chụp lại (trong não) trạng thái: *"File này đang import thư viện gì? Module này phụ thuộc vào ai?"*.

## 2. Post-Task Audit (Kiểm tra Hậu kỳ)
Trước khi báo cáo với User là "Xong", tự chạy bảng hỏi:
1. **Scope Check**: Thay đổi vừa rồi có đi quá giới hạn yêu cầu không?
2. **Side-Effect Check**: Việc sửa logic này có vô tình làm sập Unit Test nào đang chạy không?
3. **Overwrite Check**: Có lỡ xóa nhầm comment hay đoạn code nào không liên quan của User không?

Nếu phát hiện lỗi tự gây ra -> TỰ ĐỘNG Revert (Rollback) và làm lại.


