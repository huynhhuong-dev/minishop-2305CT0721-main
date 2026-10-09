# Ghi chú bài thực hành Tuần 4

**Học phần:** 04210 Bảo mật phần mềm (Software Security)  
**Sinh viên:** Nguyễn Đoàn Huỳnh Hương - MSSV: 2305CT0721  
**Lớp:** 261042100201_B  

---

## 1. Thông tin về phép kiểm cũ đã sửa (Mục 5.4)

- **Tên phép kiểm đã sửa:** `test_admin_page` trong tệp `tests/test_smoke.py`.
- **Hành vi cũ mà nó khẳng định:** Đăng nhập bằng tài khoản người dùng thường (`lan`), gửi yêu cầu tới `/admin` và khẳng định mã trạng thái trả về là `200` cùng với nội dung `"Quan tri nguoi dung"` (bảo vệ hành vi sai/lỗ hổng như thể là mong đợi của hệ thống).
- **Hành vi mới:** Đăng nhập bằng tài khoản người dùng thường (`lan`), gửi yêu cầu tới `/admin` và khẳng định máy chủ từ chối với mã trạng thái `403` (`Forbidden`) cùng nội dung thông báo `"Tu choi"`.

---

## 2. Hai giới hạn của bản vá tuần này (Mục 15)

1. **Bản vá chỉ đóng một trong hai chỗ mang nhãn HOTRO-3:**  
   Bản vá `HOTRO-3a` tuần này mới chỉ xử lý trang quản trị `/admin`. Chỗ còn lại mang nhãn `HOTRO-3b` nằm ở phương thức `_show_order` phục vụ trang chi tiết đơn hàng (`/don/<id>`): máy chủ hiện tại mới chỉ kiểm tra đơn hàng có tồn tại trong CSDL hay không, nhưng chưa kiểm tra đơn hàng này có thuộc quyền sở hữu của người dùng đang đăng nhập hay không (lỗ hổng IDOR - Insecure Direct Object References). Chỗ này sẽ được giải quyết ở tuần 5.

2. **Phép kiểm vai trò viết trực tiếp trong phương thức phục vụ trang:**  
   Phép kiểm tra `if user["role"] != "admin":` được viết trực tiếp bên trong phương thức `_show_admin`. Cách tiếp cận này hoạt động tốt với một ứng dụng đơn giản chỉ có một trang quản trị duy nhất. Tuy nhiên, khi hệ thống mở rộng với nhiều trang và chức năng quản trị khác nhau, việc kiểm tra phân tán như vậy rất dễ bị bỏ sót lập trình viên quên thêm mã kiểm tra ở trang mới. Về mặt kiến trúc, phép kiểm quyền nên được đặt ở một vị trí tập trung mà mọi yêu cầu đều phải đi qua (chẳng hạn tại tầng định tuyến `_route_get` hoặc thông qua middleware / decorator phân quyền) theo nguyên lý trung gian đầy đủ (Complete Mediation). Học phần không đòi hỏi làm phần này trong tuần 4.
