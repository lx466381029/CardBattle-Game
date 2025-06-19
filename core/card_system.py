"""
卡牌系统管理 - 牌库、手牌、出牌逻辑
Card System Management - Deck, Hand, and Card Playing Logic
"""

import random
from data.cards import create_starting_deck
from utils.helpers import shuffle_list


class CardSystem:
    """卡牌管理系统，处理牌库、手牌、出牌逻辑"""
    
    def __init__(self, initial_deck=None):
        """初始化卡牌系统"""
        if initial_deck is None:
            initial_deck = create_starting_deck()
        
        self.deck = shuffle_list(initial_deck)  # 牌库
        self.hand = []                          # 手牌
        self.played_cards = []                  # 已使用卡牌堆
        self.max_hand_size = 5                  # 最大手牌数量
        
    def draw_cards(self, count):
        """抽牌到手牌"""
        cards_drawn = 0
        
        for _ in range(count):
            # 检查手牌是否已满
            if len(self.hand) >= self.max_hand_size:
                break
                
            # 从牌库抽牌
            if len(self.deck) > 0:
                card = self.deck.pop(0)
                self.hand.append(card)
                cards_drawn += 1
            elif len(self.played_cards) > 0:
                # 牌库空了，重新洗牌
                self._reshuffle_played_cards()
                if len(self.deck) > 0:
                    card = self.deck.pop(0)
                    self.hand.append(card)
                    cards_drawn += 1
            else:
                # 牌库和弃牌堆都空了，无法抓牌
                break
        
        return cards_drawn
                    
    def fill_hand(self):
        """补充手牌到满"""
        needed = self.max_hand_size - len(self.hand)
        if needed > 0:
            return self.draw_cards(needed)
        return 0
        
    def play_card(self, card_index, battle_context):
        """出牌"""
        if not (0 <= card_index < len(self.hand)):
            return False, "无效的卡牌索引"
        
        card = self.hand[card_index]
        
        # 检查是否可以使用
        if not card.can_play(battle_context.player):
            return False, f"MP不足，需要 {card.mp_cost} MP"
        
        # 消耗MP
        battle_context.player.consume_mp(card.mp_cost)
        
        # 执行卡牌效果
        card.execute_effect(battle_context)
        
        # 推进罗盘
        event_type = battle_context.compass.advance(card.compass_points)
        battle_context.handle_compass_event(event_type)
        
        # 移动卡牌到弃牌堆
        played_card = self.hand.pop(card_index)
        self.played_cards.append(played_card)
        
        return True, f"使用了 {card.name}"
        
    def add_negative_card(self, negative_card):
        """添加负面卡牌到牌库顶部"""
        self.deck.insert(0, negative_card)
        
    def remove_card_from_hand(self, card_index):
        """从手牌中移除卡牌（用于弃牌等效果）"""
        if 0 <= card_index < len(self.hand):
            removed_card = self.hand.pop(card_index)
            self.played_cards.append(removed_card)
            return removed_card
        return None
        
    def get_hand_info(self):
        """获取手牌信息"""
        hand_info = []
        for i, card in enumerate(self.hand):
            info = card.get_display_info()
            info['index'] = i
            info['playable'] = False  # 这个需要在有battle_context时才能确定
            hand_info.append(info)
        return hand_info
        
    def get_deck_count(self):
        """获取牌库剩余数量"""
        return len(self.deck)
        
    def get_hand_count(self):
        """获取手牌数量"""
        return len(self.hand)
        
    def get_played_count(self):
        """获取弃牌堆数量"""
        return len(self.played_cards)
        
    def _reshuffle_played_cards(self):
        """重新洗牌弃牌堆"""
        if len(self.played_cards) > 0:
            self.deck = shuffle_list(self.played_cards)
            self.played_cards.clear()
            
    def reset_for_new_battle(self):
        """为新战斗重置卡牌系统"""
        # 将所有卡牌重新放入牌库
        all_cards = self.deck + self.hand + self.played_cards
        self.deck = shuffle_list(all_cards)
        self.hand.clear()
        self.played_cards.clear()
        
        # 抽取初始手牌
        self.fill_hand()
        
    def get_statistics(self):
        """获取卡牌系统统计信息"""
        return {
            'deck_count': self.get_deck_count(),
            'hand_count': self.get_hand_count(),
            'played_count': self.get_played_count(),
            'total_cards': self.get_deck_count() + self.get_hand_count() + self.get_played_count(),
            'hand_full': len(self.hand) >= self.max_hand_size
        } 