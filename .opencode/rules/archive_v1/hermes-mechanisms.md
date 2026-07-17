---
trigger: model_decision
description: "HERMES MECHANISMS (Self-Learning Extension) - Trước khi kết thúc tác vụ, tự hỏi: 'Mình có học được gì từ tác vụ này để đóng gói thành skill mới kh..."
---
# HERMES MECHANISMS (Self-Learning Extension)
**Principle:** Tích hợp logic tự học, tự cải thiện và tạo skill của Hermes Agent vào hệ thống Antigravity.

## 1. VÒNG LẶP TỰ HỌC (AUTONOMOUS SKILL CREATION)
- **Điều kiện kích hoạt:** Khi hoàn thành một chuỗi tác vụ phức tạp (≥3 bước) thành công hoặc giải quyết xong một lỗi khó.
- **Cơ chế:** Tự động đánh giá xem quy trình này có lặp lại trong tương lai không. Nếu có, trích xuất chuỗi hành động thành một file chuẩn trong `workflows/` hoặc `skills/`.
- **Tự cải thiện (Self-Healing):** Nếu sử dụng một skill/workflow có sẵn mà bị lỗi, **bắt buộc** phải phân tích lỗi, sửa trực tiếp file code/markdown của skill đó để nó thông minh hơn trong lần chạy tới, sau đó mới báo cáo user.

## 2. LẬP MÔ HÌNH NGƯỜI DÙNG (DIALECTIC MODELING)
- **Điều kiện kích hoạt:** Bất cứ khi nào user chê, sửa sai, hoặc đưa ra yêu cầu về phong cách code.
- **Cơ chế:** Cập nhật ngầm vào `memory/layer1_user_profile.md` và `memory/layer2_coding_preferences.md`.
- **Luật tuyệt đối:** Không bao giờ để user phải sửa một thói quen/lỗi sai (assumptions) quá 2 lần giữa các phiên làm việc.

## 3. UỶ QUYỀN SUB-AGENT (DELEGATION & PARALLEL)
- **Điều kiện kích hoạt:** Khi có nhiều tác vụ độc lập (VD: Quét lỗi bảo mật + Tải file + Build project).
- **Cơ chế:** Không chờ tuần tự. Phải viết file python script nhỏ ném vào `run_command` chạy ngầm (WaitMsBeforeAsync: 0) để tạo các sub-agent ảo xử lý song song, thu thập log về sau.

## 4. TỰ ĐỘNG HÓA LỊCH TRÌNH (CRON-LIKE AUTOMATION)
- **Cơ chế:** Nếu user yêu cầu "làm việc này mỗi X giờ", tự động viết một script Python loop sử dụng `time.sleep` kết hợp với ghi log vào `tmp/cron_reports/`, chạy nền bằng `run_command` (hoặc Task Scheduler của Windows). Không cần user phải tự setup cron.

## YÊU CẦU THỰC THI (DEFINITION OF DONE)
Trước khi kết thúc tác vụ, tự hỏi: "Mình có học được gì từ tác vụ này để đóng gói thành skill mới không?". Nếu có, chủ động hỏi: `[PROPOSED SKILL UPDATE] Trích xuất logic vừa làm thành Skill mới? [Y/N]`


