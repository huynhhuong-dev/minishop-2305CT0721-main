# Danh mục tài sản và bốn ca lạm dụng - Tuần 3

## 1. Sáu tài sản, có xếp hạng

| Thứ hạng | Tài sản | Chủ của tài sản | Một câu: mất nó thì thiệt hại là gì |
|---|---|---|---|
| 1 | Thông tin xác thực người dùng (Mật khẩu và dữ liệu băm) | Người dùng và Quản trị viên | Nếu bị lộ, kẻ tấn công có thể giả mạo danh tính, đăng nhập vào tài khoản của người dùng và chiếm đoạt quyền quản trị hệ thống. |
| 2 | Khoá ký phiên đăng nhập (SESSION_KEY) | Hệ thống máy chủ MiniShop | Nếu bị lộ, kẻ tấn công có thể tự sinh chữ ký cookie hợp lệ để mạo danh bất kỳ tài khoản nào mà không cần biết mật khẩu. |
| 3 | Phiên đăng nhập đang hoạt động (Session ID) | Người dùng đang đăng nhập | Nếu mã phiên bị đoán được hoặc đánh cắp, kẻ tấn công có thể chiếm quyền điều khiển phiên làm việc (Session Hijacking) của người dùng đó. |
| 4 | Dữ liệu đơn hàng và lịch sử mua sắm | Người dùng sở hữu đơn hàng | Nếu bị truy cập trái phép, thông tin riêng tư về giao dịch và tiêu dùng của khách hàng bị tiết lộ. |
| 5 | Dữ liệu kho hàng và giá sản phẩm | Cửa hàng MiniShop | Nếu bị can thiệp thay đổi trái phép, cửa hàng có thể bị sai lệch tồn kho hoặc thất thoát tài chính khi bán sai giá. |
| 6 | Mã nguồn và cấu hình máy chủ | Đội ngũ phát triển MiniShop | Nếu bị lộ, kẻ tấn công có thể tìm thấy các lỗ hổng bảo mật và khoá bí mật để lên kế hoạch tấn công sâu hơn vào hệ thống. |

## 2. Bốn ca lạm dụng, mẫu ba phần

| # | Kẻ thực hiện là ai, chạm được tới đâu | Hành vi, viết bằng động từ chủ động | Kết quả mà kẻ ấy mong muốn |
|---|---|---|---|
| 1 | Kẻ tấn công có quyền đọc tệp cơ sở dữ liệu `minishop.db` | Thu thập các chuỗi băm mật khẩu MD5 trần và dùng bảng tra cứu sẵn (Rainbow Table) để tra ngược ra mật khẩu gốc của người dùng. | Đăng nhập trái phép vào tài khoản của người dùng khác để chiếm đoạt tài khoản hoặc đặc quyền quản trị. |
| 2 | Kẻ tấn công đọc được mã nguồn MiniShop (biết khoá cứng `SESSION_KEY`) | Tự tính toán chữ ký HMAC/MD5 với khoá cố định đã biết và tạo cookie phiên giả mạo gửi lên máy chủ. | Chiếm đoạt phiên làm việc của bất kỳ người dùng nào mà không cần biết mật khẩu thật. |
| 3 | Người dùng thông thường đã đăng nhập, quan sát thấy mã phiên (Session ID) là số tự tăng tuần tự (1, 2, 3...) | Sửa đổi giá trị Session ID trong cookie trình duyệt thành các số nguyên liền trước hoặc liền sau để gửi yêu cầu. | Mạo danh phiên làm việc của người dùng khác đang trực tuyến mà không bị phát hiện. |
| 4 | Khách hàng thông thường đã đăng nhập vào hệ thống | Thay đổi giá trị tham số trên thanh địa chỉ URL (`/don/<order_id>`) sang mã định danh đơn hàng của người khác. | Xem trộm nội dung chi tiết đơn hàng và thông tin cá nhân của khách hàng khác trong hệ thống. |
