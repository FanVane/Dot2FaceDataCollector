"""
    这是程序的窗口配置文件，类似于前端。
    可以在这里将窗口与【对象类】，【对象类】与【绘制类】进行绑定
    本质上是对gvc中的root的增删改查。
"""
from globals import GlobalVarControl as gvc
import objects as obj
import drawers as dwr


def goto_mainWindow():
    # 对象模块初始化
    gvc.obj_root = obj.RunAble()
    # 绘制模块初始化
    gvc.draw_root = dwr.DrawAble()
    # 加入一个按钮
    mainmenu_button_start_rect = (
        0.4 * gvc.screen_width, 0.4 * gvc.screen_height, 0.2 * gvc.screen_width, 0.12 * gvc.screen_height)
    button_start = obj.SimpleRectButton(mainmenu_button_start_rect, "TEST", "WORK!")
    button_start.set_tapped_response(do_stuff)
    gvc.obj_root.add_part("button_start", button_start)
    gvc.draw_root.add_part("button_start", dwr.SimpleRectButtonDrawer(button_start))


    # 主菜单参数设置
    mainmenu_button_start_rect = (
        0.4 * gvc.screen_width, 0.4 * gvc.screen_height, 0.2 * gvc.screen_width, 0.12 * gvc.screen_height)
    mainmenu_button_exit_rect = (
        0.4 * gvc.screen_width, 0.8 * gvc.screen_height, 0.2 * gvc.screen_width, 0.12 * gvc.screen_height)

    button_start = obj.SimpleRectButton(mainmenu_button_start_rect, "TEST", "WORK!")
    button_start.set_tapped_response(goto_collectWindow)

    button_exit = obj.SimpleRectButton(mainmenu_button_exit_rect, "EXIT", "GOODBYE")
    button_exit.set_tapped_response(obj.exit_program)
    # 主菜单对象绑定到对象维护列表
    gvc.obj_root.add_part("button_start", button_start)
    gvc.obj_root.add_part("button_exit", button_exit)

    # 初始化主菜单绘制布局
    gvc.draw_root.add_part("title",
                           dwr.TextDrawer("Dot4Bike: DataCollector", (0.3 * gvc.screen_width, 0.2 * gvc.screen_height)))
    gvc.draw_root.add_part("button_start", dwr.SimpleRectButtonDrawer(button_start))
    gvc.draw_root.add_part("button_exit", dwr.SimpleRectButtonDrawer(button_exit))

    # 放置一个光标
    mouse_follower = obj.MouseFollower()
    gvc.obj_root.add_part("mouse_follower", mouse_follower)
    gvc.draw_root.add_part("mouse_follower", dwr.MouseFollowerDrawer(mouse_follower))

    # 标注按钮
    mainmenu_button_bike_mark_rect = (
        0.4 * gvc.screen_width, 0.6 * gvc.screen_height, 0.2 * gvc.screen_width, 0.12 * gvc.screen_height)
    button_bike_mark = obj.SimpleRectButton(mainmenu_button_bike_mark_rect, "MARKBIKE", "WORK!")
    button_bike_mark.set_tapped_response(goto_bikeMarkWindow)
    gvc.obj_root.add_part("button_bike_mark", button_bike_mark)
    gvc.draw_root.add_part("button_bike_mark", dwr.SimpleRectButtonDrawer(button_bike_mark))


def goto_collectWindow():
    # 对象模块初始化
    gvc.obj_root = obj.RunAble()
    # 绘制模块初始化
    gvc.draw_root = dwr.DrawAble()
    # 初始化收集界面对象
    # 收集界面参数设置
    # 放置一个光标
    mouse_follower = obj.MouseFollower()
    gvc.obj_root.add_part("mouse_follower", mouse_follower)
    gvc.draw_root.add_part("mouse_follower", dwr.MouseFollowerDrawer(mouse_follower))


def goto_bikeMarkWindow():
    # 对象模块初始化
    gvc.obj_root = obj.RunAble()
    # 绘制模块初始化
    gvc.draw_root = dwr.DrawAble()

    # 标注界面参数设置
    bike_marker = obj.BikeMarker()
    gvc.obj_root.add_part("bike_marker", bike_marker)
    gvc.draw_root.add_part("bike_marker", dwr.BikeMarkerDrawer(bike_marker))

    # 放置一个光标
    mouse_follower = obj.MouseFollower()
    gvc.obj_root.add_part("mouse_follower", mouse_follower)
    gvc.draw_root.add_part("mouse_follower", dwr.MouseFollowerDrawer(mouse_follower))

