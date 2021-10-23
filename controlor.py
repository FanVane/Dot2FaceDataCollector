"""
    这个文件是获取用户输入相关的文件。
"""
import cv2
from globals import GlobalVarControl as gvc


def get_user_input(event, x, y, flags, param):
    gvc.mouse_x = x
    gvc.mouse_y = y
    gvc.mouse_left_button_down = (event == cv2.EVENT_LBUTTONDOWN)
