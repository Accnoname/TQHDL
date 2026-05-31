# Báo Cáo Thử Nghiệm: Tác Động AI Lên Thị Trường Việc Làm (2010-2025)

Tài liệu này là báo cáo thử (draft) nhằm trình bày quy trình phân tích, trực quan hóa và các phát hiện chiến lược từ bộ dữ liệu tuyển dụng giai đoạn 2010-2025. Báo cáo được thiết kế để dễ cập nhật, có thể thay thế các đoạn mô tả bằng số liệu thực tế sau khi chạy đầy đủ pipeline.

---

## Mục lục

1. Tóm tắt điều hành
2. Bối cảnh và mục tiêu
3. Mô tả dữ liệu
4. Quy trình phân tích và phương pháp
5. Kết quả tổng quan (Step 01)
6. Phân tích đơn biến (Step 02)
7. Phân tích song biến (Step 03)
8. Xu hướng theo thời gian (Step 04)
9. Phân tích kỹ năng và text (Step 05)
10. Phân tích chiến lược (Step 06)
11. Hàm ý và khuyến nghị
12. Hạn chế và rủi ro
13. Kế hoạch tiếp theo
14. Phụ lục

---

## 1. Tóm tắt điều hành

Bộ dữ liệu tuyển dụng giai đoạn 2010-2025 cung cấp góc nhìn đa chiều về mức độ tác động của AI lên thị trường lao động. Thông qua chuỗi biểu đồ EDA và phân tích chiến lược, báo cáo này phác họa xu hướng dài hạn, mối quan hệ giữa lương và rủi ro tự động hóa, cũng như cấu trúc kỹ năng đang được thị trường ưu tiên.

Các điểm nhấn chính trong báo cáo thử:

- Xu hướng đề cập AI trong tin tuyển dụng tăng dần theo thời gian, phản ánh mức độ thâm nhập công nghệ AI vào các ngành nghề.
- Lương trung vị biến động theo cấp độ kinh nghiệm và ngành nghề, cho thấy khoảng cách giá trị giữa các vị trí và lĩnh vực.
- Rủi ro tự động hóa có mức chênh lệch đáng kể giữa các ngành, gợi ý sự khác biệt về khả năng thay thế bởi AI.
- Kỹ năng cốt lõi và từ khóa AI đóng vai trò then chốt trong việc hình thành lợi thế cạnh tranh của ứng viên.
- Ở góc nhìn chiến lược, giai đoạn áp dụng AI của ngành có liên hệ với tỷ lệ rủi ro dịch chuyển việc làm.

Lưu ý: Báo cáo hiện chưa đính kèm các số liệu cụ thể, vì đây là bản thử nghiệm nhằm định hình cấu trúc trình bày. Các giá trị định lượng sẽ được cập nhật ở bản hoàn chỉnh.

---

## 2. Bối cảnh và mục tiêu

### 2.1 Bối cảnh

Giai đoạn 2010-2025 chứng kiến sự phát triển nhanh của AI trong nhiều lĩnh vực như tài chính, y tế, thương mại điện tử và sản xuất. Cùng thời điểm đó, thị trường lao động xuất hiện các dấu hiệu chuyển dịch: nhu cầu kỹ năng AI tăng, yêu cầu tái đào tạo (reskilling) trở nên phổ biến, và rủi ro tự động hóa bắt đầu ảnh hưởng đến cấu trúc việc làm.

### 2.2 Mục tiêu phân tích

- Mô tả bức tranh tổng quan về tin tuyển dụng trong giai đoạn 2010-2025.
- Xác định phân phối các biến quan trọng: lương, cường độ AI, rủi ro tự động hóa, mức độ áp dụng AI.
- Phát hiện mối quan hệ giữa lương, rủi ro và ngành nghề.
- Theo dõi xu hướng dài hạn và đánh giá mức độ thay đổi theo thời gian.
- Đưa ra hàm ý chiến lược cho doanh nghiệp, nhân sự và đào tạo.

