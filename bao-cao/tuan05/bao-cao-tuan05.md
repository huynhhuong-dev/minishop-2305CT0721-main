# Báo cáo thực hành Tuần 5: Ba bản vá cho lỗi chèn mã và lỗi diễn giải sai dữ liệu

**Học phần:** 04210 Bảo mật phần mềm (Software Security)  
**Sinh viên:** Nguyễn Đoàn Huỳnh Hương  
**MSSV:** 2305CT0721  
**Lớp:** 261042100201_B  

---

## 1. Bốn đường đi của dữ liệu (Mục 4.2)

### Đường đi 1: Tham số `username` của biểu mẫu đăng nhập tới bộ diễn giải câu lệnh của SQLite
- **Bước 1.** `app.py`, dòng 180: Phương thức `self._read_form()` đọc dữ liệu biểu mẫu gửi lên từ yêu cầu HTTP POST tại đường dẫn `/login`.
- **Bước 2.** `app.py`, dòng 181: Chương trình lấy giá trị của tham số `username` do người dùng nhập từ từ điển dữ liệu form: `username = form.get("username", [""])[0]`.
- **Bước 3.** `app.py`, dòng 183: Giá trị `username` được truyền trực tiếp làm đối số đầu vào cho hàm xác thực tài khoản `db.find_login(username, password)`.
- **Bước 4.** `db.py`, dòng 50: Trước bản vá, giá trị `username` được nối trực tiếp vào câu lệnh SQL bằng phép cộng chuỗi: `sql = "SELECT * FROM users WHERE username = '" + username + "'"`.
- **Bước 5.** `db.py`, dòng 51: Chuỗi câu lệnh SQL hoàn chỉnh sau khi ghép được giao cho phương thức `conn.execute(sql)` để bộ diễn giải câu lệnh của SQLite phân tích cú pháp và thực thi.

---

### Đường đi 2: Tham số `q` của địa chỉ URL tới bộ diễn giải câu lệnh của SQLite
- **Bước 1.** `app.py`, dòng 107: Hàm `urlparse(self.path)` tách địa chỉ yêu cầu HTTP GET thành các phần cấu thành (path, query,...).
- **Bước 2.** `app.py`, dòng 109: Hàm `parse_qs(parsed.query, keep_blank_values=True)` phân tích chuỗi truy vấn URL thành cặp tên và giá trị tham số.
- **Bước 3.** `app.py`, dòng 124: Chương trình lấy giá trị của tham số tìm kiếm `q` do người gửi yêu cầu đặt: `keyword = query.get("q", [""])[0]`.
- **Bước 4.** `app.py`, dòng 125: Giá trị `keyword` được truyền làm đối số vào hàm tra cứu cơ sở dữ liệu `db.search_products(keyword)`.
- **Bước 5.** `db.py`, dòng 65: Trước bản vá, giá trị `keyword` được nối trực tiếp vào văn bản câu lệnh bằng phép cộng chuỗi: `sql = "SELECT * FROM products WHERE name LIKE '%" + keyword + "%' ORDER BY id"`.
- **Bước 6.** `db.py`, dòng 66: Chuỗi truy vấn hoàn chỉnh được giao cho bộ diễn giải câu lệnh của SQLite phân tích và thực thi qua `conn.execute(sql).fetchall()`.

---

### Đường đi 3: Tham số `q` của địa chỉ URL tới bộ dựng trang của trình duyệt
- **Bước 1.** `app.py`, dòng 107: Hàm `urlparse(self.path)` tách địa chỉ URL nhận được từ yêu cầu HTTP của người dùng.
- **Bước 2.** `app.py`, dòng 109: Hàm `parse_qs` trích xuất các tham số trên query string của URL.
- **Bước 3.** `app.py`, dòng 124: Chương trình lấy giá trị của tham số `q` từ người dùng gửi lên: `keyword = query.get("q", [""])[0]`.
- **Bước 4.** `app.py`, dòng 125: Giá trị `keyword` được truyền vào hàm kết xuất giao diện HTML `views.search_page(keyword, ...)`.
- **Bước 5.** `views.py`, dòng 97: Trước bản vá, biến `keyword` được nối trực tiếp vào chuỗi HTML hiển thị bằng phép cộng chuỗi: `body = "<p>Ket qua cho tu khoa: <b>" + keyword + "</b></p>"` mà không qua bước thoát ký tự an toàn.
- **Bước 6.** `app.py`, dòng 125: Thân trang HTML chứa chuỗi nguyên vẹn được gửi trả về máy khách qua `self._send(200, ...)`; tại đây, bộ dựng trang (HTML/DOM parser và JavaScript engine) của trình duyệt web sẽ trực tiếp diễn giải và thực thi các thẻ kịch bản.

---

### Đường đi 4: Đoạn nằm sau `/don/` trong đường dẫn URL tới trang chi tiết đơn hàng gửi về trình duyệt
- **Bước 1.** `app.py`, dòng 107: Hàm `urlparse(self.path)` tách địa chỉ yêu cầu và lấy thành phần đường dẫn `path`.
- **Bước 2.** `app.py`, dòng 136-137: Bộ định tuyến kiểm tra tiền tố `path.startswith("/don/")` và gọi phương thức xử lý `self._show_order(path, user)`.
- **Bước 3.** `app.py`, dòng 148: Chương trình cắt chuỗi đường dẫn để lấy mã định danh đơn hàng dạng số: `order_id = int(path[len("/don/"):])`.
- **Bước 4.** `app.py`, dòng 149: Hàm `db.get_order(order_id)` được gọi để truy vấn bản ghi đơn hàng từ cơ sở dữ liệu SQLite theo ID.
- **Bước 5.** `app.py`, dòng 153: Trước bản vá, hệ thống chỉ kiểm tra `order is None` mà bỏ qua việc so sánh quyền sở hữu `order["user_id"] == user["id"]`, gửi bản ghi vào hàm tạo trang `views.order_detail_page(order, user)`.
- **Bước 6.** `app.py`, dòng 153: Máy chủ gửi phản hồi HTTP với mã trạng thái 200 kèm toàn bộ thông tin đơn hàng về trình duyệt người dùng qua `self._send(200, ...)`.

