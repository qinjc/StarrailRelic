data = {
    'base_data': {
        '生命值': 1125 + 1028,
        '攻击力': 698 + 635,
        '防御力': 436 + 396,
        '速度': 101,
    },
    'path': '虚无',
    'type': '雷',
    # 攻击模组
    'model': [
        {
            'description': '终结技（对单）',
            'label': ['终结技'],
            'stat': '攻击力',
            'ability_multiplier': 3.72
        },
        {
            'description': '终结技（对群）',
            'label': ['终结技'],
            'stat': '攻击力',
            'ability_multiplier': 3
        },
        {
            'description': '终结技（弹射）',
            'label': ['终结技'],
            'stat': '攻击力',
            'ability_multiplier': 0.25 * 6
        },
        {
            'description': '战技',
            'label': ['战技'],
            'stat': '攻击力',
            'ability_multiplier': 1.6
        },
    ]
}

buffs = [
    {
        'description': '行迹分支',
        'label': ['通用'],
        'data': {
            '攻击力百分比': 0.28,
            '暴击伤害': 0.24,
            '增伤': 0.08
        }
    },
    {
        'description': '额外能力1 雷心',
        'label': ['通用'],
        'data': {
            '增伤': 0.9
        }
    },
    {
        'description': '额外能力3 奈落',
        'label': ['通用'],
        'data': {
            '倍率': 1.6
        }
    },
    {
        'description': '天赋（终结技减抗）',
        'label': ['终结技'],
        'data': {
            '抗性': -0.2
        }
    },
    {
        'description': '星魂一',
        'label': ['通用'],
        'data': {
            '暴击率': 0.18
        }
    },
    {
        'description': '光锥：行于流逝的岸 叠二 通用',
        'label': ['通用'],
        'data': {
            '暴击伤害': 0.42,
            '增伤': 0.28
        }
    },
    {
        'description': '光锥：行于流逝的岸 叠二 终结技增伤',
        'label': ['终结技'],
        'data': {
            '增伤': 0.28
        }
    },
    # {
    #     'description': '花火光锥：但战斗还未结束 叠一',
    #     'label': ['通用'],
    #     'data': {
    #         '增伤': 0.3
    #     }
    # },
    {
        'description': '花火光锥：过往未来 叠五',
        'label': ['通用'],
        'data': {
            '增伤': 0.36
        }
    },
    {
        'description': '花火战技',
        'label': ['通用'],
        'data': {
            '暴击伤害': 0.24 * (1.66 + 0.1 + 0.1) + 0.45
        }
    },
    {
        'description': '花火天赋',
        'label': ['通用'],
        'data': {
            '增伤': 0.06 * 3
        }
    },
    {
        'description': '花火终结技',
        'label': ['通用'],
        'data': {
            '增伤': 0.1 * 3
        }
    },
    {
        'description': '花火额外能力1 夜想曲',
        'label': ['通用'],
        'data': {
            '攻击力百分比': 0.15
        }
    },
    {
        'description': '佩拉光锥 决心如汗珠般闪耀 叠五',
        'label': ['通用'],
        'data': {
            '防御': -0.16
        }
    },
    {
        'description': '佩拉秘技 先发制人',
        'label': ['通用'],
        'data': {
            '防御': -0.2
        }
    },
    {
        'description': '佩拉终结技 领域压制',
        'label': ['通用'],
        'data': {
            '防御': -0.42
        }
    },
    {
        'description': '佩拉遗器内圈二件套 折断的龙骨',
        'label': ['通用'],
        'data': {
            '暴击伤害': 0.1
        }
    },
    {
        'description': '符玄战技 太微行棋，灵台示影',
        'label': ['通用'],
        'data': {
            '暴击率': 0.12
        }
    },
    {
        'description': '符玄遗器内圈二件套 折断的龙骨',
        'label': ['通用'],
        'data': {
            '暴击伤害': 0.1
        }
    },
]

relics = {
    'outer_relics': [
        [
            {
                'name': '死水深潜的先驱',
                'num': 4,
                'buff': [
                    {
                        'description': '死水深潜的先驱 二件套',
                        'label': ['通用'],
                        'data': {
                            '增伤': 0.12
                        }
                    },
                    {
                        'description': '死水深潜的先驱 四件套',
                        'label': ['通用'],
                        'data': {
                            '暴击率': 0.08,
                            '暴击伤害': 0.24,
                        }
                    },
                ]
            }
        ]
    ],
    'inner_relics': [
        [
            {
                'name': '出云显世与高天神国',
                'num': 2,
                'buff': [
                    {
                        'description': '出云显世与高天神国 二件套',
                        'label': ['通用'],
                        'data': {
                            '暴击率': 0.12,
                            '攻击力百分比': 0.12,
                        }
                    }
                ]
            },
        ],
        [
            {
                'name': '停转的萨尔索图',
                'num': 2,
                'buff': [
                    {
                        'description': '停转的萨尔索图 二件套（通用）',
                        'label': ['通用'],
                        'data': {
                            '暴击率': 0.08,
                        }
                    },
                    {
                        'description': '停转的萨尔索图 二件套（条件触发）',
                        'label': ['追加攻击', '终结技'],
                        'data': {
                            '增伤': 0.15,
                        }
                    },
                ]
            }
        ]
    ]
}

# 基础伤害 暴击伤害 增伤 虚弱
# 防御 抗性 易伤 伤害减免 击破状态
# 伤害计算：
# https://honkai-star-rail.fandom.com/wiki/Damage
# https://honkai-star-rail.fandom.com/wiki/Toughness#Damage_Formula
