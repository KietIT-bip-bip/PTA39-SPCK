# ==========================================================
# signup.py - Trang ĐĂNG KÝ (ui/signup.ui)
# ==========================================================
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6 import uic
import os
import re

from entities.user import NguoiDung
from entities.users import QuanLyNguoiDung


class TrangDangKy(QMainWindow):
    def __init__(self, cua_so_chinh, thu_muc_goc):
        super().__init__()
        self.cua_so_chinh = cua_so_chinh
        self.thu_muc_goc = thu_muc_goc
        self.nguoi_dung_moi = None  # tài khoản vừa tạo

        duong_dan_ui = os.path.join(self.thu_muc_goc, "ui", "signup.ui")
        uic.loadUi(duong_dan_ui, self)

        # bắt sự kiện cho các nút bấm
        self.nut_dang_ky.clicked.connect(self.xu_ly_dang_ky)       # nút ĐĂNG KÍ
        self.nut_chuyen_dang_nhap.clicked.connect(self.chuyen_trang_dang_nhap)   # nút sang Login

        self.show()

    # ------------------ xử lý sự kiện ------------------
    def xu_ly_dang_ky(self):
        # lấy dữ liệu từ form
        ho_ten_nhap = self.o_ho_ten.text().strip()
        email_nhap = self.o_email.text().strip()
        mat_khau_nhap = self.o_mat_khau.text()
        nhap_lai_nhap = self.o_nhap_lai_mat_khau.text()

        # kiểm tra họ tên
        if ho_ten_nhap == "":
            self.hien_thong_bao("Vui lòng nhập đầy đủ họ tên!")
            return

        # kiểm tra email + mật khẩu
        loi = self.__kiem_tra_du_lieu(email_nhap, mat_khau_nhap)
        if loi is not None:
            self.hien_thong_bao(loi)
            return

        # kiểm tra nhập lại mật khẩu
        if nhap_lai_nhap != mat_khau_nhap:
            self.hien_thong_bao("Mật khẩu và Nhập lại mật khẩu không trùng khớp!")
            return

        # 1. tạo người dùng mới
        self.nguoi_dung_moi = NguoiDung(ho_ten=ho_ten_nhap, email=email_nhap, mat_khau=mat_khau_nhap)
        # 2. thêm vào danh sách + lưu json (them_nguoi_dung tự lưu)
        quan_ly_nguoi_dung = QuanLyNguoiDung()
        if not quan_ly_nguoi_dung.them_nguoi_dung(self.nguoi_dung_moi):
            self.hien_thong_bao("Email này đã được đăng ký!")
            return
        # 3. thành công -> sang trang chủ
        self.hien_thong_bao("Đăng ký thành công!")
        self.__chuyen_trang_chu()

    def chuyen_trang_dang_nhap(self):
        from pages.login import LoginPage

        self.trang_dang_nhap = LoginPage(main_window=self.cua_so_chinh, root_dir=self.thu_muc_goc)
        self.close()

    # ------------------ hàm hỗ trợ ------------------
    def __chuyen_trang_chu(self):
        from pages.home import TrangChu

        self.trang_chu = TrangChu(
            cua_so_chinh=self.cua_so_chinh, thu_muc_goc=self.thu_muc_goc, tai_khoan=self.nguoi_dung_moi
        )
        self.close()

    def __kiem_tra_du_lieu(self, email, mat_khau):
        mau_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(mau_email, email) is None:
            return "Email không hợp lệ!"

        if len(mat_khau) < 6:
            return "Mật khẩu phải từ 6 ký tự trở lên!"

        return None

    def hien_thong_bao(self, noi_dung):
        hop_thoai = QMessageBox()
        hop_thoai.setWindowTitle("Thông báo")
        hop_thoai.setText(noi_dung)
        hop_thoai.setIcon(QMessageBox.Icon.Information)
        hop_thoai.setStandardButtons(QMessageBox.StandardButton.Ok)
        hop_thoai.exec()
