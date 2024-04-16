import importlib
import logging
import os
import time
from copy import deepcopy
import pickle
from functools import reduce
from itertools import chain
from threading import Thread

from PIL import ImageGrab, ImageChops
import keyboard
import numpy as np

# while True:
#     x, y = pyautogui.position()
#     print(x, y)
#     time = __import__('time')
#     time.sleep(0.1)

NAVIGATION = {
    'color': (1871, 221, 1872, 222),

    'position': (1890, 373, 1983, 408),
    'level': (1920, 413, 2000, 457),
    'main_entry_name': (1923, 530, 2220, 575),
    'main_entry_value': (2326, 530, 2456, 575),

    'sub_entry_data_3': (1923, 593, 2456, 734),
    'suit_name_3': (1869, 762, 2456, 806),
    'flag_3': (1869, 812, 1970, 849),

    'sub_entry_data_4': (1923, 593, 2456, 785),
    'suit_name_4': (1869, 813, 2456, 857),
    'flag_4': (1869, 866, 1970, 900)
}

COLOR = {
    'orange': (183, 141, 97),
    'purple': (139, 101, 197)
}

# 主词条
MAIN_ENTRY = {'攻击力', '攻击力百分比', '防御力百分比', '生命值', '生命值百分比',
              '暴击率', '暴击伤害', '击破特攻', '效果命中', '能量恢复效率', '治疗量加成', '速度',
              '火属性伤害提高', '物理属性伤害提高', '雷属性伤害提高', '风属性伤害提高', '冰属性伤害提高', '虚数属性伤害提高', '量子属性伤害提高'}
# 副词套
SUB_ENTRY = {'攻击力', '攻击力百分比', '防御力', '防御力百分比', '生命值', '生命值百分比',
             '暴击率', '暴击伤害', '击破特攻', '效果命中', '效果抵抗', '速度'}
# 总词条
ENTRY = MAIN_ENTRY | SUB_ENTRY | {'速度百分比'}
# 百分数词条
PER_ENTRY = {'攻击力百分比', '防御力百分比', '生命值百分比', '速度百分比', '暴击率', '暴击伤害', '击破特攻', '效果命中', '效果抵抗'}
# 数值词条
NON_PER_ENTRY = ENTRY - PER_ENTRY
# 面板词条（即舍去xx伤害提高）
PANEL_ENTRY = {key for key in ENTRY if ('属性伤害提高' not in key)}
# 乘区词条（爆伤乘区记在面板词条中，因此九大乘区，八个乘区词条）
MULTIPLIER_ENTRY = {'倍率', '增伤', '虚弱', '防御', '抗性', '易伤', '减伤', '击破状态'}

# 套装
INNER_SUIT = {'毁烬焚骨的大公', '幽锁深牢的系囚', '宝命长存的莳者', '骇域漫游的信使', '密林卧雪的猎人', '晨昏交界的翔鹰',
              '流星追迹的怪盗', '街头出身的拳王', '云无留迹的过客', '野穗伴行的快枪手', '戍卫风雪的铁卫', '繁星璀璨的天才',
              '净庭教宗的圣骑士', '激奏雷电的乐队', '熔岩锻铸的火匠', '盗匪荒漠的废土客', '机心戏梦的钟表匠', '死水深潜的先驱'}
OUTER_SUIT = {'梦想之地匹诺康尼', '苍穹战线格拉默', '折断的龙骨', '繁星竞技场', '太空封印站', '不老者的仙舟', '生命的翁瓦克',
              '星体差分机', '盗贼公国塔利亚', '泛银河商业公司', '筑城者的贝洛伯格', '停转的萨尔索图', '无主荒星茨冈尼亚',
              '出云显世与高天神国'}
SUIT = INNER_SUIT | OUTER_SUIT

POSITION_INDEX = {'头部': 0, '手部': 1, '躯干': 2, '脚部': 3, '位面球': 4, '连结绳': 5}
POSITION_LIB = ['头部', '手部', '躯干', '脚部', '位面球', '连结绳']

MULTIPLIER_LIB = ['基础', '暴伤', '增伤', '虚弱', '防御', '抗性', '易伤', '减伤', '击破状态']

output_file_name = 'relics.pkl.qjc'

# 等级
ATTACKER_LEVEL = 80
ENEMY_LEVEL = 95


