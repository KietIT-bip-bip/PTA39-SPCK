from PyQt6.QtWidgets import QMainWindow, QMessageBox
import sys
from PyQt6 import uic
import os
import re

# mock data
account = {"fullname": "Kiet", "email": "Kiet@gmail.com", "password": "150110"}


class LoginPage(QMainWindow):
    def __init__(self, main_window, root_dir):
        super().__init__()  # ke thua cac code init cua lop cha
        self.main_window = main_window  # luu tham so
        self.root_dir = root_dir

        # load file ui
        ui_path = self.root_dir + "/ui/login.ui"
        uic.loadUi(ui_path, self)

        # bat su kien cho cac nut bam
        # 1. nut login
        self.login.clicked.connect(
            self.handle_login
        )  # click vao nut login -> goi ham handle_login
        # 2. nut chuyen register
        self.nav_signup.clicked.connect(
            self.goto_signup
        )  # click vao nut chuyen signup -> goi ham goto_registergoto_signup


        # chay app
        self.show()

    # ------------------ xu ly su kien ------------------
    def handle_login(self):
        # lay du lieu tu input form
        email_input = (
            self.email.text().strip()
        )  # lay du lieu tu username input, xoa khoang trang 2 dau
        password_input = self.password.text()

        # validate du lieu
        if self.__validate_input(email_input, password_input) is not None:
            print(self.__validate_input(email_input, password_input))
            # co loi -> bao loi
            self.__show_message(self.__validate_input(email_input, password_input))
            return  # khong lam gi nua
        else:
            # thanh cong -> chuyen sang home
            self.__goto_home()

    def goto_signup(self):
        from pages.signup import SignupPage

        self.signup_page = SignupPage(
            main_window=self.main_window, root_dir=self.root_dir
        )
        self.close()  # ✅ đóng cửa sổ
    def __goto_home(self):
        from pages.home import HomePage

        self.home_page = HomePage(main_window=self.main_window, root_dir=self.root_dir, cur_acc=account)
        self.close()  # ✅ đóng cửa sổ

    def __validate_input(self, email, password):
        # kiem tra email
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(regex, email) is None:
            return "Email khong hop le!"

        # kiem tra password
        if len(password) < 6:
            return "Password phai tu 6 chu so tro len!"

        # kiem tra khop tai khoan (mock data)
        if email != account["email"] or password != account["password"]:
            return "Email hoac password khong chinh xac!"

        return None  # khong co loi
    
    # ------------------ ham ho tro ------------------
    def __show_message(self, message):
        # Khởi tạo hộp thoại thông báo
        msg = QMessageBox()
        msg.setWindowTitle("Thông báo")
        msg.setText(message)
        msg.setIcon(
            QMessageBox.Icon.Information
        )  # Các icon mặc định: Information, Warning, Critical, Question
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)  # Nút bấm OK
        # Hiển thị hộp thoại
        msg.exec()