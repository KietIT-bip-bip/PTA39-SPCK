# ==========================================================
# login.py - Trang ĐĂNG NHẬP (ui/login.ui)
# ==========================================================
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
import os
import re

from entities.users import QuanLyNguoiDung


class LoginPage(QMainWindow):
    # LƯU Ý: giữ tên LoginPage, main_window, root_dir vì app.py gọi đúng tên này
    def __init__(self, main_window, root_dir):
        super().__init__()  # kế thừa code __init__ của lớp cha
        self.cua_so_chinh = main_window  # cửa sổ chính
        self.thu_muc_goc = root_dir      # thư mục gốc của dự án
        self.quan_ly_nguoi_dung = QuanLyNguoiDung()  # đọc danh sách người dùng từ users.json
        self.nguoi_dung_dang_nhap = None         # người dùng đăng nhập thành công

        # nạp style chung (chữ đen, không đổi theo Dark mode)
        self.__nap_giao_dien_chung()

        # load file ui
        duong_dan_ui = os.path.join(self.thu_muc_goc, "ui", "login.ui")
        uic.loadUi(duong_dan_ui, self)

        # bắt sự kiện cho các nút bấm
        self.nut_dang_nhap.clicked.connect(self.xu_ly_dang_nhap)          # nút Login
        self.nut_chuyen_dang_ky.clicked.connect(self.chuyen_trang_dang_ky)    # nút sang Sign up

        self.show()

    # ------------------ xử lý sự kiện ------------------
    def xu_ly_dang_nhap(self):
        # lấy dữ liệu người dùng nhập, strip() xóa khoảng trắng 2 đầu
        email_nhap = self.o_email.text().strip()
        mat_khau_nhap = self.o_mat_khau.text()

        # kiểm tra dữ liệu, có lỗi -> báo lỗi rồi dừng
        loi = self.__kiem_tra_du_lieu(email_nhap, mat_khau_nhap)
        if loi is not None:
            self.hien_thong_bao(loi)
            return

        # tìm tài khoản theo email trong file json
        nguoi_dung = self.quan_ly_nguoi_dung.tim_nguoi_dung(email_nhap)
        if nguoi_dung is None or nguoi_dung.lay_mat_khau() != mat_khau_nhap:
            self.hien_thong_bao("Email hoặc mật khẩu không đúng!")
            return

        # đúng hết -> sang trang chủ
        self.nguoi_dung_dang_nhap = nguoi_dung
        self.__chuyen_trang_chu()

    def chuyen_trang_dang_ky(self):
        from pages.signup import TrangDangKy

        self.trang_dang_ky = TrangDangKy(cua_so_chinh=self.cua_so_chinh, thu_muc_goc=self.thu_muc_goc)
        self.close()

    # ------------------ hàm hỗ trợ ------------------
    def __chuyen_trang_chu(self):
        from pages.home import TrangChu

        self.trang_chu = TrangChu(
            cua_so_chinh=self.cua_so_chinh, thu_muc_goc=self.thu_muc_goc, tai_khoan=self.nguoi_dung_dang_nhap
        )
        self.close()

    def __nap_giao_dien_chung(self):
        # Đọc file assets/style.qss rồi gắn cho CẢ app (QApplication)
        # -> chỉ cần làm 1 lần ở trang đầu tiên, mọi trang sau đều dùng được
        duong_dan_qss = os.path.join(self.thu_muc_goc, "assets", "style.qss")
        with open(duong_dan_qss, "r", encoding="utf-8") as tep:
            QApplication.instance().setStyleSheet(tep.read())

    def __kiem_tra_du_lieu(self, email, mat_khau):
        # kiểm tra email đúng dạng abc@gmail.com
        mau_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(mau_email, email) is None:
            return "Email không hợp lệ!"

        # kiểm tra độ dài mật khẩu
        if len(mat_khau) < 6:
            return "Mật khẩu phải từ 6 ký tự trở lên!"

        return None  # không có lỗi

    def hien_thong_bao(self, noi_dung):
        # hộp thoại thông báo có nút OK
        hop_thoai = QMessageBox()
        hop_thoai.setWindowTitle("Thông báo")
        hop_thoai.setText(noi_dung)
        hop_thoai.setIcon(QMessageBox.Icon.Information)
        hop_thoai.setStandardButtons(QMessageBox.StandardButton.Ok)
        hop_thoai.exec()
