# Bảng yêu cầu an toàn (security requirements) của MiniShop, tuần 2

Họ tên:

MSSV:

Sửa tệp này ngay trên trình duyệt: bấm biểu tượng cây bút (**Edit this file**), gõ vào giữa hai dấu `|`, rồi bấm **Commit changes**. Mỗi hàng của bảng phải nằm trên đúng một dòng. Gõ vài hàng thì bấm **Commit changes** một lần, để không mất bài nếu lỡ đóng trang.

## 1. Mười hai yêu cầu (tầng L2, Mục 5 của tài liệu thực hành buổi 2)

Hàng YC-10 là hàng mẫu, chép từ Mục 5.3 của tài liệu thực hành buổi 2 và điền sẵn để đối chiếu. Giữ nguyên hàng ấy; mười một hàng còn lại là bài của sinh viên.

| Mã | Phát biểu | Điều kiện nghiệm thu (acceptance condition) | Cách kiểm chứng (verification) | Vị trí trong mã nguồn |
|---|---|---|---|---|
| YC-01 |  |  |  |  |
| YC-02 |  |  |  |  |
| YC-03 |  |  |  |  |
| YC-04 |  |  |  |  |
| YC-05 |  |  |  |  |
| YC-06 |  |  |  |  |
| YC-07 |  |  |  |  |
| YC-08 |  |  |  |  |
| YC-09 |  |  |  |  |
| YC-10 (hàng mẫu, điền sẵn) | Máy chủ MiniShop không được phục vụ yêu cầu đến từ máy khác trong mạng phòng máy | Ứng dụng chỉ lắng nghe trên địa chỉ vòng lặp nội bộ, không lắng nghe trên địa chỉ mà máy khác gọi tới được | Chạy MiniShop, rồi từ máy bên cạnh mở địa chỉ IP của máy này kèm cổng 8000; trình duyệt máy bên cạnh phải báo không kết nối được | `app.py`, dòng `HOST = "127.0.0.1"` |
| YC-11 |  |  |  |  |
| YC-12 |  |  |  |  |

## 2. Hai tiêu chí chấp nhận (acceptance criteria), tầng L3 phần a

### Tiêu chí thứ nhất, cho yêu cầu YC-__ (ghi mã đã chọn, thí dụ YC-07)

- Đầu vào:
- Kết quả quan sát được phải là:
- Kết quả chứng tỏ chưa đạt:

### Tiêu chí thứ hai, cho yêu cầu YC-__ (ghi mã đã chọn)

- Đầu vào:
- Kết quả quan sát được phải là:
- Kết quả chứng tỏ chưa đạt:

## 3. Yêu cầu thứ mười ba, tầng L3 phần b

| Mã | Phát biểu | Điều kiện nghiệm thu | Cách kiểm chứng |
|---|---|---|---|
| YC-13 |  |  |  |

Vì sao MiniShop cần yêu cầu này:

Điều gì xảy ra nếu thiếu nó:
