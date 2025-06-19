# 回合制卡牌战斗游戏 - Pygame实现设计文档

> **Card Battle Game - PyGame Implementation Design Document**

---

## 🎯 项目概述

基于pygame开发的回合制卡牌战斗游戏，实现玩家与怪物的卡牌对战系统。游戏采用模块化设计，支持卡牌效果、罗盘系统、AI敌人等核心功能。

### 核心特性
- 🃏 **卡牌战斗系统**：多种类型卡牌，无限制出牌
- 🌀 **罗盘机制**：卡牌使用驱动罗盘，触发负面事件
- 👾 **AI敌人系统**：自动化敌人行为与攻击
- ⚔️ **伤害结算系统**：护甲、生命值、魔法值管理
- 🎮 **回合制战斗**：出牌阶段 + 结算阶段

---

## 🖥️ 界面设计与布局

### 主战斗界面（1024x768分辨率）
```
┌─────────────────────────────────────────────────────────────────┐
│                          Turn: 3                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🧌 Enemy: Forest Goblin              🌀 Compass (8/12):        │
│  💖 HP: 45/80  ⚔️ ATK: 12              ┌─■─■─■─□─□─□─┐           │
│                                        │ □         ★ │           │
│  👤 Player: Hero                       │ □         □ │           │
│  💖 HP: 100  ⚔️ ATK: 8                 │ ■         □ │           │
│  ⚡ MP: 50   🛡️ Armor: 5               └─■─■─■─□─□─□─┘           │
│                                        ■=Normal  □=Negative  ★=Lucky │
├─────────────────────────────────────────────────────────────────┤
│  Hand (5/5 cards):                                             │
│  [⚔️ Strike] [🛡️ Block] [❤️ Heal] [🔥 Fireball] [⭐ Buff]       │
│   ATK+3      DEF+5      HP+8       ATK+5        ATK+2/Turn     │
│   MP:0       MP:1       MP:2       MP:3         MP:1           │
├─────────────────────────────────────────────────────────────────┤
│  Battle Log:                                     │             │
│  > You played Strike, dealt 8 damage to Enemy   │             │
│  > Compass advanced by 2 points                 │   [🔥 ATTACK] │
│  > Enemy attacks you for 10 damage              │             │
│  > Compass event: Dark Energy triggered!        │             │
│  > You lost 3 HP from dark energy               │             │
│                                                  │             │
└─────────────────────────────────────────────────┴─────────────┘
```

### 界面区域划分
1. **顶部回合栏**：当前回合数显示
2. **战斗信息区**：敌人信息（左上）、玩家信息（左下）、环形罗盘（右侧）
3. **手牌展示区**：当前手牌、卡牌属性和消耗
4. **底部左侧日志区（4/5）**：战斗行动记录、滚动显示
5. **底部右侧按钮区（1/5）**：进攻按钮，结束出牌阶段

---

## 🏗️ 核心架构设计

### 文件结构
```
CardBattle/
├── main.py                 # 游戏入口
├── config/
│   ├── settings.py         # 游戏配置
│   └── constants.py        # 常量定义
├── core/
│   ├── game.py            # 游戏主控制器
│   ├── battle_manager.py   # 战斗管理器
│   ├── card_system.py      # 卡牌系统
│   ├── compass_system.py   # 罗盘系统
│   ├── enemy_ai.py         # 敌人AI
│   └── damage_system.py    # 伤害结算系统
├── ui/
│   ├── game_ui.py         # 游戏界面管理
│   ├── card_ui.py         # 卡牌UI组件
│   └── battle_ui.py       # 战斗界面组件
├── data/
│   ├── cards.py           # 卡牌数据定义
│   ├── enemies.py         # 敌人数据
│   └── events.py          # 罗盘事件数据
└── utils/
    ├── animation.py       # 动画效果
    └── sound.py           # 音效管理
```

---

## 🎮 核心模块设计

### 1. Game类（游戏主控制器）
```python
class Game:
    """游戏主控制器，管理游戏状态和主循环"""
    
    def __init__(self):
        # 初始化pygame、屏幕、时钟等
        pass
    
    def run(self):
        # 主游戏循环
        # 处理事件、更新逻辑、渲染画面
        pass
    
    def handle_events(self, events):
        # 处理用户输入和界面事件
        pass
```

