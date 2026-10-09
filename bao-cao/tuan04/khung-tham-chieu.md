# Báo cáo Phần C: Góc nhìn khung tham chiếu OWASP SAMM và NIST SSDF (Tuần 4)

**Học phần:** 04210 Bảo mật phần mềm (Software Security)  
**Sinh viên:** Nguyễn Đoàn Huỳnh Hương - MSSV: 2305CT0721  
**Lớp:** 261042100201_B  

---

## Ô 1: Đánh giá ba tiêu chí chất lượng hoạt động "Perform basic threat modeling" (OWASP SAMM v2 - Design > Threat Assessment > Threat Modeling, Level 1)

**Câu hỏi đánh giá của SAMM:**  
*"Do you identify and manage architectural design flaws with threat modeling?"*

**Ba tiêu chí chất lượng và bằng chứng trong kho MiniShop:**
1. *Tiêu chí 1: Nhận diện và lập sơ đồ kiến trúc các thành phần hệ thống cùng các ranh giới tin cậy.*  
   - **Bằng chứng:** Tệp `bao-cao/tuan04/so-do-luong-du-lieu.md` tại Mục 1 đã mô hình hóa đầy đủ 12 phần tử (3 tác nhân ngoài, 7 tiến trình, 2 kho dữ liệu), 11 luồng dữ liệu và 3 ranh giới tin cậy rõ ràng.  
   - **Tự đánh giá:** Đạt.
2. *Tiêu chí 2: Áp dụng phương pháp phân tích mối đe dọa có cấu trúc (như STRIDE) để chỉ ra các rủi ro thiết kế.*  
   - **Bằng chứng:** Tệp `bao-cao/tuan04/so-do-luong-du-lieu.md` tại Mục 2 đã lập bảng phân tích STRIDE 12 hàng cho từng phần tử, chỉ ra rủi ro leo thang quyền tại trang quản trị (HOTRO-3a) và đề xuất các giải pháp khắc phục.  
   - **Tự đánh giá:** Đạt.
3. *Tiêu chí 3: Quy trình mô hình hóa mối đe dọa được thực hiện định kỳ và tích hợp chính thức vào quy trình phát triển phần mềm (SDLC) của nhóm.*  
   - **Bằng chứng:** Trong kho MiniShop, việc lập sơ đồ và bảng STRIDE mới chỉ dừng lại ở bài thực hành tuần 4, chưa có quy trình kiểm tra tự động hay chính sách bắt buộc cập nhật Threat Model trong quy trình CI/CD cho mọi tính năng mới.  
   - **Tự đánh giá:** Chưa đạt.

**Câu trả lời SAMM cho MiniShop:**  
**No** (Theo quy tắc nghiêm ngặt của OWASP SAMM: một hoạt động chỉ được trả lời "Yes" khi nhóm đáp ứng đầy đủ tất cả các tiêu chí chất lượng được định nghĩa ở mức đó).

---

## Ô 2: Hai nguyên tắc an toàn kiến trúc của SAMM (Design > Secure Architecture)

1. **Nguyên tắc 1: Complete Mediation (Trung gian đầy đủ - Mọi truy cập đều phải qua kiểm soát)**  
   - *Gắn với phần tử trên sơ đồ:* Tiến trình `( P5 ) Trang quan tri`.  
   - *Gắn với công việc tuần này:* Bản vá `HOTRO-3a` trong `app.py`. Trước đây hệ thống vi phạm nguyên tắc này khi chỉ ẩn liên kết `/admin` trên giao diện người dùng thường mà không kiểm tra quyền ở máy chủ. Bản vá đã áp dụng nguyên tắc Trung gian đầy đủ bằng cách chặn và kiểm tra vai trò admin ở phía máy chủ ngay tại cửa ngõ phục vụ trang quản trị, từ chối mọi yêu cầu không có thẩm quyền với mã HTTP 403.

2. **Nguyên tắc 2: Do Not Trust User Input (Không tin cậy dữ liệu đầu vào từ phía người dùng)**  
   - *Gắn với phần tử trên sơ đồ:* Tiến trình `( P1 ) Bo dinh tuyen HTTP` và `( P3 ) Doc nguoi dung hien tai` (nhận dữ liệu từ Luồng `L1` vượt qua Ranh giới tin cậy 1).  
   - *Gắn với công việc tuần này:* Bài thực hành Phần A (OpenSSF Deserialization Lab). Dữ liệu gửi lên từ cookie nằm ngoài ranh giới tin cậy nên tuyệt đối không được đưa trực tiếp vào hàm thực thi mã `eval()`, mà phải được xử lý bằng bộ đọc dữ liệu thuần túy `JSON.parse()` kết hợp kiểm tra chặt chẽ kiểu dữ liệu (`typeof == 'string'`) và giới hạn độ dài (`< 20`) trước khi sử dụng.

---

## Ô 3: Liên hệ với nhiệm vụ PW.1.1 của NIST SSDF 1.1

Hoạt động xây dựng sơ đồ luồng dữ liệu (DFD), phân tích nguy cơ bằng ma trận STRIDE và xây dựng bảng truy vết kiểm thử trong tuần 4 trực tiếp thực hiện nhiệm vụ **PW.1.1** của **NIST SSDF 1.1** (*"Use forms of risk modeling – such as threat modeling – to identify design vulnerabilities and prioritize mitigation efforts"*) bằng việc phát hiện khuyết điểm thiết kế kiến trúc về kiểm soát truy cập (CWE-862 / HOTRO-3a), áp dụng bản vá kiểm tra quyền phía máy chủ và thiết lập các ca kiểm thử hồi quy tự động nhằm ngăn ngừa lỗ hổng tái phát.

---

## Ô 4: Sự kiện kích hoạt việc vẽ lại sơ đồ luồng dữ liệu (DFD)

Một sự kiện điển hình khiến sơ đồ DFD của MiniShop phải vẽ lại là **khi hệ thống tích hợp thêm cổng thanh toán trực tuyến của bên thứ ba (Third-party Payment Gateway)**: sự kiện này làm thay đổi cấu trúc luồng dữ liệu cốt lõi của ứng dụng, đòi hỏi bổ sung thêm tác nhân ngoài mới (Cổng thanh toán), mở thêm các tiến trình xử lý giao dịch và webhook (`IPN - Instant Payment Notification`), hình thành thêm ranh giới tin cậy mới giữa MiniShop và hệ thống thanh toán ngoài mạng, cũng như làm nảy sinh các nguy cơ tấn công giả mạo (Spoofing) và sửa đổi giao dịch (Tampering) mới cần phải mô hình hóa lại từ đầu.
