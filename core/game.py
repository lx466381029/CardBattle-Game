"""
游戏主控制器 - 整合所有系统的主游戏循环
Game Controller - Main Game Loop Integrating All Systems
"""

import pygame
import sys
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND_COLOR
from core.battle_manager import BattleManager
from ui.game_ui import GameUI


class Game:
    """游戏主控制器"""
    
    def __init__(self):
        """初始化游戏"""
        # 初始化pygame
        pygame.init()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Card Battle Game - 回合制卡牌战斗游戏")
        
        # 游戏时钟
        self.clock = pygame.time.Clock()
        
        # 创建游戏系统
        self.battle_manager = BattleManager()
        self.ui = GameUI(self.screen, self.battle_manager)
        
        # 游戏状态
        self.running = True
        
        # 统计信息
        self.frame_count = 0
        self.total_time = 0
        
    def run(self):
        """运行游戏主循环"""
        print("游戏启动...")
        
        # 开始战斗
        self.battle_manager.start_battle()
        
        # 主游戏循环
        while self.running:
            dt = self.clock.tick(FPS)
            self.total_time += dt
            self.frame_count += 1
            
            self._handle_events()
            self._update()
            self._render()
        
        # 游戏结束
        self._cleanup()
        
    def _handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                self._handle_keyboard_input(event.key)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    self._handle_mouse_click(event.pos)
                    
            elif event.type == pygame.MOUSEMOTION:
                self.ui.handle_hover(event.pos)
    
    def _handle_keyboard_input(self, key):
        """处理键盘输入"""
        # ESC键退出游戏
        if key == pygame.K_ESCAPE:
            self.running = False
            return
        
        # R键重新开始
        if key == pygame.K_r:
            self.battle_manager.reset_battle()
            return
        
        # 空格键快速出击
        if key == pygame.K_SPACE:
            game_state = self.battle_manager.get_game_state()
            if (game_state['phase'] == 'CARD_PHASE' and 
                not game_state['battle_ended'] and 
                not game_state.get('skip_next_turn', False)):
                success, message = self.battle_manager.start_settlement_phase()
                if not success:
                    print(f"无法出击: {message}")
            return
        
        # 数字键1-5快速出牌
        if pygame.K_1 <= key <= pygame.K_5:
            card_index = key - pygame.K_1
            game_state = self.battle_manager.get_game_state()
            
            if (game_state['phase'] == 'CARD_PHASE' and 
                not game_state['battle_ended'] and 
                card_index < len(game_state['hand'])):
                
                success, message = self.battle_manager.play_card(card_index)
                if not success:
                    print(f"出牌失败: {message}")
    
    def _handle_mouse_click(self, pos):
        """处理鼠标点击"""
        game_state = self.battle_manager.get_game_state()
        action = self.ui.handle_click(pos, game_state)
        
        if action is None:
            return
        
        action_type, action_data = action
        
        if action_type == 'play_card':
            success, message = self.battle_manager.play_card(action_data)
            if not success:
                print(f"出牌失败: {message}")
                
        elif action_type == 'attack':
            success, message = self.battle_manager.start_settlement_phase()
            if not success:
                print(f"无法出击: {message}")
                
        elif action_type == 'restart':
            self.battle_manager.reset_battle()
    
    def _update(self):
        """更新游戏状态"""
        # 目前所有游戏逻辑都在BattleManager中处理
        # 这里可以添加其他需要每帧更新的逻辑
        pass
    
    def _render(self):
        """渲染游戏画面"""
        # 获取游戏状态
        game_state = self.battle_manager.get_game_state()
        
        # 渲染界面
        self.ui.render(self.screen, game_state)
        
        # 渲染调试信息（可选）
        if self.frame_count % 60 == 0:  # 每秒更新一次
            self._render_debug_info(game_state)
        
        # 更新显示
        pygame.display.flip()
    
    def _render_debug_info(self, game_state):
        """渲染调试信息（控制台输出）"""
        if self.frame_count > 0:
            avg_fps = 1000 / (self.total_time / self.frame_count) if self.total_time > 0 else 0
            
            debug_info = {
                'FPS': f"{avg_fps:.1f}",
                'Turn': game_state['turn_count'],
                'Phase': game_state['phase'],
                'Player HP': f"{game_state['player']['hp']}/{game_state['player']['max_hp']}",
                'Player MP': f"{game_state['player']['mp']}/{game_state['player']['max_mp']}",
                'Player ATK': game_state['player']['atk'],
                'Enemy HP': f"{game_state['enemy']['hp']}/{game_state['enemy']['max_hp']}",
                'Hand Size': len(game_state['hand']),
                'Deck Count': game_state['deck_count']
            }
            
            # 只在状态发生变化时输出（避免刷屏）
            if not hasattr(self, 'last_debug_info') or self.last_debug_info != debug_info:
                print("=== 游戏状态 ===")
                for key, value in debug_info.items():
                    print(f"{key}: {value}")
                print("===============")
                self.last_debug_info = debug_info.copy()
    
    def _cleanup(self):
        """清理资源"""
        print("游戏结束，正在清理资源...")
        
        # 显示最终统计
        if self.total_time > 0:
            avg_fps = 1000 / (self.total_time / self.frame_count)
            total_seconds = self.total_time / 1000
            
            print(f"游戏运行时间: {total_seconds:.1f}秒")
            print(f"平均FPS: {avg_fps:.1f}")
            print(f"总帧数: {self.frame_count}")
            
            # 战斗统计
            battle_stats = self.battle_manager.get_battle_statistics()
            print("=== 战斗统计 ===")
            for key, value in battle_stats.items():
                print(f"{key}: {value}")
        
        pygame.quit()
        print("再见！")
    
    def get_game_info(self):
        """获取游戏信息（供外部调用）"""
        return {
            'running': self.running,
            'frame_count': self.frame_count,
            'total_time': self.total_time,
            'avg_fps': 1000 / (self.total_time / self.frame_count) if self.total_time > 0 else 0,
            'battle_state': self.battle_manager.get_game_state()
        } 