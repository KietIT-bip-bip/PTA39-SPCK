# ==========================================================
# users.py - Class QuanLyNguoiDung: quản lý DANH SÁCH người dùng
# ==========================================================
# Chức năng: lấy / tìm / thêm / sửa / xóa
# Mỗi lần thêm, sửa, xóa -> tự động lưu lại vào data/users.json

import os
from data.data_io import DataIO
from entities.user import NguoiDung

# Đường dẫn tới file users.json (thư mục data nằm cạnh thư mục entities)
THU_MUC_GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_NGUOI_DUNG = os.path.join(THU_MUC_GOC, "data", "users.json")


class QuanLyNguoiDung:
    def __init__(self):
        self.__danh_sach_nguoi_dung = []  # list chứa các object NguoiDung
        self.doc_file()  # tạo xong là đọc dữ liệu từ file json luôn

    # ------------------ ĐỌC / GHI FILE JSON ------------------
    def doc_file(self):
        # Chưa có file -> danh sách rỗng
        if not os.path.exists(FILE_NGUOI_DUNG):
            self.__danh_sach_nguoi_dung = []
            return
        danh_sach_dict = DataIO.read_json(FILE_NGUOI_DUNG)  # json -> list dict
        # dùng vòng for đổi từng dict thành object NguoiDung
        self.__danh_sach_nguoi_dung = []
        for du_lieu in danh_sach_dict:
            self.__danh_sach_nguoi_dung.append(NguoiDung.tao_tu_dict(du_lieu))

    def luu_file(self):
        # đổi từng object NguoiDung thành dict rồi ghi ra file
        danh_sach_dict = []
        for nguoi_dung in self.__danh_sach_nguoi_dung:
            danh_sach_dict.append(nguoi_dung.chuyen_thanh_dict())
        DataIO.write_json(FILE_NGUOI_DUNG, danh_sach_dict)

    # ------------------ LẤY / TÌM ------------------
    def lay_tat_ca(self):
        return self.__danh_sach_nguoi_dung

    def tim_nguoi_dung(self, email):
        # Tìm người dùng theo email, không thấy -> trả về None
        for nguoi_dung in self.__danh_sach_nguoi_dung:
            if nguoi_dung.lay_email() == email:
                return nguoi_dung
        return None

    # ------------------ THÊM ------------------
    def them_nguoi_dung(self, nguoi_dung_moi):
        # Email đã tồn tại -> không thêm, trả về False
        if self.tim_nguoi_dung(nguoi_dung_moi.lay_email()) is not None:
            return False
        self.__danh_sach_nguoi_dung.append(nguoi_dung_moi)
        self.luu_file()
        return True

    # ------------------ SỬA ------------------
    def sua_nguoi_dung(self, nguoi_dung_da_sua):
        # Tìm vị trí người dùng có cùng email rồi thay bằng người dùng đã sửa
        for vi_tri in range(len(self.__danh_sach_nguoi_dung)):
            if self.__danh_sach_nguoi_dung[vi_tri].lay_email() == nguoi_dung_da_sua.lay_email():
                self.__danh_sach_nguoi_dung[vi_tri] = nguoi_dung_da_sua
                self.luu_file()
                return True
        return False

    # ------------------ XÓA ------------------
    def xoa_nguoi_dung(self, email):
        nguoi_dung = self.tim_nguoi_dung(email)
        if nguoi_dung is None:
            return False
        self.__danh_sach_nguoi_dung.remove(nguoi_dung)
        self.luu_file()
        return True
