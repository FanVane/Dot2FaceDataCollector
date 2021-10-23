"""
    这是本程序的绘制类文件。
    绘制类通过与对象类的绑定，实现draw方法，实现对控件的管理。
"""
import cv2
from globals import GlobalVarControl as gvc
import os


def load_useful_frames():
    gvc.img_background = cv2.resize(cv2.imread("./sprites/background.png"), (gvc.screen_width, gvc.screen_height))


class DrawAble(object):
    """
        这是一个接口类，每个对象类实现其中的init方法和run方法，实现不同的绘制方式。
        除了提供统一标准之外，还提供了抽象的绘图分类的可能性。
    """

    def __init__(self):
        self.drawable_dict = {}

    def add_part(self, name, drawable):
        self.drawable_dict[name] = drawable

    def modify_part(self, name, new_drawable):
        self.drawable_dict[name] = new_drawable

    def draw(self):
        for drawable in self.drawable_dict.values():
            drawable.draw()


class SimpleRectButtonDrawer(object):
    def __init__(self, button):
        """
            一个可draw的button至少要有SimpleRectButton的所有属性
        """
        self.button = button

    def draw(self):
        # 先绘制一个长方形
        if self.button.touched:
            draw_rect(self.button.rect, self.button.color_up)
        else:
            draw_rect(self.button.rect, self.button.color_down)
        # 再绘制四根线条
        point_top_left = (self.button.rect[0], self.button.rect[1])
        point_top_right = (self.button.rect[0] + self.button.rect[2], self.button.rect[1])
        point_bottom_left = (self.button.rect[0], self.button.rect[1] + self.button.rect[3])
        point_bottom_right = (self.button.rect[0] + self.button.rect[2], self.button.rect[1] + self.button.rect[3])
        draw_line(point_top_left, point_top_right)
        draw_line(point_top_left, point_bottom_left)
        draw_line(point_bottom_left, point_bottom_right)
        draw_line(point_top_right, point_bottom_right)
        # 最后绘制上面的文字
        text = self.button.text_up
        if self.button.touched:
            text = self.button.text_down
        point = (self.button.rect[0] + 0.15 * self.button.rect[2], self.button.rect[1] + 0.6 * self.button.rect[3])
        draw_text(point, text)


class MouseFollowerDrawer(object):
    def __init__(self, mouse_follower):
        self.mouse_follower = mouse_follower

    def draw(self):
        draw_circle((self.mouse_follower.x, self.mouse_follower.y), 8)


class CircleDrawer(object):
    def __init__(self, point, radius):
        self.radius = radius
        self.point = point

    def draw(self):
        draw_circle(self.point, self.radius)


class TextDrawer(object):
    def __init__(self, text, point):
        self.text = text
        self.point = point

    def draw(self):
        draw_text(self.point, self.text)


"""
    实现特殊功能的自定义绘制类
"""


