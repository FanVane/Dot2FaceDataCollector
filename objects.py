"""
    这是程序的对象类文件。
    【对象类】是程序进行逻辑处理，与用户进行逻辑交互的基本单元。
    每个对象类都维护一系列变量，并实现run方法，进行相应的设置。
"""
import os

import pyautogui

from globals import GlobalVarControl as gvc
import windows as wds
import cv2
import json


class RunAble(object):
    """
        这是一个接口，每个对象类实现其中的init方法和update方法，实现不同的状态变化。
        除了作为统一的接口标准之外，还可以直接用于抽象的类的封装。
    """

    def __init__(self):
        self.obj_dict = {}

    def add_part(self, name, update_able):
        self.obj_dict[name] = update_able

    def modify_part(self, name, new_update_able):
        self.obj_dict[name] = new_update_able

    def update(self):
        for update_able in self.obj_dict.values():
            update_able.update()


"""
    常用的默认对象类
"""


class SimpleRectButton(object):
    def __init__(self, rect, text_up, text_down=None, color_up=gvc.COLOR_BLUE, color_down=gvc.COLOR_WHITE):
        # rect是一个x y w h四元组
        self.rect = rect
        self.text_up = text_up
        self.text_down = text_down
        if text_down is None:
            self.text_down = text_up
        self.color_up = color_up
        self.color_down = color_down

        # 被触碰、被点击
        self.touched = False
        self.tapped = False

        # 点击后的反应函数
        self.tapped_response = no_response

    def update(self):
        # 被触碰
        self.touched = mouse_in_rect(self.rect)
        # 被点击
        self.tapped = mouse_in_rect(self.rect) and gvc.mouse_left_button_down
        if self.tapped:
            self.tapped_response()

    def set_tapped_response(self, response):
        self.tapped_response = response


class MouseFollower(object):
    def __init__(self):
        self.x = gvc.mouse_x
        self.y = gvc.mouse_y

    def update(self):
        self.x = gvc.mouse_x
        self.y = gvc.mouse_y


"""
    实现特殊功能的自定义对象类
"""


