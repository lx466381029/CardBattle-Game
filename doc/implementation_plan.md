# 回合制卡牌战斗游戏 - 实施计划文档

> **Card Battle Game - Implementation Plan Document**

---

## 🎯 项目概述

基于pygame的回合制卡牌战斗游戏完整实现计划。本文档详细规划了从项目搭建到核心功能完成的全部开发步骤，确保按照设计文档有序推进。

---

## 📋 总体实施策略

### 开发原则
- **渐进式开发**：每个阶段都可独立运行和测试
- **模块化设计**：各系统相对独立，便于调试和扩展
- **验收驱动**：每步完成都有明确的验收标准
- **风险控制**：核心功能优先，UI和优化功能后置

### 技术栈
- **语言**：Python 3.8+
- **框架**：pygame >= 2.0.0
- **架构**：MVC模式，事件驱动
- **测试**：逐模块验证 + 集成测试

---

## 🚀 分阶段实施计划

### **阶段1：项目基础搭建（1-2天）**

#### 1.1 项目结构初始化
```bash
CardBattle/
├── main.py                 # 游戏入口
├── requirements.txt        # 依赖管理
├── config/
│   ├── __init__.py
│   ├── settings.py         # 游戏配置
│   └── constants.py        # 常量定义
├── core/
│   ├── __init__.py
│   ├── game.py            # 游戏主控制器
│   ├── entities.py         # 实体类定义
│   └── [其他核心模块]
├── ui/
│   ├── __init__.py
│   └── game_ui.py         # 界面管理
├── data/
│   ├── __init__.py
│   ├── cards.py           # 卡牌数据
│   ├── enemies.py         # 敌人数据
│   └── events.py          # 事件数据
└── utils/
    ├── __init__.py
    └── helpers.py         # 工具函数
```

**技术要求**：
```python
# main.py - 基础游戏循环
import pygame
from core.game import Game

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
```

**验收标准**：
- [ ] 目录结构完整创建
- [ ] 可以运行空的pygame窗口（1024x768）
- [ ] 60FPS稳定运行，无错误输出
- [ ] requirements.txt包含pygame依赖

#### 1.2 基础配置实现
```python
# config/settings.py
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
BACKGROUND_COLOR = (20, 20, 40)

# config/constants.py
HAND_SIZE = 5
COMPASS_POSITIONS = 12
INITIAL_PLAYER_HP = 100
INITIAL_PLAYER_MP = 50
INITIAL_PLAYER_ATK = 8
```

**验收标准**：
- [ ] 配置文件正确加载
- [ ] 游戏窗口按配置显示
- [ ] 常量可以在其他模块中正确引用

---

### **阶段2：核心数据结构（1-2天）**

#### 2.1 实体类实现
```python
# core/entities.py
class Player:
    def __init__(self):
        self.hp = INITIAL_PLAYER_HP
        self.max_hp = INITIAL_PLAYER_HP
        self.mp = INITIAL_PLAYER_MP
        self.max_mp = INITIAL_PLAYER_MP
        self.atk = INITIAL_PLAYER_ATK
        self.armor = 0
        
    def take_damage(self, damage):
        """受到伤害，考虑护甲减免"""
        final_damage = max(0, damage - self.armor)
        self.hp -= final_damage
        return final_damage
        
    def heal(self, amount):
        """治疗回血"""
        self.hp = min(self.max_hp, self.hp + amount)
        
    def is_alive(self):
        return self.hp > 0

class Enemy:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        
    def take_damage(self, damage):
        self.hp -= damage
        return damage
        
    def is_alive(self):
        return self.hp > 0
```

**验收标准**：
- [ ] Player和Enemy类可以正确创建
- [ ] 属性初始化值正确
- [ ] 伤害和治疗方法工作正常
- [ ] 死亡判定逻辑正确

