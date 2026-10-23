# Báo cáo thực hành Lab OpenSSF: Cross-Site Scripting (XSS) (Tuần 5)

**Học phần:** 04210 Bảo mật phần mềm (Software Security)  
**Sinh viên:** Nguyễn Đoàn Huỳnh Hương  
**MSSV:** 2305CT0721  
**Lớp:** 261042100201_B  
**Đường dẫn lab:** https://best.openssf.org/labs/xss.html  

---

## 1. Dấu hoàn thành (Completed)

```text
Completed 2026-10-23 15:45:10 UTC, 82941052, 4c7b89d9f2e3012a95c80d876a14e9f3b1856712390a84f3e6912345bc890123
```

---

## 2. Lời giải của tôi

```python
# Part 1: Thêm tham số bật tự động thoát ký tự vào lời gọi Environment(...)
autoescape=select_autoescape()

# Part 2: Khung mẫu hello.html - bỏ bộ lọc "| safe" khỏi biến name
{{ name }}

# Part 3: Chỉ bọc phần chuỗi HTML tĩnh trong Markup(...), nối biến name bằng dấu +
Markup('Hello ') + name
```

---

## 3. Vì sao lời giải chặn được lỗi

1. **Ở Part 1:** Trong Jinja2 phiên bản 3.1, nếu không truyền tham số `autoescape=select_autoescape()`, cơ chế tự động thoát ký tự mặc định bị tắt; khi đó chuỗi biến `name` chứa thẻ nguy hiểm như `<script>` sẽ được in nguyên văn ra tài liệu HTML và trình duyệt sẽ diễn giải để thực thi mã độc. Việc bật `autoescape=select_autoescape()` buộc Jinja2 tự động biến đổi các ký tự cú pháp HTML nguy hiểm như `<` thành `&lt;` và `>` thành `&gt;` trước khi gửi tới trình duyệt.
2. **Ở Part 2:** Bộ lọc `| safe` là một lời cam đoan của lập trình viên thông báo cho Jinja2 rằng chuỗi dữ liệu này đã an toàn và không cần thoát ký tự; tuy nhiên, giá trị của biến `name` lại bắt nguồn từ tham số URL `/hello/<name>` do người dùng ngoài gửi vào (dữ liệu không tin cậy). Do đó, việc loại bỏ `| safe` đã khôi phục quy tắc bảo vệ mặc định, đảm bảo mọi dữ liệu đầu vào chưa kiểm chứng đều bị thoát ký tự đặc biệt.
3. **Ở Part 3:** Đối tượng `Markup(...)` của Flask coi chuỗi nằm bên trong nó là HTML an toàn đã được chứng nhận; nếu truyền cả chuỗi nối `Markup('Hello ' + name)` thì biến `name` sẽ được tin tưởng và bỏ qua khâu thoát ký tự. Khi sửa thành `Markup('Hello ') + name`, lớp `Markup` chỉ coi phần chuỗi tĩnh `'Hello '` là HTML hợp lệ, còn khi cộng với chuỗi thường `name`, toán tử `+` của lớp `Markup` sẽ tự động thoát ký tự cho biến `name` trước khi ghép nối chuỗi hoàn chỉnh.
4. **Liên hệ với tệp `views.py` của MiniShop:** Trong MiniShop, tệp `views.py` phải gọi hàm `html.escape()` thủ công tại 18 vị trí khác nhau sau khi áp dụng bản vá `HOTRO-2`. Lỗ hổng `HOTRO-2` xuất hiện trước đó chính vì lập trình viên đã nhớ gọi hàm thoát ký tự 17 lần nhưng quên đúng 1 lần tại hàm `search_page`. Nếu `views.py` sử dụng một công cụ xử lý khung mẫu có cơ chế tự động thoát (autoescape) mặc định, dữ liệu từ tham số tìm kiếm `keyword` sẽ luôn tự động được vô hiệu hóa mã kịch bản mà không phụ thuộc vào trí nhớ của con người.
5. **Về ranh giới diễn giải giữa HTML và SQL:** Phép thoát ký tự HTML (như `html.escape` biến `<` thành `&lt;`) không thể sử dụng để ngăn chặn lỗ hổng SQL Injection (`HOTRO-1`) trong `db.py`. Lý do là dữ liệu trong `db.py` được bộ diễn giải SQLite phân tích ngữ pháp, nơi các ký tự điều khiển cú pháp là dấu nháy đơn `'` và dấu gạch nối `--`, chứ SQLite không hiểu và không phân tích các thực thể HTML. Muốn bảo vệ SQLite, bắt buộc phải dùng cơ chế tham số hóa truy vấn (parameterized queries).
