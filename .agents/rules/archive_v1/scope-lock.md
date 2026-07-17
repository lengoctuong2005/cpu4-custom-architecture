---
trigger: model_decision
description: "Core Rule: Strict Scope Lock (Khóa Phạm Vi Nhiệm Vụ)"
---
# Core Rule: Strict Scope Lock (Khóa Phạm Vi Nhiệm Vụ)

**TÔN CHỈ**: Làm đúng và đủ những gì được yêu cầu. Không hơn, không kém.

## 1. Ranh giới Nhiệm vụ (Task Boundaries)
- Yêu cầu "Fix Bug" -> Chỉ tìm và diệt Bug.
- Yêu cầu "Add Feature" -> Chỉ thêm code mới.
- **CẤM CHỈ ĐỊNH**: Tự động Refactor code cho "đẹp hơn", đổi Code Style, đổi Design Pattern, hoặc tự ý nâng cấp Thư viện nếu User không yêu cầu.

## 2. Xử lý Vấn đề Phát sinh (Out of Scope)
- Nếu trong quá trình fix bug A, phát hiện ra đoạn code B viết rất tệ hoặc có nguy cơ dính bug C.
- **Hành động**: ĐỂ NGUYÊN ĐOẠN CODE B. Chỉ Note lại ở cuối câu trả lời: *"Note: Tôi phát hiện function B thiếu kiểm tra null, bạn có muốn tôi mở rộng scope để fix luôn không?"*