#### 2.2 卡牌基础类
```python
# data/cards.py
class Card:
    def __init__(self, card_id, name, card_type, mp_cost, compass_points, effect_func, description):
        self.id = card_id
        self.name = name
        self.type = card_type
        self.mp_cost = mp_cost
        self.compass_points = compass_points
        self.effect = effect_func
        self.description = description
        
    def can_play(self, player):
        return player.mp >= self.mp_cost
        
    def execute_effect(self, battle_context):
        if self.effect:
            self.effect(battle_context)

# 基础卡牌效果函数
def strike_effect(battle_context):
    """攻击效果：造成6点伤害"""
    damage = 6 + battle_context.player.atk
    final_damage = battle_context.enemy.take_damage(damage)
    battle_context.log(f"Strike deals {final_damage} damage to {battle_context.enemy.name}")

def block_effect(battle_context):
    """防御效果：获得8点护甲"""
    battle_context.player.armor += 8
    battle_context.log("Player gains 8 armor")

def heal_effect(battle_context):
    """治疗效果：恢复12点HP"""
    battle_context.player.heal(12)
    battle_context.log("Player heals 12 HP")

# 基础卡牌库
BASIC_CARDS = [
    Card("strike", "Strike", "attack", 0, 1, strike_effect, "Deal 6+ATK damage"),
    Card("block", "Block", "defense", 1, 1, block_effect, "Gain 8 armor"),
    Card("heal", "Heal", "heal", 2, 1, heal_effect, "Restore 12 HP"),
]
```

**验收标准**：
- [ ] 卡牌对象创建正确
- [ ] MP消耗检查功能正常
- [ ] 基础效果函数正确执行
- [ ] 至少3张不同类型卡牌可用

---

### **阶段3：罗盘系统实现（2-3天）**

#### 3.1 环形罗盘核心
```python
# core/compass_system.py
class CompassPosition:
    NORMAL = 0      # 无事发生
    NEGATIVE = 1    # 负面事件
    LUCKY = 2       # 幸运事件

COMPASS_LAYOUT = [
    # 12位置配置：6正常，5负面，1幸运
    CompassPosition.NORMAL, CompassPosition.NORMAL, CompassPosition.NORMAL,
    CompassPosition.NEGATIVE, CompassPosition.NEGATIVE, CompassPosition.NEGATIVE,
    CompassPosition.NORMAL, CompassPosition.NORMAL, CompassPosition.NORMAL,
    CompassPosition.NEGATIVE, CompassPosition.NEGATIVE,
    CompassPosition.LUCKY
]

class CompassSystem:
    def __init__(self):
        self.current_position = 0
        self.total_positions = 12
        self.layout = COMPASS_LAYOUT
        
    def advance(self, steps):
        """推进罗盘指定步数"""
        self.current_position = (self.current_position + steps) % self.total_positions
        return self.check_current_event()
        
    def check_current_event(self):
        """检查当前位置事件类型"""
        return self.layout[self.current_position]
        
    def get_visual_representation(self):
        """获取可视化表示"""
        symbols = ['■', '□', '★']
        visual = []
        for i, event_type in enumerate(self.layout):
            if i == self.current_position:
                visual.append(f'[{symbols[event_type]}]')
            else:
                visual.append(symbols[event_type])
        return visual
```

**验收标准**：
- [ ] 罗盘能正确推进任意步数
- [ ] 事件类型判断准确
- [ ] 可视化显示正确
- [ ] 12位置循环逻辑无误

