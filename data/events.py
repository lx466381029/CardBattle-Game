"""
罗盘事件系统 - 负面事件和幸运事件定义
Compass Event System - Negative and Lucky Event Definitions
"""

import random
from data.cards import NEGATIVE_CARDS, Card


class CompassEvent:
    """罗盘事件基础类"""
    
    def __init__(self, name, description, effect_func):
        """初始化事件"""
        self.name = name
        self.description = description
        self.effect = effect_func
        
    def trigger(self, battle_context):
        """触发事件效果"""
        battle_context.log(f"罗盘事件: {self.name}!")
        battle_context.log(f"效果: {self.description}")
        if self.effect:
            self.effect(battle_context)


# ============ 负面事件效果函数 ============

def add_curse_card_event(battle_context):
    """添加诅咒卡牌到牌库"""
    # 随机选择一张负面卡牌
    negative_card = random.choice(NEGATIVE_CARDS)
    # 创建卡牌副本
    curse_card = Card(
        negative_card.id, negative_card.name, negative_card.type, 
        negative_card.mp_cost, negative_card.compass_points, 
        negative_card.effect, negative_card.description
    )
    
    # 添加到牌库顶部
    battle_context.card_system.add_negative_card(curse_card)
    battle_context.log(f"一张 {curse_card.name} 被添加到你的牌库中")


def lose_hp_event(battle_context):
    """立即失去HP"""
    damage = 3
    actual_damage = battle_context.player.take_damage(damage)
    battle_context.log(f"你失去了 {actual_damage} 点HP")


def skip_turn_event(battle_context):
    """跳过下一个出牌阶段"""
    battle_context.skip_next_turn = True
    battle_context.log("你将跳过下一个出牌阶段")


def lose_mp_event(battle_context):
    """失去MP"""
    mp_loss = 2
    actual_loss = min(battle_context.player.mp, mp_loss)
    battle_context.player.mp -= actual_loss
    battle_context.log(f"你失去了 {actual_loss} 点MP")


def weaken_attack_event(battle_context):
    """降低攻击力"""
    atk_reduction = 2
    battle_context.player.atk = max(0, battle_context.player.atk - atk_reduction)
    battle_context.log(f"你的攻击力降低了 {atk_reduction} 点")


def discard_card_event(battle_context):
    """随机弃置一张手牌"""
    if len(battle_context.card_system.hand) > 0:
        discarded_card = random.choice(battle_context.card_system.hand)
        battle_context.card_system.hand.remove(discarded_card)
        battle_context.card_system.played_cards.append(discarded_card)
        battle_context.log(f"你弃置了 {discarded_card.name}")
    else:
        battle_context.log("手牌为空，无法弃置")


# ============ 幸运事件效果函数 ============

def heal_bonus_event(battle_context):
    """立即恢复HP"""
    heal_amount = 15
    actual_heal = battle_context.player.heal(heal_amount)
    battle_context.log(f"你恢复了 {actual_heal} 点HP")


def mp_bonus_event(battle_context):
    """获得额外MP"""
    mp_bonus = 3
    actual_restore = battle_context.player.restore_mp(mp_bonus)
    battle_context.log(f"你获得了 {actual_restore} 点MP")


def double_attack_event(battle_context):
    """下次攻击伤害翻倍"""
    # 这个效果需要在战斗管理器中实现状态跟踪
    battle_context.double_next_attack = True
    battle_context.log("你的下次攻击伤害将翻倍！")


def armor_bonus_event(battle_context):
    """立即获得护甲"""
    armor_amount = 10
    battle_context.player.add_armor(armor_amount)
    battle_context.log(f"你获得了 {armor_amount} 点护甲")


def draw_bonus_event(battle_context):
    """抽取额外卡牌"""
    draw_count = 2
    battle_context.card_system.draw_cards(draw_count)
    battle_context.log(f"你抽取了 {draw_count} 张卡牌")


def strengthen_event(battle_context):
    """永久增加攻击力"""
    atk_bonus = 1
    battle_context.player.atk += atk_bonus
    battle_context.log(f"你的攻击力永久增加了 {atk_bonus} 点")


# ============ 事件库定义 ============

NEGATIVE_EVENTS = [
    CompassEvent("诅咒侵蚀", "一张诅咒卡牌被添加到你的牌库", add_curse_card_event),
    CompassEvent("黑暗能量", "你立即失去3点HP", lose_hp_event),
    CompassEvent("精神涣散", "跳过下一个出牌阶段", skip_turn_event),
    CompassEvent("魔力燃烧", "你失去2点MP", lose_mp_event),
    CompassEvent("力量衰退", "你的攻击力降低2点", weaken_attack_event),
    CompassEvent("心神不宁", "随机弃置一张手牌", discard_card_event),
]

LUCKY_EVENTS = [
    CompassEvent("神圣祝福", "立即恢复15点HP", heal_bonus_event),
    CompassEvent("魔力涌动", "获得3点额外MP", mp_bonus_event),
    CompassEvent("战斗狂热", "下次攻击伤害翻倍", double_attack_event),
    CompassEvent("完美防御", "立即获得10点护甲", armor_bonus_event),
    CompassEvent("灵感迸发", "抽取2张额外卡牌", draw_bonus_event),
    CompassEvent("力量觉醒", "攻击力永久增加1点", strengthen_event),
]


def get_random_negative_event():
    """获取随机负面事件"""
    return random.choice(NEGATIVE_EVENTS)


def get_random_lucky_event():
    """获取随机幸运事件"""
    return random.choice(LUCKY_EVENTS)


def trigger_compass_event(event_type, battle_context):
    """根据事件类型触发相应事件"""
    from core.compass_system import CompassPosition
    
    if event_type == CompassPosition.NORMAL:
        battle_context.log("罗盘静静地转动...")
        
    elif event_type == CompassPosition.NEGATIVE:
        event = get_random_negative_event()
        event.trigger(battle_context)
        
    elif event_type == CompassPosition.LUCKY:
        event = get_random_lucky_event()
        event.trigger(battle_context)
        
    else:
        battle_context.log("罗盘发出了奇怪的声音...")


def get_event_statistics():
    """获取事件统计信息"""
    return {
        'negative_events_count': len(NEGATIVE_EVENTS),
        'lucky_events_count': len(LUCKY_EVENTS),
        'total_events': len(NEGATIVE_EVENTS) + len(LUCKY_EVENTS)
    } 