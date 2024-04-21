from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget,
                             QDialog, QDialogButtonBox, QLabel)


class CustomDialog(QDialog):
    def __init__(self, old_value, new_value, parent=None):
        super().__init__(parent)
        self.old_value = old_value
        self.new_value = new_value
        self.initUI()

    def initUI(self):
        self.setWindowTitle("确认修改")

        # 创建布局
        layout = QVBoxLayout()

        # 显示提示信息
        message = f"是否确定要将 value 从 '{self.old_value}' 改为 '{self.new_value}'？"
        layout.addWidget(QLabel(message))

        # 创建按钮框并添加确认和取消按钮
        buttonBox = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        layout.addWidget(buttonBox)

        # 设置布局
        self.setLayout(layout)

        # 连接按钮信号
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.value = "初始值"  # 初始的value变量
        self._initUI()

    def _initUI(self):
        # 创建布局和控件
        self.layout = QVBoxLayout()
        self.lineEdit = QLineEdit(self.value, self)
        self.pushButton = QPushButton("修改值", self)

        # 将控件添加到布局中
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.pushButton)

        # 设置窗口的布局
        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

        # 连接按钮信号
        self.pushButton.clicked.connect(self.showCustomDialog)

    def showCustomDialog(self):
        new_value = self.lineEdit.text()  # 获取lineEdit中的文本
        dialog = CustomDialog(self.value, new_value, self)

        # 显示对话框并获取用户响应
        if dialog.exec_():
            old_value = self.value
            # 用户点击了确认，修改value变量
            self.value = new_value
            print(f"Value has been changed from {old_value} to: {self.value}")
        else:
            # 用户点击了取消，不执行修改
            print("Modification cancelled by the user.")


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