class Relic:
    def __init__(self):
        self.suit = 'Empty'
        self.position = -1
        self.level = -1
        self.main_entry = ['Empty', 0]
        self.sub_entry = {key: 0 for key in ENTRY}

    @classmethod
    def from_data(cls, suit: str, position: int, level: int, main_entry: list, sub_entry: dict):
        new_relic = Relic()
        new_relic.suit = suit
        new_relic.position = position
        new_relic.level = level
        new_relic.main_entry = deepcopy(main_entry)
        new_relic.sub_entry = deepcopy(sub_entry)

        return new_relic

    def __str__(self):
        s = ''
        s += '套装: ' + self.suit + ', '
        s += '部位: ' + POSITION_LIB[self.position] + ', '
        s += '等级: ' + str(self.level) + ', '
        s += '主词条: {}'.format('{}+{:.3f}'.format(*self.main_entry)
                              if self.main_entry[0] in NON_PER_ENTRY else
                              '{}+{:.1f}%'.format(self.main_entry[0], self.main_entry[1] * 100)) + ', '
        s += '副词条: {}'.format('、'.join(
            ['{}+{:.3f}'.format(key, value) if key in NON_PER_ENTRY else '{}+{:.1f}%'.format(key, value * 100)
             for key, value in self.sub_entry.items() if value]
        ))
        return s
        pass

    def __eq__(self, other):
        if self.position != other.position:
            return False
        if self.suit != other.suit:
            return False
        if self.level != other.level:
            return False
        if self.main_entry != other.main_entry:
            return False
        if self.sub_entry != other.sub_entry:
            return False
        return True
    #
    # def __add__(self, other):
    #     rst = Relic()
    #     for value in rst.entry:
    #         rst.entry[value] = self.entry[value] + other.entry[value]
    #     return rst
    #
    # @classmethod
    # def sum(cls, arrange):
    #     rst = Relic()
    #     for entry_name in rst.entry.keys():
    #         rst.entry[entry_name] = sum(map(lambda relic: relic.entry[entry_name], arrange))
    #     return rst


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
    # def __init__(self, ocr, bbox_key, invert, det=True):
    #     super().__init__()
    #     self.result = None
    #     self.ocr = ocr
    #     self.bbox_key = bbox_key
    #     self.invert = invert
    #     self.det = det

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


# 从屏幕或者文件中获取玩家的库存遗器
def get_relics():
    if output_file_name in os.listdir():
        with open(output_file_name, 'rb') as fp:
            relics = pickle.load(fp)
    else:
        relics = scan_relics()
        with open(output_file_name, 'wb') as fp:
            pickle.dump(relics, fp)
    return relics