### 2. BattleManager类（战斗管理器）
```python
class BattleManager:
    """战斗状态管理，控制回合流程"""
    
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn_count = 1
        self.phase = "CARD_PHASE"  # CARD_PHASE, BATTLE_PHASE
        self.battle_ended = False
        
    def start_battle(self):
        # 初始化战斗：补充手牌、重置状态
        pass
    
    def next_turn(self):
        # 推进到下一回合：出牌阶段 → 结算阶段 → 下一回合
        pass
    
    def end_turn(self):
        # 强制结束当前出牌阶段，进入结算
        pass
    
    def check_victory_condition(self):
        # 检查胜负条件
        pass
```

### 3. CardSystem类（卡牌系统）
```python
class CardSystem:
    """卡牌管理系统，处理牌库、手牌、出牌逻辑"""
    
    def __init__(self, deck):
        self.deck = deck.copy()      # 牌库
        self.hand = []               # 手牌
        self.played_cards = []       # 已使用卡牌
        
    def draw_cards(self, count):
        # 抽牌到手牌，补充至指定数量
        pass
    
    def play_card(self, card_index, battle_context):
        # 出牌：检查MP、执行效果、驱动罗盘
        pass
    
    def add_negative_card(self, negative_card):
        # 添加负面卡牌到牌库顶部
        pass
```

### 4. CompassSystem类（罗盘系统）
```python
class CompassPosition:
    """罗盘位置定义"""
    NORMAL = 0      # 无事发生 (■)
    NEGATIVE = 1    # 负面事件 (□) 
    LUCKY = 2       # 幸运事件 (★)

# 12位置环形罗盘配置（顺时针）
COMPASS_LAYOUT = [
    # 位置0-8: 正常位置和负面事件混合
    NORMAL, NORMAL, NORMAL, NEGATIVE, NEGATIVE, NEGATIVE,
    NORMAL, NORMAL, NORMAL, NEGATIVE, NEGATIVE, 
    # 位置11: 幸运事件（终点）
    LUCKY
]

class CompassSystem:
    """环形罗盘机制管理"""
    
    def __init__(self):
        self.current_position = 0       # 当前位置(0-11)
        self.total_positions = 12       # 总位置数
        self.layout = COMPASS_LAYOUT    # 位置事件类型
        
    def advance(self, steps):
        """推进罗盘指定步数"""
        self.current_position = (self.current_position + steps) % self.total_positions
        return self.check_current_event()
    
    def check_current_event(self):
        """检查当前位置的事件类型"""
        return self.layout[self.current_position]
    
    def get_visual_representation(self):
        """获取罗盘的可视化表示"""
        symbols = ['■', '□', '★']
        current_ring = []
        for i, event_type in enumerate(self.layout):
            if i == self.current_position:
                current_ring.append(f'[{symbols[event_type]}]')  # 当前位置用括号
            else:
                current_ring.append(symbols[event_type])
        return current_ring
```

### 5. EnemyAI类（敌人AI）
```python
class EnemyAI:
    """敌人AI行为控制"""
    
    def __init__(self, enemy_data):
        self.enemy = enemy_data
        self.ai_pattern = "SIMPLE_ATTACK"  # 当前AI模式
        
    def perform_action(self, battle_context):
        # 执行敌人行动：攻击、技能、防御等
        pass
    
    def calculate_damage(self, target):
        # 计算对目标造成的伤害
        pass
```

### 6. DamageSystem类（伤害结算系统）
```python
class DamageSystem:
    """统一的伤害和治疗结算系统"""
    
    @staticmethod
    def apply_damage(target, damage_value, damage_type="physical"):
        # 计算护甲减免，应用伤害
        pass
    
    @staticmethod
    def apply_healing(target, heal_value):
        # 应用治疗效果
        pass
    
    @staticmethod
    def check_death(unit):
        # 检查单位是否死亡
        pass
```

---

## 🃏 卡牌数据结构

