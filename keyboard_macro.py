import sys
import threading
import time
from datetime import datetime

import keyboard
import pyautogui

# 控制程序运行的全局标志
is_running = False
current_loops = 0
target_loops = 0

def get_time():
    """获取当前时间的函数，用于输出提示"""
    return datetime.now().strftime("%H:%M:%S")

def start_macro():
    """启动宏的函数，由快捷键触发"""
    global is_running, current_loops
    
    if not is_running:
        print(f"\n[{get_time()}] 检测到按键 'Ctrl+S'：程序将于 5 秒后启动循环...")
        
        def delayed_start():
            global is_running, current_loops
            time.sleep(5)
            current_loops = 0  # 每次重新启动时重置计数
            is_running = True
            print(f"[{get_time()}] 循环已启动！正在交替按下 Tab 和 Enter...")
            
        threading.Thread(target=delayed_start, daemon=True).start()

def stop_macro():
    """停止宏的函数，由快捷键触发"""
    global is_running
    
    if is_running:
        is_running = False
        print(f"\n[{get_time()}] 检测到按键 'Ctrl+E'：循环已手动终止。按下 'Ctrl+S' 可重新开始，或直接退出。")

def main():
    global is_running, target_loops, current_loops
    
    # 启动前获取用户输入的循环次数
    try:
        user_input = input("请输入要循环的次数 (输入 0 表示无限循环): ")
        target_loops = int(user_input)
        if target_loops < 0:
            target_loops = 0
    except ValueError:
        print("输入无效，默认设置为无限循环 (0)。")
        target_loops = 0

    # 绑定全局热键
    keyboard.add_hotkey('ctrl+s', start_macro)
    keyboard.add_hotkey('ctrl+e', stop_macro)

    print("=" * 45)
    print("键盘模拟程序已准备就绪")
    if target_loops == 0:
        print("当前模式：无限循环")
    else:
        print(f"当前模式：循环 {target_loops} 次后自动停止")
    print("1. 按下 'Ctrl+S' 键：等待5秒后开始 Tab 和 Enter 循环")
    print("2. 按下 'Ctrl+E' 键：随时手动终止循环")
    print("3. 直接关闭此黑框窗口：彻底退出程序")
    print("=" * 45)

    try:
        # 主循环
        while True:
            if is_running:
                # 模拟按下 Tab 并输出提示
                pyautogui.press('tab')
                print(f"[{get_time()}] 已模拟按下 => Tab")
                time.sleep(0.5)
                
                # 在等待后、按下 Enter 前再次检查是否已经被叫停
                if not is_running:
                    continue
                
                # 模拟按下 Enter 并输出提示
                pyautogui.press('enter')
                print(f"[{get_time()}] 已模拟按下 => Enter")
                time.sleep(0.5)

                # 如果设定了目标次数，则增加计数并检查是否完成
                if target_loops > 0:
                    current_loops += 1
                    print(f"[{get_time()}] --- 进度: {current_loops} / {target_loops} ---")
                    if current_loops >= target_loops:
                        print(f"\n[{get_time()}] 成功完成 {target_loops} 次循环，自动停止。")
                        is_running = False
            else:
                # 暂停状态下，降低 CPU 占用
                time.sleep(0.1)
                
    except KeyboardInterrupt:
        print(f"\n[{get_time()}] 程序已关闭。")
        sys.exit()

if __name__ == "__main__":
    main()
