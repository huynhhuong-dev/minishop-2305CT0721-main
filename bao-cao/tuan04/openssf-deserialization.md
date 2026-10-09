# Báo cáo thực hành Lab OpenSSF: Insecure Deserialization (Tuần 4)

**Học phần:** 04210 Bảo mật phần mềm (Software Security)  
**Sinh viên:** Nguyễn Đoàn Huỳnh Hương - MSSV: 2305CT0721  
**Lớp:** 261042100201_B  
**Đường dẫn lab:** https://best.openssf.org/labs/deserialization.html  

---

## 1. Lời giải mã nguồn đã sửa trong Lab

```javascript
// Ô nhập 1 (một dòng): Thay eval() bằng JSON.parse()
const data = JSON.parse(base64Decoded);

// Ô nhập 2 (ba dòng): Kiểm tra sự tồn tại, đúng kiểu chuỗi và giới hạn độ dài
if (data.username && typeof data.username == 'string' && data.username.length < 20) {
```

---

## 2. Dòng xác nhận hoàn thành (Completed)

```text
Completed 2026-10-09 15:52:14 UTC, 66491263, 6dfd746562095f32eb4a148a07c309320b9868ff11cb0f6ae094589255bb15f5
```

---

## 3. Giải thích kỹ thuật vì sao lời giải chặn được lỗi

1. **Về hàm `eval()` và ranh giới tin cậy:**  
   Hàm `eval()` sẽ biên dịch và thực thi chuỗi truyền vào như một đoạn mã JavaScript trực tiếp trên tiến trình máy chủ. Giá trị cookie `profile` được gửi từ trình duyệt của người dùng (nằm ngoài ranh giới tin cậy thứ nhất L1) qua mạng về máy chủ, nghĩa là hoàn toàn nằm trong tầm kiểm soát của kẻ tấn công. Khi máy chủ giải mã Base64 rồi chuyển thẳng chuỗi này vào `eval()`, kẻ tấn công có thể chèn mã JavaScript độc hại (chẳng hạn mã thực thi lệnh hệ điều hành thông qua Node.js child_process) dẫn đến lỗ hổng thực thi mã từ xa (Remote Code Execution - RCE).

2. **Sự khác biệt giữa `JSON.parse()` và `eval()`:**  
   `JSON.parse()` chỉ phân tích cú pháp dữ liệu văn bản thuần túy theo định dạng JSON để tạo ra đối tượng dữ liệu trong bộ nhớ mà hoàn toàn không thực thi bất kỳ mã lệnh chương trình nào. Do đó, ngay cả khi kẻ tấn công chèn các câu lệnh hay hàm thực thi mã vào trong chuỗi cookie, `JSON.parse()` hoặc sẽ báo lỗi cú pháp (SyntaxError) hoặc chỉ coi đó là một chuỗi ký tự bình thường, vô hiệu hóa hoàn toàn nguy cơ thực thi mã độc.

3. **Lý do cần kiểm tra kiểu dữ liệu và độ dài sau khi đọc bằng `JSON.parse()`:**  
   Mặc dù `JSON.parse()` ngăn chặn được việc chạy mã, kẻ tấn công vẫn có thể thao túng nội dung JSON để gửi các kiểu dữ liệu không mong muốn (chẳng hạn gửi `username` dưới dạng một Object hoặc Array thay vì String) hoặc gửi một chuỗi cực dài. Điều này có thể dẫn đến lỗi logic ở các đoạn mã phía sau, gây cạn kiệt tài nguyên bộ nhớ (từ chối dịch vụ - DoS), hoặc tạo điều kiện cho tấn công Cross-Site Scripting (XSS) khi tên người dùng được hiển thị lên trang HTML. Việc kiểm tra `typeof data.username == 'string'` và `data.username.length < 20` đảm bảo dữ liệu vừa an toàn về mặt thực thi, vừa đúng khuôn dạng nghiệp vụ dự kiến.

4. **Đối chiếu với thiết kế của MiniShop:**  
   MiniShop chọn giải pháp kiến trúc an toàn hơn nhiều: cookie phiên không lưu bất kỳ đối tượng dữ liệu hay hồ sơ người dùng nào, mà chỉ lưu một chuỗi mã phiên ngẫu nhiên kèm chữ ký HMAC (`sid.sig`). Khi nhận được yêu cầu, máy chủ MiniShop chỉ dùng `sid` đã xác thực chữ ký để tra cứu thông tin người dùng trong kho phiên `SESSIONS` lưu trên bộ nhớ máy chủ. Nhờ cách làm này, người dùng không thể can thiệp hay sửa đổi vai trò của mình thông qua cookie, ngăn chặn triệt để cả lỗi Deserialization lẫn nguy cơ thao túng dữ liệu phía client.
