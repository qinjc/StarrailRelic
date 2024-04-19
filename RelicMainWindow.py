import sys
from copy import deepcopy
from itertools import chain

from Relic import Relic
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QMessageBox, QDialog
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

from RelicsGetter import get_relics
from Constants import *

from RelicInspect import Ui_MainWindow  # 导入转换后的ui模块
from RelicModifyConfirmDialog import Ui_Dialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # 使用Ui_MainWindow中的setupUi方法来设置界面
        self.setup()

    def setup(self):
        def relic_filter_func(t_relic):
            if self.radioButton.isChecked() and t_relic.level == 15:
                return False
            return True

        def flush_model_data():
            self.model.update_data(relic_filter_func)

        def display_selected(current: QModelIndex):
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
            dialog_ui = Ui_Dialog()
            dialog = QDialog(self)
            dialog_ui.setupUi(dialog)
            dialog.setWindowTitle('是否确定修改？')

            # 找到圣遗物原属性并显示
            current: QModelIndex = self.tableView.currentIndex()
            current_row = current.row()
            old_relic: Relic = self.model.data_view[current_row]

            lineEdit_sub_entry_names_old = [dialog_ui.__getattribute__('lineEdit_sub_entry_{}_name_old'.format(i))
                                            for i in range(1, 5)]
            lineEdit_sub_entry_values_old = [dialog_ui.__getattribute__('lineEdit_sub_entry_{}_value_old'.format(i))
                                             for i in range(1, 5)]

            dialog_ui.lineEdit_suit.setText(old_relic.suit)
            dialog_ui.lineEdit_position.setText(POSITION_LIB[old_relic.position])
            dialog_ui.lineEdit_level_old.setText(str(old_relic.level))
            dialog_ui.lineEdit_main_entry_name_old.setText(old_relic.main_entry[0])
            dialog_ui.lineEdit_main_entry_value_old.setText('{:.3f}'.format(old_relic.main_entry[1]))

            names_old = sorted(old_relic.sub_entry.keys())
            for i in range(len(old_relic.sub_entry)):
                lineEdit_sub_entry_names_old[i].setText(names_old[i])
                lineEdit_sub_entry_values_old[i].setText('{:.3f}'.format(old_relic.sub_entry[names_old[i]]))

            # 显示新属性
            lineEdit_sub_entry_names_new = [dialog_ui.__getattribute__('lineEdit_sub_entry_{}_name_new'.format(i))
                                            for i in range(1, 5)]
            lineEdit_sub_entry_values_new = [dialog_ui.__getattribute__('lineEdit_sub_entry_{}_value_new'.format(i))
                                             for i in range(1, 5)]

            dialog_ui.lineEdit_level_new.setText(str(self.spinBox_level.value()))
            dialog_ui.lineEdit_main_entry_name_new.setText(self.lineEdit_main_entry_name.text())
            dialog_ui.lineEdit_main_entry_value_new.setText(self.lineEdit_main_entry_value.text())

            for i in range(4):
                lineEdit_sub_entry_names_new[i].setText(self.lineEdit_sub_entry_names[i].text())
                lineEdit_sub_entry_values_new[i].setText(self.lineEdit_sub_entry_values[i].text())

            if dialog.exec_():
                # 获取圣遗物新属性
                new_relic = deepcopy(old_relic)
                # 获取新等级
                new_relic.level = int(dialog_ui.lineEdit_level_new.text())
                # 获取新主词条
                new_relic.main_entry[1] = float(self.lineEdit_main_entry_value.text())
                # 获取新副词条
                for i in range(4):
                    if lineEdit_sub_entry_names_new[i].text() and lineEdit_sub_entry_values_new[i].text():
                        if lineEdit_sub_entry_names_new[i].text() in SUB_ENTRY:
                            new_relic.sub_entry[lineEdit_sub_entry_names_new[i].text()]\
                                = float(lineEdit_sub_entry_values_new[i].text())
                # 更新
                self.model.update_relic(old_relic, new_relic)
                # print(new_relic)

        def on_pushButton_reset():
            current: QModelIndex = self.tableView.currentIndex()
            display_selected(current)

        self.radioButton.toggled.connect(flush_model_data)
        self._setup_data()
        self._setup_col_span()
        selection_model = self.tableView.selectionModel()
        selection_model.currentChanged.connect(display_selected)
        self.pushButton_reset.clicked.connect(on_pushButton_reset)
        self.pushButton_modify.clicked.connect(on_pushButton_modify)

        # TODO: 表格列排序（包括双爆分和期望双爆分）
        # self.tableView.sortByColumn()

    def _setup_data(self):
        output_file_name = 'relics.pkl.qjc'
        sample_data = get_relics(output_file_name)
        sample_data = list(chain.from_iterable(sample_data))

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

    def update_data(self, filter_):
        self.beginResetModel()
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
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
