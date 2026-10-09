# Sơ đồ luồng dữ liệu của MiniShop và Phân tích mối đe dọa (Tuần 4)

**Học phần:** 04210 Bảo mật phần mềm (Software Security)  
**Sinh viên:** Nguyễn Đoàn Huỳnh Hương - MSSV: 2305CT0721  
**Lớp:** 261042100201_B  

---

## 1. Sơ đồ luồng dữ liệu đầy đủ (DFD - Level 1)

### 1.1. Sơ đồ dạng khối ký tự (Text-based DFD)

```text
[E1] Nguoi dung thuong -------(L1)------->|
[E2] Quan tri vien -----------(L2)------->| === RANH GIOI 1: Trinh duyet - May chu (Internet/Mang) ===
[E3] Khach chua dang nhap ----(L3)------->|
                                          v
                               ( P1 ) Bo dinh tuyen HTTP
                                      |          \
                                    (L4)         (L5)
                                      v            v
             ( P3 ) Doc nguoi dung        ( P2 ) Xu ly dang nhap
                    hien tai                       |
                    |   ^                         (L6)
                (L7)|   |(L8)                      v
                    v   |         ( P7 ) Sinh va ky ma phien [HOTRO-5, HOTRO-8]
             [ D2 ] Kho phien                      |
                    trong bo nho                   |
                    [HOTRO-8]                      |
================================== RANH GIOI 2: Phan quyen & Dieu huong nghiep vu =================
        |                                          |                                      |
        v                                          v                                      v
 ( P4 ) Tim kiem                          ( P5 ) Trang quan tri                 ( P6 ) Chi tiet don hang
        san pham                                 [HOTRO-3a]                            [HOTRO-3b]
        |                                          |                                      |
       (L9)                                      (L10)                                  (L11)
        \                                          |                                      /
================================== RANH GIOI 3: Ung dung - He luu tru SQLite ======================
         \                                         |                                     /
          v                                        v                                    v
                               [ D1 ] Tep co so du lieu (SQLite)
                                      bang users, products, orders
                                      [HOTRO-4]
```

### 1.2. Danh sách 12 phần tử trên sơ đồ
- **3 Tác nhân ngoài (External Entities):**
  1. `[E1] Người dùng thường`: Người dùng đã đăng nhập với tài khoản có vai trò thông thường (role: `user`).
  2. `[E2] Quản trị viên`: Người dùng đã đăng nhập với tài khoản quản trị hệ thống (role: `admin`).
  3. `[E3] Khách chưa đăng nhập`: Người dùng ẩn danh truy cập xem sản phẩm hoặc trang đăng nhập.
- **7 Tiến trình (Processes):**
  1. `( P1 ) Bộ định tuyến HTTP`: Tiếp nhận yêu cầu HTTP GET/POST, phân tích đường dẫn và điều phối đến các hàm xử lý.
  2. `( P2 ) Xử lý đăng nhập`: Xác thực thông tin đăng nhập từ biểu mẫu và kích hoạt việc tạo phiên làm việc mới.
  3. `( P3 ) Đọc người dùng hiện tại`: Đọc cookie phiên từ yêu cầu, kiểm tra chữ ký và truy vấn mã người dùng tương ứng.
  4. `( P4 ) Tìm kiếm sản phẩm`: Tiếp nhận từ khóa tìm kiếm và truy vấn danh sách sản phẩm tương ứng.
  5. `( P5 ) Trang quản trị`: Xử lý hiển thị danh sách người dùng và các chức năng quản trị hệ thống (`HOTRO-3a`).
  6. `( P6 ) Chi tiết đơn hàng`: Xử lý hiển thị thông tin chi tiết một đơn hàng cụ thể theo mã đơn (`HOTRO-3b`).
  7. `( P7 ) Sinh và ký mã phiên`: Khởi tạo mã định danh phiên ngẫu nhiên an toàn và ký chữ ký HMAC (`HOTRO-5`, `HOTRO-8`).
- **2 Kho dữ liệu (Data Stores):**
  1. `[ D1 ] Tệp cơ sở dữ liệu (SQLite)`: Lưu trữ dữ liệu lâu dài gồm các bảng `users`, `products`, `orders` (`HOTRO-4`).
  2. `[ D2 ] Kho phiên trong bộ nhớ`: Từ điển `SESSIONS` lưu trong RAM ánh xạ mã phiên (`sid`) với mã người dùng (`user_id`).

