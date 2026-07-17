# Bảo vệ thao tác phá hủy (Destructive Action Guard)

*   **Mục đích**: Ngăn chặn mất mát dữ liệu hoặc làm hỏng trạng thái Git/DB không thể vãn hồi.
*   **Trigger**: Kích hoạt khi có ý định chạy các lệnh phá hoại (destructive) như `git reset --hard`, `git clean -fd`, `rm -rf`, `DROP TABLE`, `DELETE FROM`, hoặc ghi đè hàng loạt file lớn.

## Nội dung cốt lõi

1.  **Kích hoạt Cảnh Báo:**
    *   Trước khi thực hiện các lệnh nguy hiểm, Agent bắt buộc phải dừng lại.
    *   Phát ra cảnh báo rõ ràng: `[WARNING] Chuẩn bị thực hiện thao tác không thể hoàn tác`.

2.  **Đánh giá Sát thương:**
    *   Liệt kê chi tiết danh sách tài nguyên bị ảnh hưởng (các file sẽ bị xóa, database table sẽ bị drop, nhánh git sẽ bị reset).

3.  **Sao lưu (Backup):**
    *   Tạo bản sao lưu tự động trước khi thực hiện.
    *   Ví dụ: Tạo nhánh tạm (temp branch) bằng `git branch backup_before_reset` trước khi chạy `git reset --hard`.
    *   Hoặc lưu trữ file ra thư mục `temp/` nếu sửa đổi hàng loạt.

4.  **Xác nhận Explicit:**
    *   Chỉ tiến hành hành động phá hủy khi đã nhận được xác nhận trực tiếp (explicit approval) của User. Nếu User chưa cấp quyền, tuyệt đối không tự chạy.
