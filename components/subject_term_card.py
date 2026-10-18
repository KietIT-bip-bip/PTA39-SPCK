# ==========================================================
# subject_term_card.py - Thẻ điểm MỘT môn học trong MỘT học kỳ
# ==========================================================
# Giao diện thẻ: ui/subject_term_card.ui
#   - ten_mon                    : tên môn học
#   - o_tx1, o_tx2, o_tx3, o_tx4 : điểm thường xuyên
#   - o_gk, o_ck                 : điểm giữa kỳ, cuối kỳ
#   - diem_tb                    : điểm trung bình (hiện sau khi tính)
#
# Có 2 loại môn:
#   - Môn thường    : nhập điểm số 0 - 10
#   - Môn đặc biệt  : nhập "Đạt" hoặc "K Đạt" (Âm Nhạc, Mĩ Thuật, Thể Dục, GDĐP)

import os
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic


class TheMonHocKy(QWidget):
    def __init__(self, thu_muc_goc, ten_mon_hoc, la_mon_dac_biet=False):
        super().__init__()
        self.ten_mon_hoc = ten_mon_hoc
        self.la_mon_dac_biet = la_mon_dac_biet

        duong_dan_ui = os.path.join(thu_muc_goc, "ui", "subject_term_card.ui")
        uic.loadUi(duong_dan_ui, self)

        self.ten_mon.setText(ten_mon_hoc)

        # gom 6 ô nhập vào 1 list để dùng vòng for cho gọn
        self.cac_o_nhap = [self.o_tx1, self.o_tx2, self.o_tx3, self.o_tx4, self.o_gk, self.o_ck]
        cac_ten_o = ["TX1", "TX2", "TX3", "TX4", "GK", "CK"]

        # xóa chữ mẫu + đặt gợi ý (placeholder) cho từng ô
        for o_nhap, ten_o in zip(self.cac_o_nhap, cac_ten_o):
            o_nhap.clear()
            if la_mon_dac_biet:
                o_nhap.setPlaceholderText("Đạt / K Đạt")
            else:
                o_nhap.setPlaceholderText(f"{ten_o} (0-10)")

        self.diem_tb.setText("--")  # chưa tính

    # ------------------ ĐỌC / ĐIỀN ĐIỂM (dùng khi lưu / mở lại) ------------------
    def lay_diem_da_nhap(self):
        # trả về list 6 chuỗi đúng như người dùng gõ
        ket_qua = []
        for o_nhap in self.cac_o_nhap:
            ket_qua.append(o_nhap.text().strip())
        return ket_qua

    def dien_diem(self, danh_sach_diem):
        # điền lại 6 ô từ dữ liệu đã lưu trong json
        for o_nhap, diem in zip(self.cac_o_nhap, danh_sach_diem):
            o_nhap.setText(diem)

    # ------------------ KIỂM TRA + TÍNH ĐIỂM ------------------
    def da_nhap_du_diem(self):
        # True nếu cả 6 ô đều đã có chữ
        for o_nhap in self.cac_o_nhap:
            if o_nhap.text().strip() == "":
                return False
        return True

    def lay_diem_tung_o(self):
        # Môn đặc biệt: mỗi ô phải là "Đạt" / "K Đạt" -> trả về list chuỗi
        # Môn thường  : mỗi ô phải là số 0 - 10   -> trả về list số
        # Sai định dạng -> trả về None
        danh_sach_diem = []

        if self.la_mon_dac_biet:
            for o_nhap in self.cac_o_nhap:
                gia_tri = o_nhap.text().strip()
                if gia_tri not in ("Đạt", "K Đạt"):
                    return None
                danh_sach_diem.append(gia_tri)
            return danh_sach_diem

        for o_nhap in self.cac_o_nhap:
            try:
                diem = float(o_nhap.text().strip())  # chữ -> số
            except ValueError:
                return None  # không phải số
            if diem < 0 or diem > 10:
                return None  # ngoài khoảng 0 - 10
            danh_sach_diem.append(diem)
        return danh_sach_diem

    def tinh_trung_binh(self):
        # Môn thường  : TB = (TX1 + TX2 + TX3 + TX4 + GK x 2 + CK x 3) / 9
        # Môn đặc biệt: có 1 ô "K Đạt" -> "K Đạt", còn lại -> "Đạt"
        danh_sach_diem = self.lay_diem_tung_o()
        if danh_sach_diem is None:
            self.diem_tb.setText("Lỗi!")
            return None

        if self.la_mon_dac_biet:
            ket_qua = "K Đạt" if "K Đạt" in danh_sach_diem else "Đạt"
            self.diem_tb.setText(ket_qua)
            return ket_qua

        tx1, tx2, tx3, tx4, gk, ck = danh_sach_diem
        tong_diem = tx1 + tx2 + tx3 + tx4 + gk * 2 + ck * 3
        diem_trung_binh = round(tong_diem / 9, 1)  # 9 = tổng hệ số 1+1+1+1+2+3
        self.diem_tb.setText(str(diem_trung_binh))
        return diem_trung_binh

    def lay_diem_trung_binh(self):
        # lấy điểm TB đang hiện (không tính lại), chưa tính / lỗi -> None
        gia_tri = self.diem_tb.text().strip()
        if gia_tri in ("--", "Lỗi!", ""):
            return None
        if self.la_mon_dac_biet:
            return gia_tri
        try:
            return float(gia_tri)
        except ValueError:
            return None
