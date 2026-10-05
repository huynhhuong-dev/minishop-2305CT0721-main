# Cheat sheet Git/GitHub cho học phần 04210

Dành cho ai chỉ thao tác trên trình duyệt: tải tệp lên, kéo thả, sửa trực tiếp trên web, không cần dòng lệnh. Kho của em: `https://github.com/HVU-04210-261/minishop-<MSSV>`. Chi tiết đầy đủ hơn (VS Code, chạy MiniShop, Copilot): tài liệu "Tự học thao tác kho GitHub và VS Code" trong `00_Thong-tin-chung`.

Trang báo lỗi 404? Em chưa **Accept invitation**, hoặc đăng nhập nhầm tài khoản: mở `github.com/notifications` rồi bấm chấp nhận.

## Bốn việc làm hằng ngày

| Muốn làm gì | Bấm gì trên web |
|---|---|
| Thêm tệp mới (ảnh, bảng, mã đã sửa trên máy) | Mở đúng thư mục `bao-cao/tuanNN/` → **Add file** → **Upload files** → kéo tệp vào khung → cuộn xuống, gõ thông điệp → **Commit changes** |
| Sửa một tệp `.md` hoặc `.py` ngay trên web | Mở tệp → biểu tượng cây bút **Edit this file** → sửa → **Commit changes** |
| Xoá tệp tải nhầm | Mở tệp → dấu ba chấm **…** → **Delete file** → **Commit changes** |
| Xem bài đã đạt yêu cầu chưa | Tab **Actions** → **tu-kiem** → dấu tích xanh = đạt; dấu X đỏ → bấm vào đọc dòng `THIEU` hay `CAM` |

Dấu hiệu một lần ghi nhận đã thành công: tệp hiện đúng thư mục, dòng trên cùng của danh sách tệp ghi đúng thông điệp vừa gõ.

## Thông điệp ghi nhận (commit message)

- **Tuần thường**: viết tự do, có ý nghĩa. Ví dụ: `tuan03: anh chup truoc khi va`.
- **Tuần có thông điệp bắt buộc** (ví dụ tuần 3): chép **nguyên văn, không dấu**, từ chính tệp `bao-cao/tuanNN/README.md` trong kho của em, đừng gõ lại tay, vì máy chấm so khớp từng ký tự. Tuần 3 cần đúng hai thông điệp, theo đúng thứ tự:
  1. Vá `db.py` xong, ghi nhận riêng với: `va: HOTRO-4 bam mat khau co muoi`
  2. Vá `app.py` xong, ghi nhận riêng với: `va: HOTRO-5 khoa ky phien, HOTRO-8 ma phien ngau nhien`
- **Một bản vá, một lần ghi nhận.** Đừng gộp hai tệp đã vá vào cùng một lần Commit, vì người chấm cần tách được từng bản vá.

## Tuyệt đối không tải lên

- `minishop.db`, mật khẩu hay API key thật, thư mục `__pycache__/`, tệp `.pyc`.
- Lời giải hay đáp án lấy từ nơi khác.
- Khi Upload, chỉ chọn **từng tệp**, đừng kéo cả thư mục, vì Git giữ mọi phiên bản mãi mãi kể cả xoá ở lần sau.

## Hạn nộp

Không có nút "Nộp bài". Giảng viên lấy lần ghi nhận cuối cùng trên nhánh `main` **trước hạn**. Mặc định: 5 ngày sau buổi học, 23:59. Vài tuần (3, 6, 9…) có thêm mốc phụ ngay tại lớp, xem lịch nộp bài được công bố riêng cho từng tuần. Ghi nhận thêm sau hạn không làm mất bài đúng hạn, nhưng phần sau hạn không được tính.

## Lỗi thường gặp

| Dấu hiệu | Sửa nhanh |
|---|---|
| 404 khi mở kho | Chưa Accept invitation, vào `github.com/notifications` |
| **tu-kiem** báo đỏ `THIEU` thông điệp | Thông điệp gõ sai hoặc có dấu, chép lại nguyên văn từ `bao-cao/tuanNN/README.md`, ghi nhận lại đúng tệp đó |
| Tệp nằm nhầm ở gốc kho thay vì `bao-cao/tuanNN` | Xoá tệp sai chỗ (mục Xoá tệp ở trên), tải lại đúng thư mục |
| Có hai tệp trùng tên, một tệp thêm `(1)` | Trình duyệt tự đổi tên khi tải lần hai, đổi tên tệp trên máy về đúng tên gốc rồi tải lại, xoá bản thừa |
| Lỡ tải `minishop.db` hay ảnh thật lên kho | Xoá theo mục Xoá tệp; nếu là dữ liệu nhạy cảm, báo giảng viên ngay vì lịch sử Git vẫn giữ bản cũ |
