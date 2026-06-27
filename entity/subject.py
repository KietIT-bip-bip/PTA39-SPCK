class Subject1Term:
    def __init__(
        self,
        hk=1,
        diem_tx1=0,
        diem_tx2=0,
        diem_tx3=0,
        diem_tx4=0,
        diem_gk=0,
        diem_ck=0,
    ) -> None:
        self.__hk = hk

        self.__diem_tx1 = 0
        self.__diem_tx2 = 0
        self.__diem_tx3 = 0
        self.__diem_tx4 = 0
        self.__diem_gk = 0
        self.__diem_ck = 0

        self.set_diem_tx1(diem_tx1)
        self.set_diem_tx2(diem_tx2)
        self.set_diem_tx3(diem_tx3)
        self.set_diem_tx4(diem_tx4)
        self.set_diem_gk(diem_gk)
        self.set_diem_ck(diem_ck)

    # =========================
    # VALIDATE

    def __check_score(self, diem):
        if not isinstance(diem, (int, float)):
            raise ValueError("Điểm phải là số")

        if diem < 0 or diem > 10:
            raise ValueError("Điểm phải nằm trong khoảng từ 0 đến 10")

        return float(diem)

    # =========================
    # GETTER

    def get_hk(self):
        return self.__hk

    def get_diem_tx1(self):
        return self.__diem_tx1

    def get_diem_tx2(self):
        return self.__diem_tx2

    def get_diem_tx3(self):
        return self.__diem_tx3

    def get_diem_tx4(self):
        return self.__diem_tx4

    def get_diem_gk(self):
        return self.__diem_gk

    def get_diem_ck(self):
        return self.__diem_ck

    # =========================
    # SETTER

    def set_diem_tx1(self, diem_moi):
        self.__diem_tx1 = self.__check_score(diem_moi)

    def set_diem_tx2(self, diem_moi):
        self.__diem_tx2 = self.__check_score(diem_moi)

    def set_diem_tx3(self, diem_moi):
        self.__diem_tx3 = self.__check_score(diem_moi)

    def set_diem_tx4(self, diem_moi):
        self.__diem_tx4 = self.__check_score(diem_moi)

    def set_diem_gk(self, diem_moi):
        self.__diem_gk = self.__check_score(diem_moi)

    def set_diem_ck(self, diem_moi):
        self.__diem_ck = self.__check_score(diem_moi)

    # =========================

    def get_diem_trung_binh_hk(self):
        tong = (
            self.__diem_tx1
            + self.__diem_tx2
            + self.__diem_tx3
            + self.__diem_tx4
            + self.__diem_gk * 2
            + self.__diem_ck * 3
        )

        return round(tong / 9, 1)


# =========================================


class Subject1TermSpecially:
    """
    Dành cho môn Đạt / K Đạt
    """

    VALID_VALUES = ("Đạt", "K Đạt")

    def __init__(
        self,
        hk=1,
        diem_tx1="Đạt",
        diem_tx2="Đạt",
        diem_tx3="Đạt",
        diem_tx4="Đạt",
        diem_gk="Đạt",
        diem_ck="Đạt",
    ) -> None:
        self.__hk = hk

        self.__diem_tx1 = "Đạt"
        self.__diem_tx2 = "Đạt"
        self.__diem_tx3 = "Đạt"
        self.__diem_tx4 = "Đạt"
        self.__diem_gk = "Đạt"
        self.__diem_ck = "Đạt"

        self.set_diem_tx1(diem_tx1)
        self.set_diem_tx2(diem_tx2)
        self.set_diem_tx3(diem_tx3)
        self.set_diem_tx4(diem_tx4)
        self.set_diem_gk(diem_gk)
        self.set_diem_ck(diem_ck)

    # =========================
    # VALIDATE

    def __check_value(self, value):
        if value not in self.VALID_VALUES:
            raise ValueError('Giá trị phải là "Đạt" hoặc "K Đạt"')

        return value

    # =========================
    # GETTER

    def get_hk(self):
        return self.__hk

    def get_diem_tx1(self):
        return self.__diem_tx1

    def get_diem_tx2(self):
        return self.__diem_tx2

    def get_diem_tx3(self):
        return self.__diem_tx3

    def get_diem_tx4(self):
        return self.__diem_tx4

    def get_diem_gk(self):
        return self.__diem_gk

    def get_diem_ck(self):
        return self.__diem_ck

    # =========================
    # SETTER

    def set_diem_tx1(self, value):
        self.__diem_tx1 = self.__check_value(value)

    def set_diem_tx2(self, value):
        self.__diem_tx2 = self.__check_value(value)

    def set_diem_tx3(self, value):
        self.__diem_tx3 = self.__check_value(value)

    def set_diem_tx4(self, value):
        self.__diem_tx4 = self.__check_value(value)

    def set_diem_gk(self, value):
        self.__diem_gk = self.__check_value(value)

    def set_diem_ck(self, value):
        self.__diem_ck = self.__check_value(value)

    # =========================

    def get_diem_trung_binh_hk(self):
        ds_diem = [
            self.__diem_tx1,
            self.__diem_tx2,
            self.__diem_tx3,
            self.__diem_tx4,
            self.__diem_gk,
            self.__diem_ck,
        ]

        if "K Đạt" in ds_diem:
            return "K Đạt"

        return "Đạt"


