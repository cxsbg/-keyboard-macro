import keyboard
import pyautogui
import time
import sys
import threading
from datetime import datetime

# 控制程序运行的全局标志
is_running = False

# 获取当前时间的函数，用于输出提示
def get_time():
    return datetime.now().strftime("%H:%M:%S")

def start_macro():
    global is_running
    if not is_running:
        print(f"\n[{get_time()}] 检测到按键 'Ctrl+S'：程序将于 5 秒后启动循环...")
        def delayed_start():
            global is_running
            time.sleep(5)
            is_running = True
            print(f"[{get_time()}] 循环已启动！正在交替按下 Tab 和 Enter...")
        threading.Thread(target=delayed_start).start()

def stop_macro():
    global is_running
    if is_running:
        is_running = False
        print(f"\n[{get_time()}] 检测到按键 'Ctrl+E'：循环已终止。按下 'Ctrl+S' 可重新开始，或直接退出。")

# 绑定全局热键
keyboard.add_hotkey('ctrl+s', start_macro)
keyboard.add_hotkey('ctrl+e', stop_macro)

print("="*45)
print("键盘模拟程序已准备就绪")
print("1. 按下 'Ctrl+S' 键：等待5秒后开始 Tab 和 Enter 循环")
print("2. 按下 'Ctrl+E' 键：立即终止循环")
print("3. 直接关闭此黑框窗口：彻底退出程序")
print("="*45)

try:
    # 主循环
    while True:
        if is_running:
            # 模拟按下 Tab 并输出提示
            pyautogui.press('tab')
            print(f"[{get_time()}] 已模拟按下 => Tab")
            time.sleep(2)
            
            # 在等待后、按下 Enter 前再次检查是否已经被叫停
            if not is_running:
                continue
                
            # 模拟按下 Enter 并输出提示
            pyautogui.press('enter')
            print(f"[{get_time()}] 已模拟按下 => Enter")
            time.sleep(2)
        else:
            # 暂停状态下，降低 CPU 占用
            time.sleep(0.1)
except KeyboardInterrupt:
    print(f"\n[{get_time()}] 程序已关闭。")
    sys.exit()