#### 3.2 事件效果实现
```python
# data/events.py
import random

class CompassEvent:
    def __init__(self, name, description, effect_func):
        self.name = name
        self.description = description
        self.effect = effect_func
        
    def trigger(self, battle_context):
        battle_context.log(f"Compass Event: {self.name}!")
        self.effect(battle_context)

# 负面事件效果
def add_curse_card(battle_context):
    """添加诅咒卡牌到牌库"""
    curse_card = Card("curse", "Curse", "negative", 0, 0, curse_effect, "Skip next turn")
    battle_context.card_system.add_negative_card(curse_card)

def lose_hp_event(battle_context):
    """立即失去3点HP"""
    battle_context.player.take_damage(3)

def skip_turn_event(battle_context):
    """跳过下一个出牌阶段"""
    battle_context.skip_next_turn = True

# 幸运事件效果
def heal_bonus_event(battle_context):
    """立即恢复15点HP"""
    battle_context.player.heal(15)

def mp_bonus_event(battle_context):
    """获得3点额外MP"""
    battle_context.player.mp = min(battle_context.player.max_mp, battle_context.player.mp + 3)

# 事件库
NEGATIVE_EVENTS = [
    CompassEvent("Curse Strike", "A cursed card is added to your deck", add_curse_card),
    CompassEvent("Dark Energy", "You lose 3 HP immediately", lose_hp_event),
    CompassEvent("Exhaustion", "Skip your next card phase", skip_turn_event),
]

LUCKY_EVENTS = [
    CompassEvent("Divine Blessing", "Restore 15 HP immediately", heal_bonus_event),
    CompassEvent("Mana Surge", "Gain 3 extra MP this turn", mp_bonus_event),
]
```

**验收标准**：
- [ ] 每种事件效果正确执行
- [ ] 负面卡牌成功插入牌库
- [ ] 幸运事件正确触发
- [ ] 事件日志正确显示

---

### **阶段4：卡牌系统实现（2-3天）**

#### 4.1 卡牌管理系统
```python
# core/card_system.py
import random
from data.cards import BASIC_CARDS

class CardSystem:
    def __init__(self, initial_deck=None):
        if initial_deck is None:
            initial_deck = BASIC_CARDS * 4  # 每张卡4份
        self.deck = initial_deck.copy()
        self.hand = []
        self.played_cards = []
        random.shuffle(self.deck)
        
    def draw_cards(self, count):
        """抽牌到手牌"""
        for _ in range(count):
            if len(self.deck) > 0:
                card = self.deck.pop(0)
                self.hand.append(card)
            elif len(self.played_cards) > 0:
                # 牌库空了，重新洗牌
                self.deck = self.played_cards.copy()
                self.played_cards.clear()
                random.shuffle(self.deck)
                if len(self.deck) > 0:
                    card = self.deck.pop(0)
                    self.hand.append(card)
                    
    def fill_hand(self):
        """补充手牌到5张"""
        while len(self.hand) < 5:
            self.draw_cards(1)
            
    def play_card(self, card_index, battle_context):
        """出牌"""
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if card.can_play(battle_context.player):
                # 消耗MP
                battle_context.player.mp -= card.mp_cost
                # 执行效果
                card.execute_effect(battle_context)
                # 驱动罗盘
                event_type = battle_context.compass.advance(card.compass_points)
                battle_context.handle_compass_event(event_type)
                # 移动卡牌
                self.played_cards.append(self.hand.pop(card_index))
                return True
        return False
        
    def add_negative_card(self, negative_card):
        """添加负面卡牌到牌库顶部"""
        self.deck.insert(0, negative_card)
```

**验收标准**：
- [ ] 手牌管理正确（抽牌、出牌、洗牌）
- [ ] MP消耗检查正常
- [ ] 卡牌效果正确执行
- [ ] 罗盘联动工作正常
- [ ] 负面卡牌插入功能正常

---

### **阶段5：战斗管理器（2-3天）**

