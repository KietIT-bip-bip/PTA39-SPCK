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
        
        # hien thi giao dien
        self.show()