class BikeMarkerDrawer(object):
    def __init__(self, bike_marker):
        self.bike_marker = bike_marker

    def draw(self):
        if self.bike_marker.state == "READY_TO_MARK" or self.bike_marker.state == "MARK_RIGHT":
            # 绘制图片，这个是基本的
            draw_image(self.bike_marker.image, self.bike_marker.base_point)

            # 有眼睛就画
            if self.bike_marker.mark_left is not None:
                draw_circle((self.bike_marker.mark_left[0] + self.bike_marker.base_point[0],
                             self.bike_marker.mark_left[1] + self.bike_marker.base_point[1]),
                            8,
                            (0, 0, 255),
                            6)
            if self.bike_marker.mark_right is not None:
                draw_circle((self.bike_marker.mark_right[0] + self.bike_marker.base_point[0],
                             self.bike_marker.mark_right[1] + self.bike_marker.base_point[1]),
                            8,
                            (0, 255, 0),
                            6)

            # 绘制信息
            text_list = [" [HELP] "]
            text_list.append("img: " + str(self.bike_marker.img_index).zfill(gvc.IMG_INDEX_LEN))
            text_list.append("[A]previous img")
            text_list.append("[D]next img")
            text_list.append("[R]first unmarked ")
            text_list.append("[E]view | edit")
            text_list.append("[S]auto next: " + ("T" if not self.bike_marker.stop_auto else "F"))
            text_list.append("[K]auto move: " + ("T" if self.bike_marker.auto_move else "F"))
            text_list.append("[M]make data: " + ("T" if self.bike_marker.making_data else "F"))
            text_list.append("[X]delete! ")
            text_list.append("[Q]quit")
            text_list.append("NEXT: " + ("LEFT" if self.bike_marker.state == "READY_TO_MARK" else "RIGHT"))
            draw_text_list((gvc.screen_width * 0.7, gvc.screen_height * 0.08), text_list, 80)

            # 绘制图片放大的部分
            if self.bike_marker.image is not None:
                try:
                    enlarge_range = self.bike_marker.img_enlarge_range

                    img_part = gvc.frame[gvc.mouse_y - enlarge_range:gvc.mouse_y + enlarge_range,
                               gvc.mouse_x - enlarge_range:gvc.mouse_x + enlarge_range]
                    enlarged_size = (self.bike_marker.img_enlarge_rect[2], self.bike_marker.img_enlarge_rect[3])

                    base_point = (self.bike_marker.img_enlarge_rect[0], self.bike_marker.img_enlarge_rect[1])
                    img_part_enlarged = cv2.resize(img_part, enlarged_size)
                    draw_image(img_part_enlarged, base_point)
                    # 绘制中间的一个点
                    draw_circle((base_point[0] + enlarged_size[0] // 2,
                                 base_point[1] + enlarged_size[1] // 2), 4, (0, 0, 255))
                except:
                    pass
        elif self.bike_marker.state == "VIEWING":
            """
                在这个模式中，我们批量绘制图形在屏幕上，便于数据管理
            """
            # 绘制脸和下方的数字
            for i in range(4):
                for j in range(5):
                    draw_point_x = gvc.screen_width * (0.18 * j + 0.05)
                    draw_point_y = gvc.screen_height * (0.22 * i + 0.08)
                    image_to_draw = self.bike_marker.view_images[5 * i + j]
                    draw_image(image_to_draw, (draw_point_x, draw_point_y))
                    draw_text((draw_point_x + image_to_draw.shape[1] * 0.3,
                               draw_point_y + image_to_draw.shape[0] * 1.2),
                              str(self.bike_marker.view_index * 20 + 5 * i + j).zfill(gvc.IMG_INDEX_LEN))


"""
    图形绘制函数
"""


def draw_rect(rect, color=gvc.COLOR_WHITE):
    rect = (int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3]))
    point_top_left = (rect[0], rect[1])
    point_bottom_right = (rect[0] + rect[2], rect[1] + rect[3])
    cv2.rectangle(gvc.frame, point_top_left, point_bottom_right, color, thickness=-1)


def draw_line(point1, point2, color=gvc.COLOR_BLACK):
    point1 = (int(point1[0]), int(point1[1]))
    point2 = (int(point2[0]), int(point2[1]))
    cv2.line(gvc.frame, point1, point2, color)


def draw_text(point, text, color=gvc.COLOR_BLACK):
    point = (int(point[0]), int(point[1]))
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(gvc.frame, text, point, font, 2, color, 8)


def draw_text_list(point, text_list, distance=20):
    point = (int(point[0]), int(point[1]))
    x = point[0]
    y = point[1]
    for text in text_list:
        draw_text((x, y), text)
        y += distance


def draw_circle(point, radius, color=gvc.COLOR_BLACK, thickness=-1):
    point = (int(point[0]), int(point[1]))
    radius = int(radius)
    cv2.circle(gvc.frame, point, radius, color, thickness)


def draw_image(image, point):
    px = int(point[0])
    py = int(point[1])
    height = image.shape[0]
    width = image.shape[1]

    # 其实是修改gvc.frame的相应部分为输入的图片
    gvc.frame[py:py + height, px:px + width] = image.copy()