# =========================================


class SubjectAllYear:
    def __init__(
        self,
        ten_mon_hoc,
        subject_hk1: Subject1Term,
        subject_hk2: Subject1Term,
    ):
        if not ten_mon_hoc.strip():
            raise ValueError("Tên môn học không được rỗng")

        self.__ten_mon_hoc = ten_mon_hoc
        self.__subject_hk1 = subject_hk1
        self.__subject_hk2 = subject_hk2
        self.__diem_ca_nam = 0

    # =========================

    def __str__(self) -> str:
        return (
            f"Môn học: {self.__ten_mon_hoc}\n"
            f"TB HK1: {self.__subject_hk1.get_diem_trung_binh_hk()}\n"
            f"TB HK2: {self.__subject_hk2.get_diem_trung_binh_hk()}\n"
            f"TB Cả năm: {self.get_diem_ca_nam()}"
        )

    # =========================
    # GETTER

    def get_ten_mon_hoc(self):
        return self.__ten_mon_hoc

    def get_subject_hk1(self):
        return self.__subject_hk1

    def get_subject_hk2(self):
        return self.__subject_hk2

    # =========================
    # SETTER

    def set_ten_mon_hoc(self, ten_moi):
        if not ten_moi.strip():
            raise ValueError("Tên môn học không được rỗng")

        self.__ten_mon_hoc = ten_moi

    # =========================

    def get_diem_ca_nam(self):
        hk1 = self.__subject_hk1.get_diem_trung_binh_hk()
        hk2 = self.__subject_hk2.get_diem_trung_binh_hk()

        self.__diem_ca_nam = round((hk1 + hk2 * 2) / 3, 1)

        return self.__diem_ca_nam


# =========================================


class SubjectAllYearSpecially:
    def __init__(
        self,
        ten_mon_hoc,
        diem_hk1: Subject1TermSpecially,
        diem_hk2: Subject1TermSpecially,
    ):
        if not ten_mon_hoc.strip():
            raise ValueError("Tên môn học không được rỗng")

        self.__ten_mon_hoc = ten_mon_hoc
        self.__diem_hk1 = diem_hk1
        self.__diem_hk2 = diem_hk2
        self.__diem_ca_nam = ""

    # =========================

    def __str__(self) -> str:
        return (
            f"Môn học: {self.__ten_mon_hoc}\n"
            f"HK1: {self.__diem_hk1.get_diem_trung_binh_hk()}\n"
            f"HK2: {self.__diem_hk2.get_diem_trung_binh_hk()}\n"
            f"Cả năm: {self.get_diem_ca_nam()}"
        )

    # =========================
    # GETTER

    def get_ten_mon_hoc(self):
        return self.__ten_mon_hoc

    def get_diem_hk1(self):
        return self.__diem_hk1

    def get_diem_hk2(self):
        return self.__diem_hk2

    # =========================
    # SETTER

    def set_ten_mon_hoc(self, ten_moi):
        if not ten_moi.strip():
            raise ValueError("Tên môn học không được rỗng")

        self.__ten_mon_hoc = ten_moi

    # =========================

    def get_diem_ca_nam(self):
        hk1 = self.__diem_hk1.get_diem_trung_binh_hk()
        hk2 = self.__diem_hk2.get_diem_trung_binh_hk()

        if hk1 == "K Đạt" or hk2 == "K Đạt":
            return "K Đạt"

        return "Đạt"
