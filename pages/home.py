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
        ui_path = self.root_dir + "/ui/home.ui"
        uic.loadUi(ui_path, self)
        
        
        # bat su kien 
        # sidebar
        self.ket_noi_sidebar()
        
        # thong tin hoc sinh
        self.hien_thi_thong_tin()
        
        # hien thi thong tin hoc ki
        self.setup_score_info()
        
        # hien thi giao dien
        self.show()
        
    # -----------------------------------------------------
    def ket_noi_sidebar(self):
        self.nut_hk1.clicked.connect(self.setup_ui_for_term_1)
        self.nut_hk2.clicked.connect(self.setup_ui_for_term_2)
        self.nut_canam.clicked.connect(self.setup_ui_for_allyear)
        self.nut_caidat.clicked.connect(self.goto_setting)
        
    def goto_setting(self):
        from pages.setting import SettingPage

        self.setting_page = SettingPage(
            main_window=self.main_window, root_dir=self.root_dir, cur_acc=self.cur_acc
        )
        self.close()
    
    def hien_thi_thong_tin(self):
        self.username.setText(f"Username: {self.cur_acc.fullname}")
        self.hoc_luc_allyear.setText(f"Username: {self.get_hoc_luc_allyear()}")
    
    def setup_score_info(self):
        pass
    
    def setup_ui_for_term_1(self):
        pass
    
    def setup_ui_for_term_2(self):
        pass
    
    def setup_ui_for_allyear(self):
        pass
    
    def get_hoc_luc_allyear(self):
        return "Chưa tổng kết."

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