### 1.3. Danh sách 11 luồng dữ liệu (Data Flows)
- `L1 (E1 -> P1)`: Yêu cầu HTTP kèm cookie phiên của người dùng thường.
- `L2 (E2 -> P1)`: Yêu cầu HTTP kèm cookie phiên của quản trị viên.
- `L3 (E3 -> P1)`: Yêu cầu HTTP không có cookie phiên của khách vãng lai.
- `L4 (P1 -> P3)`: Chuỗi cookie đọc từ tiêu đề HTTP chuyển sang hàm nhận diện người dùng.
- `L5 (P1 -> P2)`: Tên đăng nhập và mật khẩu từ biểu mẫu gửi lên chuyển sang hàm xử lý đăng nhập.
- `L6 (P2 -> P7)`: Yêu cầu sinh một mã phiên mới sau khi xác thực danh tính thành công.
- `L7 (P3 -> D2)`: Tra mã phiên để lấy mã người dùng trong từ điển phiên.
- `L8 (D2 -> P3)`: Trả về mã người dùng ứng với mã phiên được tra cứu.
- `L9 (P4 -> D1)`: Câu truy vấn SQL tìm kiếm sản phẩm theo từ khóa.
- `L10 (P5 -> D1)`: Câu truy vấn SQL lấy toàn bộ danh sách người dùng cho trang quản trị.
- `L11 (P6 -> D1)`: Câu truy vấn SQL lấy thông tin chi tiết một đơn hàng cụ thể.

### 1.4. Ba ranh giới tin cậy (Trust Boundaries)
1. **RANH GIỚI 1: Trình duyệt - Máy chủ (Internet/Mạng)**
   - *Lý do:* Phân tách môi trường mạng bên ngoài và máy khách không tin cậy (E1, E2, E3) với máy chủ nội bộ MiniShop (P1). Dữ liệu vượt qua ranh giới này (HTTP request, parameters, cookies) đều có thể bị kẻ tấn công thao túng hoặc làm giả.
2. **RANH GIỚI 2: Phân quyền & Điều hướng nghiệp vụ**
   - *Lý do:* Phân tách tầng điều hướng/quản lý phiên chung (P1, P3) với các tiến trình nghiệp vụ yêu cầu quyền hạn riêng biệt (P5 yêu cầu vai trò admin; P6 yêu cầu quyền sở hữu đơn hàng). Cần có cơ chế kiểm tra ủy quyền (Complete Mediation) tại ranh giới này.
3. **RANH GIỚI 3: Ứng dụng - Hệ lưu trữ SQLite**
   - *Lý do:* Phân tách không gian bộ nhớ của tiến trình ứng dụng Python (P4, P5, P6) với tầng lưu trữ tệp tin bền vững trên hệ điều hành (D1). Các truy vấn phải được tham số hóa để bảo đảm an toàn dữ liệu trên đĩa.

### 1.5. Vị trí 4 nhãn lỗ hổng trên sơ đồ
- **HOTRO-3a:** Đặt tại tiến trình `( P5 ) Trang quan tri` (thiếu kiểm tra vai trò admin ở phía máy chủ trước khi trả về dữ liệu quản trị).
- **HOTRO-3b:** Đặt tại luồng `L11` và tiến trình `( P6 ) Chi tiet don hang` (chưa kiểm tra quyền sở hữu đơn hàng của người dùng đang đăng nhập).
- **HOTRO-5:** Đặt tại tiến trình `( P7 ) Sinh va ky ma phien` (khoá ký phiên SESSION_KEY trước đây bị gán cứng trong mã nguồn).
- **HOTRO-8:** Đặt tại tiến trình `( P7 ) Sinh va ky ma phien` và `[ D2 ] Kho phien trong bo nho` (mã phiên sid trước đây là số nguyên tự tăng tuần tự).

---

## 2. Bảng phân tích mối đe dọa STRIDE (12 hàng)

Quy tắc rút ngắn áp dụng theo Mục 7.1:
- Tác nhân ngoài: S, R.
- Tiến trình: S, T, R, I, D, E.
- Kho dữ liệu: T, I, D (thêm R nếu là kho nhật ký kiểm toán).

