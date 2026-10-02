# Ghi chú bài thực hành Tuần 3

## Phần 1: Thông tin làm bài
- Bản đề: Đề B
- Số máy: PM401 - Máy học viên
- Sinh viên: Nguyễn Đoàn Huỳnh Hường - MSSV: 2305CT0721

## Phần 2: Sử dụng tệp cứu hộ
- Không dùng tệp cứu hộ (tự thực hiện hoàn chỉnh cả ba bản vá HOTRO-4, HOTRO-5, HOTRO-8 và bài kiểm thử hồi quy).

## Phần 3: Ba giới hạn của ba bản vá
1. **Về HOTRO-4**: Tài liệu LFD121 xếp Argon2id trước PBKDF2 và nói rõ PBKDF2 là thuật toán dễ bị tấn công bằng phần cứng chuyên dụng nhất trong ba thuật toán được khuyến nghị. Học phần dùng PBKDF2 vì thư viện chuẩn của Python không có Argon2id và phòng máy không có quyền cài thêm gói. Đây là giới hạn còn lại của bản vá, và nó thuộc về môi trường chứ không thuộc về tham số: số vòng lặp dùng ở đây là sáu trăm nghìn, đúng mức bảng hướng dẫn của OWASP khuyến nghị cho PBKDF2 kèm HMAC-SHA256.
2. **Về HOTRO-5**: Biến môi trường là cách lưu bí mật yếu hơn một kho bí mật chuyên dụng, vì giá trị của nó lộ ra cho toàn bộ tiến trình đã nạp nó. Nó vẫn tốt hơn hẳn việc ghi cứng trong mã nguồn.
3. **Về HOTRO-8**: Bản vá làm cho mã phiên không đoán được, nhưng nó không đặt hạn cho phiên và không đặt thuộc tính an toàn cho cookie. Hai việc ấy nằm ngoài phạm vi tuần 3.
