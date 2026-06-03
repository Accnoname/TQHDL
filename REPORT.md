# BÁO CÁO DỰ ÁN: AI IMPACT ON JOB MARKET (2010–2025)

## 1. GIỚI THIỆU

### 1.1. Đặt vấn đề
Trí tuệ nhân tạo (AI) đã chuyển mình từ phòng nghiên cứu trở thành lực lượng kinh tế cốt lõi, đặc biệt từ sau sự bùng nổ của Generative AI (2022). Tuy nhiên, tác động của AI lên thị trường lao động vẫn gây tranh cãi: AI tạo ra hay triệt tiêu việc làm? Ngành nào chịu rủi ro cao nhất? Kỹ năng nào được ưu tiên?
Dự án này sử dụng bộ dữ liệu tuyển dụng đa quốc gia (2010–2025) để xây dựng một Hệ thống Dashboard Phân tích Tương tác, giúp giải đáp các câu hỏi chiến lược trên.

### 1.2. Mục tiêu
- **Phân tích xu hướng:** Theo dõi sự bùng nổ của từ khóa AI trong tin tuyển dụng qua 16 năm.
- **Đánh giá rủi ro:** Phân tích rủi ro tự động hóa và dịch chuyển việc làm theo từng ngành.
- **Biến động thu nhập:** Khảo sát mức lương trung vị, lạm phát lương và yêu cầu kỹ năng.
- **Xây dựng giải pháp BI (Business Intelligence):** Phát triển Dashboard tương tác bằng Streamlit, hỗ trợ bộ lọc thời gian thực và giao diện chuẩn doanh nghiệp.

---

## 2. DỮ LIỆU VÀ TIỀN XỬ LÝ

### 2.1. Mô tả Dữ liệu
Bộ dữ liệu mô phỏng (`ai_job_market_mock.csv`) gồm bản ghi tin tuyển dụng trải dài từ 2010 đến 2025.
- **Không gian:** 9 khu vực (Bắc Mỹ, Châu Âu, Đông Á...).
- **Ngành nghề:** 9 lĩnh vực (Tech, Finance, Healthcare, Manufacturing...).
- **Chỉ số AI:** Tỷ lệ đề cập AI, Điểm rủi ro tự động hóa, Mức độ trưởng thành AI của ngành.

### 2.2. Kỹ thuật Tiền xử lý
- **Xử lý chuỗi:** Phân tách (split/explode) các danh sách kỹ năng cốt lõi và từ khóa AI.
- **Chuẩn hóa Categorical:** Xếp hạng các mức độ kinh nghiệm (Intern -> Executive) và rủi ro (Low -> High) theo thứ tự Ordinal để biểu đồ hiển thị logic.
- **Bảo toàn Dữ liệu Khuyết:** Điền khuyết có chủ đích cho các tin không yêu cầu kỹ năng AI để bảo vệ nguyên vẹn kích thước mẫu thay vì xóa bỏ.

---

## 3. KIẾN TRÚC DASHBOARD TƯƠNG TÁC

Dự án đã được nâng cấp toàn diện từ các biểu đồ tĩnh (Matplotlib) lên **Interactive Web Dashboard** bằng nền tảng Streamlit.

### 3.1. Tính năng công nghệ cốt lõi
- **Dynamic Filters:** Sidebar cho phép lọc đa chiều theo: Giai đoạn (Năm), Khoảng lương, Khu vực, Ngành nghề, Cấp độ kinh nghiệm. Mọi biểu đồ trên trang phản ứng tức thì (Real-time).
- **Native Light/Dark Mode:** Hệ thống tích hợp CSS Injection (Glassmorphism) để tự động thích ứng với chế độ sáng/tối, bo góc, đổ bóng và tối ưu viền chọn.
- **Material Symbols:** Ứng dụng bộ biểu tượng tiêu chuẩn Google Material, mang lại giao diện B2B gọn gàng và chuyên nghiệp.

### 3.2. Cấu trúc 4 Thẻ Phân Tích (Tabs)
1. **Tổng Quan:** Đo lường xu hướng vĩ mô và sức hút của các ngành/quốc gia.
2. **Lương & Kỹ Năng:** Động lực học vi mô của thu nhập và các từ khóa cốt lõi.
3. **Rủi Ro AI:** Cảnh báo mức độ an toàn nghề nghiệp.
4. **Bản Đồ Thế Giới:** Phân tích dữ liệu không gian bằng Choropleth Plotly.

