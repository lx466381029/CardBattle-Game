"""
游戏界面管理 - 完整的UI渲染和交互处理
Game UI Management - Complete UI Rendering and Interaction Handling
"""

import pygame
import os
from utils.helpers import (
    format_hp_display, format_mp_display, get_health_color, 
    get_mp_color, get_compass_symbol_color, get_turn_phase_name
)


class GameUI:
    """游戏界面管理类"""
    
    def __init__(self, screen, battle_manager):
        """初始化游戏界面"""
        self.screen = screen
        self.battle_manager = battle_manager
        
        # 字体设置 - 使用支持中文的字体
        self._init_fonts()
        
        # 颜色定义
        self.colors = {
            'background': (20, 20, 40),
            'white': (255, 255, 255),
            'red': (255, 100, 100),
            'green': (100, 255, 100),
            'blue': (100, 200, 255),
            'yellow': (255, 255, 100),
            'gray': (128, 128, 128),
            'dark_gray': (64, 64, 64),
            'button_bg': (100, 50, 50),
            'button_hover': (150, 75, 75),
            'card_bg': (60, 60, 80),
            'card_border': (100, 100, 120)
        }
        
        # 界面布局 - 调整以适应更大字体
        self.layout = {
            'turn_area': (0, 0, 1024, 50),
            'battle_area': (0, 50, 1024, 220),
            'hand_area': (0, 270, 820, 220),
            'button_area': (820, 270, 204, 220),
            'log_area': (0, 490, 820, 278),
            'status_area': (820, 490, 204, 278)
        }
        
        # 交互元素
        self.card_rects = []
        self.button_rects = {}
        
    def _init_fonts(self):
        """初始化字体，优先使用系统中文字体"""
        # 尝试使用Windows系统字体
        chinese_fonts = [
            "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",   # 黑体
            "C:/Windows/Fonts/simsun.ttc",   # 宋体
        ]
        
        # 增大字体尺寸
        font_found = False
        for font_path in chinese_fonts:
            if os.path.exists(font_path):
                try:
                    self.font_large = pygame.font.Font(font_path, 36)    # 从32增加到36
                    self.font_medium = pygame.font.Font(font_path, 28)   # 从24增加到28
                    self.font_small = pygame.font.Font(font_path, 22)    # 从18增加到22
                    font_found = True
                    print(f"使用中文字体: {font_path}")
                    break
                except:
                    continue
        
        # 如果没找到中文字体，使用默认字体但增大尺寸
        if not font_found:
            print("未找到中文字体，使用默认字体（可能无法正确显示中文）")
            self.font_large = pygame.font.Font(None, 36)
            self.font_medium = pygame.font.Font(None, 28)
            self.font_small = pygame.font.Font(None, 22)
        
    def render(self, screen, game_state):
        """渲染完整界面"""
        # 清屏
        screen.fill(self.colors['background'])
        
        # 渲染各个区域
        self.render_turn_counter(game_state)
        self.render_battle_area(game_state)
        self.render_hand_area(game_state)
        self.render_button_area(game_state)
        self.render_log_area(game_state)
        self.render_status_area(game_state)
        
        # 如果战斗结束，显示结果
        if game_state['battle_ended']:
            self.render_battle_result(game_state)
        
        # 更新显示
        pygame.display.flip()
        
    def render_turn_counter(self, game_state):
        """渲染回合数和阶段信息"""
        x, y, w, h = self.layout['turn_area']
        
        # 背景
        pygame.draw.rect(self.screen, self.colors['dark_gray'], (x, y, w, h))
        
        # 回合信息
        phase_name = "出牌阶段" if game_state['phase'] == 'CARD_PHASE' else "结算阶段"
        turn_text = f"回合 {game_state['turn_count']} - {phase_name}"
        text_surface = self.font_medium.render(turn_text, True, self.colors['white'])
        text_x = x + w // 2 - text_surface.get_width() // 2
        self.screen.blit(text_surface, (text_x, y + 12))
        
    def render_battle_area(self, game_state):
        """渲染战斗区域"""
        x, y, w, h = self.layout['battle_area']
        
        # 敌人信息 (左上)
        self.render_enemy_info(game_state, x + 20, y + 20)
        
        # 玩家信息 (左下)
        self.render_player_info(game_state, x + 20, y + 130)
        
        # 罗盘信息 (右侧)
        self.render_compass_info(game_state, x + 600, y + 20)
        
    def render_enemy_info(self, game_state, x, y):
        """渲染敌人信息"""
        enemy = game_state['enemy']
        
        # 敌人名称
        name_text = f"敌人: {enemy['name']}"
        name_surface = self.font_medium.render(name_text, True, self.colors['red'])
        self.screen.blit(name_surface, (x, y))
        
        # 敌人状态
        hp_text = f"HP: {enemy['hp']}/{enemy['max_hp']}"
        atk_text = f"ATK: {enemy['atk']}"
        
        hp_color = self.colors['red'] if enemy['hp'] < enemy['max_hp'] * 0.3 else self.colors['white']
        hp_surface = self.font_small.render(hp_text, True, hp_color)
        atk_surface = self.font_small.render(atk_text, True, self.colors['white'])
        
        self.screen.blit(hp_surface, (x, y + 35))
        self.screen.blit(atk_surface, (x + 200, y + 35))
        
    def render_player_info(self, game_state, x, y):
        """渲染玩家信息"""
        player = game_state['player']
        
        # 玩家名称
        name_text = "玩家: 英雄"
        name_surface = self.font_medium.render(name_text, True, self.colors['green'])
        self.screen.blit(name_surface, (x, y))
        
        # 玩家状态
        hp_text = f"HP: {player['hp']}/{player['max_hp']}"
        mp_text = f"MP: {player['mp']}/{player['max_mp']}"
        atk_text = f"ATK: {player['atk']}"
        armor_text = f"护甲: {player['armor']}"
        
        hp_color = self.colors['red'] if player['hp'] < player['max_hp'] * 0.3 else self.colors['white']
        mp_color = self.colors['blue'] if player['mp'] > player['max_mp'] * 0.5 else self.colors['yellow']
        
        hp_surface = self.font_small.render(hp_text, True, hp_color)
        mp_surface = self.font_small.render(mp_text, True, mp_color)
        atk_surface = self.font_small.render(atk_text, True, self.colors['white'])
        armor_surface = self.font_small.render(armor_text, True, self.colors['blue'])
        
        self.screen.blit(hp_surface, (x, y + 35))
        self.screen.blit(mp_surface, (x + 150, y + 35))
        self.screen.blit(atk_surface, (x + 280, y + 35))
        self.screen.blit(armor_surface, (x + 380, y + 35))
        
    def render_compass_info(self, game_state, x, y):
        """渲染罗盘信息"""
        compass_stats = game_state['compass_stats']
        compass_visual = game_state['compass_visual']
        
        # 罗盘标题
        title_text = f"罗盘 ({compass_stats['current_position']}/11):"
        title_surface = self.font_medium.render(title_text, True, self.colors['yellow'])
        self.screen.blit(title_surface, (x, y))
        
        # 罗盘可视化 (简化为一行显示)
        visual_text = " ".join(compass_visual)
        visual_surface = self.font_small.render(visual_text, True, self.colors['yellow'])
        self.screen.blit(visual_surface, (x, y + 35))
        
        # 罗盘说明
        legend_text = "■=正常  □=负面  ★=幸运  [ ]=当前位置"
        legend_surface = self.font_small.render(legend_text, True, self.colors['gray'])
        self.screen.blit(legend_surface, (x, y + 65))
        
    def render_hand_area(self, game_state):
        """渲染手牌区域"""
        x, y, w, h = self.layout['hand_area']
        
        # 清空卡牌矩形列表
        self.card_rects.clear()
        
        # 背景
        pygame.draw.rect(self.screen, self.colors['dark_gray'], (x, y, w, h), 2)
        
        # 手牌标题
        hand_count = len(game_state['hand'])
        deck_count = game_state['deck_count']
        title_text = f"手牌 ({hand_count}/5) | 牌库: {deck_count}"
        title_surface = self.font_medium.render(title_text, True, self.colors['white'])
        self.screen.blit(title_surface, (x + 10, y + 10))
        
        # 渲染每张手牌 - 调整卡牌大小以适应更大字体
        card_width = 155
        card_height = 140
        card_spacing = 8
        start_x = x + 20
        start_y = y + 55
        
        for i, card_info in enumerate(game_state['hand']):
            card_x = start_x + i * (card_width + card_spacing)
            card_y = start_y
            
            # 记录卡牌矩形用于点击检测
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            self.card_rects.append(card_rect)
            
            # 渲染单张卡牌
            self.render_single_card(card_info, card_x, card_y, card_width, card_height)
            
    def render_single_card(self, card_info, x, y, width, height):
        """渲染单张卡牌"""
        # 背景颜色（根据可用性）
        if card_info['playable']:
            bg_color = self.colors['card_bg']
            border_color = self.colors['white']
        else:
            bg_color = self.colors['gray']
            border_color = self.colors['dark_gray']
            
        # 卡牌背景
        pygame.draw.rect(self.screen, bg_color, (x, y, width, height))
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2)
        
        # 卡牌名称
        name_surface = self.font_small.render(card_info['name'], True, self.colors['white'])
        name_x = x + width // 2 - name_surface.get_width() // 2
        self.screen.blit(name_surface, (name_x, y + 5))
        
        # 卡牌类型
        type_surface = self.font_small.render(f"[{card_info['type']}]", True, self.colors['yellow'])
        type_x = x + width // 2 - type_surface.get_width() // 2
        self.screen.blit(type_surface, (type_x, y + 30))
        
        # MP消耗
        mp_text = f"MP: {card_info['mp_cost']}"
        mp_surface = self.font_small.render(mp_text, True, self.colors['blue'])
        self.screen.blit(mp_surface, (x + 5, y + 60))
        
        # 罗盘点数
        compass_text = f"罗盘: {card_info['compass_points']}"
        compass_surface = self.font_small.render(compass_text, True, self.colors['yellow'])
        self.screen.blit(compass_surface, (x + 5, y + 85))
        
        # 卡牌描述
        desc_lines = self.wrap_text(card_info['description'], width - 10, self.font_small)
        for i, line in enumerate(desc_lines[:2]):  # 最多显示2行
            line_surface = self.font_small.render(line, True, self.colors['white'])
            self.screen.blit(line_surface, (x + 5, y + 110 + i * 20))
            
    def render_button_area(self, game_state):
        """渲染按钮区域"""
        x, y, w, h = self.layout['button_area']
        
        # 清空按钮矩形列表
        self.button_rects.clear()
        
        # 出击按钮
        if game_state['phase'] == 'CARD_PHASE' and not game_state['battle_ended']:
            button_text = "出击"
            button_enabled = True
        else:
            button_text = "等待中..."
            button_enabled = False
            
        button_rect = pygame.Rect(x + 20, y + 20, w - 40, 60)
        self.button_rects['attack'] = button_rect
        
        # 按钮颜色
        if button_enabled:
            button_color = self.colors['button_bg']
            text_color = self.colors['white']
        else:
            button_color = self.colors['gray']
            text_color = self.colors['dark_gray']
            
        pygame.draw.rect(self.screen, button_color, button_rect)
        pygame.draw.rect(self.screen, self.colors['white'], button_rect, 2)
        
        # 按钮文字
        text_surface = self.font_medium.render(button_text, True, text_color)
        text_x = button_rect.centerx - text_surface.get_width() // 2
        text_y = button_rect.centery - text_surface.get_height() // 2
        self.screen.blit(text_surface, (text_x, text_y))
        
        # 重新开始按钮
        if game_state['battle_ended']:
            restart_rect = pygame.Rect(x + 20, y + 90, w - 40, 60)
            self.button_rects['restart'] = restart_rect
            
            pygame.draw.rect(self.screen, self.colors['green'], restart_rect)
            pygame.draw.rect(self.screen, self.colors['white'], restart_rect, 2)
            
            restart_text = self.font_medium.render("重新开始", True, self.colors['white'])
            text_x = restart_rect.centerx - restart_text.get_width() // 2
            text_y = restart_rect.centery - restart_text.get_height() // 2
            self.screen.blit(restart_text, (text_x, text_y))
            
    def render_log_area(self, game_state):
        """渲染战斗日志区域"""
        x, y, w, h = self.layout['log_area']
        
        # 背景
        pygame.draw.rect(self.screen, self.colors['dark_gray'], (x, y, w, h), 2)
        
        # 标题
        title_surface = self.font_medium.render("战斗日志:", True, self.colors['white'])
        self.screen.blit(title_surface, (x + 10, y + 10))
        
        # 日志内容
        logs = game_state['battle_log']
        log_y = y + 45
        
        for i, log_msg in enumerate(logs[-12:]):  # 显示最近12条，因为字体更大了
            log_surface = self.font_small.render(f"> {log_msg}", True, self.colors['white'])
            self.screen.blit(log_surface, (x + 10, log_y + i * 22))
            
    def render_status_area(self, game_state):
        """渲染状态信息区域"""
        x, y, w, h = self.layout['status_area']
        
        # 背景
        pygame.draw.rect(self.screen, self.colors['dark_gray'], (x, y, w, h), 2)
        
        # 标题
        title_surface = self.font_medium.render("状态信息", True, self.colors['white'])
        self.screen.blit(title_surface, (x + 10, y + 10))
        
        # 特殊状态
        status_y = y + 45
        if game_state['skip_next_turn']:
            skip_surface = self.font_small.render("跳过下回合", True, self.colors['red'])
            self.screen.blit(skip_surface, (x + 10, status_y))
            status_y += 25
            
        if game_state['double_next_attack']:
            double_surface = self.font_small.render("下次攻击翻倍", True, self.colors['green'])
            self.screen.blit(double_surface, (x + 10, status_y))
            status_y += 25
            
        # 操作提示
        status_y += 10
        tips = [
            "操作提示:",
            "- 点击卡牌使用",
            "- 点击结束回合",
            "- ESC键退出"
        ]
        
        for tip in tips:
            tip_surface = self.font_small.render(tip, True, self.colors['gray'])
            self.screen.blit(tip_surface, (x + 10, status_y))
            status_y += 22
            
    def render_battle_result(self, game_state):
        """渲染战斗结果"""
        # 半透明遮罩
        overlay = pygame.Surface((1024, 768))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 结果窗口
        result_width = 450
        result_height = 220
        result_x = 512 - result_width // 2
        result_y = 384 - result_height // 2
        
        pygame.draw.rect(self.screen, self.colors['card_bg'], 
                        (result_x, result_y, result_width, result_height))
        pygame.draw.rect(self.screen, self.colors['white'], 
                        (result_x, result_y, result_width, result_height), 3)
        
        # 结果文字
        if game_state['victory']:
            result_text = "胜利！"
            text_color = self.colors['green']
        else:
            result_text = "失败..."
            text_color = self.colors['red']
            
        result_surface = self.font_large.render(result_text, True, text_color)
        text_x = result_x + result_width // 2 - result_surface.get_width() // 2
        self.screen.blit(result_surface, (text_x, result_y + 60))
        
        # 提示文字
        tip_text = "点击重新开始按钮继续游戏"
        tip_surface = self.font_small.render(tip_text, True, self.colors['white'])
        tip_x = result_x + result_width // 2 - tip_surface.get_width() // 2
        self.screen.blit(tip_surface, (tip_x, result_y + 140))
        
    def handle_click(self, pos, game_state):
        """处理鼠标点击事件"""
        # 检查卡牌点击
        for i, card_rect in enumerate(self.card_rects):
            if card_rect.collidepoint(pos):
                if i < len(game_state['hand']) and game_state['hand'][i]['playable']:
                    return ('play_card', i)
                
        # 检查按钮点击
        for button_name, button_rect in self.button_rects.items():
            if button_rect.collidepoint(pos):
                if button_name == 'attack':
                    return ('attack', None)
                elif button_name == 'restart':
                    return ('restart', None)
                
        return None
        
    def wrap_text(self, text, max_width, font):
        """文字换行处理"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
                
        if current_line:
            lines.append(current_line.strip())
            
        return lines

    def handle_hover(self, pos):
        """处理鼠标悬停"""
        # 简单实现，可以在卡牌上添加悬停效果
        pass 