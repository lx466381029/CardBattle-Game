"""
战斗管理器 - 回合制战斗控制和上下文管理
Battle Manager - Turn-based Combat Control and Context Management
"""

from core.entities import Player, Enemy
from core.card_system import CardSystem
from core.compass_system import CompassSystem
from data.events import trigger_compass_event
from utils.helpers import validate_game_state


class BattleContext:
    """战斗上下文，传递给各种效果函数"""
    
    def __init__(self, player, enemy, card_system, compass, battle_manager):
        """初始化战斗上下文"""
        self.player = player
        self.enemy = enemy
        self.card_system = card_system
        self.compass = compass
        self.battle_manager = battle_manager
        
        # 特殊状态标记
        self.skip_next_turn = False
        self.double_next_attack = False
        
        # 战斗日志
        self.battle_log = []
        
    def log(self, message):
        """添加战斗日志"""
        self.battle_log.append(message)
        print(f"[战斗] {message}")
        
    def handle_compass_event(self, event_type):
        """处理罗盘事件"""
        trigger_compass_event(event_type, self)
        
    def get_recent_logs(self, count=8):
        """获取最近的日志"""
        return self.battle_log[-count:] if len(self.battle_log) > count else self.battle_log


class BattleManager:
    """战斗管理器 - 控制整个战斗流程"""
    
    def __init__(self):
        """初始化战斗管理器"""
        # 创建游戏实体
        self.player = Player()
        self.enemy = Enemy("Forest Goblin", 80, 12)
        
        # 创建游戏系统
        self.card_system = CardSystem()
        self.compass = CompassSystem()
        
        # 战斗状态
        self.turn_count = 1
        self.phase = "CARD_PHASE"  # CARD_PHASE, SETTLEMENT_PHASE
        self.battle_ended = False
        self.victory = False
        
        # 创建战斗上下文
        self.battle_context = BattleContext(
            self.player, self.enemy, self.card_system, 
            self.compass, self
        )
        
        # 每回合MP恢复量
        self.mp_recovery_per_turn = 3
        
    def start_battle(self):
        """开始战斗"""
        self.battle_context.log("=== 战斗开始 ===")
        self.battle_context.log(f"面对敌人: {self.enemy.name} (HP:{self.enemy.hp}/ATK:{self.enemy.atk})")
        
        # 补充初始手牌
        cards_drawn = self.card_system.fill_hand()
        self.battle_context.log(f"抽取了 {cards_drawn} 张初始手牌")
        
        self.battle_context.log(f"回合 {self.turn_count} 开始 - 出牌阶段")
        
    def play_card(self, card_index):
        """玩家出牌"""
        if self.phase != "CARD_PHASE" or self.battle_ended:
            return False, "当前不能出牌"
            
        if self.battle_context.skip_next_turn:
            return False, "本回合被跳过，无法出牌"
        
        success, message = self.card_system.play_card(card_index, self.battle_context)
        
        if success:
            self.battle_context.log(message)
            # 检查战斗是否结束（主要针对直接伤害卡牌）
            self._check_battle_end()
            
        return success, message
        
    def start_settlement_phase(self):
        """开始结算阶段"""
        if self.phase != "CARD_PHASE" or self.battle_ended:
            return False, "无法进入结算阶段"
            
        self.phase = "SETTLEMENT_PHASE"
        self.battle_context.log("--- 进入结算阶段 ---")
        
        # 玩家攻击结算
        self._player_attack_settlement()
        
        # 检查敌人是否死亡
        if self._check_battle_end():
            return True, "结算完成"
        
        # 敌人攻击
        self._enemy_turn()
        
        # 进入下一回合
        self._next_turn()
        
        return True, "结算完成"
        
    def _player_attack_settlement(self):
        """玩家攻击结算"""
        if not self.enemy.is_alive():
            return
            
        # 计算玩家总攻击力
        total_damage = self.player.atk
        
        # 检查是否有攻击翻倍效果
        if self.battle_context.double_next_attack:
            total_damage *= 2
            self.battle_context.log(f"攻击翻倍效果触发！伤害从 {self.player.atk} 提升至 {total_damage}")
            self.battle_context.double_next_attack = False
        
        # 对敌人造成伤害
        if total_damage > 1:  # 基础攻击力1不造成伤害
            actual_damage = self.enemy.take_damage(total_damage - 1)  # 减去基础1点攻击
            self.battle_context.log(f"玩家攻击造成 {actual_damage} 点伤害给 {self.enemy.name}")
        else:
            self.battle_context.log("玩家攻击力不足，未造成伤害")
        
    def _enemy_turn(self):
        """敌人回合"""
        if not self.enemy.is_alive():
            return
            
        # 敌人攻击
        damage = self.enemy.get_attack_damage()
        actual_damage = self.player.take_damage(damage)
        
        self.battle_context.log(f"{self.enemy.name} 攻击造成 {actual_damage} 点伤害")
        
        # 检查战斗结束
        self._check_battle_end()
        
    def _next_turn(self):
        """进入下一回合"""
        if self.battle_ended:
            return
            
        self.turn_count += 1
        self.phase = "CARD_PHASE"
        
        # 重置玩家属性
        self.player.reset_for_new_turn()
        
        # 恢复MP
        mp_restored = self.player.restore_mp(self.mp_recovery_per_turn)
        if mp_restored > 0:
            self.battle_context.log(f"恢复了 {mp_restored} 点MP")
        
        # 处理特殊状态
        if self.battle_context.skip_next_turn:
            self.battle_context.log("跳过此回合的出牌阶段")
            self.battle_context.skip_next_turn = False
            # 直接进入结算阶段
            self.start_settlement_phase()
            return
        
        # 补充手牌
        cards_drawn = self.card_system.fill_hand()
        if cards_drawn > 0:
            self.battle_context.log(f"抽取了 {cards_drawn} 张卡牌")
        
        self.battle_context.log(f"回合 {self.turn_count} 开始 - 出牌阶段")
        
    def _check_battle_end(self):
        """检查战斗结束条件"""
        if not self.player.is_alive():
            self.battle_ended = True
            self.victory = False
            self.battle_context.log("=== 战败 ===")
            self.battle_context.log("你被击败了...")
            return True
            
        elif not self.enemy.is_alive():
            self.battle_ended = True
            self.victory = True
            self.battle_context.log("=== 胜利 ===")
            self.battle_context.log(f"成功击败了 {self.enemy.name}！")
            return True
            
        return False
        
    def get_game_state(self):
        """获取完整的游戏状态"""
        # 验证游戏状态
        state_valid, errors = validate_game_state(self.player, self.enemy)
        
        # 检查手牌可用性
        hand_info = self.card_system.get_hand_info()
        for card_info in hand_info:
            card = self.card_system.hand[card_info['index']]
            # 只有在出牌阶段且未被跳过时才能出牌
            card_info['playable'] = (card.can_play(self.player) and 
                                   self.phase == "CARD_PHASE" and 
                                   not self.battle_context.skip_next_turn)
        
        return {
            # 基础战斗信息
            'turn_count': self.turn_count,
            'phase': self.phase,
            'battle_ended': self.battle_ended,
            'victory': self.victory,
            
            # 实体状态
            'player': self.player.get_status_info(),
            'enemy': self.enemy.get_status_info(),
            
            # 卡牌系统
            'hand': hand_info,
            'deck_count': self.card_system.get_deck_count(),
            'played_count': self.card_system.get_played_count(),
            
            # 罗盘系统
            'compass_position': self.compass.get_current_position(),
            'compass_visual': self.compass.get_visual_representation(),
            'compass_stats': self.compass.get_statistics(),
            
            # 特殊状态
            'skip_next_turn': self.battle_context.skip_next_turn,
            'double_next_attack': self.battle_context.double_next_attack,
            
            # 战斗日志
            'battle_log': self.battle_context.get_recent_logs(),
            
            # 系统状态
            'state_valid': state_valid,
            'errors': errors if not state_valid else []
        }
        
    def reset_battle(self):
        """重置战斗（用于重新开始）"""
        # 重置实体
        self.player = Player()
        self.enemy = Enemy("Forest Goblin", 80, 12)
        
        # 重置卡牌系统
        self.card_system.reset_for_new_battle()
        
        # 重置罗盘
        self.compass.reset_position()
        
        # 重置战斗状态
        self.turn_count = 1
        self.phase = "CARD_PHASE"
        self.battle_ended = False
        self.victory = False
        
        # 重新创建战斗上下文
        self.battle_context = BattleContext(
            self.player, self.enemy, self.card_system, 
            self.compass, self
        )
        
        # 开始新战斗
        self.start_battle()
        
    def get_battle_statistics(self):
        """获取战斗统计信息"""
        return {
            'turns_elapsed': self.turn_count,
            'cards_played': self.card_system.get_played_count(),
            'compass_position': self.compass.get_current_position(),
            'player_hp_percentage': (self.player.hp / self.player.max_hp) * 100,
            'enemy_hp_percentage': (self.enemy.hp / self.enemy.max_hp) * 100,
            'battle_outcome': 'victory' if self.victory else 'defeat' if self.battle_ended else 'ongoing'
        } 