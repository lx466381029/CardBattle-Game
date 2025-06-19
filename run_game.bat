@echo off
chcp 65001 >nul
echo ==========================================
echo    回合制卡牌战斗游戏 - Card Battle Game
echo ==========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo 正在检查依赖包...
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装pygame依赖包...
    pip install pygame>=2.0.0
    if %errorlevel% neq 0 (
        echo 错误: pygame安装失败
        pause
        exit /b 1
    )
    echo pygame安装成功！
)

echo.
echo 启动游戏...
echo ==========================================
python main.py

echo.
echo 游戏已结束
pause 