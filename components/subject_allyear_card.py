# ==========================================================
# subject_allyear_card.py - Thẻ điểm CẢ NĂM của MỘT môn học
# ==========================================================
# Giao diện thẻ: ui/subject_allyear_card.ui
#   - ten_mon        : tên môn học
#   - o_tb_hk1       : điểm TB HK1 (chỉ đọc)
#   - o_tb_hk2       : điểm TB HK2 (chỉ đọc)
#   - diem_tb_ca_nam : điểm TB cả năm
#
# Công thức môn thường: TB cả năm = (TB HK1 + TB HK2 x 2) / 3
# Môn đặc biệt: 1 học kỳ "K Đạt" -> cả năm "K Đạt"

import os
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic


class TheMonCaNam(QWidget):
    def __init__(self, thu_muc_goc, ten_mon_hoc, la_mon_dac_biet=False):
        super().__init__()
        self.ten_mon_hoc = ten_mon_hoc
        self.la_mon_dac_biet = la_mon_dac_biet

        duong_dan_ui = os.path.join(thu_muc_goc, "ui", "subject_allyear_card.ui")
        uic.loadUi(duong_dan_ui, self)

        self.ten_mon.setText(ten_mon_hoc)
        self.o_tb_hk1.clear()
        self.o_tb_hk2.clear()
        self.diem_tb_ca_nam.setText("--")

        # 2 ô HK1, HK2 chỉ để xem, không cho sửa
        self.o_tb_hk1.setReadOnly(True)
        self.o_tb_hk2.setReadOnly(True)

    def cap_nhat_diem(self, diem_hk1, diem_hk2):
        self.o_tb_hk1.setText(str(diem_hk1))
        self.o_tb_hk2.setText(str(diem_hk2))

        if self.la_mon_dac_biet:
            if diem_hk1 == "K Đạt" or diem_hk2 == "K Đạt":
                self.diem_tb_ca_nam.setText("K Đạt")
            else:
                self.diem_tb_ca_nam.setText("Đạt")
            return

        try:
            tb_ca_nam = round((float(diem_hk1) + float(diem_hk2) * 2) / 3, 1)  # HK2 hệ số 2
            self.diem_tb_ca_nam.setText(str(tb_ca_nam))
        except (ValueError, TypeError):
            self.diem_tb_ca_nam.setText("Lỗi")
