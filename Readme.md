# 📚 Tech Option - Quản Lý Điểm Học Tập - Quốc Kiệt

Ứng dụng quản lý điểm cho học sinh THCS viết bằng **Python + PyQt6**, giao diện thiết kế bằng **Qt Designer**, dữ liệu lưu trong **file JSON**.

## Chức năng
- Đăng ký / đăng nhập (tài khoản lưu trong `data/users.json`)
- Nhập điểm HK1, HK2 cho 12 môn (TX1-TX4, GK, CK); môn Âm Nhạc, Mĩ Thuật, Thể Dục, GDĐP nhập Đạt / K Đạt
- Tính điểm trung bình môn, trung bình học kỳ, xét học lực
- Tổng kết cả năm: TB cả năm = (TB HK1 + TB HK2 x 2) / 3
- Điểm được lưu lại, mở app lần sau vẫn còn
- Xuất bảng điểm ra file .json, tự chọn nơi lưu trên máy
- Cài đặt: đổi tên, mật khẩu, số điện thoại, xem hướng dẫn, đánh giá app

## Cấu trúc thư mục
```
assets/       hình ảnh (imgs) và style.qss (giao diện chung)
pages/        các trang: login, signup, home (ui/home_basic.ui), setting
ui/           file .ui thiết kế bằng Qt Designer
components/   thẻ điểm 1 môn: TheMonHocKy (1 học kỳ), TheMonCaNam (cả năm)
entities/     class dữ liệu NguoiDung (có bảng điểm) + class quản lý QuanLyNguoiDung
data/         file JSON lưu dữ liệu + data_io.py (đọc/ghi JSON)
app.py        file chạy chương trình
```

## Cài đặt và chạy (Windows)
1. Cài Python 3.10 trở lên.
2. Mở Terminal tại thư mục dự án, cài thư viện:
   ```
   pip install -r Requirements.txt
   ```
3. Chạy app:
   ```
   python app.py
   ```

## Tài khoản dùng thử
- Email: `Kiet@gmail.com`
- Mật khẩu: `150110`
