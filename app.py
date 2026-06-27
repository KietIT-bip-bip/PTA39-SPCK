from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from PyQt6 import uic
import os

from pages.login import LoginPage  # trang dau tien truy cap
from pages.home import HomePage

# lay duong dan den cac file con
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# chi chay khi run bang app.py
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # first_page = LoginPage(main_window=None, root_dir=BASE_DIR)
    first_page = HomePage(
        main_window=None,
        root_dir=BASE_DIR,
        cur_acc={"fullname": "Kiet", "email": "Kiet@gmail.com", "password": "150110"},
    )
    sys.exit(app.exec())
