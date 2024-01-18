import sys

from PySide2 import QtWidgets
from PySide2.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar,
    QFileDialog, QMessageBox, QDialog,
    QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton
)
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Qt

from model import Photo
from model import Stats

class MainWindow(QMainWindow):
    BACKGROUND_IMAGE_PATH = "./resources/background.png"
    WINDOW_HEIGHT = 300
    WINDOW_WIDTH = 450

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.init_window()
        self.init_menu()

        self.status = None

    def init_window(self):
        self.setWindowTitle("回忆卡")
        self.setFixedSize(MainWindow.WINDOW_WIDTH, MainWindow.WINDOW_HEIGHT)
        self.setStyleSheet(f"border-image: url({MainWindow.BACKGROUND_IMAGE_PATH})")


    def init_menu(self):
        menuBar = self.menuBar()

        file_menu = menuBar.addMenu("&操作")

        load_action = QAction("指定导入图片文件夹", self)
        history_action = QAction("查看历史", self)
        exit_action = QAction("退出", self)

        file_menu.addAction(load_action)
        file_menu.addAction(history_action)
        file_menu.addAction(exit_action)

        load_action.triggered.connect(self.on_load_triggered)
        history_action.triggered.connect(self.on_history_triggered)
        exit_action.triggered.connect(self.on_exit_triggered)

    def on_load_triggered(self):
        print("Load pictures...")

        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        print(f"Selected fold_path: {folder_path}")

        is_succeed, msg_txt, ok_photo_paths = Photo.check_photos(folder_path)
        display_photo = False
        if not is_succeed:
            self.show_error_messagebox(msg_txt)
        elif msg_txt:
            res = QMessageBox.warning(None, 
                                      "错误", 
                                      f"{msg_txt}\n\n虽然有上面的文件格式有问题，但还是有符合格式要求的文件，是否继续?",
                                      QMessageBox.Yes, QMessageBox.No,
                                      defaultButton=QMessageBox.Yes)
            if res == QMessageBox.Yes:
                display_photo = True
        else:
            display_photo = True

        if display_photo:
            self.stats = Stats()
            photos = Photo.get_photos(ok_photo_paths)
            for photo in photos:
                self.show_photo_dialog(photo, self.stats)

            self.on_history_triggered()

    def on_history_triggered(self):
        print("Show history...")

        history_txt = f"总共猜了 {self.stats.total_guess_num} 次；\n" \
                      + f"猜对了 {self.stats.guess_right_num} 次；\n" \
                      + f"猜错了 {self.stats.guess_wrong_num} 次；\n"

        QMessageBox.information(None, 
                                "猜猜看历史",
                                history_txt)

    def on_exit_triggered(self):
        print("Exit...")

        self.app.quit()

    def show_error_messagebox(self, msg_txt):
        QMessageBox.critical(None, 
                             "错误信息",
                             msg_txt)

    def show_photo_dialog(self, photo, stats):
        # test
        print(f"photo image path: {photo.image_path}")

        photo_dialog = PhotoDialog(photo, stats)
        photo_dialog.exec_()


class PhotoDialog(QDialog):
    PHOTO_IMAGE_HEIGHT = 600
    PHOTO_IMAGE_WIDTH = 600

    def __init__(self, photo, stats, parent=None):
        super().__init__()
        self.photo = photo
        self.stats = stats

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedSize(PhotoDialog.PHOTO_IMAGE_WIDTH, PhotoDialog.PHOTO_IMAGE_HEIGHT)
        pixmap = QPixmap(photo.image_path)
        pixmap = pixmap.scaled(image_label.size(),
                               Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)

        self.line_editor = QLineEdit()
        self.line_editor.setPlaceholderText("请输入猜测该图片拍摄的月份")

        push_button = QPushButton()
        push_button.setText("确认输入")
        push_button.clicked.connect(self.check_guess)

        child_layout = QHBoxLayout()
        child_layout.addWidget(self.line_editor)
        child_layout.addWidget(push_button)
        
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addLayout(child_layout)
        self.setLayout(layout)

    def check_guess(self):
        guess_month = self.line_editor.text()

        if guess_month.isdigit():
            if self.photo.month == int(guess_month):
                self.stats.guess_right()
                QMessageBox.information(None, 
                                        "提示",
                                        "月份猜对了哦")
            else:
                self.stats.guess_wrong()
                QMessageBox.warning(None, 
                                    "提示",
                                    "月份猜错了哦")
        else:
            QMessageBox.critical(None, 
                                 "错误信息",
                                 "输入的不是月份数")

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow(app)
    w.show()
    app.exec_()