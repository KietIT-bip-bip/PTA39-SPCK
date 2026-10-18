# ==========================================================
# home.py - Trang CHỦ: bảng điểm HK1, HK2, Cả năm (ui/home.ui)
# ==========================================================
# - Dùng VÒNG FOR tạo thẻ điểm cho 12 môn học (TheMonHocKy, TheMonCaNam)
# - Bấm "Tính điểm TB" -> tính điểm + học lực, LƯU điểm vào users.json
# - Mở app lại -> điểm cũ được điền lại từ users.json
# - "Xuất bảng điểm" -> lưu bảng điểm ra file .json ở nơi người dùng chọn

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt6 import uic
import os

from data.data_io import DataIO
from entities.users import QuanLyNguoiDung
from components.subject_term_card import TheMonHocKy
from components.subject_allyear_card import TheMonCaNam

TEN_FILE_UI = "home_basic.ui"  # giao diện trang chủ (trong thư mục ui)

# Danh sách 12 môn học: (tên môn, là môn đặc biệt?)
# Môn đặc biệt = môn chỉ xét Đạt / K Đạt (không tính điểm số)
DANH_SACH_MON_HOC = [
    ("Toán", False),
    ("Ngữ Văn", False),
    ("Tiếng Anh", False),
    ("KHTN", False),
    ("Lịch Sử & Địa Lý", False),
    ("Tin Học", False),
    ("GDCD", False),
    ("Công Nghệ", False),
    ("Âm Nhạc", True),
    ("Mĩ Thuật", True),
    ("Thể Dục", True),
    ("GDĐP", True),
]


