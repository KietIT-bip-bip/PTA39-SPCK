# home.py
# Trang chính của ứng dụng.
# Hiển thị bảng điểm học kỳ 1, học kỳ 2 và cả năm.
# Cho phép người dùng nhập điểm và tính trung bình học kỳ.

import os

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget
from PyQt6 import uic

from pages.sub_term_widget import SubTermWidget
from pages.sub_allyear_widget import SubAllyearWidget


class HomePage(QMainWindow):
    """
    Trang chính của ứng dụng quản lý điểm học sinh.

    Mọi tên widget trong file .ui được gom vào bảng TEN_WIDGET bên dưới.
    Nếu đổi tên widget trong Qt Designer, CHỈ cần sửa bảng đó.
    """

    # Tên file giao diện nằm trong thư mục ui/
    TEN_FILE_UI = "home_basic.ui"

    # ----------------------------------------------------------
    # BẢNG TÊN WIDGET: "vai trò trong code": "objectName trong file .ui"
    # Sửa cột bên phải cho khớp với home_basic.ui của bạn.
    # ----------------------------------------------------------
    TEN_WIDGET = {
        # (3 khối HK1/HK2/Cả năm được code tự tìm, xem anh_xa_widget)
        # 3 vùng chứa danh sách môn (phải có layout bên trong)
        "ds_mon_hk1": "subject_list_hk1",
        "ds_mon_hk2": "subject_list_hk2",
        "ds_mon_canam": "subject_list_allyear",
        # Nút ở sidebar
        "nut_hk1": "nut_hk1",
        "nut_hk2": "nut_hk2",
        "nut_canam": "nut_canam",
        "nut_caidat": "nut_caidat",
        # Nút "Tính điểm TB" trong header mỗi học kỳ
        "nut_tinh_hk1": "nut_tinh_tb_hk",
        "nut_tinh_hk2": "cal_hk_2",
        # Label / ô hiển thị
        "lbl_username": "username",
        "lbl_hoc_luc_sidebar": "hoc_luc_allyear",
        "lbl_hoc_luc_canam": "hoc_luc_allyear_lb",
        # HK1: đang đoán (lineEdit_85, label_9), kiểm tra lại trong Designer
        "o_tb_hk1": "lineEdit_85",
        "lbl_hoc_luc_hk1": "label_9",
        # HK2: đi cặp với nút cal_hk_2
        "o_tb_hk2": "tb_term_2",
        "lbl_hoc_luc_hk2": "hoc_luc_2",
    }

    # ----------------------------------------------------------
    # Danh sách 12 môn học: (tên hiển thị, là_môn_đặc_biệt)
    # Môn đặc biệt = môn Đạt/K Đạt (không tính điểm số)
    # ----------------------------------------------------------
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

    # ----------------------------------------------------------

    def __init__(self, main_window, root_dir, cur_acc):
        """
        Tham số:
            main_window : cửa sổ chính của ứng dụng (dùng để điều hướng)
            root_dir    : đường dẫn thư mục gốc của dự án
            cur_acc     : tài khoản đang đăng nhập (dict có "fullname", ...)
        """
        super().__init__()

        self.main_window = main_window
        self.root_dir = str(root_dir)
        self.cur_acc = cur_acc

        # Load giao diện từ file .ui
        ui_path = os.path.join(self.root_dir, "ui", self.TEN_FILE_UI)
        uic.loadUi(ui_path, self)

        # Kiểm tra toàn bộ tên widget MỘT LẦN, báo hết tất cả tên thiếu
        self.anh_xa_widget()

        # Danh sách lưu widget cho từng học kỳ / cả năm
        self.danh_sach_widget_hk1 = []
        self.danh_sach_widget_hk2 = []
        self.danh_sach_widget_canam = []

        # Bước 1: Xóa widget cứng trong UI và thêm widget động
        self.tao_va_chen_widget_mon_hoc()

        # Bước 2: Gắn sự kiện cho các nút bấm
        self.ket_noi_nut_bam()

        # Bước 3: Hiển thị thông tin học sinh
        self.hien_thi_thong_tin_hoc_sinh()

        # Bước 4: Mặc định hiển thị tab HK1
        self.setup_ui_for_term_1()

        self.show()

    # ----------------------------------------------------------
    # PHẦN 0: ÁNH XẠ TÊN WIDGET
    # ----------------------------------------------------------

    def anh_xa_widget(self):
        """
        Tìm từng widget theo bảng TEN_WIDGET và gán thành thuộc tính của self
        (self.khoi_hk1, self.nut_hk1, ...). Nếu thiếu widget nào thì báo
        TẤT CẢ cái thiếu cùng danh sách tên thật có trong file .ui.
        """
        thieu = []
        for vai_tro, ten_trong_ui in self.TEN_WIDGET.items():
            widget = self.findChild(QWidget, ten_trong_ui)
            if widget is None:
                thieu.append(f"  - {vai_tro}: không thấy '{ten_trong_ui}'")
            else:
                setattr(self, vai_tro, widget)

        # Tự tìm 3 khối: khối = widget tổ tiên của vùng danh sách môn
        # mà nằm ngay trong scrollAreaWidgetContents
        if not thieu:
            noi_dung = self.findChild(QWidget, "scrollAreaWidgetContents")
            for vai_tro, vung in (
                ("khoi_hk1", self.ds_mon_hk1),
                ("khoi_hk2", self.ds_mon_hk2),
                ("khoi_canam", self.ds_mon_canam),
            ):
                khoi = vung
                while khoi.parentWidget() is not None and (
                    khoi.parentWidget() is not noi_dung
                ):
                    khoi = khoi.parentWidget()
                setattr(self, vai_tro, khoi)

        if thieu:
            ten_co_san = sorted(
                w.objectName() for w in self.findChildren(QWidget) if w.objectName()
            )
            raise RuntimeError(
                f"File {self.TEN_FILE_UI} thiếu {len(thieu)} widget mà code cần:\n"
                + "\n".join(thieu)
                + "\n\nCác tên widget thật có trong file .ui:\n  "
                + ", ".join(ten_co_san)
                + "\n\n=> Sửa bảng TEN_WIDGET ở đầu class HomePage cho khớp."
            )

    # ----------------------------------------------------------
    # PHẦN 1: KHỞI TẠO GIAO DIỆN
    # ----------------------------------------------------------

    def xoa_tat_ca_widget_trong_layout(self, layout):
        """Xóa sạch tất cả widget con bên trong một layout."""
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    # ----------------------------------------------------------

    def tao_va_chen_widget_mon_hoc(self):
        """
        Tạo SubTermWidget và SubAllyearWidget cho 12 môn học,
        rồi thêm vào layout của 3 vùng danh sách môn.
        """
        layout_hk1 = self.ds_mon_hk1.layout()
        layout_hk2 = self.ds_mon_hk2.layout()
        layout_canam = self.ds_mon_canam.layout()

        # Báo rõ nếu vùng chứa chưa có layout (tránh lỗi 'NoneType')
        for ten, layout in (
            ("ds_mon_hk1", layout_hk1),
            ("ds_mon_hk2", layout_hk2),
            ("ds_mon_canam", layout_canam),
        ):
            if layout is None:
                raise RuntimeError(
                    f"Widget '{self.TEN_WIDGET[ten]}' chưa có layout. "
                    "Trong Qt Designer: chuột phải vào nó → Lay out → "
                    "Lay Out Vertically."
                )

        self.xoa_tat_ca_widget_trong_layout(layout_hk1)
        self.xoa_tat_ca_widget_trong_layout(layout_hk2)
        self.xoa_tat_ca_widget_trong_layout(layout_canam)

        for ten_mon, la_mon_dac_biet in self.DANH_SACH_MON_HOC:
            widget_mon_hk1 = SubTermWidget(
                root_dir=self.root_dir, ten_mon_hoc=ten_mon, is_special=la_mon_dac_biet
            )
            self.danh_sach_widget_hk1.append(widget_mon_hk1)
            layout_hk1.addWidget(widget_mon_hk1)

            widget_mon_hk2 = SubTermWidget(
                root_dir=self.root_dir, ten_mon_hoc=ten_mon, is_special=la_mon_dac_biet
            )
            self.danh_sach_widget_hk2.append(widget_mon_hk2)
            layout_hk2.addWidget(widget_mon_hk2)

            widget_mon_canam = SubAllyearWidget(
                root_dir=self.root_dir, ten_mon_hoc=ten_mon, is_special=la_mon_dac_biet
            )
            self.danh_sach_widget_canam.append(widget_mon_canam)
            layout_canam.addWidget(widget_mon_canam)

    # ----------------------------------------------------------
    # PHẦN 2: KẾT NỐI SỰ KIỆN
    # ----------------------------------------------------------

    def ket_noi_nut_bam(self):
        """Gắn sự kiện cho tất cả các nút bấm trong giao diện."""
        # Sidebar: chuyển tab xem điểm
        self.nut_hk1.clicked.connect(self.setup_ui_for_term_1)
        self.nut_hk2.clicked.connect(self.setup_ui_for_term_2)
        self.nut_canam.clicked.connect(self.setup_ui_for_allyear)

        # Sidebar: chuyển sang trang cài đặt
        self.nut_caidat.clicked.connect(self.goto_setting)

        # Nút tính điểm TB trong header từng học kỳ
        self.nut_tinh_hk1.clicked.connect(self.tinh_va_hien_thi_tb_hk1)
        self.nut_tinh_hk2.clicked.connect(self.on_nut_tinh_tb_hk2_clicked)

    # ----------------------------------------------------------
    # PHẦN 3: ĐIỀU HƯỚNG (NAVIGATION)
    # ----------------------------------------------------------

    def goto_setting(self):
        """Chuyển sang trang cài đặt."""
        from pages.setting import SettingPage

        self.setting_page = SettingPage(
            main_window=self.main_window, root_dir=self.root_dir, cur_acc=self.cur_acc
        )
        self.close()

    # ----------------------------------------------------------

    def hien_khoi(self, khoi_can_hien):
        """Chỉ hiện khối được chọn, ẩn 2 khối còn lại."""
        for khoi in (self.khoi_hk1, self.khoi_hk2, self.khoi_canam):
            khoi.setVisible(khoi is khoi_can_hien)

    def setup_ui_for_term_1(self):
        """Xem Học Kỳ 1."""
        self.hien_khoi(self.khoi_hk1)

    def setup_ui_for_term_2(self):
        """Xem Học Kỳ 2 (tự tính TB nếu đã nhập đủ điểm)."""
        self.hien_khoi(self.khoi_hk2)

        if self.kiem_tra_du_diem(self.danh_sach_widget_hk2):
            self.tinh_va_hien_thi_tb_hk2()

    def setup_ui_for_allyear(self):
        """Xem Cả năm (tự cập nhật từ kết quả HK1 và HK2)."""
        self.hien_khoi(self.khoi_canam)
        self.cap_nhat_bang_diem_ca_nam()

    # ----------------------------------------------------------
    # PHẦN 4: HIỂN THỊ THÔNG TIN
    # ----------------------------------------------------------

    def hien_thi_thong_tin_hoc_sinh(self):
        """Hiển thị tên học sinh và học lực lên vùng header."""
        ho_ten = self.cur_acc["fullname"]
        self.lbl_username.setText(f"username: {ho_ten}")
        self.lbl_hoc_luc_sidebar.setText("Học Lực: Chưa tổng kết")
        self.lbl_hoc_luc_canam.setText("Chưa tổng kết")

    # ----------------------------------------------------------
    # PHẦN 5: TÍNH ĐIỂM TRUNG BÌNH
    # ----------------------------------------------------------

    def kiem_tra_du_diem(self, danh_sach_widget):
        """True nếu tất cả 12 môn đã nhập đủ điểm."""
        for widget_mon in danh_sach_widget:
            if not widget_mon.tat_ca_da_nhap():
                return False
        return True

    # ----------------------------------------------------------

    def tinh_va_hien_thi_tb_hk1(self):
        """Tính điểm TB Học Kỳ 1 và hiển thị học lực."""
        if not self.kiem_tra_du_diem(self.danh_sach_widget_hk1):
            self.show_message("Vui lòng nhập đủ điểm tất cả các môn trước khi tính!")
            return

        danh_sach_diem_mon_thuong = []
        tat_ca_mon_dac_biet_dat = True

        for widget_mon in self.danh_sach_widget_hk1:
            diem_tb = widget_mon.tinh_trung_binh()

            if diem_tb is None:
                self.show_message(
                    f"Nhập liệu sai ở môn '{widget_mon.ten_mon_hoc}'!\n"
                    "Vui lòng kiểm tra lại."
                )
                return

            if widget_mon.is_special:
                if diem_tb == "K Đạt":
                    tat_ca_mon_dac_biet_dat = False
            else:
                danh_sach_diem_mon_thuong.append(diem_tb)

        if len(danh_sach_diem_mon_thuong) > 0:
            diem_tb_hk1 = round(
                sum(danh_sach_diem_mon_thuong) / len(danh_sach_diem_mon_thuong), 1
            )
        else:
            diem_tb_hk1 = 0

        self.o_tb_hk1.setText(str(diem_tb_hk1))

        hoc_luc = self.xac_dinh_hoc_luc(
            danh_sach_diem_mon_thuong, tat_ca_mon_dac_biet_dat
        )
        self.lbl_hoc_luc_hk1.setText(hoc_luc)

        self.cap_nhat_bang_diem_ca_nam()

    # ----------------------------------------------------------

    def tinh_va_hien_thi_tb_hk2(self):
        """Tính điểm TB Học Kỳ 2 và hiển thị học lực."""
        danh_sach_diem_mon_thuong = []
        tat_ca_mon_dac_biet_dat = True

        for widget_mon in self.danh_sach_widget_hk2:
            diem_tb = widget_mon.tinh_trung_binh()

            if diem_tb is None:
                return

            if widget_mon.is_special:
                if diem_tb == "K Đạt":
                    tat_ca_mon_dac_biet_dat = False
            else:
                danh_sach_diem_mon_thuong.append(diem_tb)

        if len(danh_sach_diem_mon_thuong) > 0:
            diem_tb_hk2 = round(
                sum(danh_sach_diem_mon_thuong) / len(danh_sach_diem_mon_thuong), 1
            )
        else:
            diem_tb_hk2 = 0

        self.o_tb_hk2.setText(str(diem_tb_hk2))

        hoc_luc = self.xac_dinh_hoc_luc(
            danh_sach_diem_mon_thuong, tat_ca_mon_dac_biet_dat
        )
        self.lbl_hoc_luc_hk2.setText(hoc_luc)

    # ----------------------------------------------------------

    def on_nut_tinh_tb_hk2_clicked(self):
        """Xử lý khi bấm nút "Tính điểm TB" ở khối HK2."""
        if not self.kiem_tra_du_diem(self.danh_sach_widget_hk2):
            self.show_message("Vui lòng nhập đủ điểm tất cả các môn HK2 trước khi tính!")
            return

        self.tinh_va_hien_thi_tb_hk2()
        self.cap_nhat_bang_diem_ca_nam()

    # ----------------------------------------------------------

    def cap_nhat_bang_diem_ca_nam(self):
        """Cập nhật bảng điểm cả năm từ điểm TB của HK1 và HK2."""
        for so_thu_tu in range(len(self.DANH_SACH_MON_HOC)):
            widget_hk1 = self.danh_sach_widget_hk1[so_thu_tu]
            widget_hk2 = self.danh_sach_widget_hk2[so_thu_tu]
            widget_canam = self.danh_sach_widget_canam[so_thu_tu]

            diem_hk1 = widget_hk1.lay_diem_trung_binh()
            diem_hk2 = widget_hk2.lay_diem_trung_binh()

            if diem_hk1 is not None and diem_hk2 is not None:
                widget_canam.cap_nhat_diem(diem_hk1, diem_hk2)

        self.cap_nhat_hoc_luc_allyear()

    # ----------------------------------------------------------

    def cap_nhat_hoc_luc_allyear(self):
        """
        Cập nhật label học lực tổng ở sidebar và trong tab Cả năm.

            - Chỉ HK1 đã tính      → "Học Lực HK1: <kết quả>"
            - Cả HK1 + HK2 đã tính → tính học lực cả năm
        """
        hoc_luc_hk1 = self.lbl_hoc_luc_hk1.text().strip()
        hoc_luc_hk2 = self.lbl_hoc_luc_hk2.text().strip()

        GIA_TRI_MAC_DINH = {"", "Học lực", "Học Lực", "Chưa đánh giá"}

        hk1_da_tinh = hoc_luc_hk1 not in GIA_TRI_MAC_DINH
        hk2_da_tinh = hoc_luc_hk2 not in GIA_TRI_MAC_DINH

        if not hk1_da_tinh:
            return

        if not hk2_da_tinh:
            self.lbl_hoc_luc_sidebar.setText(f"Học Lực HK1: {hoc_luc_hk1}")
            return

        danh_sach_diem_ca_nam = []
        tat_ca_mon_dac_biet_dat = True

        for widget_canam in self.danh_sach_widget_canam:
            gia_tri = widget_canam.sub_tb_allyear.text().strip()

            if widget_canam.is_special:
                if gia_tri == "K Đạt":
                    tat_ca_mon_dac_biet_dat = False
            else:
                try:
                    danh_sach_diem_ca_nam.append(float(gia_tri))
                except ValueError:
                    pass

        if len(danh_sach_diem_ca_nam) == 0:
            return

        hoc_luc_ca_nam = self.xac_dinh_hoc_luc(
            danh_sach_diem_ca_nam, tat_ca_mon_dac_biet_dat
        )

        self.lbl_hoc_luc_sidebar.setText(f"Học Lực: {hoc_luc_ca_nam}")
        self.lbl_hoc_luc_canam.setText(hoc_luc_ca_nam)

    # ----------------------------------------------------------
    # PHẦN 6: XÁC ĐỊNH HỌC LỰC
    # ----------------------------------------------------------

    def xac_dinh_hoc_luc(self, danh_sach_diem_mon_thuong, tat_ca_mon_dat=True):
        """
        Luật xét học lực:
            - RỚT        : có ít nhất 1 môn đặc biệt "K Đạt"
            - Xuất sắc   : >= 6/8 môn >= 9  VÀ điểm thấp nhất >= 8
            - Giỏi       : >= 6/8 môn >= 8  VÀ điểm thấp nhất >= 6
            - Khá        : >= 6/8 môn >= 6  VÀ điểm thấp nhất >= 5
            - Trung bình : >= 6/8 môn >= 5  VÀ điểm thấp nhất >= 3.5
            - Chưa đạt   : còn lại
        """
        if not tat_ca_mon_dat:
            return "RỚT"

        if len(danh_sach_diem_mon_thuong) == 0:
            return "Chưa đánh giá"

        so_mon_tren_9 = sum(1 for diem in danh_sach_diem_mon_thuong if diem >= 9)
        so_mon_tren_8 = sum(1 for diem in danh_sach_diem_mon_thuong if diem >= 8)
        so_mon_tren_6 = sum(1 for diem in danh_sach_diem_mon_thuong if diem >= 6)
        so_mon_tren_5 = sum(1 for diem in danh_sach_diem_mon_thuong if diem >= 5)
        diem_thap_nhat = min(danh_sach_diem_mon_thuong)

        if so_mon_tren_9 >= 6 and diem_thap_nhat >= 8:
            return "Xuất sắc"

        if so_mon_tren_8 >= 6 and diem_thap_nhat >= 6:
            return "Giỏi"

        if so_mon_tren_6 >= 6 and diem_thap_nhat >= 5:
            return "Khá"

        if so_mon_tren_5 >= 6 and diem_thap_nhat >= 3.5:
            return "Trung bình"

        return "Chưa đạt"

    # ----------------------------------------------------------
    # PHẦN 7: TIỆN ÍCH
    # ----------------------------------------------------------

    def show_message(self, message):
        """Hiển thị hộp thoại thông báo cho người dùng."""
        hop_thoai = QMessageBox()
        hop_thoai.setWindowTitle("Thông báo")
        hop_thoai.setText(message)
        hop_thoai.setIcon(QMessageBox.Icon.Information)
        hop_thoai.setStandardButtons(QMessageBox.StandardButton.Ok)
        hop_thoai.exec()