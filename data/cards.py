"""
卡牌系统数据定义 - 卡牌类和基础卡牌库
Card System Data - Card Classes and Basic Card Library
"""

class Card:
    """卡牌基础数据结构"""
    
    def __init__(self, card_id, name, card_type, mp_cost, compass_points, effect_func, description, is_direct_damage=False):
        """初始化卡牌"""
        self.id = card_id
        self.name = name                    # 卡牌名称
        self.type = card_type              # 卡牌类型：'attack', 'defense', 'heal', 'buff', 'negative'
        self.mp_cost = mp_cost             # 魔法值消耗
        self.compass_points = compass_points # 罗盘推进点数
        self.effect = effect_func          # 卡牌效果函数
        self.description = description      # 卡牌描述
        self.is_direct_damage = is_direct_damage  # 是否为直接伤害卡牌
        
    def can_play(self, player):
        """检查是否可以使用（MP是否足够）"""
        return player.mp >= self.mp_cost
    
    def execute_effect(self, battle_context):
        """执行卡牌效果"""
        if self.effect:
            self.effect(battle_context)
            
    def get_display_info(self):
        """获取显示信息"""
        return {
            'name': self.name,
            'type': self.type,
            'mp_cost': self.mp_cost,
            'compass_points': self.compass_points,
            'description': self.description,
            'is_direct_damage': self.is_direct_damage
        }


# ============ 直接伤害卡牌效果函数 ============

def fireball_effect(battle_context):
    """火球效果：直接造成15点伤害"""
    base_damage = 15
    final_damage = battle_context.enemy.take_damage(base_damage)
    battle_context.log(f"Fireball直接造成 {final_damage} 点伤害给 {battle_context.enemy.name}")


# ============ 攻击力累加卡牌效果函数 ============

def strike_effect(battle_context):
    """攻击效果：增加6点攻击力"""
    atk_bonus = 6
    battle_context.player.atk += atk_bonus
    battle_context.log(f"Strike增加 {atk_bonus} 点攻击力（当前攻击力: {battle_context.player.atk}）")


def heavy_blow_effect(battle_context):
    """重击效果：增加12点攻击力"""
    atk_bonus = 12
    battle_context.player.atk += atk_bonus
    battle_context.log(f"Heavy Blow增加 {atk_bonus} 点攻击力（当前攻击力: {battle_context.player.atk}）")


# ============ 防御类卡牌效果函数 ============

def block_effect(battle_context):
    """防御效果：获得8点护甲"""
    armor_amount = 8
    battle_context.player.add_armor(armor_amount)
    battle_context.log(f"Block获得 {armor_amount} 点护甲")


def iron_will_effect(battle_context):
    """钢铁意志效果：获得15点护甲"""
    armor_amount = 15
    battle_context.player.add_armor(armor_amount)
    battle_context.log(f"Iron Will获得 {armor_amount} 点护甲")


# ============ 治疗类卡牌效果函数 ============

def heal_effect(battle_context):
    """治疗效果：恢复12点HP"""
    heal_amount = 12
    actual_heal = battle_context.player.heal(heal_amount)
    battle_context.log(f"Heal恢复 {actual_heal} 点HP")


def greater_heal_effect(battle_context):
    """强效治疗效果：恢复20点HP"""
    heal_amount = 20
    actual_heal = battle_context.player.heal(heal_amount)
    battle_context.log(f"Greater Heal恢复 {actual_heal} 点HP")


# ============ 负面卡牌效果（由罗盘事件插入）============

def curse_effect(battle_context):
    """诅咒效果：跳过下一个出牌阶段"""
    battle_context.skip_next_turn = True
    battle_context.log("Curse：下一回合跳过出牌阶段！")


def drain_effect(battle_context):
    """吸取效果：失去5点HP"""
    damage = 5
    actual_damage = battle_context.player.take_damage(damage)
    battle_context.log(f"Drain：失去 {actual_damage} 点HP")


def weakness_effect(battle_context):
    """虚弱效果：本回合攻击力减半"""
    if battle_context.player.atk > 1:
        reduced_atk = max(1, battle_context.player.atk // 2)
        battle_context.player.atk = reduced_atk
        battle_context.log(f"Weakness：攻击力减半至 {reduced_atk}")
    else:
        battle_context.log("Weakness：攻击力已是最低值")


# ============ 基础卡牌库定义 ============

BASIC_CARDS = [
    # 攻击累加类卡牌
    Card("strike", "Strike", "attack", 0, 1, strike_effect, "增加6点攻击力", False),
    Card("heavy_blow", "Heavy Blow", "attack", 2, 2, heavy_blow_effect, "增加12点攻击力", False),
    
    # 直接伤害类卡牌
    Card("fireball", "Fireball", "attack", 3, 3, fireball_effect, "直接造成15点伤害", True),
    
    # 防御类卡牌
    Card("block", "Block", "defense", 1, 1, block_effect, "获得8点护甲"),
    Card("iron_will", "Iron Will", "defense", 2, 1, iron_will_effect, "获得15点护甲"),
    
    # 治疗类卡牌
    Card("heal", "Heal", "heal", 2, 1, heal_effect, "恢复12点HP"),
    Card("greater_heal", "Greater Heal", "heal", 4, 2, greater_heal_effect, "恢复20点HP"),
]

# 负面卡牌库（由罗盘事件插入）
NEGATIVE_CARDS = [
    Card("curse", "Curse", "negative", 0, 0, curse_effect, "跳过下一回合"),
    Card("drain", "Drain", "negative", 0, 0, drain_effect, "失去5点HP"),
    Card("weakness", "Weakness", "negative", 0, 0, weakness_effect, "攻击力减半"),
]


def create_starting_deck():
    """创建起始牌库"""
    # 每种基础卡牌3份
    starting_deck = []
    for card in BASIC_CARDS:
        for _ in range(3):
            # 创建卡牌副本，避免引用同一对象
            new_card = Card(
                card.id, card.name, card.type, card.mp_cost, 
                card.compass_points, card.effect, card.description, card.is_direct_damage
            )
            starting_deck.append(new_card)
    
    return starting_deck


def get_card_by_id(card_id):
    """根据ID获取卡牌模板"""
    all_cards = BASIC_CARDS + NEGATIVE_CARDS
    for card in all_cards:
        if card.id == card_id:
            return card
    return None 