from PyQt5.QtWidgets import QDialog
from RelicFilterDialogUI import Ui_Dialog


class RelicFilterDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(RelicFilterDialog, self).__init__()
        self.setupUi(self)
        self.suit_checked_set = {attr for attr in self.__dir__()
                                 if 'checkBox_innersuit' in attr or 'checkBox_outersuit' in attr}
        self.position_checked_set = {attr for attr in self.__dir__() if 'checkBox_position' in attr}
        self.main_entry_checked_set = {attr for attr in self.__dir__() if 'checkBox_main_entry' in attr}
        self.sub_entry_checked_set = {attr for attr in self.__dir__() if 'checkBox_sub_entry' in attr}
