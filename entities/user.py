# ==========================================================
# user.py - Class NguoiDung: lưu thông tin MỘT học sinh (tài khoản)
# ==========================================================
# Mỗi NguoiDung gồm:
#   - ho_ten, email, mat_khau, sdt : thông tin tài khoản
#   - danh_gia  : số sao học sinh đánh giá app (0 = chưa đánh giá)
#   - bang_diem : điểm đã nhập của 2 học kỳ, dạng
#       {"hk1": {"Toán": ["8", "9", "7", "8", "8", "9"], ...},
#        "hk2": {...}}
#     6 ô theo thứ tự: TX1, TX2, TX3, TX4, GK, CK


class NguoiDung:
    def __init__(self, ho_ten, email, mat_khau, sdt="", danh_gia=0, bang_diem=None):
        # dấu __ ở đầu: thuộc tính "riêng tư", chỉ đọc/sửa qua hàm lay_... / sua_...
        self.__ho_ten = ho_ten
        self.__email = email
        self.__mat_khau = mat_khau
        self.__sdt = sdt
        self.__danh_gia = danh_gia

        # chưa có bảng điểm -> tạo bảng điểm rỗng cho 2 học kỳ
        if bang_diem is None:
            bang_diem = {"hk1": {}, "hk2": {}}
        self.__bang_diem = bang_diem

    def __str__(self):
        return f"NguoiDung(ho_ten={self.__ho_ten}, email={self.__email})"

    # ------------------ HÀM LẤY (lay_...) ------------------
    def lay_ho_ten(self):
        return self.__ho_ten

    def lay_email(self):
        return self.__email

    def lay_mat_khau(self):
        return self.__mat_khau

    def lay_sdt(self):
        return self.__sdt

    def lay_danh_gia(self):
        return self.__danh_gia

    # hoc_ky: "hk1" hoặc "hk2" -> trả về dict {tên môn: [6 ô điểm]}
    def lay_diem_hoc_ky(self, hoc_ky):
        return self.__bang_diem.get(hoc_ky, {})

    # ------------------ HÀM SỬA (sua_..., có kiểm tra) ------------------
    def sua_ho_ten(self, ho_ten_moi):
        if ho_ten_moi.strip() != "":
            self.__ho_ten = ho_ten_moi

    def sua_mat_khau(self, mat_khau_moi):
        if len(mat_khau_moi) >= 6:
            self.__mat_khau = mat_khau_moi

    def sua_sdt(self, sdt_moi):
        # isdigit(): chỉ toàn chữ số
        if sdt_moi.isdigit():
            self.__sdt = sdt_moi

    def sua_danh_gia(self, so_sao):
        if 1 <= so_sao <= 5:
            self.__danh_gia = so_sao

    def sua_diem_hoc_ky(self, hoc_ky, diem_cac_mon):
        self.__bang_diem[hoc_ky] = diem_cac_mon

    # ------------------ CHUYỂN ĐỔI object <-> dict ------------------
    # object -> dict (để lưu vào file json)
    def chuyen_thanh_dict(self):
        return {
            "ho_ten": self.__ho_ten,
            "email": self.__email,
            "mat_khau": self.__mat_khau,
            "sdt": self.__sdt,
            "danh_gia": self.__danh_gia,
            "bang_diem": self.__bang_diem,
        }

    # dict -> object (khi đọc từ file json)
    @classmethod
    def tao_tu_dict(cls, du_lieu):
        return cls(
            ho_ten=du_lieu.get("ho_ten", ""),
            email=du_lieu.get("email", ""),
            mat_khau=du_lieu.get("mat_khau", ""),
            sdt=du_lieu.get("sdt", ""),
            danh_gia=du_lieu.get("danh_gia", 0),
            bang_diem=du_lieu.get("bang_diem", {"hk1": {}, "hk2": {}}),
        )