def cal_score(arrange, char_info, buffs):
    # 创建人物面板
    # 键包含大小生命值攻击力防御力速度等，即圣遗物的所有词条除去增伤词条
    # 或者在游戏中打开人物面板的属性详情，包括基础属性和进阶属性，但不包括伤害属性
    relics_properties = {key: 0 for key in PANEL_ENTRY}

    # 记录不同攻击模组下的伤害
    expect_damage_with_type = dict()

    # 遍历圣遗物词条，计算人物面板
    for relic in arrange:
        # 主词条（若主词条为增伤词条，则加入buffs中），反之则加入人物面板
        # 主词条为增伤词条
        if '属性伤害提高' in relic.main_entry[0]:
            main_entry_buff = {
                'description': '遗器主词条，套装：{}'.format(relic.suit),
                'label': ['通用'],
                'data': {
                    '增伤': relic.main_entry[1]
                }
            }
            buffs = buffs + [main_entry_buff]
        # 主词条为人物面板词条
        elif relic.main_entry[0] in relics_properties.keys():
            relics_properties[relic.main_entry[0]] += relic.main_entry[1]
        # 发生异常
        else:
            raise ValueError('未知圣遗物主属性，圣遗物详情：\n\t{}'.format(relic))

        # 所有副词条加入人物面板
        for property_name, property_value in relic.sub_entry.items():
            # 副词条加入人物面板
            if property_name in relics_properties.keys():
                relics_properties[property_name] += property_value
            # 发生异常
            else:
                raise ValueError('未知圣遗物副词条，圣遗物详情：\n\t{}'.format(relic))

    # 遍历攻击模组
    for model in char_info['model']:
        # 该模组下的面板
        model_char_properties = deepcopy(relics_properties)

        # 1. 基础伤害区
        # 技能倍率
        ability_multiplier = model['ability_multiplier']
        # 技能属性
        stat_name = model['stat']
        stat = 0
        # 附加伤害
        extra_dmg = 0

        # 2. 暴击区
        base_crit_rate = 0.05
        base_crit_dmg = 0.5

        # 3. 增伤区
        dmg_boost_multiplier = 1

        # 4. 虚弱区
        weaken_multiplier = 1

        # 5. 防御区
        # 防御系数
        enemy_defense = 1

        # 6. 抗性区
        res_multiplier = 1

        # 7. 易伤区
        vulnerability_multiplier = 1

        # 8. 减伤区
        dmg_mitigation_multiplier = 1

        # 9. 击破状态区
        broken_multiplier = 0.9

        # 计算buff
        for buff in buffs:
            # 判断当前攻击模组是否满足buff类型
            label_check = False
            if '通用' in buff['label']:
                label_check = True
            elif set(buff['label']) & set(model['label']):
                label_check = True

            if not label_check:
                continue

            for entry, value in buff['data'].items():
                # 面板属性词条
                if entry in PANEL_ENTRY:
                    model_char_properties[entry] += value
                # 乘区词条
                elif entry in MULTIPLIER_ENTRY:
                    if entry == '倍率':
                        ability_multiplier *= value
                    elif entry == '附加伤害':
                        extra_dmg += value
                    elif entry == '增伤':
                        dmg_boost_multiplier += value
                    elif entry == '虚弱':
                        weaken_multiplier += value
                    elif entry == '防御':
                        enemy_defense += value
                    elif entry == '抗性':
                        res_multiplier -= value
                    elif entry == '易伤':
                        vulnerability_multiplier += value
                    elif entry == '减伤':
                        dmg_mitigation_multiplier *= value
                    elif entry == '击破状态':
                        broken_multiplier = value
                    else:
                        raise ValueError('未知buff，buff详情：\n\t{}'.format(buff))
                # 发生异常
                else:
                    raise ValueError('未知BUFF，BUFF详情：\n\t{}'.format(buff))

        # 计算期望暴击乘区
        crit_rate = min(1.0, base_crit_rate + model_char_properties['暴击率'])
        crit_dmg = base_crit_dmg + model_char_properties['暴击伤害']
        crit_multiplier = 1 + crit_rate * crit_dmg

        # 计算防御乘区
        def_multiplier = (ATTACKER_LEVEL + 20) / (ATTACKER_LEVEL + 20 + (ENEMY_LEVEL + 20) * max(0, enemy_defense))

        # 计算状态值（生命值/攻击力/防御力），并依次计算基础乘区
        stat += char_info['base_data'][stat_name] * (1 + model_char_properties['{}百分比'.format(stat_name)])\
            + model_char_properties['{}'.format(stat_name)]
        base_dmg = ability_multiplier * stat + extra_dmg

        # 计算各属性
        attack = char_info['base_data']['攻击力'] * (1 + model_char_properties['攻击力百分比']) + model_char_properties['攻击力']
        defense = char_info['base_data']['防御力'] * (1 + model_char_properties['防御力百分比']) + model_char_properties['防御力']
        hp = char_info['base_data']['生命值'] * (1 + model_char_properties['生命值百分比']) + model_char_properties['生命值']
        speed = char_info['base_data']['速度'] * (1 + model_char_properties['速度百分比']) + model_char_properties['速度']

        # 给面板添加进最终值
        model_char_panel_properties = {
            '攻击力': attack,
            '防御力': defense,
            '生命值': hp,
            '暴击率': crit_rate,
            '暴击伤害': crit_dmg,
            '速度': speed,
        }

        # 计算伤害
        multipliers = [base_dmg,
                       crit_multiplier,
                       dmg_boost_multiplier,
                       weaken_multiplier,
                       def_multiplier,
                       res_multiplier,
                       vulnerability_multiplier,
                       dmg_mitigation_multiplier,
                       broken_multiplier]
        dmg = reduce((lambda x, y: x * y), multipliers)
        expect_damage_with_type[model['description']] = {
            '伤害': dmg,
            '各乘区': multipliers,
            '面板增益': model_char_properties,
            '面板': model_char_panel_properties,
        }

    total_dmg = sum(map(lambda x: x['伤害'], expect_damage_with_type.values()))

    return total_dmg, expect_damage_with_type, relics_properties