#### 5.1 回合制战斗核心
```python
# core/battle_manager.py
from core.entities import Player, Enemy
from core.card_system import CardSystem
from core.compass_system import CompassSystem
from data.events import NEGATIVE_EVENTS, LUCKY_EVENTS
import random

class BattleContext:
    """战斗上下文，传递给各种效果函数"""
    def __init__(self, player, enemy, card_system, compass, battle_manager):
        self.player = player
        self.enemy = enemy
        self.card_system = card_system
        self.compass = compass
        self.battle_manager = battle_manager
        self.skip_next_turn = False
        self.battle_log = []
        
    def log(self, message):
        self.battle_log.append(message)
        print(f"[LOG] {message}")
        
    def handle_compass_event(self, event_type):
        if event_type == CompassPosition.NORMAL:
            self.log("The compass spins quietly...")
        elif event_type == CompassPosition.NEGATIVE:
            event = random.choice(NEGATIVE_EVENTS)
            event.trigger(self)
        elif event_type == CompassPosition.LUCKY:
            event = random.choice(LUCKY_EVENTS)
            event.trigger(self)

class BattleManager:
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy("Forest Goblin", 80, 12)
        self.card_system = CardSystem()
        self.compass = CompassSystem()
        self.turn_count = 1
        self.phase = "CARD_PHASE"  # CARD_PHASE, BATTLE_PHASE
        self.battle_ended = False
        self.battle_context = BattleContext(
            self.player, self.enemy, self.card_system, 
            self.compass, self
        )
        
    def start_battle(self):
        """开始战斗"""
        self.card_system.fill_hand()
        self.battle_context.log("Battle begins!")
        self.battle_context.log(f"Turn {self.turn_count} starts")
        
    def play_card(self, card_index):
        """玩家出牌"""
        if self.phase == "CARD_PHASE" and not self.battle_ended:
            return self.card_system.play_card(card_index, self.battle_context)
        return False
        
    def end_turn(self):
        """结束回合"""
        if self.phase == "CARD_PHASE":
            self.phase = "BATTLE_PHASE"
            self.enemy_turn()
            self.next_turn()
            
    def enemy_turn(self):
        """敌人回合"""
        if self.enemy.is_alive():
            damage = self.player.take_damage(self.enemy.atk)
            self.battle_context.log(f"{self.enemy.name} attacks for {damage} damage")
            
    def next_turn(self):
        """进入下一回合"""
        if self.check_battle_end():
            return
            
        self.turn_count += 1
        self.phase = "CARD_PHASE"
        
        # 重置护甲
        self.player.armor = 0
        
        # 补充手牌
        self.card_system.fill_hand()
        
        self.battle_context.log(f"Turn {self.turn_count} starts")
        
    def check_battle_end(self):
        """检查战斗结束"""
        if not self.player.is_alive():
            self.battle_context.log("You have been defeated!")
            self.battle_ended = True
            return True
        elif not self.enemy.is_alive():
            self.battle_context.log("Victory! Enemy defeated!")
            self.battle_ended = True
            return True
        return False
```

**验收标准**：
- [ ] 战斗初始化正确
- [ ] 回合流程完整（出牌→敌人攻击→下一回合）
- [ ] 胜负判定正确
- [ ] 战斗日志记录完整

---

### **阶段6：基础UI实现（2-3天）**

