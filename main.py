#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回合制卡牌战斗游戏 - 主入口文件
Card Battle Game - Main Entry Point
"""

from core.game import Game

def main():
    """游戏主函数"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main() 