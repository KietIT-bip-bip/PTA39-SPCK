from PyQt6.QtWidgets import QMainWindow, QMessageBox
import sys
from PyQt6 import uic
import os
import re

# mock data
account = {"fullname": "", "email": "", "password": ""}


class SignupPage(QMainWindow):
    def __init__(self, main_window, root_dir):
        super().__init__()  # ke thua cac code init cua lop cha
        self.main_window = main_window  # luu tham so
        self.root_dir = root_dir

        # load file ui
        ui_path = self.root_dir + "/GUI/signup.ui"
        uic.loadUi(ui_path, self)

        # bat su kien cho cac nut bam
        # TODO

        # chay app
        self.show()

    # ------------------ xu ly su kien ------------------
    # TODO
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