---

## 3. Mô tả dữ liệu

### 3.1 Phạm vi dữ liệu

- Thời gian: 2010-2025
- Đơn vị phân tích: tin tuyển dụng (job posting)
- Không gian: đa quốc gia
- Đa ngành nghề

### 3.2 Các trường quan trọng

Nhóm biến chính thường xuất hiện:

- Thông tin thời gian: năm đăng tuyển
- Thông tin vị trí: quốc gia, khu vực, ngành nghề
- Thông tin kỹ năng: danh sách kỹ năng cốt lõi, từ khóa AI
- Biến AI: mức độ AI, điểm tự động hóa, yêu cầu tái đào tạo
- Biến kinh tế: lương (USD)

### 3.3 Chất lượng dữ liệu

Những điểm cần lưu ý trong dữ liệu tuyển dụng:

- Thiếu dữ liệu ở một số trường (lương hoặc kỹ năng)
- Sự không đồng nhất trong cách ghi kỹ năng
- Phân bố mất cân bằng giữa các quốc gia và ngành

Các xử lý cơ bản được thực hiện:

- Làm sạch chuỗi văn bản (trim, chuẩn hóa)
- Chuyển đổi chuỗi kỹ năng sang danh sách
- Loại bỏ hoặc ghi nhận missing values

---

## 4. Quy trình phân tích và phương pháp

### 4.1 Quy trình tổng thể

1. Data cleaning và feature engineering
2. EDA tổng quan
3. Phân tích đơn biến
4. Phân tích song biến
5. Xu hướng theo thời gian
6. Phân tích kỹ năng và text
7. Tổng hợp chiến lược
8. Báo cáo và tài liệu hóa

### 4.2 Nguyên tắc trực quan hóa

- Ưu tiên nguyên tắc “tính toán trước, vẽ sau” để giảm nhiễu dữ liệu.
- Gom nhóm (groupby) trước khi vẽ các biểu đồ mật độ lớn.
- Giới hạn top N để biểu đồ dễ đọc.
- Màu sắc có chủ đích, tránh lạm dụng.

### 4.3 Hệ thống biểu đồ

Các biểu đồ được chia theo từng bước (step):

- Step 01: Tổng quan
- Step 02: Đơn biến
- Step 03: Song biến
- Step 04: Xu hướng thời gian
- Step 05: Kỹ năng và text
- Step 06: Chiến lược

---

## 5. Kết quả tổng quan (Step 01)

### 5.1 Tin đăng theo năm

Biểu đồ cho thấy số lượng tin đăng theo năm. Thông thường, xu hướng sẽ phản ánh:

- Giai đoạn tăng trưởng rõ rệt khi thị trường mở rộng
- Một số năm có thể sụt giảm do biến động kinh tế hoặc khủng hoảng

### 5.2 Top ngành nghề

Top ngành nghề giúp xác định lĩnh vực có nhu cầu tuyển dụng lớn nhất. Đây là nền tảng để:

- Xác định ngành ưu tiên đào tạo kỹ năng
- Dự báo thị trường lao động trong tương lai

### 5.3 Top quốc gia

Phân bố quốc gia cho thấy mức độ tập trung của thị trường lao động. Các quốc gia dẫn đầu thường là những nơi có:

- Hệ sinh thái công nghệ phát triển
- Nhu cầu nhân lực lớn

### 5.4 Cấp độ kinh nghiệm theo khu vực

Biểu đồ stacked 100% thể hiện tỷ lệ Junior, Mid, Senior, Lead, Executive theo khu vực. Các khu vực có tỷ lệ Senior cao thường phản ánh:

- Thị trường trưởng thành
- Nhu cầu vị trí quản lý và chuyên gia

---

## 6. Phân tích đơn biến (Step 02)

### 6.1 Phân bổ cường độ AI

