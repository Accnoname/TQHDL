# 🔄 Lịch Sử Cập Nhật (Changelog)

Tất cả các thay đổi đáng chú ý của dự án sẽ được ghi nhận tại tệp này. Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Added
- Thêm cấu trúc thư mục chuẩn: data/, src/, reports/, configs/, notebooks/.
- Thêm requirements.txt và config.yaml để chuẩn hóa môi trường.
- Thêm step_06_strategic_insights.py bao gồm biểu đồ World Heatmap tương tác bằng Plotly.
- Khởi tạo 4 tệp quản lý dự án tiêu chuẩn: RULES.md, TASKS.md, EXPERIMENTS.md, CHANGELOG.md.
- Thêm World Heatmap theo lương (median) bên cạnh heatmap theo nhu cầu tuyển dụng.
- Thêm dashboard tĩnh reports/dashboard.html tổng hợp toàn bộ biểu đồ.

### Changed
- Di chuyển dữ liệu vào data/raw và cập nhật src/data/load_data.py.
- Di chuyển các script sang src/visualization và chuyển output về reports/figures.
- Cập nhật main.py sử dụng src/visualization/plots.py.
- Đơn giản hóa main.py và plots.py để chạy trực tiếp các bước step_01..06.
- Khôi phục loader đơn giản với hàm load() phục vụ phân tích nhanh.

### Changed
- Tái cấu trúc (Refactored) quy trình trực quan hóa dữ liệu từ tổ chức theo Domain (viz_01 -> viz_06) sang tổ chức theo Data Analysis Workflow (step_01 -> step_06).
- Gỡ biểu đồ bong bóng và dồn layout còn 3 biểu đồ ở bước 03.
- Thay pie chart cấp độ kinh nghiệm bằng cột chồng 100% theo quốc gia (Top 15) ở bước 01.
- Chuyển phân bố cấp độ kinh nghiệm sang theo khu vực ở bước 01.
- Thay donut ở bước 02 bằng pie cho biểu đồ 1, violin cho biểu đồ 2, box+sample cho biểu đồ 4; giữ cột chồng theo ngành cho biểu đồ 3.
- Tối ưu trực quan bước 06: chỉnh thang quadrant theo dữ liệu, thay violin/box bằng median+IQR, và tách lương với nhu cầu ở biểu đồ kỹ năng.
- Tách các biểu đồ dạng subplot thành ảnh riêng theo số thứ tự cho các bước 01-05 và 06.

### Removed
- Xóa bỏ các file cũ viz_01_overview.py, viz_02_ai_impact.py, viz_03_salary.py, viz_04_skills.py, viz_05_automation.py, viz_06_questions.py.

## [1.0.0] - 2026-05-25
### Added
- Thiết lập ban đầu với các tệp viz_ phân tích theo chủ đề Lương, Kỹ năng, AI Impact.
- Tải bộ dữ liệu ai_impact_jobs_2010_2025.csv.