class BikeMarker(object):
    """
        内部属性：
            当前图片序号
            当前状态： 等待标注 标注中
            鼠标点击位置
    """

    def __init__(self):
        self.auto_move = True

        # 和图片大小、显示相关的参数
        self.target_size = (int(0.66 * gvc.screen_width), int(0.66 * gvc.screen_height))
        self.img_scale = (0, 0)

        self.img_enlarge_range = int(0.02 * gvc.screen_width)  # 图像放大的范围
        self.img_enlarge_rect = \
            (0, int(0.7 * gvc.screen_height), int(0.4 * gvc.screen_width), int(0.3 * gvc.screen_height))
        # 图像放大的比例

        self.base_point = (0, 0)
        self.state = "READY_TO_MARK"
        self.mark_left = None
        self.mark_right = None

        # 跳到最后一张已标注图片
        img_index = 0
        while os.path.exists("marked_bikes/" + (str(img_index).zfill(gvc.IMG_INDEX_LEN)) + ".jpg"):
            img_index += 1
        self.img_index = img_index - 1

        # VIEWING模式的index（5*4的表格展示）
        self.view_index = 0
        self.view_images = None

        # 加载图片
        self.view_lock = False
        self.image = cv2.imread("marked_bikes/" + (str(self.img_index).zfill(gvc.IMG_INDEX_LEN)) + ".jpg")
        if self.image is None:
            self.load_unmarked_image("unmarked_bikes/")
            if self.image is None:
                self.img_index += 1
                # 进入什么都不能干模式
                self.view_load_images()
                self.state = "VIEWING"
                self.view_lock = True
                self.load_eyes()
        else:
            self.image, self.img_scale = self.img_size_2_fit()
            self.load_eyes()
        self.key = gvc.key
        gvc.mouse_left_button_down = False

        # 是否自动下张图
        self.stop_auto = False
        # 是否爬取图片
        self.making_data = False

    def update(self):
        self.key = gvc.key
        if self.state == "READY_TO_MARK":

            if self.key == ord('a') or self.key == ord('A'):
                self.load_previous_img()

            if self.key == ord('d') or self.key == ord('D'):
                self.load_next_img()

            if self.key == ord('e') or self.key == ord('E'):
                self.key = -1
                self.view_load_images()
                self.state = "VIEWING"

            if self.key == ord('s') or self.key == ord('S'):
                self.stop_auto = not self.stop_auto

            if self.key == ord('k') or self.key == ord('K'):
                self.auto_move = not self.auto_move

            if self.key == ord('x') or self.key == ord('X'):
                # 如果存在删除这张标注过的
                if os.path.exists("marked_bikes/" + (str(self.img_index).zfill(gvc.IMG_INDEX_LEN)) + ".jpg"):
                    os.remove("marked_bikes/" + (str(self.img_index).zfill(gvc.IMG_INDEX_LEN)) + ".jpg")
                if os.path.exists("marked_bikes/" + (str(self.img_index).zfill(gvc.IMG_INDEX_LEN)) + ".txt"):
                    os.remove("marked_bikes/" + (str(self.img_index).zfill(gvc.IMG_INDEX_LEN)) + ".txt")
                # 重新加载一张新图
                self.img_index -= 1
                self.load_next_img()

            if self.key == ord('q') or self.key == ord('Q'):
                self.key = -1
                wds.goto_mainWindow()

            if self.key == ord('R') or self.key == ord('r'):
                # 去第一个未标注的数据集
                wds.goto_bikeMarkWindow()

            if self.key == ord('M') or self.key == ord('m'):
                # 收集更多的raw data（不必切换状态）
                self.making_data = not self.making_data

            # 按动鼠标标注
            if gvc.mouse_left_button_down:
                self.mark_left = (gvc.mouse_x - self.base_point[0], gvc.mouse_y - self.base_point[1])
                # 鼠标自动移动
                if self.auto_move:
                    pyautogui.moveTo(int(0.66 * gvc.screen_width) - gvc.mouse_x, gvc.mouse_y)

                gvc.mouse_left_button_down = False
                self.state = "MARK_RIGHT"


        elif self.state == "MARK_RIGHT":
            if self.key == ord('s') or self.key == ord('S'):
                self.stop_auto = not self.stop_auto

            if self.key == ord('k') or self.key == ord('K'):
                self.auto_move = not self.auto_move

            if gvc.mouse_left_button_down:
                self.mark_right = (gvc.mouse_x - self.base_point[0], gvc.mouse_y - self.base_point[1])

                # 完成一次标注，保存什么的
                cv2.imwrite(f"marked_bikes/{str(self.img_index).zfill(gvc.IMG_INDEX_LEN)}.jpg", self.image)
                with open(f"marked_bikes/{str(self.img_index).zfill(gvc.IMG_INDEX_LEN)}.txt", "w") as f:
                    json.dump((self.mark_left, self.mark_right), f)
                # 进行标注之后的事项
                if not self.stop_auto:
                    self.load_next_img()
                # 切换状态
                gvc.mouse_left_button_down = False
                # 鼠标自动移动
                if self.auto_move:
                    pyautogui.moveTo(int(0.66 * gvc.screen_width) - gvc.mouse_x, gvc.mouse_y)

                self.state = "READY_TO_MARK"


        elif self.state == "VIEWING":
            # 从数据中取得完成的图像

            if self.key == ord('a') or self.key == ord('A'):
                if self.view_index > 0:
                    self.view_index -= 1
                    self.view_load_images()

            if self.key == ord('d') or self.key == ord('D'):
                self.view_index += 1
                self.view_load_images()

            if self.key == ord('e') or self.key == ord('E'):
                self.key = -1
                if not self.view_lock:
                    self.state = "READY_TO_MARK"

            if self.key == ord('q') or self.key == ord('Q'):
                self.key = -1
                wds.goto_mainWindow()

        # 其它事件
        if self.making_data:
            pass

    def make_data(self):
        url_home = "???"

    def load_next_img(self):
        self.img_index += 1
        self.image = cv2.imread("marked_bikes/" + (str(self.img_index).zfill(gvc.IMG_INDEX_LEN)) + ".jpg")
        if self.image is None:
            # 加载未标注的图片进来
            self.load_unmarked_image("unmarked_bikes/")
            if self.image is None:  # 如果还是没加载出来
                self.img_index -= 1
                self.image = cv2.imread("marked_bikes/" + (str(self.img_index).zfill(gvc.IMG_INDEX_LEN)) + ".jpg")
        # 映射图像到合适的大小并记录scale
        self.image, self.img_scale = self.img_size_2_fit()
        self.load_eyes()

    def load_previous_img(self):
        self.img_index -= 1
        self.image = cv2.imread("marked_bikes/" + (str(self.img_index).zfill(gvc.IMG_INDEX_LEN)) + ".jpg")
        if self.image is None:
            self.img_index += 1
            self.image = cv2.imread("marked_bikes/" + (str(self.img_index).zfill(gvc.IMG_INDEX_LEN)) + ".jpg")
        self.image, self.img_scale = self.img_size_2_fit()
        self.load_eyes()

    def img_size_2_fit(self):
        """
            将图片裁剪为需要的形状，并返回图片和比例
        """
        img_scale = (self.image.shape[0] // self.target_size[0], self.image.shape[1] // self.target_size[1])
        img_resized = cv2.resize(self.image, self.target_size)
        return img_resized, img_scale

    def load_eyes(self):
        try:
            with open(f"marked_bikes/{str(self.img_index).zfill(gvc.IMG_INDEX_LEN)}.txt", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.mark_left = None
            self.mark_right = None
            return
        self.mark_left = data[0]
        self.mark_right = data[1]

    def load_unmarked_image(self, path):
        # 加载成功则删除自己，并将自己作为图片。
        for root, dirs, files in os.walk(path):
            if len(files) == 0:
                return None
            else:
                filename = os.path.join(root, files[0])
                unmarked_image = cv2.imread(filename)
                if unmarked_image is None:
                    # 打不开 直接删掉
                    continue
                else:
                    # 打开了 赋值并删掉
                    self.image = unmarked_image
                os.remove(filename)

    def view_load_images(self):
        item_width = int(0.18 * gvc.screen_width)
        item_height = int(0.18 * gvc.screen_height)
        self.view_images = []
        for index in range(self.view_index * 20, self.view_index * 20 + 20):
            # 将每个图片都格式化加载到其中
            image = cv2.imread("marked_bikes/" + (str(index).zfill(gvc.IMG_INDEX_LEN)) + ".jpg")
            if image is None:
                image = cv2.imread("sprites/background.png")
            # 读取数据
            try:
                with open(f"marked_bikes/{str(index).zfill(gvc.IMG_INDEX_LEN)}.txt", "r") as f:
                    data = json.load(f)
                    mark_left = data[0]
                    mark_right = data[1]
            except FileNotFoundError:
                mark_left = None
                mark_right = None
            # 有就画
            if mark_left is not None:
                draw_circle(image, (mark_left[0], mark_left[1]), 8, (0, 0, 255), 6)
            if mark_right is not None:
                draw_circle(image, (mark_right[0], mark_right[1]), 8, (0, 255, 0), 6)
            image = cv2.resize(image, (item_width, item_height))
            self.view_images.append(image)


"""
    事件判断函数
"""


def in_rect(point, rect):
    return (rect[0] + rect[2]) > point[0] > rect[0] and (rect[1] + rect[3]) > point[1] > rect[1]


def mouse_in_rect(rect):
    return (rect[0] + rect[2]) > gvc.mouse_x > rect[0] and (rect[1] + rect[3]) > gvc.mouse_y > rect[1]


"""
    状态更新函数（事件响应函数）
"""


def no_response():
    pass


def exit_program():
    exit()


def dot_tracer_next():
    if gvc.obj_root.obj_dict["dot_tracer"].state == "READY_TO_START":
        gvc.obj_root.obj_dict["dot_tracer"].count_down = gvc.obj_root.obj_dict["dot_tracer"].count_down_original
        gvc.obj_root.obj_dict["dot_tracer"].state = "COUNTING_DOWN"
        gvc.obj_root.obj_dict["control_button"].text_up = "WAIT"
        gvc.obj_root.obj_dict["control_button"].text_down = "WAIT"
        if gvc.obj_root.obj_dict["dot_tracer"].make_path:
            gvc.obj_root.obj_dict["dot_tracer"].path = []

    elif gvc.obj_root.obj_dict["dot_tracer"].state == "FINISHED":
        wds.goto_mainWindow()


def draw_circle(image, point, radius, color=gvc.COLOR_BLACK, thickness=-1):
    point = (int(point[0]), int(point[1]))
    radius = int(radius)
    cv2.circle(image, point, radius, color, thickness)
