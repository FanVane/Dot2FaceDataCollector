"""
    这是本程序的全局变量管理类。
    主要为程序的运行状态维护一系列变量，包括用户输入，鼠标位置等。
"""
import screeninfo


class GlobalVarControl(object):
    # 获取窗口大小
    screen_id = 0  # 屏幕id
    screen = screeninfo.get_monitors()[screen_id]  # 屏幕对象
    screen_width, screen_height = screen.width, screen.height  # 屏幕长宽

    # 设置显示窗口
    window_name = 'Dot2Face'  # 窗口名称

    # 用户原始输入
    mouse_x = 0
    mouse_y = 0
    mouse_left_button_down = False

    # 顶层对象类和绘制类
    obj_root = None
    draw_root = None

    # 循环次数计数器
    LOOP_NUM = 0

    # 加载常用图形
    img_background = None
    # 帧的显示
    frame = None

    # 加载常用颜色
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_BLUE = (238, 150, 17)

    # 摄像头参数设置
    capture = None

    # 检测键盘输入
    key = None

    # 图片名称的位数
    # [这个属性不要乱改，改的话需要写个python脚本修改整个数据集的名称！]
    IMG_INDEX_LEN = 4