def check_suit_available(step, relic, suit_need):
    """
    判断如果选了relic，并且在step进度下，能否满足成套装suit_need
    :param step:
    :param relic:
    :param suit_need:
    :return:
    """
    for p in ['outer', 'inner']:
        # 剩余需求数
        need_num = sum(map(lambda x: max(0, x['num']), suit_need[p]))
        if relic.suit in map(lambda x: x['name'], suit_need[p]):
            need_num -= 1
        # 还未选的数量（外圈内圈算法不一致）
        remain_num = max(0, 4 - step) if p == 'outer' else min(2, 5 - step)
        # 剩余需求数多于还未选的数量，即无论如何无法满足套装需求
        if need_num > remain_num:
            return False

    return True


def dfs(step: int, arrange: list, best_arrange_dict: dict, suit_need: dict,
        player_relics: dict, char_info: dict, buffs: list):
    """

    :param step: 当前的遍历层数
    :param arrange: 当前遍历的遗器搭配
    :param best_arrange_dict: 搜索过程中的最优结果
    :param suit_need: 外圈和内圈每种套装还需要的遗器数量
    :param player_relics: 玩家的所有库存遗器
    :param char_info: 角色的基本信息
    :param buffs: buffs包含圣遗物套装和其余buff
    """
    if step == 6:
        dmg, expect_damage_with_type, relics_properties = cal_score(arrange, char_info, buffs)
        if dmg > best_arrange_dict['max_damage']:
            best_arrange_dict.update({
                'max_damage': dmg,
                'best_arrange': deepcopy(arrange),
                'expect_damage_with_type': expect_damage_with_type,
                'relics_properties': relics_properties
            })
        return

    for relic in player_relics[step]:
        # 只选满级遗器
        if relic.level != 15:
            continue

        # 剩余需求数多于还未选的数量，即无论如何无法满足套装需求
        if not check_suit_available(step, relic, suit_need):
            continue

        # 更新套装剩余需求
        for p in ['outer', 'inner']:
            for relic_suit in suit_need[p]:
                if relic.suit == relic_suit['name']:
                    relic_suit['num'] -= 1

        arrange.append(relic)
        dfs(step + 1, arrange, best_arrange_dict, suit_need, player_relics, char_info, buffs)
        arrange.pop()

        # 更新套装剩余需求
        for p in ['outer', 'inner']:
            for relic_suit in suit_need[p]:
                if relic.suit == relic_suit['name']:
                    relic_suit['num'] += 1


def research_suit(player_relics, char_info, extra_buffs, relics_info):
    max_arrange_dict = {
        'max_damage': 0,
        'best_arrange': [],
        'expect_damage_with_type': dict(),
        'best_relics_properties': dict(),
        'best_buff': list()
    }

    # 遍历外圈与内圈
    outer_relics_lib = relics_info['outer_relics']
    inner_relics_lib = relics_info['inner_relics']
    for outer_relics_combination in outer_relics_lib:
        for inner_relics_combination in inner_relics_lib:
            # 统计套装遗器数量
            suit_cnt = {}
            for relic in outer_relics_combination + inner_relics_combination:
                suit_cnt[relic['name']] = relic['num']

            # 输出当前计算的套装
            dealt_suit_cnt = map(lambda suit: '{}{}'.format(*suit) if suit[1] > 1 else None, suit_cnt.items())
            dealt_suit_cnt = list(filter(None, dealt_suit_cnt))
            suit_str = ' + '.join(dealt_suit_cnt) if dealt_suit_cnt else '无套装'
            print('正在计算: {}'.format(suit_str))

            # 提取遗器套装带来的buff
            outer_relics_buffs = chain.from_iterable(map(lambda x: x['buff'], outer_relics_combination))
            inner_relics_buffs = chain.from_iterable(map(lambda x: x['buff'], inner_relics_combination))
            relics_buffs = list(outer_relics_buffs) + list(inner_relics_buffs)

            def del_buff(x: dict):
                del x['buff']
                return x

            # 深度优先搜索
            arrange_dict = {
                'max_damage': 0,
                'best_arrange': [],
                'expect_damage_with_type': dict(),
                'best_relics_properties': dict(),
            }

            # 获取内外圈遗器的套装需求数量
            suit_need = {
                'outer': list(map(del_buff, deepcopy(outer_relics_combination))),
                'inner': list(map(del_buff, deepcopy(inner_relics_combination)))
            }
            buffs = relics_buffs + extra_buffs
            dfs(0, [], arrange_dict, suit_need, player_relics, char_info, buffs)
            print('期望伤害：{}\n'.format(arrange_dict['max_damage']))

            # 与最优遗器组合作对比
            if arrange_dict['max_damage'] > max_arrange_dict['max_damage']:
                max_arrange_dict.update(arrange_dict)
                max_arrange_dict['best_buff'] = buffs

    return max_arrange_dict