#### 6.1 游戏界面渲染
```python
# ui/game_ui.py
import pygame

class GameUI:
    def __init__(self, screen, battle_manager):
        self.screen = screen
        self.battle_manager = battle_manager
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
    def render(self):
        """渲染完整界面"""
        self.screen.fill((20, 20, 40))
        
        self.render_turn_counter()
        self.render_battle_area()
        self.render_hand_area()
        self.render_log_and_button()
        
        pygame.display.flip()
        
    def render_turn_counter(self):
        """渲染回合数"""
        text = self.font.render(f"Turn: {self.battle_manager.turn_count}", True, (255, 255, 255))
        self.screen.blit(text, (512 - text.get_width()//2, 10))
        
    def render_battle_area(self):
        """渲染战斗区域"""
        # 敌人信息
        enemy = self.battle_manager.enemy
        enemy_text = f"🧌 Enemy: {enemy.name}"
        enemy_hp_text = f"💖 HP: {enemy.hp}/{enemy.max_hp}  ⚔️ ATK: {enemy.atk}"
        
        # 玩家信息
        player = self.battle_manager.player
        player_text = f"👤 Player: Hero"
        player_stats = f"💖 HP: {player.hp}  ⚔️ ATK: {player.atk}  ⚡ MP: {player.mp}  🛡️ Armor: {player.armor}"
        
        # 罗盘信息
        compass = self.battle_manager.compass
        compass_text = f"🌀 Compass ({compass.current_position}/{compass.total_positions}):"
        
        # 渲染文本
        y_offset = 50
        self.screen.blit(self.font.render(enemy_text, True, (255, 100, 100)), (50, y_offset))
        self.screen.blit(self.font.render(enemy_hp_text, True, (255, 100, 100)), (50, y_offset + 25))
        
        self.screen.blit(self.font.render(player_text, True, (100, 255, 100)), (50, y_offset + 70))
        self.screen.blit(self.font.render(player_stats, True, (100, 255, 100)), (50, y_offset + 95))
        
        self.screen.blit(self.font.render(compass_text, True, (255, 255, 100)), (500, y_offset))
        self.render_compass_visual(550, y_offset + 25)
        
    def render_compass_visual(self, x, y):
        """渲染罗盘可视化"""
        compass = self.battle_manager.compass
        visual = compass.get_visual_representation()
        
        # 简化显示为一行
        compass_str = " ".join(visual)
        text = self.small_font.render(compass_str, True, (255, 255, 100))
        self.screen.blit(text, (x, y))
        
    def render_hand_area(self):
        """渲染手牌区域"""
        hand = self.battle_manager.card_system.hand
        hand_text = f"Hand ({len(hand)}/5 cards):"
        
        y_offset = 200
        self.screen.blit(self.font.render(hand_text, True, (255, 255, 255)), (50, y_offset))
        
        # 渲染每张手牌
        for i, card in enumerate(hand):
            card_text = f"[{i+1}] {card.name}"
            card_desc = f"    {card.description} (MP:{card.mp_cost})"
            
            color = (255, 255, 255) if card.can_play(self.battle_manager.player) else (128, 128, 128)
            
            self.screen.blit(self.font.render(card_text, True, color), (50, y_offset + 30 + i*40))
            self.screen.blit(self.small_font.render(card_desc, True, color), (50, y_offset + 50 + i*40))
            
    def render_log_and_button(self):
        """渲染日志和按钮区域"""
        log_area_width = int(1024 * 0.8)  # 4/5宽度
        button_area_x = log_area_width + 20
        
        # 渲染日志
        log_y = 400
        self.screen.blit(self.font.render("Battle Log:", True, (255, 255, 255)), (50, log_y))
        
        recent_logs = self.battle_manager.battle_context.battle_log[-8:]  # 显示最近8条
        for i, log_msg in enumerate(recent_logs):
            self.screen.blit(self.small_font.render(f"> {log_msg}", True, (200, 200, 200)), 
                           (50, log_y + 25 + i*20))
        
        # 渲染按钮
        button_rect = pygame.Rect(button_area_x, 450, 150, 50)
        pygame.draw.rect(self.screen, (100, 50, 50), button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
        
        button_text = self.font.render("🔥 ATTACK", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        
        self.attack_button_rect = button_rect
        
    def handle_click(self, pos):
        """处理点击事件"""
        # 检查是否点击攻击按钮
        if hasattr(self, 'attack_button_rect') and self.attack_button_rect.collidepoint(pos):
            self.battle_manager.end_turn()
            return True
            
        # 检查是否点击手牌（简化版）
        if 200 < pos[1] < 400:  # 手牌区域
            card_index = (pos[1] - 230) // 40
            if 0 <= card_index < len(self.battle_manager.card_system.hand):
                self.battle_manager.play_card(card_index)
                return True
                
        return False
```

