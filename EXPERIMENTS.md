# 🧪 Nhật ký Thử nghiệm (Experiments Log)

Tệp này ghi lại toàn bộ lịch sử các lần chạy thử nghiệm mô hình, các thông số đầu vào và kết quả đạt được để tiện cho việc so sánh và đánh giá.

## 📊 Bảng Thử nghiệm

| Ngày (Date) | ID Thử nghiệm | Phiên bản Dữ liệu | Thuật toán / Mô hình | Tham số chính (Hyperparameters) | RMSE | MAE | R² Score | Ghi chú (Notes / Thay đổi) | Trạng thái |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| 2026-05-28 | EXP-001 | v1.0_raw | Baseline (Linear Regression) | N/A | 4.25 | 3.10 | 0.65 | Chạy baseline với dữ liệu thô chưa qua xử lý. | 🟢 Hoàn thành |
| 2026-05-28 | EXP-002 | v1.1_clean | Random Forest | n_estimators=100, max_depth=10 | 2.80 | 2.15 | 0.82 | Đã xử lý missing values, dùng Random Forest. Kết quả cải thiện rõ rệt. | 🟢 Hoàn thành |

---
## 💡 Hướng dẫn điền:
- ID Thử nghiệm: Mã duy nhất cho mỗi lần chạy (ví dụ: EXP-001).
- Phiên bản Dữ liệu: Đánh dấu version của dataset để biết đang dùng dữ liệu nào.
- Tham số chính: Chỉ ghi lại những tham số quan trọng có ảnh hưởng lớn đến kết quả.
- Trạng thái: Dùng các biểu tượng: 🟢 Hoàn thành, 🟡 Đang chạy, 🔴 Lỗi/Thất bại, 🌟 Phiên bản Tốt nhất.
