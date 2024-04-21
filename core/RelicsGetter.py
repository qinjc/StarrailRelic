import logging
import os
import pickle
import sys
import time
from threading import Thread

import keyboard
from PIL import ImageGrab, ImageChops
import numpy as np

from core.Constants import *
import core.Relic
from core.Relic import Relic


# 从屏幕或者文件中获取玩家的库存遗器
def get_relics(output_file_path, output_file_name):
    sys.path.append('core')
    output_file = os.path.join(output_file_path, output_file_name)
    if output_file_name in os.listdir(output_file_path):
        with open(output_file, 'rb') as fp:
            relics = pickle.load(fp)
    else:
        relics = scan_relics()
        with open(output_file, 'wb') as fp:
            pickle.dump(relics, fp)
    return relics


# 提供位置返回识别结果
# invert为是否将图片反色
def m_ocr(ocr, bbox_key, invert, det=True):
    img = ImageGrab.grab(NAVIGATION[bbox_key])
    if invert:
        img = ImageChops.invert(img)
    # if bbox_key == 'level':
    #     img.show()
    img_arr = np.array(img)
    rst = ocr.ocr(img_arr, cls=False, bin=True, det=det)
    return rst


class ocr_thread(Thread):
    def __init__(self, func, *args, **kwargs):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def run(self):
        self.result = self.func(*self.args, **self.kwargs)

    def get_result(self):
        return self.result


# 纠正套装名字
def correct_suit_name(relic):
    max_score = 0
    s1 = set(relic.suit)
    for suit_name in SUIT:
        s2 = set(suit_name)
        intersection = s1 & s2
        union = s1 | s2
        score = len(intersection) / len(union)
        if score > max_score:
            relic.suit = suit_name
            max_score = score


