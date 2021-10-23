"""
    这是本程序的入口程序。
    程序会在一系列初始设置后，进入一个主循环。在循环中不断对用户的输入做出响应。
    本程序主要使用opencv-python。按钮等逻辑完全由自己实现。
"""
import cv2
import time
from globals import GlobalVarControl as gvc
import controlor as ctl
import objects as obj
import drawers as dwr
import windows as wds

# 设置显示方式为全屏显示
cv2.namedWindow(gvc.window_name, cv2.WND_PROP_FULLSCREEN)
# 移动窗口到左上角
cv2.moveWindow(gvc.window_name, gvc.screen.x - 1, gvc.screen.y - 1)
cv2.setWindowProperty(gvc.window_name, cv2.WND_PROP_FULLSCREEN,
                      cv2.WINDOW_FULLSCREEN)
# 设置基本obj和draw
gvc.obj_root = obj.RunAble()
gvc.draw_root = dwr.DrawAble()
# 在外部设置获取鼠标输入的函数
cv2.setMouseCallback(gvc.window_name, ctl.get_user_input)
# 加载常用图形
dwr.load_useful_frames()
# 摄像头参数设置
# gvc.capture = cv2.VideoCapture(0)
# 初始化窗口
wds.goto_mainWindow()
gvc.frame = gvc.img_background.copy()
# 进入主循环
while True:
    # 主循环——收集用户输入-更新对象状态（时序逻辑）-绘制图形（组合逻辑）
    # 采集原始用户输入 (初始化时已经实现了)
    # 分析用户输入，因为程序足够简单，opencv提供的原始用户输入已经足够
    if gvc.LOOP_NUM > 1:
        # 进行对象状态的递归更新
        gvc.obj_root.update()

        # 进行绘制器的递归绘制
        gvc.frame = gvc.img_background.copy()
        gvc.draw_root.draw()

    # 显示结果
    cv2.imshow(gvc.window_name, gvc.frame)
    gvc.key = cv2.waitKey(1)
    gvc.LOOP_NUM += 1