# 输出
def output(max_arrange_dict):
    # 统计套装
    suit_cnt = {}
    for relic in max_arrange_dict['best_arrange']:
        suit_cnt[relic.suit] = suit_cnt.get(relic.suit, 0) + 1

    # 处理None值（即不足2件套的散件）
    dealt_suit_cnt = map(lambda suit: '{}{}'.format(*suit) if suit[1] > 1 else None, suit_cnt.items())
    dealt_suit_cnt = list(filter(None, dealt_suit_cnt))
    suit_str = ' + '.join(dealt_suit_cnt)
    print('最佳套装: {}'.format(suit_str))

    # 列出各部位遗器
    for relic in max_arrange_dict['best_arrange']:
        print(relic)

    # 总期望伤害
    print('期望伤害: {}'.format(max_arrange_dict['max_damage']))

    # 分列各攻击模组
    for damage_type, damage_value in max_arrange_dict['expect_damage_with_type'].items():
        print('\t{}伤害: {}'.format(damage_type, damage_value['伤害']))

        print('\t{}乘区: '.format(damage_type))
        for i, multiplier_value in enumerate(damage_value['各乘区']):
            print('\t\t{}乘区: {:.3f}'.format(MULTIPLIER_LIB[i], multiplier_value))

        print('\t{}面板增益: '.format(damage_type))
        for i, (entry_name, entry_value) in enumerate(damage_value['面板增益'].items()):
            print('\t\t{}: {:.3f}'.format(entry_name, entry_value))

        print('\t{}面板: '.format(damage_type))
        for i, (entry_name, entry_value) in enumerate(damage_value['面板'].items()):
            print('\t\t{}: {:.3f}'.format(entry_name, entry_value))

        print()

    # 遗器词条提供的增益
    print('遗器主副词条增益: ')
    for i, (entry_name, entry_value) in enumerate(max_arrange_dict['relics_properties'].items()):
        print('\t{}: {:.3f}'.format(entry_name, entry_value))

    # 所处的所有buff
    print('所吃buff: ')
    for i, buff in enumerate(max_arrange_dict['best_buff']):
        print('\t{}：{}'.format(
            buff['description'], ', '.join(map(lambda x: '{}{:.3f}'.format(*x), buff['data'].items()))
        ))


def main(char_name):
    print('计算{}：'.format(char_name))

    # 获取玩家库存遗器
    player_relics = get_relics()

    # 获取角色的信息 和 圣遗物方案
    char_file = importlib.import_module('character_info.{}'.format(char_name))
    char_info = char_file.__getattribute__('data')
    extra_buffs = char_file.__getattribute__('buffs')
    relics_info = char_file.__getattribute__('relics')

    # 遍历所有套装得到的最高伤害
    max_arrange_dict = research_suit(player_relics, char_info, extra_buffs, relics_info)

    # 输出结果
    output(max_arrange_dict)


def test():
    relics = get_relics()

    # Relics = []
    # for r in relics:
    #     for i in r:
    #         print(i)
    print('\n总计: {}件'.format(sum(map(lambda x: len(x), relics))))


def statistic():
    relics = get_relics()
    relics = chain.from_iterable(relics)
    relics = sorted(relics, key=lambda x: x.sub_entry.get('暴击率', 0) * 2 + x.sub_entry.get('暴击伤害', 0), reverse=True)
    for relic in relics:
        score = (relic.sub_entry.get('暴击率', 0) * 2 + relic.sub_entry.get('暴击伤害', 0)) * 100
        print('{:.1f}'.format(score), end='\t')
        print(relic)


if __name__ == '__main__':
    # test()
    main('黄泉')
    # statistic()