### Card类定义
```python
class Card:
    """卡牌基础数据结构"""
    
    def __init__(self, card_id, name, card_type, mp_cost, compass_points, effect_func, description):
        self.id = card_id
        self.name = name                    # 卡牌名称（英文）
        self.type = card_type              # 'attack', 'defense', 'heal', 'buff', 'control', 'negative'
        self.mp_cost = mp_cost             # 魔法值消耗
        self.compass_points = compass_points # 罗盘点数
        self.effect = effect_func          # 卡牌效果函数
        self.description = description      # 卡牌描述
        
    def can_play(self, player):
        # 检查是否可以使用（MP是否足够）
        return player.mp >= self.mp_cost
    
    def execute_effect(self, battle_context):
        # 执行卡牌效果
        self.effect(battle_context)
```

### 基础卡牌库示例
```python
BASIC_CARDS = [
    # 攻击类卡牌
    Card("strike", "Strike", "attack", 0, 1, strike_effect, "Deal 6 damage"),
    Card("heavy_blow", "Heavy Blow", "attack", 2, 2, heavy_blow_effect, "Deal 12 damage"),
    Card("fireball", "Fireball", "attack", 3, 3, fireball_effect, "Deal 15 damage"),
    
    # 防御类卡牌
    Card("block", "Block", "defense", 1, 1, block_effect, "Gain 8 armor"),
    Card("iron_will", "Iron Will", "defense", 2, 1, iron_will_effect, "Gain 15 armor"),
    
    # 治疗类卡牌
    Card("heal", "Heal", "heal", 2, 1, heal_effect, "Restore 12 HP"),
    Card("greater_heal", "Greater Heal", "heal", 4, 2, greater_heal_effect, "Restore 20 HP"),
    
    # 负面类卡牌（由罗盘事件插入）
    Card("curse", "Curse", "negative", 0, 0, curse_effect, "Skip next turn"),
    Card("drain", "Drain", "negative", 0, 0, drain_effect, "Lose 5 HP"),
]
```

---

## 🌀 罗盘事件系统

### 环形罗盘设计
```python
class CompassPosition:
    """罗盘位置定义"""
    NORMAL = 0      # 无事发生 (■)
    NEGATIVE = 1    # 负面事件 (□) 
    LUCKY = 2       # 幸运事件 (★)

# 12位置环形罗盘配置（顺时针）
COMPASS_LAYOUT = [
    # 位置0-8: 正常位置和负面事件混合
    NORMAL, NORMAL, NORMAL, NEGATIVE, NEGATIVE, NEGATIVE,
    NORMAL, NORMAL, NORMAL, NEGATIVE, NEGATIVE, 
    # 位置11: 幸运事件（终点）
    LUCKY
]

class CompassSystem:
    """环形罗盘机制管理"""
    
    def __init__(self):
        self.current_position = 0       # 当前位置(0-11)
        self.total_positions = 12       # 总位置数
        self.layout = COMPASS_LAYOUT    # 位置事件类型
        
    def advance(self, steps):
        """推进罗盘指定步数"""
        self.current_position = (self.current_position + steps) % self.total_positions
        return self.check_current_event()
    
    def check_current_event(self):
        """检查当前位置的事件类型"""
        return self.layout[self.current_position]
    
    def get_visual_representation(self):
        """获取罗盘的可视化表示"""
        symbols = ['■', '□', '★']
        current_ring = []
        for i, event_type in enumerate(self.layout):
            if i == self.current_position:
                current_ring.append(f'[{symbols[event_type]}]')  # 当前位置用括号
            else:
                current_ring.append(symbols[event_type])
        return current_ring
```

### 罗盘可视化布局
```
环形罗盘12位置布局：
        11  0   1
    10  ┌─────────┐  2
 9      │    ★    │      3
    8   │         │  4
        └─────────┘
        7   6   5

位置说明：
- 位置 0,1,2,6,7,8: 正常位置 (■) - 无事发生
- 位置 3,4,5,9,10: 负面事件 (□) - 触发负面效果  
- 位置 11: 幸运事件 (★) - 触发正面效果
```

### 事件类型详细定义

#### 1. 正常位置 (■ Normal)
```python
def normal_event(battle_context):
    """无事发生，罗盘正常推进"""
    battle_context.add_log("The compass spins quietly...")
    # 无额外效果
```

#### 2. 负面事件 (□ Negative) 
```python
NEGATIVE_EVENTS = [
    CompassEvent("Curse Strike", "A cursed card is added to your deck", add_curse_card),
    CompassEvent("Dark Energy", "You lose 3 HP immediately", lose_hp_event),
    CompassEvent("Exhaustion", "Skip your next card phase", skip_turn_event),
    CompassEvent("Mana Burn", "You lose 2 MP", lose_mp_event),
    CompassEvent("Weakness", "Your next attack deals 50% damage", weaken_attack_event),
]
```