---

## 4. KẾT QUẢ PHÂN TÍCH

### 4.1. Sự bùng nổ của Kỷ nguyên AI
- **Tỷ lệ đề cập AI:** Từ mức rất thấp vào 2010, tỷ lệ tin tuyển dụng yêu cầu AI đã vọt lên ~69% (vào năm 2025). Hai điểm bùng nổ được ghi nhận vào năm 2018 (mạng Transformer) và 2022 (ChatGPT).
- **Sự trỗi dậy của ngành Sản xuất:** Ngành Công nghệ (Tech) và Sản xuất (Manufacturing) dẫn đầu nhu cầu nhân sự AI, phản ánh xu hướng Cách mạng Công nghiệp 4.0 khi Robotics trực tiếp tham gia dây chuyền vật lý.

### 4.2. Nghịch lý Tiền Lương & Kỹ Năng
- **Đường cong thâm niên bị san phẳng:** Khoảng cách lương trung vị giữa cấp bậc Intern và Executive bị thu hẹp. Trong kỷ nguyên số, giá trị nhân sự được định đoạt bằng "Tốc độ cập nhật công nghệ mới" thay vì số năm kinh nghiệm đơn thuần.
- **Tài chính dẫn đầu đãi ngộ:** Ngành Finance trả lương trung vị cao nhất để bù đắp rủi ro (Risk Premium) trong việc áp dụng thuật toán AI vào thị trường vốn.
- **Kỹ năng thiết yếu:** Kỹ năng **Giao tiếp (Communication)** đứng Top đầu cùng với Python/SQL. Thị trường khát khao các "Phiên dịch viên công nghệ" kết nối thuật toán rập khuôn với chiến lược kinh doanh linh hoạt.

### 4.3. Cảnh báo Rủi ro Tự động hóa
- **Nguy cơ hiện hữu:** Hơn 75% vị trí công việc có điểm rủi ro tự động hóa cao (0.6 - 0.8). Lưỡi hái của tự động hóa đã chuyển dịch từ lao động chân tay sang lao động tri thức (Cognitive tasks).
- **Rủi ro ở Giai đoạn Trưởng thành (Mature):** Các doanh nghiệp áp dụng AI ở mức "Mature" lại là nơi tiềm ẩn rủi ro đào thải nhân sự khốc liệt nhất. Khi hệ thống đi vào ổn định, sức người bị gạt bỏ để tối đa hóa biên lợi nhuận.
- **Áp lực Reskilling:** Nhu cầu "Tái đào tạo" phình to nuốt chửng biểu đồ. Tỷ lệ khấu hao năng lực diễn ra quá nhanh khiến việc "Học tập suốt đời" nay trở thành thứ thuế sinh tồn bắt buộc.

### 4.4. Bất đối xứng Quyền lực (Chủ nghĩa Thực dân Dữ liệu)
- Bản đồ tương tác chứng minh sự bất bình đẳng địa lý sâu sắc: Bắc Mỹ và Tây Âu kiểm soát phần lớn lượng tin đăng và thiết lập mức lương "kịch trần", trong khi các khu vực như Nam Mỹ hay Châu Á thường đảm nhận vai trò gia công, dán nhãn dữ liệu thô với chi phí rẻ mạt.

---

## 5. KẾT LUẬN

Dự án bóc tách thành công những động lực ngầm định của thị trường lao động. Kỷ nguyên AI không triệt tiêu công việc một cách mù quáng, nhưng nó đòi hỏi một cuộc thanh lọc kỹ năng khốc liệt. **Learning Agility (Sự nhạy bén trong học tập)** là tấm khiên duy nhất chống lại rủi ro tự động hóa.
Hệ thống Streamlit Dashboard ra đời đã đáp ứng hoàn hảo vai trò của một trạm radar phân tích thời gian thực, là công cụ thiết yếu để các nhà hoạch định chiến lược và ứng viên nắm bắt định hướng tương lai.
