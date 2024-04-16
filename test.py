import keyboard
import pyautogui
from threading import Thread
from time import sleep
from itertools import chain


# while True:
#     x, y = pyautogui.position()
#     print(x, y)
#     time = __import__('time')
#     time.sleep(0.1)
# flag = True


# def func(sec):
#     global flag
#     sleep(sec)
#     keyboard.wait('`')
#     flag = False
#
#
# # 创建 Thread 实例
# t1 = Thread(target=func, args=(1, ))
#
# # 启动线程运行
# t1.start()
#
# while flag:
#     print('check...')
#     sleep(0.5)


def main():
    print('waiting for typing \'`\'')
    # 检测键盘"`"键启动
    keyboard.wait('`')
    print('running')

    n = 3
    # 循环n次，消耗2n个燃料，刷取3n次副本
    for i in range(n):
        # 右上角查看开拓力(2268, 89)
        pyautogui.click(2268, 89)
        sleep(0.5)
        # 点击确认以选择补充方式为燃料(1547, 978)
        pyautogui.click(1547, 978)
        sleep(0.5)
        # 点击‘+’至2个燃料(1834, 844)
        pyautogui.click(1834, 844)
        sleep(0.5)
        # 点击确定以添加燃料(1567, 991)
        pyautogui.click(1567, 991)
        sleep(2)
        # 点击空白处关闭对话框(2000, 1000)
        pyautogui.click(2000, 1000)
        sleep(0.5)
        # 进行三次循环
        for _ in range(3):
            # 点击再来一次开始(1606, 1266)
            pyautogui.click(1606, 1266)
            # sleep若干秒
            sleep(3)
            # 尝试开启符玄大招回血(374, 1191)
            pyautogui.click(374, 1191)
            # sleep若干秒
            sleep(50)


def test():
    def func1(*args, **kwargs):
        print(args)
        print(kwargs)

    def func2(*args, **kwargs):
        func1(*args, **kwargs)

    func2(aaa=111)


if __name__ == '__main__':
    test()

