# ==========================================================
# setting.py - Trang CÀI ĐẶT (ui/setting.ui)
# ==========================================================
# - Xem thông tin: họ tên, email, SĐT
# - Đổi tên / mật khẩu / SĐT (lưu vào users.json)
# - Hướng dẫn sử dụng, đánh giá app, đăng xuất
# Ô nhập dùng QInputDialog: hộp thoại nhỏ có sẵn của PyQt để hỏi 1 giá trị.

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QLineEdit
from PyQt6 import uic
import os

from entities.users import QuanLyNguoiDung


class TrangCaiDat(QMainWindow):
    def __init__(self, cua_so_chinh, thu_muc_goc, tai_khoan):
        super().__init__()
        self.cua_so_chinh = cua_so_chinh
        self.thu_muc_goc = thu_muc_goc
        self.tai_khoan = tai_khoan

        duong_dan_ui = os.path.join(self.thu_muc_goc, "ui", "setting.ui")
        uic.loadUi(duong_dan_ui, self)

        self.hien_thi_thong_tin()

        # bắt sự kiện
        self.nut_trang_chu.clicked.connect(self.chuyen_trang_chu)
        self.nut_doi_ten.clicked.connect(self.doi_ten)
        self.nut_doi_mat_khau.clicked.connect(self.doi_mat_khau)
        self.nut_doi_sdt.clicked.connect(self.doi_sdt)
        self.nut_huong_dan.clicked.connect(self.xem_huong_dan)
        self.nut_danh_gia.clicked.connect(self.danh_gia_app)
        self.nut_dang_xuat.clicked.connect(self.dang_xuat)

        self.show()

    # ------------------ hiển thị ------------------
    def hien_thi_thong_tin(self):
        self.ho_ten.setText(f"Name: {self.tai_khoan.lay_ho_ten()}")
        self.email.setText(f"Email: {self.tai_khoan.lay_email()}")
        sdt = self.tai_khoan.lay_sdt()
        self.sdt.setText(f"SDT: {sdt if sdt != '' else 'chưa cập nhật'}")

    def luu_tai_khoan(self, thong_bao):
        QuanLyNguoiDung().sua_nguoi_dung(self.tai_khoan)  # lưu vào users.json
        self.hien_thi_thong_tin()
        self.hien_thong_bao(thong_bao)

    # ------------------ đổi thông tin ------------------
    def doi_ten(self):
        # getText trả về 2 giá trị: chữ đã nhập, và True nếu bấm OK
        ten_moi, bam_ok = QInputDialog.getText(self, "Đổi tên", "Nhập tên mới:")
        if not bam_ok:
            return
        if ten_moi.strip() == "":
            self.hien_thong_bao("Tên không được để trống!")
            return
        self.tai_khoan.sua_ho_ten(ten_moi.strip())
        self.luu_tai_khoan("Đổi tên thành công!")

    def doi_mat_khau(self):
        an_chu = QLineEdit.EchoMode.Password  # hiện dấu * thay vì chữ
        mat_khau_cu, bam_ok = QInputDialog.getText(self, "Đổi mật khẩu", "Nhập mật khẩu cũ:", an_chu)
        if not bam_ok:
            return
        if mat_khau_cu != self.tai_khoan.lay_mat_khau():
            self.hien_thong_bao("Mật khẩu cũ không đúng!")
            return
        mat_khau_moi, bam_ok = QInputDialog.getText(self, "Đổi mật khẩu", "Nhập mật khẩu mới:", an_chu)
        if not bam_ok:
            return
        if len(mat_khau_moi) < 6:
            self.hien_thong_bao("Mật khẩu mới phải từ 6 ký tự trở lên!")
            return
        self.tai_khoan.sua_mat_khau(mat_khau_moi)
        self.luu_tai_khoan("Đổi mật khẩu thành công!")

    def doi_sdt(self):
        sdt_moi, bam_ok = QInputDialog.getText(self, "Đổi SĐT", "Nhập số điện thoại mới:")
        if not bam_ok:
            return
        sdt_moi = sdt_moi.strip()
        if not sdt_moi.isdigit() or len(sdt_moi) != 10:
            self.hien_thong_bao("Số điện thoại phải gồm đúng 10 chữ số!")
            return
        self.tai_khoan.sua_sdt(sdt_moi)
        self.luu_tai_khoan("Đổi số điện thoại thành công!")

    # ------------------ hướng dẫn + đánh giá ------------------
    def xem_huong_dan(self):
        self.hien_thong_bao(
            "HƯỚNG DẪN SỬ DỤNG\n\n"
            "1. Chọn HK1 / HK2 ở thanh công cụ phía dưới.\n"
            "2. Nhập 6 cột điểm cho từng môn (TX1-TX4, GK, CK).\n"
            "   Môn Âm Nhạc, Mĩ Thuật, Thể Dục, GDĐP nhập: Đạt / K Đạt.\n"
            "3. Bấm 'Tính điểm TB' để tính điểm và lưu lại.\n"
            "4. Chọn 'Cả năm' để xem tổng kết.\n"
            "5. Bấm 'Xuất bảng điểm' để lưu bảng điểm ra file .json."
        )

    def danh_gia_app(self):
        # getInt: hỏi 1 số nguyên trong khoảng 1 - 5
        so_sao, bam_ok = QInputDialog.getInt(
            self, "Đánh giá", "Bạn chấm app mấy sao? (1 - 5)",
            self.tai_khoan.lay_danh_gia() or 5, 1, 5,  # giá trị mặc định, nhỏ nhất, lớn nhất
        )
        if not bam_ok:
            return
        self.tai_khoan.sua_danh_gia(so_sao)
        self.luu_tai_khoan(f"Cảm ơn bạn đã đánh giá {'⭐' * so_sao}!")

    # ------------------ chuyển trang ------------------
    def chuyen_trang_chu(self):
        from pages.home import TrangChu

        self.trang_chu = TrangChu(
            cua_so_chinh=self.cua_so_chinh, thu_muc_goc=self.thu_muc_goc, tai_khoan=self.tai_khoan
        )
        self.close()

    def dang_xuat(self):
        from pages.login import LoginPage

        self.trang_dang_nhap = LoginPage(main_window=self.cua_so_chinh, root_dir=self.thu_muc_goc)
        self.close()

    # ------------------ hàm hỗ trợ ------------------
    def hien_thong_bao(self, noi_dung):
        hop_thoai = QMessageBox()
        hop_thoai.setWindowTitle("Thông báo")
        hop_thoai.setText(noi_dung)
        hop_thoai.setIcon(QMessageBox.Icon.Information)
        hop_thoai.setStandardButtons(QMessageBox.StandardButton.Ok)
        hop_thoai.exec()
