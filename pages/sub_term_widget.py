# sub_term_widget.py
# Widget hiển thị điểm 1 môn học trong 1 học kỳ.
# Được load từ file ui/subject_compenent.ui

from PyQt6.QtWidgets import QWidget
from PyQt6 import uic


class SubTermWidget(QWidget):
    """
    Widget cho 1 môn học trong 1 học kỳ.

    Giao diện gồm:
        - sub_name   : QLabel   - tên môn học
        - tx1, tx2, tx3, tx4 : QLineEdit - điểm thường xuyên
        - gk         : QLineEdit - điểm giữa kỳ
        - ck         : QLineEdit - điểm cuối kỳ
        - sub_tb     : QLabel   - điểm trung bình (hiển thị sau khi tính)

    Có 2 loại môn:
        - Môn thường   (is_special=False): nhập điểm số 0–10
        - Môn đặc biệt (is_special=True) : nhập "Đạt" hoặc "K Đạt"
          (dành cho Âm Nhạc, Mĩ Thuật, Thể Dục, GDĐP)
    """

    def __init__(self, root_dir, ten_mon_hoc, is_special=False):
        """
        Khởi tạo widget.

        Tham số:
            root_dir    : đường dẫn đến thư mục gốc của dự án
            ten_mon_hoc : tên môn học hiển thị (vd: "Toán", "Ngữ Văn")
            is_special  : True nếu là môn Đạt/K Đạt, mặc định False
        """
        super().__init__()

        # Lưu thông tin
        self.ten_mon_hoc = ten_mon_hoc
        self.is_special = is_special

        # Load giao diện từ file .ui
        ui_path = root_dir + "/ui/subject_compenent.ui"
        uic.loadUi(ui_path, self)

        # Hiển thị tên môn học lên label
        self.sub_name.setText(ten_mon_hoc)

        # Xóa text mặc định trong các ô nhập điểm
        self.tx1.clear()
        self.tx2.clear()
        self.tx3.clear()
        self.tx4.clear()
        self.gk.clear()
        self.ck.clear()

        # Thiết lập gợi ý (placeholder) cho các ô nhập
        if is_special:
            # Môn đặc biệt: chỉ nhập "Đạt" hoặc "K Đạt"
            goi_y = "Đạt / K Đạt"
            self.tx1.setPlaceholderText(goi_y)
            self.tx2.setPlaceholderText(goi_y)
            self.tx3.setPlaceholderText(goi_y)
            self.tx4.setPlaceholderText(goi_y)
            self.gk.setPlaceholderText(goi_y)
            self.ck.setPlaceholderText(goi_y)
        else:
            # Môn thường: nhập số từ 0 đến 10
            self.tx1.setPlaceholderText("TX1 (0-10)")
            self.tx2.setPlaceholderText("TX2 (0-10)")
            self.tx3.setPlaceholderText("TX3 (0-10)")
            self.tx4.setPlaceholderText("TX4 (0-10)")
            self.gk.setPlaceholderText("GK (0-10)")
            self.ck.setPlaceholderText("CK (0-10)")

        # Ô trung bình ban đầu để trống
        self.sub_tb.setText("--")

    # ----------------------------------------------------------

    def tat_ca_da_nhap(self):
        """
        Kiểm tra xem người dùng đã nhập đủ tất cả 6 ô điểm chưa.

        Trả về:
            True  nếu tất cả 6 ô đều có nội dung (không trống)
            False nếu còn ít nhất 1 ô chưa nhập
        """
        # Gom 6 ô nhập vào 1 danh sách để dễ duyệt
        danh_sach_o_nhap = [
            self.tx1, self.tx2, self.tx3, self.tx4,
            self.gk, self.ck
        ]

        for o_nhap in danh_sach_o_nhap:
            if o_nhap.text().strip() == "":
                return False  # Còn ô trống → chưa đủ

        return True  # Tất cả đã có nội dung

    # ----------------------------------------------------------

    def lay_diem_tung_o(self):
        """
        Đọc và kiểm tra hợp lệ từ 6 ô nhập điểm.

        Với môn thường:
            - Mỗi ô phải là số từ 0.0 đến 10.0
            - Trả về danh sách 6 số float: [tx1, tx2, tx3, tx4, gk, ck]

        Với môn đặc biệt:
            - Mỗi ô phải là "Đạt" hoặc "K Đạt" (không phân biệt hoa thường)
            - Trả về danh sách 6 chuỗi: ["Đạt", "K Đạt", ...]

        Trả về:
            Danh sách điểm nếu hợp lệ
            None nếu có ô sai định dạng
        """
        danh_sach_o_nhap = [
            self.tx1, self.tx2, self.tx3, self.tx4,
            self.gk, self.ck
        ]

        if self.is_special:
            # Môn đặc biệt: chỉ chấp nhận "Đạt" hoặc "K Đạt"
            gia_tri_hop_le = {"Đạt", "K Đạt"}
            danh_sach_diem = []

            for o_nhap in danh_sach_o_nhap:
                gia_tri = o_nhap.text().strip()
                if gia_tri not in gia_tri_hop_le:
                    return None  # Giá trị không hợp lệ
                danh_sach_diem.append(gia_tri)

            return danh_sach_diem

        else:
            # Môn thường: chuyển sang số float và kiểm tra khoảng hợp lệ
            danh_sach_diem = []

            for o_nhap in danh_sach_o_nhap:
                van_ban = o_nhap.text().strip()
                try:
                    diem = float(van_ban)
                except ValueError:
                    return None  # Không phải số → lỗi

                if diem < 0 or diem > 10:
                    return None  # Ngoài khoảng 0–10 → lỗi

                danh_sach_diem.append(diem)

            return danh_sach_diem

    # ----------------------------------------------------------

    def tinh_trung_binh(self):
        """
        Tính điểm trung bình học kỳ và hiển thị kết quả lên sub_tb.

        Công thức cho môn thường:
            TB = (TX1 + TX2 + TX3 + TX4 + GK×2 + CK×3) / 9
            (TX có hệ số 1, GK hệ số 2, CK hệ số 3)

        Với môn đặc biệt:
            - "Đạt"   nếu tất cả 6 ô đều là "Đạt"
            - "K Đạt" nếu có ít nhất 1 ô là "K Đạt"

        Trả về:
            float      nếu là môn thường và tính thành công
            str        nếu là môn đặc biệt ("Đạt" hoặc "K Đạt")
            None       nếu có lỗi nhập liệu
        """
        danh_sach_diem = self.lay_diem_tung_o()

        # Nếu dữ liệu không hợp lệ thì báo lỗi
        if danh_sach_diem is None:
            self.sub_tb.setText("Lỗi!")
            return None

        if self.is_special:
            # Môn đặc biệt: có K Đạt → kết quả là K Đạt
            if "K Đạt" in danh_sach_diem:
                ket_qua = "K Đạt"
            else:
                ket_qua = "Đạt"

            self.sub_tb.setText(ket_qua)
            return ket_qua

        else:
            # Môn thường: áp dụng công thức có hệ số
            tx1, tx2, tx3, tx4, gk, ck = danh_sach_diem

            tong_diem = tx1 + tx2 + tx3 + tx4 + gk * 2 + ck * 3
            # Chia cho 9 vì tổng hệ số = 1+1+1+1+2+3 = 9
            diem_trung_binh = round(tong_diem / 9, 1)

            self.sub_tb.setText(str(diem_trung_binh))
            return diem_trung_binh

    # ----------------------------------------------------------

    def lay_diem_trung_binh(self):
        """
        Lấy điểm trung bình đang hiển thị trên sub_tb (không tính lại).

        Dùng để truyền sang widget cả năm sau khi đã tính.

        Trả về:
            float  nếu môn thường và đã tính
            str    nếu môn đặc biệt ("Đạt" hoặc "K Đạt")
            None   nếu chưa tính hoặc có lỗi
        """
        gia_tri = self.sub_tb.text().strip()

        # Nếu chưa tính hoặc bị lỗi thì trả về None
        if gia_tri in ("--", "Lỗi!", ""):
            return None

        if self.is_special:
            return gia_tri  # Trả về chuỗi "Đạt" hoặc "K Đạt"

        # Môn thường: chuyển sang số
        try:
            return float(gia_tri)
        except ValueError:
            return None