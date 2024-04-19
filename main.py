import importlib
from copy import deepcopy
from functools import reduce
from itertools import chain

from Constants import *
from RelicsGetter import get_relics

output_file_name = 'relics.pkl.qjc'


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
        attack = char_info['base_data']['攻击力'] * (1 + model_char_properties['攻击力百分比']) + model_char_properties[
            '攻击力']
        defense = char_info['base_data']['防御力'] * (1 + model_char_properties['防御力百分比']) + \
            model_char_properties['防御力']
        hp = char_info['base_data']['生命值'] * (1 + model_char_properties['生命值百分比']) + model_char_properties[
            '生命值']
        speed = char_info['base_data']['速度'] * (1 + model_char_properties['速度百分比']) + model_char_properties[
            '速度']

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


def calc_max_damage(player_relics, char_name):
    print('计算{}：'.format(char_name))

    # 获取角色的信息 和 圣遗物方案
    char_file = importlib.import_module('character_info.{}'.format(char_name))
    char_info = char_file.__getattribute__('data')
    extra_buffs = char_file.__getattribute__('buffs')
    relics_info = char_file.__getattribute__('relics')

    # 遍历所有套装得到的最高伤害
    max_arrange_dict = research_suit(player_relics, char_info, extra_buffs, relics_info)

    # 输出结果
    output(max_arrange_dict)


def statistic():
    relics = get_relics(output_file_name)
    relics = chain.from_iterable(relics)
    relics = sorted(relics, key=lambda x: x.get_crit_score(), reverse=True)
    for relic in relics:
        score = (relic.sub_entry.get('暴击率', 0) * 2 + relic.sub_entry.get('暴击伤害', 0)) * 100
        print('{:.1f}'.format(score), end='\t')
        print(relic)


def strengthen_relics():
    relics = get_relics(output_file_name)
    relics = chain.from_iterable(relics)

    # 有强化价值的套装
    relic_suit_filter = ['毁烬焚骨的大公', '幽锁深牢的系囚', '密林卧雪的猎人', '街头出身的拳王',
                         '野穗伴行的快枪手', '繁星璀璨的天才', '激奏雷电的乐队', '熔岩锻铸的火匠',
                         '盗匪荒漠的废土客', '机心戏梦的钟表匠',

                         '苍穹战线格拉默', '繁星竞技场', '太空封印站', '泛银河商业公司',
                         '停转的萨尔索图', '无主荒星茨冈尼亚', '出云显世与高天神国']

    # 有强化价值的主词条（对应六个部位）
    # base_entry = {'攻击力百分比', '防御力百分比', '生命值百分比'}
    base_entry = {'攻击力百分比'}
    relic_main_entry_filter = [
        {'生命值'},
        {'攻击力'},
        {'暴击率', '暴击伤害'},
        base_entry,
        {'火属性伤害提高', '物理属性伤害提高', '雷属性伤害提高', '风属性伤害提高', '冰属性伤害提高',
         '虚数属性伤害提高', '量子属性伤害提高'} | base_entry,
        {'击破特攻', '能量恢复效率'} | base_entry,
    ]

    # 过滤值得强化的套装和主词条
    def relic_filter_func(t_relic):
        if t_relic.level == 15:
            return False
        if t_relic.suit not in relic_suit_filter:
            return False
        if t_relic.main_entry[0] not in relic_main_entry_filter[t_relic.position]:
            return False
        return True

    relics = filter(relic_filter_func, relics)
    import heapq
    relics = list(relics)
    heapq.heapify(relics)
    relics_sorted = heapq.nsmallest(len(relics), relics)

    for relic in relics_sorted:
        print('期望双爆分: {:.2f}'.format(relic.get_crit_score_expectation()))
        print('当前双爆分: {:.2f}'.format(relic.get_crit_score()))
        print(relic.format_str())


def main():
    # relics = get_relics()
    # calc_max_damage(relics, '黄泉')
    # statistic()
    strengthen_relics()


if __name__ == '__main__':
    main()
