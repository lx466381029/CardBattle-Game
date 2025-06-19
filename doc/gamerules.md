# 核心战斗模块设计任务拆分文档（gamerules.md）

> 阶段目标：完成回合制核心战斗模块的功能实现（出牌 → 罗盘 → 怪物攻击）。

---

## 🎯 阶段目标概述

实现卡牌回合战斗的最小可运行版本，支持以下完整回合流程：
1. 玩家出牌（无限制出牌次数）
2. 罗盘点数变化与事件触发
3. 怪物行动与伤害结算
4. 回合状态更新与进入下一轮


## 📦 模块结构设计

### 1. BattleManager（战斗管理器）
- 管理整体战斗状态与回合推进
- 维护队列（玩家、怪物）与阶段（出牌/结算）

#### 主要方法：
```ts
startBattle() // 初始化战斗单元与牌库
nextTurn() // 控制回合流程（出牌 → 罗盘 → 怪物 → 状态更新）
```

---

### 2. CardSystem（卡牌系统）
- 管理手牌、出牌逻辑、卡牌效果结算
- 与罗盘系统联动

#### 数据结构：
```ts
Card {
  id: string,
  name: string,
  type: 'attack' | 'defense' | 'buff' | 'heal' | 'control' | 'negative',
  mpCost: number,
  effect: (context) => void,
  compassPoint: number, // 驱动罗盘点数
}
```

#### 方法：
```ts
drawCards(count: number)
playCard(cardId: string)
resolveCardEffect(card: Card)
```

---

### 3. CompassSystem（罗盘系统）
- 接收卡牌驱动的点数变动
- 每累计超过指定阈值，触发一个罗盘格事件（负面事件）
- 事件：插入负面卡牌、扣血、跳过回合等

#### 数据结构：
```ts
Compass {
  currentPoint: number,
  triggerThreshold: number = 10,
  triggerEvent: () => void
}
```

#### 方法：
```ts
addPoints(points: number) // 累积点数
checkTrigger() // 是否触发事件
```

---

### 4. EnemyAI（怪物AI系统）
- 每回合固定执行一次攻击
- 可扩展为行为策略（当前阶段使用随机或固定值）

#### 数据结构：
```ts
Enemy {
  hp: number,
  atk: number,
  ai: () => void // 简单攻击逻辑
}
```

#### 方法：
```ts
performAction() // 执行一次攻击逻辑
```

---

### 5. DamageSystem（结算与伤害系统）
- 处理所有单位的伤害运算、护甲减免、生命变更
- 统一管理玩家与怪物的生命状态

#### 方法：
```ts
applyDamage(target, value)
checkDeath(target)
```

---

## ✅ 初始功能完成判定标准
- [ ] 玩家可连续出牌并生效（至少3种卡牌类型）
- [ ] 罗盘点数变化能触发负面事件（至少插入负面卡牌）
- [ ] 怪物每回合自动攻击并造成伤害
- [ ] 血量归零将终结战斗（胜/负）


## ⏱️ 建议开发节奏（按优先级）
1. ✅ BattleManager + EnemyAI 基础框架（控制轮换）
2. ✅ CardSystem + CompassSystem 联动
3. ✅ 初始卡牌库加载 & 出牌逻辑验证
4. ✅ 罗盘事件与负面卡牌机制实现
5. ✅ 怪物攻击与伤害结算逻辑完成


## 🔄 未来扩展预留点
- 玩家护甲/魔法/技能系统支持
- 敌人AI行为多样化（如蓄力、控制等）
- 场景卡牌、负面卡牌图标资源支持
- Buff/Debuff效果管理

---

> 本文档由策划同步用于各AI模块协作与代码规划参考，如需结构变更，请增量记录。