class TrangChu(QMainWindow):
    def __init__(self, cua_so_chinh, thu_muc_goc, tai_khoan):
        super().__init__()
        self.cua_so_chinh = cua_so_chinh
        self.thu_muc_goc = thu_muc_goc
        self.tai_khoan = tai_khoan  # học sinh đang đăng nhập (object NguoiDung)

        duong_dan_ui = os.path.join(self.thu_muc_goc, "ui", TEN_FILE_UI)
        uic.loadUi(duong_dan_ui, self)

        # list lưu các thẻ của từng học kỳ / cả năm
        self.the_hk1 = []
        self.the_hk2 = []
        self.the_ca_nam = []

        # Bước 1: tạo thẻ 12 môn bằng vòng for
        self.tao_the_mon_hoc()
        # Bước 2: gắn sự kiện cho nút bấm
        self.ket_noi_nut_bam()
        # Bước 3: hiện thông tin học sinh
        self.hien_thi_thong_tin_hoc_sinh()
        # Bước 4: điền lại điểm đã lưu
        self.dien_diem_da_luu()
        # Bước 5: mặc định xem HK1
        self.xem_hk1()

        self.show()

    # ==================== PHẦN 1: TẠO THẺ MÔN HỌC ====================
    def tao_the_mon_hoc(self):
        bo_cuc_hk1 = self.ds_mon_hk1.layout()
        bo_cuc_hk2 = self.ds_mon_hk2.layout()
        bo_cuc_ca_nam = self.ds_mon_ca_nam.layout()

        # VÒNG FOR: mỗi môn -> 3 thẻ (HK1, HK2, Cả năm)
        for ten_mon, la_mon_dac_biet in DANH_SACH_MON_HOC:
            the_hk1 = TheMonHocKy(self.thu_muc_goc, ten_mon, la_mon_dac_biet)
            self.the_hk1.append(the_hk1)
            bo_cuc_hk1.addWidget(the_hk1)

            the_hk2 = TheMonHocKy(self.thu_muc_goc, ten_mon, la_mon_dac_biet)
            self.the_hk2.append(the_hk2)
            bo_cuc_hk2.addWidget(the_hk2)

            the_ca_nam = TheMonCaNam(self.thu_muc_goc, ten_mon, la_mon_dac_biet)
            self.the_ca_nam.append(the_ca_nam)
            bo_cuc_ca_nam.addWidget(the_ca_nam)

    # ==================== PHẦN 2: SỰ KIỆN ====================
    def ket_noi_nut_bam(self):
        # thanh bên: chuyển khối xem điểm
        self.nut_hk1.clicked.connect(self.xem_hk1)
        self.nut_hk2.clicked.connect(self.xem_hk2)
        self.nut_ca_nam.clicked.connect(self.xem_ca_nam)
        self.nut_cai_dat.clicked.connect(self.chuyen_trang_cai_dat)
        self.nut_xuat_bang_diem.clicked.connect(self.xuat_bang_diem)

        # nút "Tính điểm TB" của từng học kỳ
        self.nut_tinh_hk1.clicked.connect(self.bam_tinh_hk1)
        self.nut_tinh_hk2.clicked.connect(self.bam_tinh_hk2)

    # ==================== PHẦN 3: CHUYỂN KHỐI / TRANG ====================
    def hien_khoi(self, khoi_can_hien):
        # mỗi khối gồm 2 phần: thanh tiêu đề + danh sách môn
        cac_khoi = {
            "hk1": [self.tieu_de_hk1, self.ds_mon_hk1],
            "hk2": [self.tieu_de_hk2, self.ds_mon_hk2],
            "ca_nam": [self.tieu_de_ca_nam, self.ds_mon_ca_nam],
        }
        # chỉ hiện khối được chọn, ẩn 2 khối còn lại
        for ten_khoi, cac_phan in cac_khoi.items():
            for phan in cac_phan:
                phan.setVisible(ten_khoi == khoi_can_hien)

    def xem_hk1(self):
        self.hien_khoi("hk1")

    def xem_hk2(self):
        self.hien_khoi("hk2")

    def xem_ca_nam(self):
        self.hien_khoi("ca_nam")
        self.cap_nhat_bang_diem_ca_nam()

    def chuyen_trang_cai_dat(self):
        self.luu_diem()  # lưu điểm đang nhập trước khi rời trang
        from pages.setting import TrangCaiDat

        self.trang_cai_dat = TrangCaiDat(
            cua_so_chinh=self.cua_so_chinh, thu_muc_goc=self.thu_muc_goc, tai_khoan=self.tai_khoan
        )
        self.close()

    # ==================== PHẦN 4: THÔNG TIN + LƯU / ĐỌC ĐIỂM ====================
    def hien_thi_thong_tin_hoc_sinh(self):
        self.ten_nguoi_dung.setText(f"Họ tên: {self.tai_khoan.lay_ho_ten()}")
        self.hoc_luc_tong.setText("Học Lực: Chưa tổng kết")
        self.hoc_luc_ca_nam.setText("Chưa tổng kết")

    def luu_diem(self):
        # gom điểm 12 môn của mỗi học kỳ thành dict rồi lưu vào users.json
        for hoc_ky, danh_sach_the in (("hk1", self.the_hk1), ("hk2", self.the_hk2)):
            diem_cac_mon = {}
            for the in danh_sach_the:
                diem_cac_mon[the.ten_mon_hoc] = the.lay_diem_da_nhap()
            self.tai_khoan.sua_diem_hoc_ky(hoc_ky, diem_cac_mon)
        QuanLyNguoiDung().sua_nguoi_dung(self.tai_khoan)

    def dien_diem_da_luu(self):
        for hoc_ky, danh_sach_the in (("hk1", self.the_hk1), ("hk2", self.the_hk2)):
            diem_cac_mon = self.tai_khoan.lay_diem_hoc_ky(hoc_ky)
            for the in danh_sach_the:
                if the.ten_mon_hoc in diem_cac_mon:
                    the.dien_diem(diem_cac_mon[the.ten_mon_hoc])
        # đã nhập đủ thì tự tính lại luôn (không hiện thông báo)
        if self.da_nhap_du_diem(self.the_hk1):
            self.tinh_hoc_ky(self.the_hk1, self.o_tb_hk1, self.hoc_luc_hk1)
        if self.da_nhap_du_diem(self.the_hk2):
            self.tinh_hoc_ky(self.the_hk2, self.o_tb_hk2, self.hoc_luc_hk2)
        self.cap_nhat_bang_diem_ca_nam()

    # ==================== PHẦN 5: TÍNH ĐIỂM TRUNG BÌNH ====================
    def da_nhap_du_diem(self, danh_sach_the):
        for the in danh_sach_the:
            if not the.da_nhap_du_diem():
                return False
        return True

    def bam_tinh_hk1(self):
        self.bam_tinh(self.the_hk1, self.o_tb_hk1, self.hoc_luc_hk1, "HK1")

    def bam_tinh_hk2(self):
        self.bam_tinh(self.the_hk2, self.o_tb_hk2, self.hoc_luc_hk2, "HK2")

    def bam_tinh(self, danh_sach_the, o_tb, nhan_hoc_luc, ten_hoc_ky):
        self.luu_diem()  # lưu lại dù chưa nhập đủ, để lần sau nhập tiếp
        if not self.da_nhap_du_diem(danh_sach_the):
            self.hien_thong_bao(f"Đã lưu điểm. Vui lòng nhập đủ điểm tất cả các môn {ten_hoc_ky} để tính TB!")
            return
        mon_bi_loi = self.tinh_hoc_ky(danh_sach_the, o_tb, nhan_hoc_luc)
        if mon_bi_loi is not None:
            self.hien_thong_bao(f"Nhập liệu sai ở môn '{mon_bi_loi}'!\nVui lòng kiểm tra lại.")
            return
        self.cap_nhat_bang_diem_ca_nam()

    def tinh_hoc_ky(self, danh_sach_the, o_tb, nhan_hoc_luc):
        # tính TB + học lực 1 học kỳ; trả về tên môn bị lỗi (nếu có)
        diem_mon_thuong = []
        tat_ca_mon_dac_biet_dat = True

        for the in danh_sach_the:
            diem_tb = the.tinh_trung_binh()
            if diem_tb is None:
                return the.ten_mon_hoc
            if the.la_mon_dac_biet:
                if diem_tb == "K Đạt":
                    tat_ca_mon_dac_biet_dat = False
            else:
                diem_mon_thuong.append(diem_tb)

        diem_tb_hoc_ky = round(sum(diem_mon_thuong) / len(diem_mon_thuong), 1)
        o_tb.setText(str(diem_tb_hoc_ky))
        nhan_hoc_luc.setText(self.xac_dinh_hoc_luc(diem_mon_thuong, tat_ca_mon_dac_biet_dat))
        return None

    def cap_nhat_bang_diem_ca_nam(self):
        # VÒNG FOR theo thứ tự môn: lấy TB HK1 + HK2 đưa vào thẻ cả năm
        for vi_tri in range(len(DANH_SACH_MON_HOC)):
            diem_hk1 = self.the_hk1[vi_tri].lay_diem_trung_binh()
            diem_hk2 = self.the_hk2[vi_tri].lay_diem_trung_binh()
            if diem_hk1 is not None and diem_hk2 is not None:
                self.the_ca_nam[vi_tri].cap_nhat_diem(diem_hk1, diem_hk2)
        self.cap_nhat_hoc_luc_ca_nam()

    def cap_nhat_hoc_luc_ca_nam(self):
        # - chỉ HK1 đã tính      -> hiện "Học Lực HK1: ..."
        # - cả HK1 + HK2 đã tính -> tính học lực cả năm
        hk1_da_tinh = self.o_tb_hk1.text().replace(".", "").isdigit()
        hk2_da_tinh = self.o_tb_hk2.text().replace(".", "").isdigit()
        if not hk1_da_tinh:
            return
        if not hk2_da_tinh:
            self.hoc_luc_tong.setText(f"Học Lực HK1: {self.hoc_luc_hk1.text()}")
            return

        diem_ca_nam = []
        tat_ca_mon_dac_biet_dat = True
        for the in self.the_ca_nam:
            gia_tri = the.diem_tb_ca_nam.text().strip()
            if the.la_mon_dac_biet:
                if gia_tri == "K Đạt":
                    tat_ca_mon_dac_biet_dat = False
            else:
                try:
                    diem_ca_nam.append(float(gia_tri))
                except ValueError:
                    pass
        if len(diem_ca_nam) == 0:
            return

        hoc_luc = self.xac_dinh_hoc_luc(diem_ca_nam, tat_ca_mon_dac_biet_dat)
        self.hoc_luc_tong.setText(f"Học Lực: {hoc_luc}")
        self.hoc_luc_ca_nam.setText(hoc_luc)

    # ==================== PHẦN 6: XÉT HỌC LỰC ====================
    def xac_dinh_hoc_luc(self, diem_mon_thuong, tat_ca_mon_dat=True):
        # - RỚT        : có ít nhất 1 môn đặc biệt "K Đạt"
        # - Xuất sắc   : >= 6/8 môn >= 9  VÀ điểm thấp nhất >= 8
        # - Giỏi       : >= 6/8 môn >= 8  VÀ điểm thấp nhất >= 6
        # - Khá        : >= 6/8 môn >= 6  VÀ điểm thấp nhất >= 5
        # - Trung bình : >= 6/8 môn >= 5  VÀ điểm thấp nhất >= 3.5
        # - Chưa đạt   : còn lại
        if not tat_ca_mon_dat:
            return "RỚT"
        if len(diem_mon_thuong) == 0:
            return "Chưa đánh giá"

        so_mon_tren_9 = sum(1 for diem in diem_mon_thuong if diem >= 9)
        so_mon_tren_8 = sum(1 for diem in diem_mon_thuong if diem >= 8)
        so_mon_tren_6 = sum(1 for diem in diem_mon_thuong if diem >= 6)
        so_mon_tren_5 = sum(1 for diem in diem_mon_thuong if diem >= 5)
        diem_thap_nhat = min(diem_mon_thuong)

        if so_mon_tren_9 >= 6 and diem_thap_nhat >= 8:
            return "Xuất sắc"
        if so_mon_tren_8 >= 6 and diem_thap_nhat >= 6:
            return "Giỏi"
        if so_mon_tren_6 >= 6 and diem_thap_nhat >= 5:
            return "Khá"
        if so_mon_tren_5 >= 6 and diem_thap_nhat >= 3.5:
            return "Trung bình"
        return "Chưa đạt"

    # ==================== PHẦN 7: XUẤT BẢNG ĐIỂM ====================
    def xuat_bang_diem(self):
        self.luu_diem()                   # lưu điểm đang nhập trước
        self.cap_nhat_bang_diem_ca_nam()  # tính lại cả năm cho mới nhất

        # QFileDialog.getSaveFileName: mở cửa sổ "Lưu file" của Windows
        # trả về 2 giá trị: đường dẫn đã chọn, và loại file
        ten_goi_y = f"bang_diem_{self.tai_khoan.lay_ho_ten()}.json"
        duong_dan, _ = QFileDialog.getSaveFileName(
            self, "Chọn nơi lưu bảng điểm", ten_goi_y, "File JSON (*.json)"
        )
        if duong_dan == "":
            return  # bấm Hủy -> không làm gì

        # gom bảng điểm thành 1 dict rồi ghi ra file bằng DataIO
        bang_diem = {
            "ho_ten": self.tai_khoan.lay_ho_ten(),
            "email": self.tai_khoan.lay_email(),
            "hoc_ky_1": self.gom_diem_hoc_ky(self.the_hk1, self.o_tb_hk1, self.hoc_luc_hk1),
            "hoc_ky_2": self.gom_diem_hoc_ky(self.the_hk2, self.o_tb_hk2, self.hoc_luc_hk2),
            "ca_nam": self.gom_diem_ca_nam(),
        }
        DataIO.write_json(duong_dan, bang_diem)
        self.hien_thong_bao(f"Đã xuất bảng điểm ra file:\n{duong_dan}")

    def gom_diem_hoc_ky(self, danh_sach_the, o_tb, nhan_hoc_luc):
        cac_mon = {}
        for the in danh_sach_the:
            cac_mon[the.ten_mon_hoc] = {
                "diem": the.lay_diem_da_nhap(),         # 6 cột: TX1-TX4, GK, CK
                "trung_binh": the.diem_tb.text(),
            }
        return {"cac_mon": cac_mon, "trung_binh": o_tb.text(), "hoc_luc": nhan_hoc_luc.text()}

    def gom_diem_ca_nam(self):
        cac_mon = {}
        for the in self.the_ca_nam:
            cac_mon[the.ten_mon_hoc] = the.diem_tb_ca_nam.text()
        return {"cac_mon": cac_mon, "hoc_luc": self.hoc_luc_ca_nam.text()}

    # ==================== PHẦN 8: TIỆN ÍCH ====================
    def hien_thong_bao(self, noi_dung):
        hop_thoai = QMessageBox()
        hop_thoai.setWindowTitle("Thông báo")
        hop_thoai.setText(noi_dung)
        hop_thoai.setIcon(QMessageBox.Icon.Information)
        hop_thoai.setStandardButtons(QMessageBox.StandardButton.Ok)
        hop_thoai.exec()
