from PyQt5.QtWidgets import QDialog
from RelicModifyConfirmDialogUI import Ui_Dialog


class RelicModifyConfirmDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(RelicModifyConfirmDialog, self).__init__()
        self.setupUi(self)