Biểu đồ phân phối cường độ AI cho thấy phần lớn công việc nằm ở mức độ thấp đến trung bình, trong khi một phần nhỏ yêu cầu AI chuyên sâu. Ý nghĩa:

- Cơ hội cho ứng viên với kỹ năng AI ở mức nền tảng
- Nhu cầu cho chuyên gia AI vẫn đang tăng

### 6.2 Phân bố điểm rủi ro tự động hóa

Histogram thể hiện sự phân bố điểm rủi ro tự động hóa. Khi điểm tập trung ở mức cao:

- Một số ngành có nguy cơ bị thay thế nhanh

Khi điểm tập trung ở mức thấp:

- Công việc mang tính sáng tạo hoặc giao tiếp vẫn giữ vai trò quan trọng

### 6.3 Giai đoạn áp dụng AI theo ngành

Biểu đồ cột chồng theo ngành thể hiện mức độ ứng dụng AI. Các ngành “Mature” thường là:

- Fintech, thương mại điện tử, công nghệ

Các ngành “Emerging” thường là:

- Các lĩnh vực truyền thống hoặc cần điều chỉnh quy trình dài hạn

### 6.4 Phân bổ mức lương

Boxplot kết hợp scatter cho thấy phân bố mức lương tổng quan. Đặc điểm nổi bật thường bao gồm:

- Lương trung vị thể hiện mặt bằng chung
- Các điểm ngoại lệ phản ánh nhóm việc làm có thu nhập rất cao

---

## 7. Phân tích song biến (Step 03)

### 7.1 Lương trung vị theo cấp độ

Kết quả cho thấy xu hướng lương tăng dần theo cấp độ kinh nghiệm. Điều này phù hợp với mô hình thị trường lao động thông thường, đồng thời nhấn mạnh giá trị của thâm niên và kỹ năng chuyên sâu.

### 7.2 Top ngành có lương cao nhất

Biểu đồ này thể hiện các ngành có lương trung vị cao nhất. Ý nghĩa:

- Tập trung nguồn lực đào tạo và tuyển dụng vào các ngành này có thể tối ưu lợi ích kinh tế.

### 7.3 Rủi ro tự động hóa theo ngành

Phân bố rủi ro theo ngành cho thấy sự khác biệt lớn:

- Một số ngành có rủi ro cao do công việc lặp lại
- Một số ngành có rủi ro thấp do cần sáng tạo hoặc tương tác con người

---

## 8. Xu hướng theo thời gian (Step 04)

### 8.1 Tỷ lệ tin đăng đề cập AI

Biểu đồ xu hướng này thường cho thấy sự gia tăng liên tục về mức độ nhắc đến AI trong tin tuyển dụng. Đây là chỉ báo rõ rệt về tốc độ thâm nhập công nghệ.

### 8.2 Lương theo năm

Lương trung vị và lương trung bình có thể phản ánh:

- Mức tăng trưởng tổng thể
- Sự biến động trong các giai đoạn kinh tế đặc biệt

### 8.3 Xu hướng rủi ro tự động hóa

Xu hướng rủi ro tự động hóa theo thời gian giúp xác định mức độ thay đổi của các công việc dưới tác động AI.

### 8.4 Xu hướng reskilling

Biểu đồ stackplot về reskilling thể hiện:

- Tỷ lệ công việc yêu cầu tái đào tạo ngày càng tăng
- Vai trò quan trọng của học tập suốt đời

---

## 9. Phân tích kỹ năng và text (Step 05)

### 9.1 Top kỹ năng cốt lõi

Danh sách kỹ năng cốt lõi giúp xác định nhóm năng lực nền tảng mà thị trường yêu cầu. Các kỹ năng này thường liên quan đến:

- Lập trình
- Phân tích dữ liệu
- Quản trị hệ thống

### 9.2 Top từ khóa AI

Từ khóa AI phổ biến phản ánh xu hướng công nghệ nổi bật. Ví dụ:

- Machine Learning
- Deep Learning
- NLP

### 9.3 Tỷ lệ reskilling theo ngành

