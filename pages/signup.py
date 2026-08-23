from collections import UserList
from entity import UserList
from entity import User
from PyQt6.QtWidgets import QMainWindow, QMessageBox
import sys
from PyQt6 import uic
import os
import re

# mock data



class SignupPage(QMainWindow):
    def __init__(self, main_window, root_dir):
        super().__init__()  # ke thua cac code init cua lop cha
        self.main_window = main_window  # luu tham so
        self.root_dir = root_dir

        # load file ui
        ui_path = self.root_dir + "/ui/signup.ui"
        uic.loadUi(ui_path, self)

        # bat su kien cho cac nut bam
         # 1. nut login
        self.signup.clicked.connect(
            self.handle_register
        )  # click vao nut login -> goi ham handle_register
        # 2. nut chuyen register
        self.nav_login.clicked.connect(
            self.goto_login
        )  # click vao nut chuyen register -> goi ham goto_login

        # chay app
        self.show()

    # ------------------ xu ly su kien ------------------
    def handle_register(self):
        # lay du lieu tu input form
        email_input = (
            self.email.text().strip()
        )  # lay du lieu tu email input, xoa khoang trang 2 dau
        password_input = self.password.text()
        confirm_password_input = self.password_2.text()
        fullname_input = self.full_name.text()

        # kiem tra fullname
        if fullname_input.strip() == "":
            self.__show_message("Vui lòng nhập đầy đủ họ tên!")
            return  # bao loi -> ket thuc
        
        # kiem tra confirm pass
        if password_input != confirm_password_input:
            self.__show_message("Vui lòng điền đúng mật khẩu!")
            return 

        # validate du lieu
        if self.__validate_input(email_input, password_input) is not None:
            print(self.__validate_input(email_input, password_input))
            # co loi -> bao loi
            self.__show_message(self.__validate_input(email_input, password_input))
            return  # khong lam gi nua
        else:
           # luu tai khoan
            # 1. tao user
            new_user = User(username=fullname_input, email=email_input, password=password_input)
            # 2. luu vao danh sach
            user_list = UserList()
            user_list.add_user(new_user)
            # 3. luu json
            user_list.save_to_json("data/user.json")

            # thanh cong -> chuyen sang home
            self.__goto_home()

    def goto_login(self):
        from pages.login import LoginPage

        self.login_page = LoginPage(
            main_window=self.main_window, root_dir=self.root_dir
        )
        self.close()  # ✅ đóng cửa sổ
    def __goto_home(self):
        from pages.home import HomePage

        self.home_page = HomePage(
            main_window=self.main_window, root_dir=self.root_dir, cur_acc=account
        )
        self.close()  # ✅ đóng cửa sổ

    def __validate_input(self, email, password):
        # kiem tra email
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(regex, email) is None:
            return "Email khong hop le!"

        # kiem tra password
        if len(password) < 6:
            return "Password phai tu 6 chu so tro len!"

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