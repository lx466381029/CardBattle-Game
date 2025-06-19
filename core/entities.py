"""
游戏实体类定义 - 玩家和敌人
Game Entities - Player and Enemy Classes
"""

from config.constants import *

class Player:
    """玩家角色类"""
    
    def __init__(self):
        """初始化玩家属性"""
        self.max_hp = INITIAL_PLAYER_HP
        self.hp = INITIAL_PLAYER_HP
        self.max_mp = INITIAL_PLAYER_MP
        self.mp = INITIAL_PLAYER_MP
        self.base_atk = INITIAL_PLAYER_ATK  # 基础攻击力
        self.atk = INITIAL_PLAYER_ATK       # 当前攻击力
        self.armor = 0                      # 护甲值，每回合重置
        
    def take_damage(self, damage):
        """受到伤害，护甲减免"""
        if damage <= 0:
            return 0
            
        # 护甲减免
        reduced_damage = max(0, damage - self.armor)
        self.armor = max(0, self.armor - damage)  # 护甲也会被消耗
        
        # 扣除HP
        actual_damage = min(reduced_damage, self.hp)
        self.hp -= actual_damage
        
        return actual_damage
        
    def heal(self, amount):
        """治疗回血"""
        if amount <= 0:
            return 0
            
        actual_heal = min(amount, self.max_hp - self.hp)
        self.hp += actual_heal
        
        return actual_heal
        
    def restore_mp(self, amount):
        """恢复MP"""
        if amount <= 0:
            return 0
            
        actual_restore = min(amount, self.max_mp - self.mp)
        self.mp += actual_restore
        
        return actual_restore
        
    def consume_mp(self, amount):
        """消耗MP"""
        if amount <= 0:
            return True
            
        if self.mp >= amount:
            self.mp -= amount
            return True
        return False
        
    def add_armor(self, amount):
        """增加护甲"""
        if amount > 0:
            self.armor += amount
            
    def reset_for_new_turn(self):
        """回合开始时重置属性"""
        self.atk = self.base_atk  # 攻击力重置为基础值1
        self.armor = 0            # 护甲重置为0
        
    def is_alive(self):
        """检查是否存活"""
        return self.hp > 0
        
    def get_status_info(self):
        """获取状态信息字典"""
        return {
            'hp': self.hp,
            'max_hp': self.max_hp,
            'hp_percentage': (self.hp / self.max_hp) * 100,
            'mp': self.mp,
            'max_mp': self.max_mp,
            'mp_percentage': (self.mp / self.max_mp) * 100,
            'atk': self.atk,
            'base_atk': self.base_atk,
            'armor': self.armor,
            'alive': self.is_alive()
        }


class Enemy:
    """敌人角色类"""
    
    def __init__(self, name="Forest Goblin", hp=None, atk=None):
        """初始化敌人属性"""
        self.name = name
        self.max_hp = hp if hp is not None else INITIAL_ENEMY_HP
        self.hp = self.max_hp
        self.atk = atk if atk is not None else INITIAL_ENEMY_ATK
        
    def take_damage(self, damage):
        """受到伤害"""
        if damage <= 0:
            return 0
            
        actual_damage = min(damage, self.hp)
        self.hp -= actual_damage
        
        return actual_damage
        
    def heal(self, amount):
        """敌人治疗（某些敌人技能可能需要）"""
        if amount <= 0:
            return 0
            
        actual_heal = min(amount, self.max_hp - self.hp)
        self.hp += actual_heal
        
        return actual_heal
        
    def is_alive(self):
        """检查是否存活"""
        return self.hp > 0
        
    def get_attack_damage(self):
        """获取攻击伤害（可以添加随机性或特殊效果）"""
        return self.atk
        
    def get_status_info(self):
        """获取状态信息字典"""
        return {
            'name': self.name,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'hp_percentage': (self.hp / self.max_hp) * 100,
            'atk': self.atk,
            'alive': self.is_alive()
        } 