---

## 2. Bảng chứng minh tính hồi quy (Mục 7.2)

Khi gỡ bỏ từng bản vá (khôi phục lại đoạn mã gốc chưa sửa) và chạy bộ kiểm thử tự động `python -m unittest discover tests`, các bài kiểm thử tương ứng chuyển sang trạng thái thất bại (báo đỏ) như sau:

| Nhãn lỗ hổng | Tên bài kiểm thử thất bại | Dòng thông báo lỗi rút gọn khi gỡ bản vá |
| :--- | :--- | :--- |
| **HOTRO-1** (đăng nhập, `db.py`) | `test_01_find_login_sql_injection` | `AssertionError: <sqlite3.Row object ...> is not None` |
| **HOTRO-1** (tìm kiếm, `db.py`) | `test_02_search_products_sql_injection` | `AssertionError: Lists differ: [<sqlite3.Row object ...>] != [] (First list contains 12 additional elements)` |
| **HOTRO-2** (kết quả tìm kiếm, `views.py`) | `test_03_search_page_xss` | `AssertionError: '<script>alert(1)</script>' unexpectedly found in ...` |
| **HOTRO-3b** (chi tiết đơn hàng, `app.py`) | `test_04_idor_order_detail` | `AssertionError: 200 != 404` |

*Ghi chú:* Sau khi áp dụng đầy đủ cả ba bản vá trở lại, toàn bộ 19 bài kiểm thử đều chuyển sang màu xanh (`OK`).

---

## 3. Vị trí thứ hai cùng lớp lỗi trong MiniShop (Mục 7.3)

- **Tên tệp:** `db.py`
- **Số dòng:** Dòng 89 – 90
- **Dòng mã trích nguyên văn:**
  ```python
  sql = "SELECT o.*, p.name AS product_name FROM orders o JOIN products p ON o.product_id = p.id WHERE o.id = ?"
  return conn.execute(sql, (order_id,)).fetchone()
  ```
- **Lớp lỗi:** Chèn câu lệnh SQL (SQL Injection – cùng lớp lỗi với `HOTRO-1`).
- **Tình trạng an toàn:** Vị trí này **ĐÃ AN TOÀN**.
- **Giải thích:** Câu lệnh truy vấn dữ liệu đơn hàng theo ID không dùng phép nối chuỗi dữ liệu người dùng mà sử dụng ký tự chỗ giữ (placeholder) `?` và truyền tham số `(order_id,)` riêng biệt vào hàm `conn.execute()`. Cơ chế này buộc trình điều khiển SQLite coi giá trị đầu vào thuần túy là dữ liệu kiểu số/chuỗi, ngăn chặn hoàn toàn nguy cơ kẻ tấn công chèn các ký tự điều khiển cú pháp SQL (như dấu nháy đơn `'` hoặc từ khóa `UNION`, `OR`) để thay đổi cấu trúc câu truy vấn.

---

## 4. Biện luận chọn mã trạng thái 404 thay vì 403 cho trang xem đơn hàng (CLO4)

Tại phương thức `_show_order` trong `app.py`, khi người dùng gửi yêu cầu xem một đơn hàng không thuộc quyền sở hữu của mình, hệ thống trả về mã trạng thái **404 Not Found** cùng thông báo `"Don hang khong ton tai."` thay vì mã **403 Forbidden** vì các lý do sau:

1. **Ngăn chặn tấn công dò quét mã đơn hàng (Information Disclosure / Resource Enumeration):**
   - Nếu trả về mã `403 Forbidden`, máy chủ đã gián tiếp xác nhận cho kẻ tấn công biết rằng đơn hàng có mã ID này **thực sự tồn tại** trên hệ thống, chỉ là tài khoản hiện tại không có quyền xem. Kẻ tấn công có thể viết kịch bản tự động duyệt qua các số nguyên từ 1 đến N để lập danh sách toàn bộ các mã đơn hàng đang tồn tại, qua đó ước lượng được số lượng giao dịch, doanh số và mật độ hoạt động kinh doanh của cửa hàng.
   - Khi trả về mã `404 Not Found`, phản hồi của hệ thống đối với trường hợp đơn hàng thực sự không tồn tại và trường hợp đơn hàng của khách hàng khác là hoàn toàn giống nhau. Kẻ tấn công không thể phân biệt được ID nào có thật và ID nào là giả lập.

2. **Áp dụng nguyên tắc phòng thủ sâu (Defense in Depth):**
   - Về mặt logic nghiệp vụ, trong phạm vi không gian làm việc của một khách hàng cá nhân, những đơn hàng của người khác vốn không thuộc về "vùng hiển thị" của họ, do đó việc coi chúng là "không tồn tại" (404) đối với người dùng đó là hoàn toàn hợp lý và an toàn hơn hẳn việc thừa nhận sự tồn tại nhưng từ chối truy cập (403).