| Phần tử | S (Spoofing) | T (Tampering) | R (Repudiation) | I (Info Disclosure) | D (Denial of Service) | E (Elevation of Privilege) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **E1 Người dùng thường** | **CO:** Kẻ tấn công giả mạo tài khoản người dùng thường bằng cách đánh cắp mật khẩu hoặc cookie phiên. | | **KHONG:** Người dùng không thể chối bỏ các yêu cầu đã gửi nếu hệ thống ghi log địa chỉ IP và hành động kèm mã phiên hợp lệ. | | | |
| **E2 Quản trị viên** | **CO:** Kẻ tấn công giả mạo danh tính quản trị viên do đoán được mật khẩu quản trị hoặc chiếm quyền phiên admin. | | **KHONG:** Hành động của quản trị viên được ghi nhận với tài khoản đặc quyền, không thể chối bỏ nếu có lưu vết. | | | |
| **E3 Khách chưa đăng nhập** | **KHONG:** Khách vãng lai chưa có danh tính trong hệ thống nên không thể giả danh một phiên hợp lệ đã định danh. | | **KHONG:** Khách chưa đăng nhập chỉ thực hiện các yêu cầu nặc danh xem công khai, không có cam kết danh tính để chối bỏ. | | | |
| **P1 Bộ định tuyến HTTP** | **KHONG:** Tiến trình P1 chạy nội bộ trên máy chủ nên kẻ tấn công không thể mạo danh chính hàm định tuyến này. | **CO:** Kẻ tấn công sửa đổi tiêu đề HTTP hoặc URL nhằm vượt qua các quy tắc định tuyến của máy chủ. | **KHONG:** Bản thân hàm định tuyến chỉ chuyển tiếp yêu cầu, không thực hiện hành vi nghiệp vụ để chối bỏ. | **CO:** P1 có thể làm lộ thông tin nhạy cảm qua thông báo lỗi chi tiết khi xảy ra ngoại lệ chưa xử lý. | **CO:** Bị quá tải từ chối dịch vụ nếu kẻ tấn công gửi lượng lớn yêu cầu HTTP liên tục làm nghẽn tiến trình. | **KHONG:** P1 chỉ thực hiện chuyển hướng đường dẫn cơ bản, bản thân nó không tự cấp thêm đặc quyền nào. |
| **P2 Xử lý đăng nhập** | **CO:** Kẻ tấn công gửi thông tin đăng nhập dò quét brute-force để giả mạo người dùng hợp lệ. | **CO:** Dữ liệu biểu mẫu POST bị sửa đổi trên đường truyền nếu không sử dụng kết nối HTTPS mã hóa. | **KHONG:** Tiến trình xác thực trực tiếp đối chiếu mật khẩu với CSDL, không thể chối bỏ kết quả xác thực. | **CO:** Thông báo đăng nhập sai có thể làm lộ việc tài khoản có tồn tại hay không trong hệ thống. | **CO:** Kẻ tấn công gửi liên tục các yêu cầu đăng nhập khiến máy chủ tốn tài nguyên băm mật khẩu gây DoS. | **KHONG:** P2 chỉ thực hiện xác thực thông tin, không gán sai vai trò nếu CSDL lưu đúng vai trò người dùng. |
| **P3 Đọc người dùng hiện tại** | **CO:** Kẻ tấn công tạo cookie phiên giả mạo nếu đoán được thuật toán sinh mã phiên hoặc khóa bí mật. | **CO:** Giá trị cookie trên trình duyệt bị sửa đổi trước khi gửi lên máy chủ. | **KHONG:** Tiến trình chỉ đọc và kiểm tra chữ ký cookie, không phát sinh hành động có thể chối bỏ. | **KHONG:** Hàm chỉ trả về đối tượng người dùng nội bộ cho tiến trình khác, không in trực tiếp ra bên ngoài. | **KHONG:** Việc giải mã và tra cứu từ điển trong RAM diễn ra rất nhanh với độ phức tạp O(1), khó gây cạn kiệt tài nguyên. | **CO:** Nếu hàm kiểm tra chữ ký bị lỗi logic, kẻ tấn công có thể mạo danh người dùng có vai trò cao hơn. |
| **P4 Tìm kiếm sản phẩm** | **KHONG:** P4 là hàm nội bộ phục vụ tìm kiếm, không mang danh tính người dùng để bị mạo danh. | **CO:** Tham số tìm kiếm chứa ký tự đặc biệt có thể phá vỡ logic câu lệnh SQL nếu không được tham số hóa. | **KHONG:** Tìm kiếm là thao tác chỉ đọc dữ liệu công khai, không phát sinh giao dịch cần chống chối bỏ. | **CO:** Có thể làm lộ các sản phẩm ẩn hoặc dữ liệu nội bộ nếu câu truy vấn SQL bị tiêm mã độc (SQLi). | **CO:** Từ khóa tìm kiếm phức tạp với ký tự đại diện (`%`, `_`) có thể khiến câu lệnh SQL quét toàn bảng gây chậm máy chủ. | **KHONG:** Tiến trình tìm kiếm chỉ trả về danh sách sản phẩm, không cung cấp cơ chế leo thang đặc quyền. |
| **P5 Trang quản trị** | **KHONG:** P5 là hàm kết xuất giao diện quản trị nội bộ trên máy chủ, không bị mạo danh phần tử. | **CO:** Kẻ tấn công can thiệp sửa đổi các tham số quản trị nếu không kiểm tra tính toàn vẹn dữ liệu. | **KHONG:** Các hành động quản trị hệ thống đều được thực thi theo quyền hạn xác định, không thể chối bỏ. | **CO:** Làm lộ toàn bộ danh sách tài khoản, vai trò và thông tin cá nhân của mọi người dùng nếu bị truy cập trái phép. | **CO:** Trang quản trị nạp toàn bộ danh sách người dùng cùng lúc vào bộ nhớ, gây chậm máy chủ khi số lượng user lớn. | **CO:** [HOTRO-3a] Người dùng thường truy cập trực tiếp URL `/admin` và xem được dữ liệu quản trị do thiếu kiểm tra vai trò. |
| **P6 Chi tiết đơn hàng** | **KHONG:** P6 là hàm nội bộ xử lý đơn hàng, không mang danh tính người gửi. | **CO:** Kẻ tấn công thay đổi mã đơn hàng trên đường dẫn (`/don/<id>`) để yêu cầu đơn hàng khác. | **KHONG:** Thao tác chỉ xem chi tiết đơn hàng đã đặt trước đó, không phát sinh giao dịch mới cần chống chối bỏ. | **CO:** [HOTRO-3b] Lộ thông tin đơn hàng của người khác khi truy cập trái phép qua tham số ID (lỗ hổng IDOR). | **KHONG:** Việc đọc chi tiết một đơn hàng theo khóa chính diễn ra tức thì, khó gây tê liệt hệ thống. | **CO:** Người dùng thường có thể xem và can thiệp vào đơn hàng của người dùng khác hoặc của quản trị viên. |
| **P7 Sinh và ký mã phiên** | **CO:** [HOTRO-8] Kẻ tấn công đoán được mã phiên tiếp theo nếu mã phiên được sinh tuần tự bằng số tự tăng. | **CO:** [HOTRO-5] Kẻ tấn công tự làm giả chữ ký phiên HMAC nếu khóa bí mật SESSION_KEY bị lộ hoặc cố định. | **KHONG:** Tiến trình sinh phiên theo quy tắc mật mã học khách quan, không thể chối bỏ mã phiên đã sinh. | **CO:** Khóa ký phiên có thể bị lộ nếu lưu cố định trong mã nguồn đưa lên kho công khai. | **KHONG:** Thao tác sinh chuỗi ngẫu nhiên bằng thư viện mật mã tiêu tốn rất ít CPU, không gây cạn kiệt tài nguyên. | **CO:** Kẻ tấn công tạo phiên giả mang quyền quản trị viên nếu làm chủ được cơ chế sinh và ký mã phiên. |
| **D1 Tệp CSDL (SQLite)** | | **CO:** Kẻ tấn công có quyền ghi tệp hoặc tiêm SQL có thể chỉnh sửa số dư, giá sản phẩm, vai trò người dùng. | **KHONG:** Tệp CSDL SQLite thuần túy lưu trữ bảng dữ liệu, không phải kho nhật ký kiểm toán (audit log). | **CO:** [HOTRO-4] Kẻ tấn công chiếm được tệp CSDL sẽ đọc được mật khẩu người dùng nếu mật khẩu không được băm có muối. | **CO:** Khóa tệp SQLite do truy vấn nặng hoặc làm đầy dung lượng đĩa cứng khiến ứng dụng không thể ghi thêm. | |
| **D2 Kho phiên trong bộ nhớ** | | **CO:** Kẻ tấn công can thiệp vào bộ nhớ tiến trình để sửa đổi cặp ánh xạ `sid -> user_id`. | **KHONG:** Từ điển `SESSIONS` chỉ lưu phiên làm việc tạm thời trong RAM, không lưu lịch sử hành vi nên không phải kho nhật ký. | **CO:** Rò rỉ dữ liệu phiên trong bộ nhớ nếu tiến trình bị đổ bộ nhớ (memory dump). | **CO:** Kẻ tấn công tạo vô số phiên làm việc ảo làm tràn bộ nhớ RAM (Memory Exhaustion DoS). | |