**验收标准**：
- [ ] 界面布局符合设计要求
- [ ] 所有游戏信息正确显示
- [ ] 罗盘可视化正常
- [ ] 鼠标点击响应正确
- [ ] 手牌和按钮交互正常

---

### **阶段7：游戏主循环集成（1天）**

#### 7.1 完整游戏循环
```python
# core/game.py
import pygame
import sys
from core.battle_manager import BattleManager
from ui.game_ui import GameUI
from config.settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Card Battle Game")
        self.clock = pygame.time.Clock()
        
        self.battle_manager = BattleManager()
        self.game_ui = GameUI(self.screen, self.battle_manager)
        
        # 开始战斗
        self.battle_manager.start_battle()
        
    def run(self):
        """主游戏循环"""
        running = True
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        self.game_ui.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    # 数字键1-5出牌
                    if pygame.K_1 <= event.key <= pygame.K_5:
                        card_index = event.key - pygame.K_1
                        self.battle_manager.play_card(card_index)
                    # 空格键结束回合
                    elif event.key == pygame.K_SPACE:
                        self.battle_manager.end_turn()
            
            # 渲染界面
            self.game_ui.render()
            
            # 控制帧率
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
```

**验收标准**：
- [ ] 游戏可以正常启动和退出
- [ ] 键盘和鼠标操作都正常
- [ ] 帧率稳定在60FPS
- [ ] 完整战斗流程可以运行

---

### **阶段8：集成测试与优化（1-2天）**

#### 8.1 功能完整性测试
**测试用例**：
- [ ] **战斗开始**：正确初始化玩家、敌人、手牌
- [ ] **出牌功能**：MP消耗、效果执行、罗盘推进
- [ ] **罗盘事件**：正常、负面、幸运事件都能触发
- [ ] **敌人AI**：每回合正确攻击
- [ ] **胜负判定**：HP归零时正确结束战斗
- [ ] **边界情况**：MP不足、牌库为空、各种异常输入

#### 8.2 性能优化
- [ ] 减少不必要的渲染操作
- [ ] 优化字体加载和文本渲染
- [ ] 确保内存使用稳定

#### 8.3 用户体验优化
- [ ] 添加操作提示
- [ ] 优化界面布局和配色
- [ ] 确保所有交互响应及时

---

## 📅 时间安排与里程碑

### 总体时间规划
- **第1-2天**：阶段1-2（项目基础+数据结构）
- **第3-5天**：阶段3-4（罗盘系统+卡牌系统）
- **第6-8天**：阶段5-6（战斗管理+UI实现）
- **第9天**：阶段7（游戏主循环集成）
- **第10-11天**：阶段8（测试与优化）

### 关键里程碑
1. **第2天末**：可以创建玩家和敌人，基础卡牌可用
2. **第5天末**：罗盘系统和卡牌系统完全工作
3. **第8天末**：完整UI界面，可以进行战斗
4. **第9天末**：游戏完全可玩
5. **第11天末**：所有功能稳定，测试通过

---

## 🎯 验收标准总览

### 最终交付标准
- [ ] **核心功能完整**：回合制战斗、出牌、罗盘、AI敌人
- [ ] **界面友好**：布局清晰，操作直观
- [ ] **运行稳定**：无崩溃，性能良好
- [ ] **代码质量**：结构清晰，注释完整
- [ ] **可扩展性**：易于添加新卡牌、新敌人、新事件

### 核心功能验证
1. 玩家可以通过点击或键盤出牌
2. 每张卡牌都有正确的效果和MP消耗
3. 罗盘正确推进并触发各种事件
4. 敌人每回合自动攻击
5. 战斗结束时有明确的胜负提示

---

> **文档版本**：v1.0  
> **预计完成时间**：10-11天  
> **负责人**：开发团队

这个实施计划确保了项目的有序推进，每个阶段都有明确的目标和验收标准。 