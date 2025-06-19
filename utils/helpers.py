"""
工具函数模块 - 游戏辅助函数和验证工具
Helper Functions Module - Game Utility Functions and Validation Tools
"""

import random


def clamp(value, min_value, max_value):
    """将数值限制在指定范围内"""
    return max(min_value, min(value, max_value))


def calculate_damage(base_damage, attacker_atk, defender_armor=0):
    """计算伤害值，考虑攻击力和护甲"""
    total_damage = base_damage + attacker_atk
    final_damage = max(0, total_damage - defender_armor)
    return final_damage


def format_hp_display(current_hp, max_hp):
    """格式化HP显示"""
    return f"{current_hp}/{max_hp}"


def format_mp_display(current_mp, max_mp):
    """格式化MP显示"""
    return f"{current_mp}/{max_mp}"


def get_health_color(current_hp, max_hp):
    """根据血量百分比获取显示颜色"""
    ratio = current_hp / max_hp if max_hp > 0 else 0
    
    if ratio > 0.7:
        return (100, 255, 100)  # 绿色 - 健康
    elif ratio > 0.3:
        return (255, 255, 100)  # 黄色 - 警告
    else:
        return (255, 100, 100)  # 红色 - 危险


def get_mp_color(current_mp, max_mp):
    """根据MP百分比获取显示颜色"""
    ratio = current_mp / max_mp if max_mp > 0 else 0
    
    if ratio > 0.5:
        return (100, 200, 255)  # 蓝色 - 充足
    elif ratio > 0.2:
        return (150, 150, 255)  # 浅蓝色 - 普通
    else:
        return (100, 100, 200)  # 深蓝色 - 不足


def validate_card_playable(card, player):
    """验证卡牌是否可以使用"""
    if not card:
        return False, "卡牌不存在"
    
    if not player:
        return False, "玩家不存在"
    
    if not player.is_alive():
        return False, "玩家已死亡"
    
    if player.mp < card.mp_cost:
        return False, f"MP不足，需要 {card.mp_cost} MP，当前只有 {player.mp} MP"
    
    return True, "可以使用"


def calculate_card_efficiency(card, player_atk):
    """计算卡牌效率值（用于AI或推荐系统）"""
    if not card:
        return 0
    
    # 简单的效率评估
    if card.type == "attack":
        # 攻击卡牌：伤害/MP消耗
        estimated_damage = 6 + player_atk  # 假设基础伤害6
        return estimated_damage / max(1, card.mp_cost)
    elif card.type == "defense":
        # 防御卡牌：护甲/MP消耗
        estimated_armor = 8  # 假设基础护甲8
        return estimated_armor / max(1, card.mp_cost)
    elif card.type == "heal":
        # 治疗卡牌：治疗量/MP消耗
        estimated_heal = 12  # 假设基础治疗12
        return estimated_heal / max(1, card.mp_cost)
    else:
        return 1


def shuffle_list(items):
    """洗牌函数，返回洗牌后的新列表"""
    shuffled = items.copy()
    random.shuffle(shuffled)
    return shuffled


def get_random_choice(items, weights=None):
    """带权重的随机选择"""
    if not items:
        return None
    
    if weights:
        return random.choices(items, weights=weights, k=1)[0]
    else:
        return random.choice(items)


def format_number_with_sign(number):
    """格式化数字，显示正负号"""
    if number > 0:
        return f"+{number}"
    elif number < 0:
        return str(number)
    else:
        return "0"


def get_percentage(current, maximum):
    """计算百分比"""
    if maximum <= 0:
        return 0
    return (current / maximum) * 100


def is_critical_hp(current_hp, max_hp, threshold=0.25):
    """检查是否处于危险血量"""
    if max_hp <= 0:
        return True
    return (current_hp / max_hp) <= threshold


def is_low_mp(current_mp, max_mp, threshold=0.3):
    """检查是否MP不足"""
    if max_mp <= 0:
        return True
    return (current_mp / max_mp) <= threshold


def get_turn_phase_name(phase):
    """获取回合阶段的中文名称"""
    phase_names = {
        "CARD_PHASE": "出牌阶段",
        "BATTLE_PHASE": "战斗阶段",
        "END_PHASE": "结束阶段"
    }
    return phase_names.get(phase, "未知阶段")


def format_battle_log_message(message, message_type="info"):
    """格式化战斗日志消息"""
    prefixes = {
        "info": "[信息]",
        "damage": "[伤害]",
        "heal": "[治疗]",
        "event": "[事件]",
        "error": "[错误]"
    }
    prefix = prefixes.get(message_type, "[信息]")
    return f"{prefix} {message}"


def get_compass_symbol_color(event_type):
    """获取罗盘符号的显示颜色"""
    from core.compass_system import CompassPosition
    
    color_map = {
        CompassPosition.NORMAL: (200, 200, 200),    # 灰色
        CompassPosition.NEGATIVE: (255, 100, 100),  # 红色
        CompassPosition.LUCKY: (255, 255, 100)      # 金色
    }
    return color_map.get(event_type, (255, 255, 255))


def validate_game_state(player, enemy):
    """验证游戏状态的完整性"""
    errors = []
    
    # 检查玩家状态
    if not player:
        errors.append("玩家对象不存在")
    else:
        if player.hp < 0:
            errors.append("玩家HP为负数")
        if player.mp < 0:
            errors.append("玩家MP为负数")
        if player.armor < 0:
            errors.append("玩家护甲为负数")
    
    # 检查敌人状态
    if not enemy:
        errors.append("敌人对象不存在")
    else:
        if enemy.hp < 0:
            errors.append("敌人HP为负数")
    
    return len(errors) == 0, errors


def create_safe_filename(filename):
    """创建安全的文件名（移除特殊字符）"""
    import re
    # 只保留字母、数字、下划线和连字符
    safe_name = re.sub(r'[^\w\-_.]', '_', filename)
    return safe_name


def log_game_event(event_type, message, additional_data=None):
    """记录游戏事件（用于调试和统计）"""
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {event_type}: {message}"
    
    if additional_data:
        log_entry += f" | Data: {additional_data}"
    
    # 这里可以扩展为写入文件或发送到日志系统
    print(log_entry)
    
    return log_entry 