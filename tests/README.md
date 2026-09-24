# Thư mục bài kiểm thử (tests)

Tệp `test_smoke.py` có sẵn từ khi giảng viên tạo kho.

Từ tuần 3: mỗi tuần thêm tệp kiểm thử theo mục "Nộp gì" của tài liệu thực hành tuần đó.

Chạy cả thư mục bằng lệnh sau, gõ ở thư mục `minishop` trên máy, tức thư mục chứa `app.py` (không gõ bên trong thư mục `tests`). Máy chỉ có lệnh `python3`, như phần lớn máy macOS, thì gõ `python3` thay cho `python`.

    python -m unittest discover -s tests