Biểu đồ này cho thấy ngành nào có nhu cầu tái đào tạo cao nhất, từ đó gợi ý:

- Ngành cần chương trình đào tạo nội bộ
- Ngành cần tái thiết kế quy trình lao động

### 9.4 Rủi ro dịch chuyển việc làm theo ngành

Biểu đồ stacked 100% giúp so sánh tỷ lệ Low, Medium, High giữa các ngành. Đây là cơ sở để:

- Xác định ngành có rủi ro cao
- Định hướng chiến lược chuyển đổi lực lượng lao động

---

## 10. Phân tích chiến lược (Step 06)

### 10.1 Phân bổ rủi ro theo giai đoạn áp dụng AI

Biểu đồ cột chồng 100% là trung tâm chiến lược trong báo cáo:

- Cho thấy mối quan hệ giữa giai đoạn áp dụng AI và tỷ lệ rủi ro
- Giúp ưu tiên các ngành đang ở giai đoạn chuyển đổi

### 10.2 Ý nghĩa chiến lược

- Ngành Mature thường có tỷ lệ rủi ro cao hơn, phản ánh quá trình tự động hóa sâu.
- Ngành Emerging có thể còn dư địa an toàn nhưng cần chuẩn bị reskilling.
- Ngành Growing là điểm nhấn cần tập trung đầu tư nhân lực và công nghệ.

---

## 11. Hàm ý và khuyến nghị

### 11.1 Đối với doanh nghiệp

- Tăng đầu tư đào tạo nội bộ về AI và dữ liệu
- Tối ưu hóa quy trình để giảm rủi ro mất việc
- Xây dựng chiến lược chuyển đổi nhân sự dài hạn

### 11.2 Đối với người lao động

- Ưu tiên phát triển kỹ năng AI nền tảng
- Sẵn sàng học kỹ năng mới theo nhu cầu thị trường
- Theo dõi xu hướng ngành để định hướng nghề nghiệp

### 11.3 Đối với tổ chức đào tạo

- Cập nhật chương trình theo xu hướng AI
- Xây dựng khóa học ngắn hạn về reskilling
- Đẩy mạnh mô hình học tập linh hoạt

---

## 12. Hạn chế và rủi ro

- Dữ liệu có thể thiếu đồng nhất theo quốc gia
- Một số biến có missing values
- Chưa có kiểm chứng định lượng sâu về nguyên nhân thay đổi
- Một số kết luận hiện ở mức mô tả, cần bổ sung bằng mô hình thống kê

---

## 13. Kế hoạch tiếp theo

- Cập nhật số liệu cụ thể từ pipeline
- Thêm các biểu đồ tương tác (Plotly) cho phần chiến lược
- Mở rộng phân tích mô hình dự đoán lương
- Bổ sung đánh giá mô hình bằng RMSE, MAE, $R^2$

---

## 14. Phụ lục

### 14.1 Danh mục biến quan trọng

- posting_year: năm đăng tuyển
- salary_usd: mức lương (USD)
- ai_intensity_score: mức độ AI
- automation_risk_score: rủi ro tự động hóa
- industry_ai_adoption_stage: giai đoạn áp dụng AI
- ai_job_displacement_risk: mức độ dịch chuyển việc làm
- reskilling_required: yêu cầu tái đào tạo

### 14.2 Checklist tái lập báo cáo

- Chạy toàn bộ pipeline phân tích
- Kiểm tra dữ liệu đầu vào
- Xác nhận các hình đã xuất trong thư mục [reports/figures](reports/figures)
- Cập nhật nội dung báo cáo với số liệu thực tế

### 14.3 Ghi chú

Báo cáo này là bản thử nhằm định hình cấu trúc. Khi có số liệu thực tế, cần cập nhật:

- Kết quả tổng quan định lượng
- Các bảng thống kê mô tả
- Mức độ thay đổi theo thời gian
- Các phát hiện chiến lược chi tiết