# 通过扫描屏幕获取玩家的库存遗器
def scan_relics():
    print('waiting...')
    # 检测键盘"`"键启动
    keyboard.wait('`')
    scroll_control_lib = [5] * 24 + [4]
    scroll_control_pos = 0

    print('importing OCR...')
    paddleocr = __import__('paddleocr')
    print('initial OCR...')
    # import paddleocr
    ocr = paddleocr.PaddleOCR(lang="ch", use_gpu=True, show_log=False)
    print('OCR is ready...')

    pyautogui = __import__('pyautogui')

    relics = [[] for _ in range(len(POSITION_LIB))]
    col_first_relic = None
    page_end = False
    detect_end = False
    offset_y = 200
    offset_y_cnt = 0
    # start_position = (249, 358)

    start_time = time.time()
    print('detection start')
    # 查询10行
    # for row in range(119):
    row = 0
    while not detect_end:
        # 每行9个
        if page_end:
            offset_y_cnt += 1
        for col in range(9):
            pyautogui.click(249 + col * 167, 358 + offset_y * offset_y_cnt, duration=0)
            print('row:{}, col:{}'.format(row, col))
            feature_color = tuple(np.array(ImageGrab.grab(NAVIGATION['color']))[0][0])

            if feature_color == COLOR['purple']:
                detect_end = True
                break
            elif feature_color != COLOR['orange']:
                raise ValueError('color: {} not found!'.format(feature_color))

            # 三词条时“二件套”的位置
            rst_3_ocr_instance = ocr_thread(m_ocr, ocr, 'flag_3', invert=True)
            rst_3_ocr_instance.start()
            rst_3_ocr_instance.join()
            rst_3_ocr_result = rst_3_ocr_instance.get_result()
            try:
                rst_3 = rst_3_ocr_result[0][0][1][0]
                rst_3_bool = (rst_3 == '二件套')
            except TypeError:
                rst_3 = None
                rst_3_bool = False

            # 四词条时“二件套”的位置
            rst_4_ocr_instance = ocr_thread(m_ocr, ocr, 'flag_4', invert=True)
            rst_4_ocr_instance.start()
            rst_4_ocr_instance.join()
            rst_4_ocr_result = rst_4_ocr_instance.get_result()
            try:
                rst_4 = rst_4_ocr_result[0][0][1][0]
                rst_4_bool = (rst_4 == '二件套')
            except TypeError:
                rst_4 = None
                rst_4_bool = False

            entry_num = 3 if rst_3_bool else 4

            # 词条检测异常，并不是恰好其中一个检测到了“二件套”
            if rst_3_bool ^ rst_4_bool == 0:
                raise Exception('entry number detects wrongly! Detected {} and {} respectively.'.format(
                    rst_3, rst_4
                ))
            else:
                # ocr 遗器位置
                position_ocr_instance = ocr_thread(m_ocr, ocr, 'position', invert=False, det=False)
                position_ocr_instance.start()
                position_ocr_instance.join()
                position_ocr_result = position_ocr_instance.get_result()
                position = POSITION_INDEX[position_ocr_result[0][0][0]]

                # ocr 遗器等级
                level_ocr_instance = ocr_thread(m_ocr, ocr, 'level', invert=True, det=False)
                level_ocr_instance.start()
                level_ocr_instance.join()
                level_ocr_result = level_ocr_instance.get_result()
                level = int(level_ocr_result[0][0][0])

                # ocr 遗器主词条属性
                main_entry_name_ocr_instance = ocr_thread(m_ocr, ocr, 'main_entry_name', invert=False, det=False)
                main_entry_name_ocr_instance.start()
                main_entry_name_ocr_instance.join()
                main_entry_name_ocr_result = main_entry_name_ocr_instance.get_result()
                main_entry_name = main_entry_name_ocr_result[0][0][0]

                # ocr 遗器主词条数值
                main_entry_value_ocr_instance = ocr_thread(m_ocr, ocr, 'main_entry_value', invert=False)
                main_entry_value_ocr_instance.start()
                main_entry_value_ocr_instance.join()
                main_entry_value_ocr_result = main_entry_value_ocr_instance.get_result()
                main_entry_value = main_entry_value_ocr_result[0][0][1][0]

                # ocr 遗器副词条
                sub_entry_ocr_instance = ocr_thread(m_ocr, ocr, 'sub_entry_data_{}'.format(entry_num), invert=True)
                sub_entry_ocr_instance.start()
                sub_entry_ocr_instance.join()
                sub_entry_ocr_result = sub_entry_ocr_instance.get_result()
                sub_entry_data = list(map(lambda x: x[1][0], sub_entry_ocr_result[0]))

                # ocr 遗器套装名
                suit_name_ocr_instance = ocr_thread(
                    m_ocr, ocr, 'suit_name_{}'.format(entry_num), invert=True, det=False)
                suit_name_ocr_instance.start()
                suit_name_ocr_instance.join()
                suit_name_ocr_result = suit_name_ocr_instance.get_result()
                suit_name = suit_name_ocr_result[0][0][0]
                # print(sub_entry_data)

            # 处理百分数
            # 主词条
            if main_entry_value[-1] == '%':
                if main_entry_name in {'生命值', '攻击力', '防御力'}:
                    main_entry_name += '百分比'
                main_entry_value = eval(main_entry_value[:-1]) / 100
            else:
                main_entry_value = eval(main_entry_value)
            if main_entry_name not in MAIN_ENTRY:
                raise ValueError('main entry "{}" not found!'.format(main_entry_name))
            main_entry = [main_entry_name, main_entry_value]

            # 副词条
            sub_entry = dict()
            for num in range(entry_num):
                entry_name, entry_value = sub_entry_data[2 * num:2 * num + 2]
                if entry_value[-1] == '%':
                    if entry_name in {'生命值', '攻击力', '防御力'}:
                        entry_name += '百分比'
                    entry_value = eval(entry_value[:-1]) / 100
                else:
                    entry_value = eval(entry_value)
                if entry_name not in SUB_ENTRY:
                    raise ValueError('sub entry "{}" not found!'.format(entry_name))
                sub_entry.update({entry_name: entry_value})

            # print(main_entry)
            # print(sub_entry)
            # print(position, level, suit_name)
            relic = Relic.from_data(suit_name, position, level, main_entry, sub_entry)
            correct_suit_name(relic)

            # 记录列首以判断是否拉到底部
            if col == 0 and not page_end:
                if not col_first_relic:
                    col_first_relic = relic
                else:
                    # 此时已经拉到页面底部
                    if col_first_relic == relic:
                        page_end = True
                        break
                    else:
                        col_first_relic = relic

            relics[relic.position].append(relic)
            print(relic)

            # sleep(0.1)

        # 若检测到四星（紫色）遗器，则中止
        if detect_end:
            break

        # 若没到页面底部，则通过鼠标滚轮继续下一行
        if not page_end:
            for _ in range(scroll_control_lib[scroll_control_pos]):
                pyautogui.scroll(-1)
            scroll_control_pos = (scroll_control_pos + 1) % len(scroll_control_lib)
        row += 1

    end_time = time.time()
    logging.info('time of detection: {}'.format(end_time - start_time))
    return relics
