from entity.subject import SubjectAllYear, SubjectAllYearSpecially


class Student:
    def __init__(self, hoten, malop="", sdt="", email="") -> None:
        self.__hoten = hoten
        self.__malop = malop
        self.__sdt = sdt
        self.__email = email
        self.__danhsach_monhoc = []

    # =========================================

    def __str__(self):
        return (
            f"Họ tên: {self.__hoten}\n"
            f"Mã lớp: {self.__malop}\n"
            f"SĐT: {self.__sdt}\n"
            f"Email: {self.__email}\n"
            f"Học lực HK1: {self.get_hoc_luc_hk(1)}\n"
            f"Học lực HK2: {self.get_hoc_luc_hk(2)}\n"
            f"Học lực cả năm: {self.get_hoc_luc_ca_nam()}"
        )

    # =========================================
    # GETTER

    def get_hoten(self):
        return self.__hoten

    def get_malop(self):
        return self.__malop

    def get_sdt(self):
        return self.__sdt

    def get_email(self):
        return self.__email

    def get_danhsach_monhoc(self):
        return self.__danhsach_monhoc

    # =========================================
    # SETTER

    def set_hoten(self, value):
        self.__hoten = value

    def set_malop(self, value):
        self.__malop = value

    def set_sdt(self, value):
        self.__sdt = value

    def set_email(self, value):
        self.__email = value

    # =========================================

    def set_danhsach_monhoc(
        self,
        toan: SubjectAllYear,
        khtn: SubjectAllYear,
        van: SubjectAllYear,
        lsdl: SubjectAllYear,
        anh: SubjectAllYear,
        tinhoc: SubjectAllYear,
        gdcd: SubjectAllYear,
        congnghe: SubjectAllYear,
        gddp: SubjectAllYearSpecially,
        mythuat: SubjectAllYearSpecially,
        amnhac: SubjectAllYearSpecially,
        theduc: SubjectAllYearSpecially,
    ):
        self.__danhsach_monhoc = [
            toan,
            khtn,
            van,
            lsdl,
            anh,
            tinhoc,
            gdcd,
            congnghe,
            gddp,
            mythuat,
            amnhac,
            theduc,
        ]

    # =========================================

    def __get_diem_mon_hk(self, mon, hk):
        if hk == 1:
            return mon.get_subject_hk1().get_diem_trung_binh_hk()

        return mon.get_subject_hk2().get_diem_trung_binh_hk()

    # =========================================

    def get_hoc_luc_hk(self, hk=1):
        # 6 mon (môn tính điểm) tren 5 + các môn còn lại >= 3.5 + special: đạt -> trung bình
        # 6 mon (môn tính điểm) tren 6 + cac mon con lai >= 5 + special: đạt -> khá
        # 6 mon (môn tính điểm) tren 8 + các môn còn lại >= 6 + special: đạt -> giỏi
        # 6 mon (môn tính điểm) tren 9 + các môn còn lại >= 8 + special: đạt -> xuất sắc
        # còn lại là chưa đạt / hoặc có 1 môn special là không đạt -> RỚT

        mon_tinh_diem = self.__danhsach_monhoc[:8]
        mon_special = self.__danhsach_monhoc[8:]

        # kiểm tra môn đạt/không đạt
        for mon in mon_special:
            diem = self.__get_diem_mon_hk(mon, hk)

            if diem == "K Đạt":
                return "RỚT"

        diem_mon_thuong = [self.__get_diem_mon_hk(mon, hk) for mon in mon_tinh_diem]

        # 6 môn chính
        so_mon_tren_9 = sum(1 for x in diem_mon_thuong if x >= 9)
        so_mon_tren_8 = sum(1 for x in diem_mon_thuong if x >= 8)
        so_mon_tren_6 = sum(1 for x in diem_mon_thuong if x >= 6)
        so_mon_tren_5 = sum(1 for x in diem_mon_thuong if x >= 5)

        min_diem = min(diem_mon_thuong)

        if so_mon_tren_9 >= 6 and min_diem >= 8:
            return "Xuất sắc"

        if so_mon_tren_8 >= 6 and min_diem >= 6:
            return "Giỏi"

        if so_mon_tren_6 >= 6 and min_diem >= 5:
            return "Khá"

        if so_mon_tren_5 >= 6 and min_diem >= 3.5:
            return "Trung bình"

        return "Chưa đạt"

    # =========================================

    def get_hoc_luc_ca_nam(self):
        # hoc luc ca nam (luật vẫn giống với học kì)
        # chỉ cần 1 học kì có môn special không đạt -> cả năm RỚT
        # còn lại tính điểm trung bình cả năm của từng môn học rồi cộng lại chia trung bình -> học lực cả năm
        mon_tinh_diem = self.__danhsach_monhoc[:8]
        mon_special = self.__danhsach_monhoc[8:]

        # special
        for mon in mon_special:
            if mon.get_diem_ca_nam() == "K Đạt":
                return "RỚT"

        diem_mon_thuong = [mon.get_diem_ca_nam() for mon in mon_tinh_diem]

        so_mon_tren_9 = sum(1 for x in diem_mon_thuong if x >= 9)
        so_mon_tren_8 = sum(1 for x in diem_mon_thuong if x >= 8)
        so_mon_tren_6 = sum(1 for x in diem_mon_thuong if x >= 6)
        so_mon_tren_5 = sum(1 for x in diem_mon_thuong if x >= 5)

        min_diem = min(diem_mon_thuong)

        if so_mon_tren_9 >= 6 and min_diem >= 8:
            return "Xuất sắc"

        if so_mon_tren_8 >= 6 and min_diem >= 6:
            return "Giỏi"

        if so_mon_tren_6 >= 6 and min_diem >= 5:
            return "Khá"

        if so_mon_tren_5 >= 6 and min_diem >= 3.5:
            return "Trung bình"

        return "Chưa đạt"