---

## 3. Bảng truy vết bốn cột (Traceability Matrix)

Bảng truy vết kết nối từ mối đe dọa trên sơ đồ kiến trúc tới yêu cầu an toàn, mã nguồn bản vá và bộ kiểm thử hồi quy:

| Mối đe dọa (từ bảng STRIDE) | Yêu cầu an toàn (từ Tuần 2) | Bản vá: tệp và mô tả dòng mã | Bài kiểm thử hồi quy: tên lớp |
| :--- | :--- | :--- | :--- |
| **T & I tại [D1] Tệp CSDL**<br>Lộ mật khẩu người dùng dạng rõ hoặc bị tra ngược bằng bảng băm cầu vồng (Rainbow table) khi tệp SQLite bị rò rỉ. | **YC-04**<br>Mật khẩu người dùng trong CSDL phải được băm bằng thuật toán an toàn, có muối ngẫu nhiên độ dài tối thiểu 16 byte và số vòng lặp đủ lớn. | `db.py`: Hàm `hash_password` áp dụng thuật toán `hashlib.pbkdf2_hmac` với SHA-256, 600.000 vòng lặp và muối sinh ngẫu nhiên từ `os.urandom(16)`. | `KiemThuHoTro4`<br>(trong `tests/test_tuan03.py`) |
| **S & T tại (P7) Sinh và ký mã phiên**<br>Kẻ tấn công giả mạo chữ ký HMAC của cookie phiên do khóa bí mật ký phiên bị ghi cứng trong mã nguồn. | **YC-05**<br>Khóa bí mật ký phiên (SESSION_KEY) phải được nạp từ biến môi trường của hệ thống hoặc sinh ngẫu nhiên an toàn, không được ghi cứng trong mã nguồn. | `app.py`: Biến `SESSION_KEY` được đọc từ biến môi trường `MINISHOP_SESSION_KEY`, nếu không có thì tự động sinh ngẫu nhiên 32 byte an toàn bằng `secrets.token_hex(32)`. | `KiemThuHoTro5`<br>(trong `tests/test_tuan03.py`) |
| **S tại (P7) & [D2] Kho phiên**<br>Kẻ tấn công đoán trước được mã định danh phiên (session ID) của người dùng khác do mã phiên là số nguyên tự tăng tuần tự. | **YC-08**<br>Mã định danh phiên làm việc phải là chuỗi ngẫu nhiên có độ dài và entropy cao, sử dụng bộ sinh ngẫu nhiên an toàn mật mã học để không thể đoán trước. | `app.py`: Hàm `_new_session_id` được sửa đổi để sinh chuỗi ngẫu nhiên 16 byte thập lục phân bằng `secrets.token_hex(16)` thay vì biến đếm `_next_sid`. | `KiemThuHoTro8`<br>(trong `tests/test_tuan03.py`) |
| **E tại (P5) Trang quản trị**<br>Người dùng có vai trò thông thường leo thang đặc quyền xem thông tin quản trị viên do hệ thống chỉ ẩn liên kết giao diện mà không kiểm tra quyền ở máy chủ. | **YC-03a**<br>Máy chủ phải thực hiện kiểm tra quyền (vai trò quản trị viên) trước khi xử lý và trả về nội dung trang quản trị `/admin`, từ chối với mã HTTP 403 nếu không đủ quyền. | `app.py`: Phương thức `_show_admin`, thêm 3 dòng kiểm tra vai trò: `if user["role"] != "admin": self._send(403, views.message_page("Tu choi", "Ban khong co quyen truy cap.", user)); return`. | `KiemThuHoTro3a`<br>(trong `tests/test_tuan04.py`) |
