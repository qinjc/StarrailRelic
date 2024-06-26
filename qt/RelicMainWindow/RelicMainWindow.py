import sys
import threading
from copy import deepcopy
from itertools import chain

from core.Relic import Relic
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QCheckBox, QMessageBox
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

from core.Constants import *
from core.RelicsGetter import get_relics

from qt.RelicMainWindow.RelicMainWindowUI import Ui_RelicMainWindow  # 导入转换后的ui模块
from qt.RelicModifyConfirmDialog.RelicModifyConfirmDialog import RelicModifyConfirmDialog
from qt.RelicFilterDialog.RelicFilterDialog import RelicFilterDialog


class RelicMainWindow(QMainWindow, Ui_RelicMainWindow):
    def __init__(self, relics_file_name):
        super(RelicMainWindow, self).__init__()
        self.relics_file_name = relics_file_name
        self.relics_arrange_by_position = []

        self.setupUi(self)  # 使用Ui_MainWindow中的setupUi方法来设置界面
        self.setFixedSize(1600, 600)
        self._setup_variable()
        self._setup_widget()

    def _setup_variable(self):
        self.ignore_full_level = False
        self.selected_suit = SUIT
        self.selected_position = set(POSITION_INDEX.values())
        self.selected_main_entry = MAIN_ENTRY
        self.selected_sub_entry = SUB_ENTRY
        self.get_relics_thread_working = False

    def _setup_widget(self):
        def relic_filter_func(t_relic: Relic):
            if self.ignore_full_level and t_relic.level == 15:
                return False
            if t_relic.suit not in self.selected_suit:
                return False
            if t_relic.position not in self.selected_position:
                return False
            if t_relic.main_entry[0] not in self.selected_main_entry:
                return False
            if not (t_relic.sub_entry.keys() | self.selected_sub_entry):
                return False
            return True

        def on_click_ignore_button():
            self.ignore_full_level = self.checkBox_ignore_full_level.isChecked()
            self.model.filter_data(relic_filter_func)

        def display_selected(current: QModelIndex):
            self.pushButton_modify.setEnabled(True)
            self.pushButton_reset.setEnabled(True)

            current_row = current.row()
            select_relic: Relic = self.model.data_view[current_row]
            self.lineEdit_suit.setText(select_relic.suit)
            self.lineEdit_position.setText(POSITION_LIB[select_relic.position])
            self.spinBox_level.setValue(select_relic.level)
            self.lineEdit_main_entry_name.setText(select_relic.main_entry[0])
            self.lineEdit_main_entry_value.setText('{:.3f}'.format(select_relic.main_entry[1]))

            names = sorted(select_relic.sub_entry.keys())
            for i in range(len(select_relic.sub_entry)):
                self.lineEdit_sub_entry_names[i].setText(names[i])
                self.lineEdit_sub_entry_values[i].setText('{:.3f}'.format(select_relic.sub_entry[names[i]]))
            if len(select_relic.sub_entry) == 3:
                self.lineEdit_sub_entry_names[3].clear()
                self.lineEdit_sub_entry_names[3].setReadOnly(False)
                self.lineEdit_sub_entry_names[3].setFrame(True)
                self.lineEdit_sub_entry_values[3].clear()
            else:
                self.lineEdit_sub_entry_names[3].setReadOnly(True)
                self.lineEdit_sub_entry_names[3].setFrame(False)

        def on_pushButton_modify():
            dialog = RelicModifyConfirmDialog()

            # 找到圣遗物原属性并显示
            current: QModelIndex = self.tableView.currentIndex()
            current_row = current.row()
            old_relic: Relic = self.model.data_view[current_row]

            lineEdit_sub_entry_names_old = [dialog.__getattribute__('lineEdit_sub_entry_{}_name_old'.format(i))
                                            for i in range(1, 5)]
            lineEdit_sub_entry_values_old = [dialog.__getattribute__('lineEdit_sub_entry_{}_value_old'.format(i))
                                             for i in range(1, 5)]

            dialog.lineEdit_suit.setText(old_relic.suit)
            dialog.lineEdit_position.setText(POSITION_LIB[old_relic.position])
            dialog.lineEdit_level_old.setText(str(old_relic.level))
            dialog.lineEdit_main_entry_name_old.setText(old_relic.main_entry[0])
            dialog.lineEdit_main_entry_value_old.setText('{:.3f}'.format(old_relic.main_entry[1]))

            names_old = sorted(old_relic.sub_entry.keys())
            for i in range(len(old_relic.sub_entry)):
                lineEdit_sub_entry_names_old[i].setText(names_old[i])
                lineEdit_sub_entry_values_old[i].setText('{:.3f}'.format(old_relic.sub_entry[names_old[i]]))

            # 显示新属性
            lineEdit_sub_entry_names_new = [dialog.__getattribute__('lineEdit_sub_entry_{}_name_new'.format(i))
                                            for i in range(1, 5)]
            lineEdit_sub_entry_values_new = [dialog.__getattribute__('lineEdit_sub_entry_{}_value_new'.format(i))
                                             for i in range(1, 5)]

            dialog.lineEdit_level_new.setText(str(self.spinBox_level.value()))
            dialog.lineEdit_main_entry_name_new.setText(self.lineEdit_main_entry_name.text())
            dialog.lineEdit_main_entry_value_new.setText(self.lineEdit_main_entry_value.text())

            for i in range(4):
                lineEdit_sub_entry_names_new[i].setText(self.lineEdit_sub_entry_names[i].text())
                lineEdit_sub_entry_values_new[i].setText(self.lineEdit_sub_entry_values[i].text())

            if dialog.exec_():
                # 获取圣遗物新属性
                new_relic = deepcopy(old_relic)
                # 获取新等级
                new_relic.level = int(dialog.lineEdit_level_new.text())
                # 获取新主词条
                new_relic.main_entry[1] = float(self.lineEdit_main_entry_value.text())
                # 获取新副词条
                for i in range(4):
                    if lineEdit_sub_entry_names_new[i].text() and lineEdit_sub_entry_values_new[i].text():
                        if lineEdit_sub_entry_names_new[i].text() in SUB_ENTRY:
                            new_relic.sub_entry[lineEdit_sub_entry_names_new[i].text()] \
                                = float(lineEdit_sub_entry_values_new[i].text())
                # 更新
                self.model.update_relic(old_relic, new_relic)
                # print(new_relic)

        def on_pushButton_reset():
            current: QModelIndex = self.tableView.currentIndex()
            display_selected(current)

        def sort_table_by_column(col):
            if col not in {3, 4}:
                return
            if col == 3:
                self.model.sort_data_view(key=lambda x: x.get_crit_score())
            elif col == 4:
                self.model.sort_data_view(key=lambda x: x.get_crit_score_expectation())

        def on_pushButton_filter():
            def on_clicked_select_suit(t_dialog: RelicFilterDialog, select_all: bool = True):
                for t_check_box_name in t_dialog.suit_checked_set:
                    t_dialog.__getattribute__(t_check_box_name).setChecked(select_all)

            def on_clicked_select_position(t_dialog: RelicFilterDialog, select_all: bool = True):
                for t_check_box_name in t_dialog.position_checked_set:
                    t_dialog.__getattribute__(t_check_box_name).setChecked(select_all)

            def on_clicked_select_main_entry(t_dialog: RelicFilterDialog, select_all: bool = True):
                for t_check_box_name in t_dialog.main_entry_checked_set:
                    t_dialog.__getattribute__(t_check_box_name).setChecked(select_all)

            def on_clicked_select_sub_entry(t_dialog: RelicFilterDialog, select_all: bool = True):
                for t_check_box_name in t_dialog.sub_entry_checked_set:
                    t_dialog.__getattribute__(t_check_box_name).setChecked(select_all)

            dialog = self.filter_dialog
            # 套装筛选
            dialog.pushButton_suit_select_all.clicked.connect(lambda: on_clicked_select_suit(dialog, True))
            dialog.pushButton_suit_select_none.clicked.connect(lambda: on_clicked_select_suit(dialog, False))
            # 位置筛选
            dialog.pushButton_position_select_all.clicked.connect(lambda: on_clicked_select_position(dialog, True))
            dialog.pushButton_position_select_none.clicked.connect(lambda: on_clicked_select_position(dialog, False))
            # 主词条筛选
            dialog.pushButton_main_entry_select_all.clicked.connect(lambda:
                                                                    on_clicked_select_main_entry(dialog, True))
            dialog.pushButton_main_entry_select_none.clicked.connect(lambda:
                                                                     on_clicked_select_main_entry(dialog, False))
            # 副词条筛选
            dialog.pushButton_sub_entry_select_all.clicked.connect(lambda: on_clicked_select_sub_entry(dialog, True))
            dialog.pushButton_sub_entry_select_none.clicked.connect(lambda: on_clicked_select_sub_entry(dialog, False))

            if dialog.exec_():
                # 获取套装的选中状态
                for check_box_name in dialog.suit_checked_set:
                    check_box: QCheckBox = dialog.__getattribute__(check_box_name)
                    suit_name = check_box.text()
                    if check_box.isChecked():
                        self.selected_suit.add(suit_name)
                    else:
                        self.selected_suit.discard(suit_name)

                # 获取位置的选中状态
                for check_box_name in dialog.position_checked_set:
                    check_box: QCheckBox = dialog.__getattribute__(check_box_name)
                    position: int = POSITION_INDEX[check_box.text()]
                    if check_box.isChecked():
                        self.selected_position.add(position)
                    else:
                        self.selected_position.discard(position)

                # 获取主词条选中状态
                for check_box_name in dialog.main_entry_checked_set:
                    check_box: QCheckBox = dialog.__getattribute__(check_box_name)
                    main_entry_name = check_box.text()
                    if check_box.isChecked():
                        self.selected_main_entry.add(main_entry_name)
                    else:
                        self.selected_main_entry.discard(main_entry_name)

                # 获取副词条选中状态
                for check_box_name in dialog.sub_entry_checked_set:
                    check_box: QCheckBox = dialog.__getattribute__(check_box_name)
                    sub_entry_name = check_box.text()
                    if check_box.isChecked():
                        self.selected_sub_entry.add(sub_entry_name)
                    else:
                        self.selected_sub_entry.discard(sub_entry_name)

                self.model.filter_data(relic_filter_func)

        def on_pushButton_get_relics():
            def scan_relics_on_thread():
                self.relics_arrange_by_position = get_relics(self.relics_file_name)
                self.model.update_data(list(chain.from_iterable(self.relics_arrange_by_position)))
                self.get_relics_thread_working = False

            if self.get_relics_thread_working:
                QMessageBox.warning(self, "别急", "扫描仍在进行中")
                return
            self.relics_arrange_by_position = get_relics(self.relics_file_name, scan=False)
            self.model.update_data(list(chain.from_iterable(self.relics_arrange_by_position)))
            if not self.relics_arrange_by_position:
                scan_confirm = QMessageBox.question(self,
                                                    f"未找到{self.relics_file_name}",
                                                    "是否确定要从屏幕上获取遗器（该过程需要OCR，可能会花费一些时间）？",
                                                    QMessageBox.Yes | QMessageBox.No)
                if scan_confirm == QMessageBox.Yes:
                    self.get_relics_thread = threading.Thread(target=scan_relics_on_thread)
                    self.get_relics_thread.start()
                    self.get_relics_thread_working = True

        self.checkBox_ignore_full_level.toggled.connect(on_click_ignore_button)
        self._setup_data()
        self._setup_col_span()
        selection_model = self.tableView.selectionModel()
        selection_model.currentChanged.connect(display_selected)
        self.pushButton_reset.clicked.connect(on_pushButton_reset)
        self.pushButton_modify.clicked.connect(on_pushButton_modify)
        self.tableView.horizontalHeader().sectionClicked.connect(sort_table_by_column)

        # 筛选的Dialog
        self.filter_dialog = RelicFilterDialog()
        self.pushButton_filter.clicked.connect(on_pushButton_filter)

        # 获取遗器
        self.pushButton_get_relics.clicked.connect(on_pushButton_get_relics)

    def _setup_data(self):
        sample_data = list(chain.from_iterable(self.relics_arrange_by_position))

        # 副词条修改框 集成
        self.lineEdit_sub_entry_names = [self.__getattribute__('lineEdit_sub_entry_{}_name'.format(i)) for i in
                                         range(1, 5)]
        self.lineEdit_sub_entry_values = [self.__getattribute__('lineEdit_sub_entry_{}_value'.format(i)) for i in
                                          range(1, 5)]

        # 创建模型并设置到视图
        self.model = MyTableModel(sample_data)
        self.tableView.setModel(self.model)

    def _setup_col_span(self):
        # 设置列宽
        self.tableView.setColumnWidth(0, 130)
        self.tableView.setColumnWidth(1, 50)
        self.tableView.setColumnWidth(2, 35)
        self.tableView.setColumnWidth(3, 50)
        self.tableView.setColumnWidth(4, 70)
        self.tableView.setColumnWidth(5, 110)
        self.tableView.setColumnWidth(6, 70)
        self.tableView.setColumnWidth(7, 90)
        self.tableView.setColumnWidth(8, 80)
        self.tableView.setColumnWidth(9, 90)
        self.tableView.setColumnWidth(10, 80)
        self.tableView.setColumnWidth(11, 90)
        self.tableView.setColumnWidth(12, 80)
        self.tableView.setColumnWidth(13, 90)
        self.tableView.setColumnWidth(14, 80)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)


