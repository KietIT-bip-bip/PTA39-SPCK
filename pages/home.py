# home.py
# Trang chính của ứng dụng.
# Hiển thị bảng điểm học kỳ 1, học kỳ 2 và cả năm.
# Cho phép người dùng nhập điểm và tính trung bình học kỳ.

from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6 import uic

from pages.sub_term_widget import SubTermWidget
from pages.sub_allyear_widget import SubAllyearWidget


class HomePage(QMainWindow):
    """
    Trang chính của ứng dụng quản lý điểm học sinh.

    Cấu trúc giao diện (từ home.ui):
        - Sidebar trái  : nút HK1, HK2, Cả năm, Cài đặt
        - Nội dung phải : scroll area chứa 3 khối (HK1 / HK2 / Cả năm)
            + widget_6  : khối HK1 (header + danh sách 12 môn)
            + widget_7  : khối HK2 (header + danh sách 12 môn)
            + widget_37 : khối Cả năm (header + danh sách 12 môn)

    Chức năng chính:
        - Hiển thị/ẩn khối theo học kỳ đang xem
        - Cho phép nhập điểm từng môn
        - Tính TB học kỳ và xác định học lực khi bấm nút "Tính điểm TB"
        - Tự động cập nhật điểm cả năm khi chuyển sang tab "Cả năm"
    """

    # ----------------------------------------------------------
    # Danh sách 12 môn học theo đúng thứ tự trong home.ui
    # Mỗi phần tử là tuple: (tên hiển thị, là_môn_đặc_biệt)
    # Môn đặc biệt = môn Đạt/K Đạt (không tính điểm số)
    # ----------------------------------------------------------
    DANH_SACH_MON_HOC = [
        ("Toán", False),  # Môn thường
        ("Ngữ Văn", False),  # Môn thường
        ("Tiếng Anh", False),  # Môn thường
        ("KHTN", False),  # Môn thường
        ("Lịch Sử & Địa Lý", False),  # Môn thường
        ("Tin Học", False),  # Môn thường
        ("GDCD", False),  # Môn thường
        ("Công Nghệ", False),  # Môn thường
        ("Âm Nhạc", True),  # Môn đặc biệt (Đạt/K Đạt)
        ("Mĩ Thuật", True),  # Môn đặc biệt (Đạt/K Đạt)
        ("Thể Dục", True),  # Môn đặc biệt (Đạt/K Đạt)
        ("GDĐP", True),  # Môn đặc biệt (Đạt/K Đạt)
    ]

    # ----------------------------------------------------------

    def __init__(self, main_window, root_dir, cur_acc):
        """
        Khởi tạo trang chủ.

        Tham số:
            main_window : cửa sổ chính của ứng dụng (dùng để điều hướng)
            root_dir    : đường dẫn thư mục gốc của dự án
            cur_acc     : tài khoản đang đăng nhập (object Student hoặc tương tự)
        """
        super().__init__()

        self.main_window = main_window
        self.root_dir = root_dir
        self.cur_acc = cur_acc

        # Load giao diện từ file home.ui
        ui_path = self.root_dir + "/ui/home.ui"
        uic.loadUi(ui_path, self)

        # Danh sách lưu 12 SubTermWidget cho từng học kỳ
        # Mỗi phần tử ứng với 1 môn học (theo thứ tự DANH_SACH_MON_HOC)
        self.danh_sach_widget_hk1 = []
        self.danh_sach_widget_hk2 = []

        # Danh sách lưu 12 SubAllyearWidget cho phần cả năm
        self.danh_sach_widget_canam = []

        # Bước 1: Xóa các widget cứng trong UI và thêm widget động
        self.tao_va_chen_widget_mon_hoc()

        # Bước 2: Gắn sự kiện cho các nút bấm
        self.ket_noi_nut_bam()

        # Bước 3: Hiển thị thông tin học sinh
        self.hien_thi_thong_tin_hoc_sinh()

        # Bước 4: Mặc định hiển thị tab HK1
        self.setup_ui_for_term_1()

        # Hiển thị cửa sổ
        self.show()

    # ----------------------------------------------------------
    # PHẦN 1: KHỞI TẠO GIAO DIỆN
    # ----------------------------------------------------------

    def xoa_tat_ca_widget_trong_layout(self, layout):
        """
        Xóa sạch tất cả widget con bên trong một layout.

        Dùng để dọn sạch các widget cứng được tạo sẵn trong file .ui
        trước khi thêm widget động của chúng ta vào.

        Tham số:
            layout : QLayout cần xóa (VD: QVBoxLayout, QHBoxLayout)
        """
        while layout.count() > 0:
            # takeAt(0) lấy ra phần tử đầu tiên và xóa nó khỏi layout
            item = layout.takeAt(0)

            # Nếu item chứa widget thì gỡ widget đó ra
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)  # Gỡ widget khỏi cây widget
                widget.deleteLater()  # Xếp hàng để Qt dọn bộ nhớ

            # Nếu item là spacer thì Qt tự dọn khi takeAt() được gọi

    # ----------------------------------------------------------

    def tao_va_chen_widget_mon_hoc(self):
        """
        Tạo SubTermWidget và SubAllyearWidget cho 12 môn học,
        sau đó thêm vào các layout tương ứng trong giao diện.

        Vị trí các layout (theo home.ui):
            - widget_9.layout()  → chứa 12 SubTermWidget cho HK1
            - widget_24.layout() → chứa 12 SubTermWidget cho HK2
            - widget_39.layout() → chứa 12 SubAllyearWidget cho Cả năm
        """
        # Lấy layout của các vùng chứa môn học
        layout_hk1 = self.widget_9.layout()
        layout_hk2 = self.widget_24.layout()
        layout_canam = self.widget_39.layout()

        # Xóa các widget cứng có sẵn trong file .ui
        self.xoa_tat_ca_widget_trong_layout(layout_hk1)
        self.xoa_tat_ca_widget_trong_layout(layout_hk2)
        self.xoa_tat_ca_widget_trong_layout(layout_canam)

        # Tạo widget mới cho từng môn học
        for ten_mon, la_mon_dac_biet in self.DANH_SACH_MON_HOC:

            # --- Tạo widget cho HK1 ---
            widget_mon_hk1 = SubTermWidget(
                root_dir=self.root_dir, ten_mon_hoc=ten_mon, is_special=la_mon_dac_biet
            )
            self.danh_sach_widget_hk1.append(widget_mon_hk1)
            layout_hk1.addWidget(widget_mon_hk1)

            # --- Tạo widget cho HK2 ---
            widget_mon_hk2 = SubTermWidget(
                root_dir=self.root_dir, ten_mon_hoc=ten_mon, is_special=la_mon_dac_biet
            )
            self.danh_sach_widget_hk2.append(widget_mon_hk2)
            layout_hk2.addWidget(widget_mon_hk2)

            # --- Tạo widget cho Cả năm ---
            widget_mon_canam = SubAllyearWidget(
                root_dir=self.root_dir, ten_mon_hoc=ten_mon, is_special=la_mon_dac_biet
            )
            self.danh_sach_widget_canam.append(widget_mon_canam)
            layout_canam.addWidget(widget_mon_canam)

    # ----------------------------------------------------------
    # PHẦN 2: KẾT NỐI SỰ KIỆN
    # ----------------------------------------------------------

    def ket_noi_nut_bam(self):
        """
        Gắn sự kiện (event) cho tất cả các nút bấm trong giao diện.
        """
        # Sidebar: chuyển tab xem điểm
        self.nut_hk1.clicked.connect(self.setup_ui_for_term_1)
        self.nut_hk2.clicked.connect(self.setup_ui_for_term_2)
        self.nut_canam.clicked.connect(self.setup_ui_for_allyear)

        # Sidebar: chuyển sang trang cài đặt
        self.nut_caidat.clicked.connect(self.goto_setting)

        # Nút tính điểm TB nằm trong header của khối HK1
        # Tên widget trong home.ui: cal_hk
        self.cal_hk.clicked.connect(self.tinh_va_hien_thi_tb_hk1)

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

    def setup_ui_for_term_1(self):
        """
        Chuyển giao diện sang chế độ xem Học Kỳ 1.
        Chỉ hiển thị khối HK1, ẩn HK2 và Cả năm.
        """
        self.widget_6.setVisible(True)  # Hiện khối HK1
        self.widget_7.setVisible(False)  # Ẩn khối HK2
        self.widget_37.setVisible(False)  # Ẩn khối Cả năm

    def setup_ui_for_term_2(self):
        """
        Chuyển giao diện sang chế độ xem Học Kỳ 2.
        Chỉ hiển thị khối HK2, ẩn HK1 và Cả năm.
        """
        self.widget_6.setVisible(False)  # Ẩn khối HK1
        self.widget_7.setVisible(True)  # Hiện khối HK2
        self.widget_37.setVisible(False)  # Ẩn khối Cả năm

        # Tự động tính TB HK2 nếu tất cả môn đã nhập đủ điểm
        if self.kiem_tra_du_diem(self.danh_sach_widget_hk2):
            self.tinh_va_hien_thi_tb_hk2()

    def setup_ui_for_allyear(self):
        """
        Chuyển giao diện sang chế độ xem Cả năm.
        Tự động cập nhật điểm cả năm từ kết quả HK1 và HK2.
        """
        self.widget_6.setVisible(False)  # Ẩn khối HK1
        self.widget_7.setVisible(False)  # Ẩn khối HK2
        self.widget_37.setVisible(True)  # Hiện khối Cả năm

        # Cập nhật bảng cả năm từ dữ liệu đã tính ở HK1 và HK2
        self.cap_nhat_bang_diem_ca_nam()

    # ----------------------------------------------------------
    # PHẦN 4: HIỂN THỊ THÔNG TIN
    # ----------------------------------------------------------

    def hien_thi_thong_tin_hoc_sinh(self):
        """Hiển thị tên học sinh và học lực lên vùng header."""
        self.username.setText(f"username: {self.cur_acc["fullname"]}")
        self.hoc_luc_allyear.setText("Học Lực: Chưa tổng kết")

    # ----------------------------------------------------------
    # PHẦN 5: TÍNH ĐIỂM TRUNG BÌNH
    # ----------------------------------------------------------

    def kiem_tra_du_diem(self, danh_sach_widget):
        """
        Kiểm tra xem tất cả 12 môn trong danh sách đã nhập đủ điểm chưa.

        Tham số:
            danh_sach_widget : danh sách 12 SubTermWidget (HK1 hoặc HK2)

        Trả về:
            True  nếu tất cả 12 môn đều đã nhập đầy đủ
            False nếu còn ít nhất 1 môn chưa đủ
        """
        for widget_mon in danh_sach_widget:
            if not widget_mon.tat_ca_da_nhap():
                return False  # Tìm thấy môn chưa đủ điểm

        return True  # Tất cả đã đủ

    # ----------------------------------------------------------

    def tinh_va_hien_thi_tb_hk1(self):
        """
        Tính điểm trung bình Học Kỳ 1 và hiển thị học lực.

        Quy trình:
            1. Kiểm tra đủ điểm tất cả 12 môn chưa
            2. Gọi tinh_trung_binh() trên từng SubTermWidget → kết quả hiện lên sub_tb
            3. Thu thập điểm 8 môn thường → tính TB học kỳ
            4. Kiểm tra môn đặc biệt có K Đạt không
            5. Xác định học lực → hiển thị lên header

        Nút gắn với hàm này: cal_hk (trong widget_11 của home.ui)
        """
        # Kiểm tra đủ điểm chưa
        if not self.kiem_tra_du_diem(self.danh_sach_widget_hk1):
            self.show_message("Vui lòng nhập đủ điểm tất cả các môn trước khi tính!")
            return

        # Thu thập điểm sau khi tính từng môn
        danh_sach_diem_mon_thuong = []  # Lưu điểm TB 8 môn thường
        tat_ca_mon_dac_biet_dat = True  # Theo dõi môn đặc biệt

        for widget_mon in self.danh_sach_widget_hk1:
            # Tính TB cho môn này và hiển thị lên sub_tb
            diem_tb = widget_mon.tinh_trung_binh()

            if diem_tb is None:
                # Có lỗi nhập liệu → báo và dừng
                self.show_message(
                    f"Nhập liệu sai ở môn '{widget_mon.ten_mon_hoc}'!\n"
                    "Vui lòng kiểm tra lại."
                )
                return

            if widget_mon.is_special:
                # Kiểm tra môn đặc biệt có không đạt không
                if diem_tb == "K Đạt":
                    tat_ca_mon_dac_biet_dat = False
            else:
                # Thu thập điểm môn thường để tính TB học kỳ
                danh_sach_diem_mon_thuong.append(diem_tb)

        # Tính TB HK1 = trung bình cộng đơn giản của 8 môn thường
        if len(danh_sach_diem_mon_thuong) > 0:
            tong_diem = sum(danh_sach_diem_mon_thuong)
            so_mon = len(danh_sach_diem_mon_thuong)
            diem_tb_hk1 = round(tong_diem / so_mon, 1)
        else:
            diem_tb_hk1 = 0

        # Hiển thị TB HK1 vào ô tb_term (trong header widget_11)
        self.tb_term.setText(str(diem_tb_hk1))

        # Xác định và hiển thị học lực vào label hoc_luc (trong header widget_11)
        hoc_luc = self.xac_dinh_hoc_luc(
            danh_sach_diem_mon_thuong, tat_ca_mon_dac_biet_dat
        )
        self.hoc_luc.setText(hoc_luc)

    # ----------------------------------------------------------

    def tinh_va_hien_thi_tb_hk2(self):
        """
        Tính điểm trung bình Học Kỳ 2 và hiển thị học lực.
        Tương tự HK1 nhưng dùng danh sách widget HK2.
        Kết quả hiển thị vào lineEdit_86 và label_21 (header widget_23).
        """
        danh_sach_diem_mon_thuong = []
        tat_ca_mon_dac_biet_dat = True

        for widget_mon in self.danh_sach_widget_hk2:
            diem_tb = widget_mon.tinh_trung_binh()

            if diem_tb is None:
                return  # Có lỗi, dừng lại

            if widget_mon.is_special:
                if diem_tb == "K Đạt":
                    tat_ca_mon_dac_biet_dat = False
            else:
                danh_sach_diem_mon_thuong.append(diem_tb)

        # Tính TB HK2
        if len(danh_sach_diem_mon_thuong) > 0:
            diem_tb_hk2 = round(
                sum(danh_sach_diem_mon_thuong) / len(danh_sach_diem_mon_thuong), 1
            )
        else:
            diem_tb_hk2 = 0

        # Hiển thị vào header HK2 (widget_23)
        # lineEdit_86 = ô TB HKII, label_21 = nhãn Học lực
        self.lineEdit_86.setText(str(diem_tb_hk2))

        hoc_luc = self.xac_dinh_hoc_luc(
            danh_sach_diem_mon_thuong, tat_ca_mon_dac_biet_dat
        )
        self.label_21.setText(hoc_luc)

    # ----------------------------------------------------------

    def cap_nhat_bang_diem_ca_nam(self):
        """
        Cập nhật bảng điểm cả năm bằng cách lấy điểm TB từ HK1 và HK2.

        Duyệt qua từng môn học:
            - Lấy điểm TB HK1 từ widget HK1 tương ứng
            - Lấy điểm TB HK2 từ widget HK2 tương ứng
            - Gọi cap_nhat_diem() trên widget cả năm

        Chỉ cập nhật môn nào mà cả 2 học kỳ đều đã có điểm.
        """
        for so_thu_tu in range(len(self.DANH_SACH_MON_HOC)):
            widget_hk1 = self.danh_sach_widget_hk1[so_thu_tu]
            widget_hk2 = self.danh_sach_widget_hk2[so_thu_tu]
            widget_canam = self.danh_sach_widget_canam[so_thu_tu]

            # Lấy điểm TB đã tính (trả về None nếu chưa tính)
            diem_hk1 = widget_hk1.lay_diem_trung_binh()
            diem_hk2 = widget_hk2.lay_diem_trung_binh()

            # Chỉ cập nhật nếu cả 2 học kỳ đã có điểm
            if diem_hk1 is not None and diem_hk2 is not None:
                widget_canam.cap_nhat_diem(diem_hk1, diem_hk2)

    # ----------------------------------------------------------
    # PHẦN 6: XÁC ĐỊNH HỌC LỰC
    # ----------------------------------------------------------

    def xac_dinh_hoc_luc(self, danh_sach_diem_mon_thuong, tat_ca_mon_dat=True):
        """
        Xác định học lực dựa trên điểm TB các môn thường và môn đặc biệt.

        Luật xét học lực (theo quy định):
            - RỚT        : có ít nhất 1 môn đặc biệt "K Đạt"
            - Xuất sắc   : ít nhất 6/8 môn >= 9  VÀ điểm thấp nhất >= 8
            - Giỏi       : ít nhất 6/8 môn >= 8  VÀ điểm thấp nhất >= 6
            - Khá        : ít nhất 6/8 môn >= 6  VÀ điểm thấp nhất >= 5
            - Trung bình : ít nhất 6/8 môn >= 5  VÀ điểm thấp nhất >= 3.5
            - Chưa đạt   : còn lại

        Tham số:
            danh_sach_diem_mon_thuong : list[float] - điểm TB 8 môn thường
            tat_ca_mon_dat            : bool - False nếu có môn đặc biệt K Đạt

        Trả về:
            str - tên học lực (VD: "Giỏi", "Khá", "RỚT", ...)
        """
        # Kiểm tra môn đặc biệt trước
        if not tat_ca_mon_dat:
            return "RỚT"

        # Nếu không có dữ liệu môn thường
        if len(danh_sach_diem_mon_thuong) == 0:
            return "Chưa đánh giá"

        # Tính các thống kê cần thiết
        so_mon_tren_9 = sum(1 for diem in danh_sach_diem_mon_thuong if diem >= 9)
        so_mon_tren_8 = sum(1 for diem in danh_sach_diem_mon_thuong if diem >= 8)
        so_mon_tren_6 = sum(1 for diem in danh_sach_diem_mon_thuong if diem >= 6)
        so_mon_tren_5 = sum(1 for diem in danh_sach_diem_mon_thuong if diem >= 5)
        diem_thap_nhat = min(danh_sach_diem_mon_thuong)

        # Xét từ cao xuống thấp
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
        """
        Hiển thị hộp thoại thông báo cho người dùng.

        Tham số:
            message : nội dung thông báo cần hiển thị
        """
        hop_thoai = QMessageBox()
        hop_thoai.setWindowTitle("Thông báo")
        hop_thoai.setText(message)
        hop_thoai.setIcon(QMessageBox.Icon.Information)
        hop_thoai.setStandardButtons(QMessageBox.StandardButton.Ok)
        hop_thoai.exec()