#### 3. 幸运事件 (★ Lucky) 
```python
LUCKY_EVENTS = [
    CompassEvent("Divine Blessing", "Restore 15 HP immediately", heal_bonus_event),
    CompassEvent("Mana Surge", "Gain 3 extra MP this turn", mp_bonus_event), 
    CompassEvent("Battle Fury", "Your next attack deals double damage", double_attack_event),
    CompassEvent("Perfect Defense", "Gain 10 armor immediately", armor_bonus_event),
    CompassEvent("Card Draw", "Draw 2 extra cards", draw_bonus_event),
]
```

---

## 🎨 UI组件设计

### GameUI类（主界面管理）
```python
class GameUI:
    """游戏界面管理类"""
    
    def __init__(self, screen, battle_manager):
        self.screen = screen
        self.battle_manager = battle_manager
        self.font = pygame.font.Font(None, 24)
        
    def render(self):
        # 渲染整个游戏界面
        self.render_player_status()
        self.render_enemy_status()
        self.render_compass()
        self.render_hand()
        self.render_battle_log()
        self.render_buttons()
    
    def handle_click(self, pos):
        # 处理鼠标点击事件
        pass
```

### CardUI类（卡牌渲染组件）
```python
class CardUI:
    """卡牌UI渲染组件"""
    
    def __init__(self, card, position, size=(120, 160)):
        self.card = card
        self.position = position
        self.size = size
        self.selected = False
        
    def render(self, screen):
        # 渲染单张卡牌：背景、文字、图标、边框
        pass
    
    def is_clicked(self, mouse_pos):
        # 检查是否被点击
        pass
```

---

## ⚡ 实现计划与里程碑

### 阶段1：核心战斗系统（优先级最高）
- [ ] **BattleManager基础框架**：回合管理、状态切换
- [ ] **基础卡牌系统**：出牌、效果执行、MP消耗
- [ ] **简单敌人AI**：固定攻击模式
- [ ] **伤害结算系统**：HP、护甲计算
- [ ] **胜负判定**：战斗结束条件

### 阶段2：罗盘系统与负面事件
- [ ] **罗盘点数累积**：卡牌驱动罗盘变化
- [ ] **负面事件触发**：达到阈值触发随机事件
- [ ] **负面卡牌插入**：动态添加到牌库
- [ ] **事件效果实现**：跳过回合、扣血、弃牌等

### 阶段3：界面优化与用户体验
- [ ] **游戏界面布局**：状态栏、手牌区、战斗区
- [ ] **卡牌UI组件**：卡牌渲染、选择效果、拖拽
- [ ] **动画效果**：出牌动画、伤害数字、状态变化
- [ ] **战斗日志**：行动记录、滚动显示

### 阶段4：扩展功能（未来版本）
- [ ] **多种敌人类型**：不同AI行为模式
- [ ] **buff/debuff系统**：状态效果管理
- [ ] **卡牌演化机制**：卡牌升级系统
- [ ] **音效与视觉效果**：增强游戏体验

---

## 📋 技术规范

### 代码规范
- **语言**：Python 3.8+
- **主要依赖**：pygame >= 2.0.0
- **编码风格**：PEP 8标准
- **注释语言**：中文注释，英文变量名
- **文档字符串**：详细的函数和类说明

### 性能要求
- **帧率**：稳定60 FPS
- **响应时间**：UI操作响应 < 100ms
- **内存使用**：< 100MB
- **启动时间**：< 3秒

### 测试要求
- **单元测试**：核心逻辑模块覆盖率 > 80%
- **集成测试**：完整战斗流程验证
- **用户测试**：界面操作流畅性验证

---

## 🔧 开发环境配置

### 依赖安装
```bash
pip install pygame>=2.0.0
pip install dataclasses  # Python 3.6兼容
```

### 项目初始化
```bash
mkdir CardBattle
cd CardBattle
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

> **文档版本**：v1.0  
> **最后更新**：2024年  
> **维护者**：CardBattle开发团队

这个设计文档将作为整个项目的开发指南，确保所有模块按照统一的架构和标准进行实现。 