class MyTableModel(QAbstractTableModel):
    def __init__(self, data: list):
        super().__init__()
        self.raw_data = data
        self.data_view = deepcopy(self.raw_data)
        self.headers = ['套装', '部位', '等级', '双爆分', '期望双爆分', '主词条属性', '主词条数值'] + \
                       ['副词条1属性', '副词条1数值', '副词条2属性', '副词条2数值'] + \
                       ['副词条3属性', '副词条3数值', '副词条4属性', '副词条4数值']

    def update_data(self, new_data):
        self.raw_data = new_data
        self.beginResetModel()
        self.data_view = deepcopy(self.raw_data)
        self.endResetModel()

    def filter_data(self, filter_):
        self.beginResetModel()
        if self.raw_data:
            self.data_view = list(filter(filter_, self.raw_data))
            self.data_view.sort(key=lambda x: x.get_crit_score_expectation(), reverse=True)
        self.endResetModel()

    def update_relic(self, old_relic: Relic, new_relic: Relic):
        for i, relic in enumerate(self.raw_data):
            if relic == old_relic:
                self.beginResetModel()
                self.raw_data[i] = new_relic
                self.endResetModel()
        for i, relic in enumerate(self.data_view):
            if relic == old_relic:
                self.beginResetModel()
                self.data_view[i] = new_relic
                self.endResetModel()

        self.beginResetModel()
        self.raw_data.sort(key=lambda x: x.get_crit_score_expectation(), reverse=True)
        self.data_view.sort(key=lambda x: x.get_crit_score_expectation(), reverse=True)
        self.endResetModel()

    def sort_data_view(self, key):
        self.beginResetModel()
        self.data_view.sort(key=key, reverse=True)
        self.endResetModel()

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if not index.isValid() or not (0 <= index.row() < len(self.data_view)):
            return None

        row, col = index.row(), index.column()
        relic_data = self.data_view[row]

        if col == 0:
            return relic_data.suit
        elif col == 1:
            return POSITION_LIB[relic_data.position]
        elif col == 2:
            return relic_data.level
        elif col == 3:
            return relic_data.get_crit_score()
        elif col == 4:
            return relic_data.get_crit_score_expectation()
        elif col == 5:
            return relic_data.main_entry[0]
        elif col == 6:
            return relic_data.main_entry[1]
        elif 7 <= col <= 14:
            sub_entry_num = (col - 7) // 2
            if sub_entry_num == 3 and len(relic_data.sub_entry) == 3:
                return None
            sub_entry_flag = (col - 7) % 2
            if sub_entry_flag == 0:
                return sorted(relic_data.sub_entry.keys())[sub_entry_num]
            else:
                return relic_data.sub_entry[sorted(relic_data.sub_entry.keys())[sub_entry_num]]
        return None

    def rowCount(self, index=QModelIndex()):
        return len(self.data_view)

    def columnCount(self, index=QModelIndex()):
        return len(self.headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = RelicMainWindow('relics.pkl.qjc')
    main_window.show()
    sys.exit(app.exec_())
