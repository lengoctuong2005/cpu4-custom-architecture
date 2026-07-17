# Quy tắc chống vòng lặp gỡ lỗi vô hạn (Anti-Loop)

*   **Mục đích**: Ngăn chặn tình trạng Agent thử-sai liên tục (trial-and-error loop) dẫn đến lãng phí token và gây ô nhiễm lịch sử code.
*   **Trigger**: Kích hoạt khi Agent tiến hành debug, fix bug, hoặc nhận được báo lỗi từ người dùng.

## Nội dung cốt lõi

1.  **Strike 1 (Lần đầu gặp lỗi)**: 
    *   Đọc log cẩn thận.
    *   Phân tích nguyên nhân gốc rễ (Root Cause Analysis).
    *   Đề xuất bản vá và tiến hành sửa lỗi.

2.  **Strike 2 (Sửa lần 1 vẫn lỗi)**: 
    *   **KHÔNG ĐƯỢC ĐOÁN TIẾP.** 
    *   Bắt buộc phải chèn thêm các lệnh in log runtime (như `print()`, `console.log()`, `logger.debug()`) vào các điểm nghi ngờ.
    *   Hoặc kích hoạt chế độ debug để thu thập thêm Telemetry (thông tin đo lường).
    *   Quan sát log mới trước khi ra quyết định sửa code tiếp.

3.  **Strike 3 (Vẫn lỗi sau Strike 2)**: 
    *   **Dừng lại ngay lập tức.** 
    *   Không được thử các giải pháp mù mờ nữa.
    *   Báo cáo lỗi với format: `[CONCERN]: Vượt quá giới hạn tự gỡ lỗi`.
    *   Tóm tắt lại các giả thuyết đã thử, log thu được và yêu cầu User can thiệp.
