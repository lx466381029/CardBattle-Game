"""
罗盘系统 - 环形罗盘机制管理
Compass System - Circular Compass Mechanism Management
"""

class CompassPosition:
    """罗盘位置类型定义"""
    NORMAL = 0      # 无事发生 (■)
    NEGATIVE = 1    # 负面事件 (□) 
    LUCKY = 2       # 幸运事件 (★)


# 12位置环形罗盘配置（顺时针）
# 6个正常位置，5个负面事件位置，1个幸运事件位置
COMPASS_LAYOUT = [
    CompassPosition.NORMAL,     # 位置0
    CompassPosition.NORMAL,     # 位置1
    CompassPosition.NORMAL,     # 位置2
    CompassPosition.NEGATIVE,   # 位置3
    CompassPosition.NEGATIVE,   # 位置4
    CompassPosition.NEGATIVE,   # 位置5
    CompassPosition.NORMAL,     # 位置6
    CompassPosition.NORMAL,     # 位置7
    CompassPosition.NORMAL,     # 位置8
    CompassPosition.NEGATIVE,   # 位置9
    CompassPosition.NEGATIVE,   # 位置10
    CompassPosition.LUCKY       # 位置11
]


class CompassSystem:
    """环形罗盘机制管理"""
    
    def __init__(self):
        """初始化罗盘系统"""
        self.current_position = 0       # 当前位置(0-11)
        self.total_positions = 12       # 总位置数
        self.layout = COMPASS_LAYOUT    # 位置事件类型布局
        
    def advance(self, steps):
        """推进罗盘指定步数"""
        if steps <= 0:
            return self.check_current_event()
            
        self.current_position = (self.current_position + steps) % self.total_positions
        return self.check_current_event()
    
    def check_current_event(self):
        """检查当前位置的事件类型"""
        return self.layout[self.current_position]
    
    def get_current_position(self):
        """获取当前位置"""
        return self.current_position
        
    def get_position_type(self, position):
        """获取指定位置的事件类型"""
        if 0 <= position < self.total_positions:
            return self.layout[position]
        return CompassPosition.NORMAL
    
    def get_visual_representation(self):
        """获取罗盘的可视化表示"""
        symbols = ['■', '□', '★']
        visual = []
        
        for i, event_type in enumerate(self.layout):
            if i == self.current_position:
                # 当前位置用括号标记
                visual.append(f'[{symbols[event_type]}]')
            else:
                visual.append(symbols[event_type])
        
        return visual
    
    def get_compass_display(self):
        """获取罗盘的圆形显示布局"""
        symbols = ['■', '□', '★']
        display = {}
        
        # 12个位置的圆形布局
        positions = {
            0: (0, -1),   # 12点钟方向
            1: (1, -1),   # 1点钟方向
            2: (1, 0),    # 3点钟方向
            3: (1, 1),    # 4点钟方向
            4: (0, 1),    # 6点钟方向
            5: (-1, 1),   # 7点钟方向
            6: (-1, 0),   # 9点钟方向
            7: (-1, -1),  # 10点钟方向
            8: (0, -1),   # 12点钟方向
            9: (1, -1),   # 1点钟方向
            10: (1, 0),   # 3点钟方向
            11: (1, 1)    # 4点钟方向
        }
        
        for i, event_type in enumerate(self.layout):
            symbol = symbols[event_type]
            if i == self.current_position:
                symbol = f'[{symbol}]'
            display[i] = {
                'symbol': symbol,
                'position': positions.get(i, (0, 0)),
                'is_current': i == self.current_position,
                'event_type': event_type
            }
        
        return display
    
    def get_steps_to_lucky(self):
        """获取到幸运事件位置的步数"""
        lucky_position = 11  # 幸运事件固定在位置11
        steps = (lucky_position - self.current_position) % self.total_positions
        return steps if steps > 0 else 12
    
    def get_next_negative_positions(self):
        """获取接下来的负面事件位置"""
        negative_positions = []
        for i in range(1, self.total_positions):
            pos = (self.current_position + i) % self.total_positions
            if self.layout[pos] == CompassPosition.NEGATIVE:
                negative_positions.append(pos)
        return negative_positions
    
    def reset_position(self, position=0):
        """重置罗盘位置"""
        if 0 <= position < self.total_positions:
            self.current_position = position
        else:
            self.current_position = 0
    
    def get_statistics(self):
        """获取罗盘统计信息"""
        normal_count = self.layout.count(CompassPosition.NORMAL)
        negative_count = self.layout.count(CompassPosition.NEGATIVE)
        lucky_count = self.layout.count(CompassPosition.LUCKY)
        
        return {
            'total_positions': self.total_positions,
            'current_position': self.current_position,
            'normal_positions': normal_count,
            'negative_positions': negative_count,
            'lucky_positions': lucky_count,
            'current_event_type': self.check_current_event()
        } 