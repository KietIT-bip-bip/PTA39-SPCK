from PyQt6.QtWidgets import QMainWindow, QMessageBox
import sys
from PyQt6 import uic
import os
import re


class HomePage(QMainWindow):
    def __init__(self, main_window, root_dir, cur_acc):
        super().__init__()
        self.main_window = main_window
        self.root_dir = root_dir
        self.cur_acc = cur_acc

        # load file ui
        ui_path = self.root_dir + "/GUI/home.ui"
        uic.loadUi(ui_path, self)

        # bat su kien cho cac nut bam
        # TODO

        # hien thi giao dien
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