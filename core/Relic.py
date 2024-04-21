import math
from copy import deepcopy

from core.Constants import *


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

    def get_crit_score(self):
        return (self.sub_entry.get('暴击率', 0) * 2 + self.sub_entry.get('暴击伤害', 0)) * 100

    def get_crit_score_expectation(self):
        # 单爆/双爆/无双爆词条
        entry_cnt = 1 if len(self.sub_entry) == 3 else 0
        entry_cnt += 1 if '暴击率' in self.sub_entry.keys() else 0
        entry_cnt += 1 if '暴击伤害' in self.sub_entry.keys() else 0

        # 剩余副词条强化数，15为遗器的最大等级，3为副词条强化步长
        remain_sub_num = math.ceil((15 - self.level) / 3)

        # 初始三词条的双爆圣遗物，第一次强化必定是新词条
        if entry_cnt == 3:
            remain_sub_num -= 1
            entry_cnt -= 1  # 空余的第四词条必定不是双爆词条

        # # 双爆词条的个数最多为2
        # entry_cnt = max(entry_cnt, 2)

        # 还能获得的双爆分期望（每个双爆词条期望5.832分）
        crit_score_expectation = remain_sub_num * (entry_cnt / 4) * 5.832

        # 强化到满级的期望双爆分
        return crit_score_expectation + self.get_crit_score()

    def format_str(self):
        s = ''
        s += '套装: ' + self.suit + '\n'
        s += '部位: ' + POSITION_LIB[self.position] + '\n'
        s += '等级: ' + str(self.level) + '\n'
        s += '主词条: \n{}'.format('\t{}+{:.3f}\n'.format(*self.main_entry)
                                if self.main_entry[0] in NON_PER_ENTRY else
                                '\t{}+{:.1f}%\n'.format(self.main_entry[0], self.main_entry[1] * 100))
        s += '副词条: \n{}'.format(''.join(
            ['\t{}+{:.3f}\n'.format(key, value) if key in NON_PER_ENTRY else '\t{}+{:.1f}%\n'.format(key, value * 100)
             for key, value in self.sub_entry.items() if value]
        )) + '\n'
        return s

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

    # 为了适配小根堆，可能获得更多的双爆词条数，会越排前，则比较结果越小
    def __lt__(self, other):
        return self.get_crit_score_expectation() > other.get_crit_score_expectation()

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
