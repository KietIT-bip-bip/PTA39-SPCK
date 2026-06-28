from PyQt6.QtWidgets import QMainWindow, QMessageBox
import sys
from PyQt6 import uic
import os
import re


class SettingPage(QMainWindow):
    def __init__(self, main_window, root_dir, cur_acc):
        super().__init__()
        self.main_window = main_window
        self.root_dir = root_dir
        self.cur_acc = cur_acc

        # load file ui
        ui_path = self.root_dir + "/ui/setting.ui"
        uic.loadUi(ui_path, self)

        # bat su kien
        # sidebar
        self.nut_home.clicked.connect(self.goto_home)

        # thong tin hoc sinh
        self.hien_thi_thong_tin()

        # danh sach chuc nang
        self.nut_dangxuat.clicked.connect(self.goto_login)

        # hien thi giao dien
        self.show()

    # ------------------------------------------------------
    def goto_home(self):
        from pages.home import HomePage

        self.home_page = HomePage(
            main_window=self.main_window, root_dir=self.root_dir, cur_acc=self.cur_acc
        )
        self.close()

    def goto_login(self):
        from pages.login import LoginPage

        self.home_page = LoginPage(main_window=self.main_window, root_dir=self.root_dir)
        self.close()

    def hien_thi_thong_tin(self):
        self.username.setText(f"Name: {self.cur_acc["fullname"]}")
        self.email.setText(f"Email: {self.cur_acc["email"]}")
        if "sdt" in self.cur_acc:
            self.sdt.setText(f"SDT: {self.cur_acc["sdt"]}")
        else:
            self.sdt.setText(f"SDT: chưa cập nhật")

    def show_message(self, message):
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
