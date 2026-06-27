# sub_allyear_widget.py
# Widget hiển thị điểm cả năm của 1 môn học.
# Được load từ file ui/allyear_component.ui

from PyQt6.QtWidgets import QWidget
from PyQt6 import uic


class SubAllyearWidget(QWidget):
    """
    Widget hiển thị tổng kết điểm cả năm của 1 môn học.

    Giao diện gồm:
        - sub_name        : QLabel    - tên môn học
        - sub_tb_hk1      : QLineEdit - điểm TB HK1 (chỉ đọc, lấy từ HK1)
        - sub_tb_hk2      : QLineEdit - điểm TB HK2 (chỉ đọc, lấy từ HK2)
        - sub_tb_allyear  : QLabel    - điểm TB cả năm (tính tự động)

    Công thức tính TB cả năm (môn thường):
        TB cả năm = (TB HK1 + TB HK2 × 2) / 3
        (HK2 có hệ số 2 vì có nhiều nội dung hơn)

    Với môn đặc biệt:
        - "Đạt"   nếu cả 2 học kỳ đều "Đạt"
        - "K Đạt" nếu có 1 học kỳ bị "K Đạt"
    """

    def __init__(self, root_dir, ten_mon_hoc, is_special=False):
        """
        Khởi tạo widget.

        Tham số:
            root_dir    : đường dẫn đến thư mục gốc của dự án
            ten_mon_hoc : tên môn học hiển thị
            is_special  : True nếu là môn Đạt/K Đạt
        """
        super().__init__()

        self.ten_mon_hoc = ten_mon_hoc
        self.is_special = is_special

        # Load giao diện từ file .ui
        ui_path = root_dir + "/ui/allyear_component.ui"
        uic.loadUi(ui_path, self)

        # Hiển thị tên môn học
        self.sub_name.setText(ten_mon_hoc)

        # Xóa placeholder text mặc định
        self.sub_tb_hk1.clear()
        self.sub_tb_hk2.clear()
        self.sub_tb_allyear.setText("--")

        # Các ô HK1 và HK2 chỉ để hiển thị, không cho người dùng sửa
        self.sub_tb_hk1.setReadOnly(True)
        self.sub_tb_hk2.setReadOnly(True)

    # ----------------------------------------------------------

    def cap_nhat_diem(self, diem_hk1, diem_hk2):
        """
        Nhận điểm TB từ HK1 và HK2, hiển thị và tính điểm cả năm.

        Hàm này được gọi từ home.py khi người dùng bấm xem "Cả năm".

        Tham số:
            diem_hk1 : float hoặc str - điểm TB HK1 của môn này
            diem_hk2 : float hoặc str - điểm TB HK2 của môn này
        """
        # Hiển thị điểm từng học kỳ lên giao diện
        self.sub_tb_hk1.setText(str(diem_hk1))
        self.sub_tb_hk2.setText(str(diem_hk2))

        # Tính và hiển thị điểm TB cả năm
        if self.is_special:
            # Môn đặc biệt: 1 học kỳ K Đạt → cả năm K Đạt
            if diem_hk1 == "K Đạt" or diem_hk2 == "K Đạt":
                self.sub_tb_allyear.setText("K Đạt")
            else:
                self.sub_tb_allyear.setText("Đạt")
        else:
            # Môn thường: áp dụng công thức có hệ số
            try:
                so_hk1 = float(diem_hk1)
                so_hk2 = float(diem_hk2)

                # HK2 nhân 2 vì có hệ số cao hơn
                tb_ca_nam = round((so_hk1 + so_hk2 * 2) / 3, 1)
                self.sub_tb_allyear.setText(str(tb_ca_nam))

            except (ValueError, TypeError):
                # Nếu dữ liệu không phải số hợp lệ
                self.sub_tb_allyear.setText("Lỗi")
