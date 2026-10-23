# Báo cáo thực hành Phần C: Góc nhìn khung tham chiếu OWASP Secure Coding Practices (Tuần 5)

**Học phần:** 04210 Bảo mật phần mềm (Software Security)  
**Sinh viên:** Nguyễn Đoàn Huỳnh Hương  
**MSSV:** 2305CT0721  
**Lớp:** 261042100201_B  
**Tài liệu đối chiếu:** OWASP Secure Coding Practices Quick Reference Guide, phiên bản 2.0.1 (SCP)  

---

## 1. Bảng đối chiếu mười mục kiểm OWASP SCP (S1 tới S10) với ba bản vá của Tuần 5

| Mã | Mục trong SCP | Dòng kiểm tra tiếng Anh trong OWASP SCP v2.0.1 | Bản dịch tiếng Việt | Đối chiếu với mã nguồn MiniShop Tuần 5 |
| :--- | :--- | :--- | :--- | :--- |
| **S1** | Input Validation | Conduct all data validation on a trusted system (e.g., The Developer's Server). | Thực hiện toàn bộ việc kiểm tra tính hợp lệ của dữ liệu trên hệ thống tin cậy (ví dụ: máy chủ của lập trình viên). | Áp dụng tại `app.py`: Mọi logic kiểm tra và phân tích cú pháp dữ liệu gửi lên từ người dùng đều được thực thi tập trung trên máy chủ Python. |
| **S2** | Input Validation | Identify all data sources and classify them into untrusted and trusted on the system. | Nhận diện mọi nguồn dữ liệu và phân loại chúng thành nguồn không tin cậy và nguồn tin cậy trên hệ thống. | Áp dụng tại Mục 1 báo cáo Tuần 5: Các tham số biểu mẫu `username`, tham số URL `q` và phần đường dẫn `/don/<id>` đều được phân loại là dữ liệu đầu vào không tin cậy. |
| **S3** | Input Validation | Validate all data provided by the client upon receipt (allowlist validation). | Kiểm tra toàn bộ dữ liệu máy khách gửi lên ngay khi tiếp nhận (kiểm tra kiểu, độ dài, định dạng theo danh sách cho phép). | Chưa áp dụng triệt để trong MiniShop: Hệ thống mới chỉ đọc dữ liệu thô mà chưa kiểm tra độ dài tối đa hoặc cấu trúc ký tự của `q` hay `username`. |
| **S4** | Input Validation | If potentially hazardous input must be allowed, implement additional safeguards such as input encoding. | Nếu bắt buộc phải cho phép dữ liệu tiềm ẩn nguy hiểm, phải áp dụng các biện pháp bảo vệ bổ sung trước khi xử lý. | Áp dụng gián tiếp: Dữ liệu người dùng tìm kiếm có thể chứa ký tự đặc biệt, cần được xử lý an toàn tại các điểm chìm. |
| **S5** | Output Encoding | Conduct all output encoding on a trusted system (e.g., The Developer's Server). | Thực hiện toàn bộ việc mã hoá/thoát đầu ra trên hệ thống tin cậy (máy chủ). | Áp dụng tại `views.py`: Phép gọi hàm thoát ký tự `html.escape()` được thực thi hoàn toàn ở phía máy chủ Python trước khi gửi nội dung HTML về trình duyệt. |
| **S6** | Output Encoding | Utilize a standard, tested routine for each type of outbound encoding. | Sử dụng các hàm xử lý tiêu chuẩn, đã được kiểm thử kỹ lưỡng cho từng loại mã hoá đầu ra. | Áp dụng tại `views.py`: Sử dụng thư viện chuẩn `html.escape` có sẵn của ngôn ngữ Python để thoát ký tự HTML, không tự viết hàm tự tạo dễ thiếu sót. |
| **S7** | Output Encoding | Contextually encode all output of untrusted data before putting it into the operating environment (HTML Body, etc.). | Thoát/mã hoá phù hợp ngữ cảnh mọi đầu ra chứa dữ liệu không tin cậy trước khi đưa vào môi trường vận hành (thân HTML, thuộc tính,...). | **Đáp ứng bản vá HOTRO-2**: Tại hàm `search_page` trong `views.py`, tham số `keyword` được bọc qua `html.escape(keyword)` trước khi ghép vào thẻ `<b>` trong thân HTML, biến `<` thành `&lt;` và `>` thành `&gt;`. |
| **S8** | Output Encoding | Contextually sanitize all output of untrusted data to queries for subsystems such as SQL, XML, and LDAP. | Làm sạch/tham số hoá phù hợp ngữ cảnh mọi đầu ra chứa dữ liệu không tin cậy gửi tới câu truy vấn của các hệ thống con như SQL, XML, LDAP. | **Đáp ứng bản vá HOTRO-1**: Tại `find_login` và `search_products` trong `db.py`, dữ liệu người dùng không được ghép chuỗi vào câu lệnh mà được chuyển thành tham số hoá qua dấu `?`, gửi tới hệ thống con SQLite. |
| **S9** | Database Security | Use strongly typed parameterized queries. | Sử dụng các câu truy vấn tham số hoá có định kiểu mạnh. | **Đáp ứng bản vá HOTRO-1**: Trong `db.py`, câu truy vấn sử dụng ký tự chỗ giữ `?` (`conn.execute(sql, (username,))` và `conn.execute(sql, ("%" + keyword + "%",))`), tách biệt hoàn toàn giữa cấu trúc lệnh và dữ liệu. |
| **S10** | Access Control | Ensure that access control decisions are made on a trusted system; verify user ownership before allowing access. | Đảm bảo các quyết định kiểm soát truy cập được đưa ra trên hệ thống tin cậy; kiểm tra quyền sở hữu dữ liệu của người dùng trước khi cấp quyền truy cập. | **Đáp ứng bản vá HOTRO-3b**: Tại `app.py`, phương thức `_show_order` kiểm tra `order["user_id"] != user["id"]` ở phía máy chủ để đảm bảo người dùng chỉ được xem đơn hàng do chính mình tạo ra. |

---

## 2. Câu hỏi về bản vá HOTRO-3b và việc chọn mã trạng thái HTTP 404

**Câu hỏi:** *Vì sao bản vá HOTRO-3b kiểm soát truy cập ở tầng máy chủ lại chọn trả về mã trạng thái 404 (Not Found) thay vì mã trạng thái 403 (Forbidden)?*

**Trả lời:**
- Bản vá `HOTRO-3b` giải quyết lỗi IDOR (Insecure Direct Object Reference) bằng cách so sánh mã người dùng hiện tại đang đăng nhập (`user["id"]`) với trường chủ sở hữu đơn hàng (`order["user_id"]`) lưu trong cơ sở dữ liệu.
- Việc chọn trả về mã **404 Not Found** (kèm thông điệp `"Don hang khong ton tai."`) thay vì mã **403 Forbidden** là một kỹ thuật phòng thủ chủ động nhằm ngăn chặn tấn công liệt kê tài nguyên (Resource Enumeration / Information Disclosure):
  1. Nếu trả về mã 403 Forbidden, máy chủ vô tình tiết lộ cho kẻ tấn công biết rằng mã đơn hàng này **thực sự tồn tại** trên hệ thống, kẻ tấn công chỉ việc thay đổi ID từ 1 đến N để lập danh sách toàn bộ các mã đơn hàng đang có hiệu lực.
  2. Khi trả về mã 404 Not Found, phản hồi cho một đơn hàng không tồn tại và phản hồi cho một đơn hàng của người khác là hoàn toàn giống nhau. Kẻ tấn công không thể dựa vào mã trạng thái HTTP hay nội dung phản hồi để suy đoán xem đơn hàng đó có tồn tại hay không.

---

## 3. Một dòng danh mục kiểm mà MiniShop còn thiếu

- **Mục kiểm:** Input Validation (Kiểm tra tính hợp lệ dữ liệu đầu vào) – Cụ thể là dòng **S3**: *"Validate all data provided by the client upon receipt (allowlist validation)"*.
- **Phân tích thực tế trên MiniShop:**
  - Hiện tại trong `app.py`, khi tiếp nhận tham số tìm kiếm `q` tại đường dẫn `/tim`, hệ thống nhận trực tiếp mọi chuỗi ký tự mà người dùng gửi lên và đưa thẳng xuống tầng cơ sở dữ liệu qua hàm `search_products(keyword)`.
  - MiniShop hoàn toàn **chưa có cơ chế kiểm tra giới hạn độ dài** của từ khoá tìm kiếm (ví dụ: giới hạn tối đa 50 ký tự), chưa kiểm tra loại bỏ các ký tự đặc biệt không hợp lệ trong tên sản phẩm, và chưa áp dụng biểu thức chính quy (Regex) để lọc các chuỗi rác quá dài có thể gây quá tải bộ nhớ hoặc làm giảm hiệu năng tìm kiếm của SQLite.
  - Tương tự, tại chức năng xem đơn hàng `/don/<id>`, hệ thống chỉ ép kiểu `int(path[len("/don/"):])` mà chưa kiểm tra giá trị `order_id` có phải là số nguyên dương hợp lệ (order_id > 0) hay không trước khi gửi truy vấn vào cơ sở dữ liệu.
