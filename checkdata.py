"""
    与其它内容独立，用于检测数据的正确性
"""

import cv2
import json
index = 0
while True:
    try:
        img = cv2.imread("datasets/" + str(index) + ".jpg")
        with open("datasets/" + str(index) + ".json", "r") as f:
            pos = json.load(f)
            # print(pos)
        x1, y1 = pos[-2]
        x2, y2 = pos[-1]

        cv2.circle(img, (x1, y1), 4, (0, 0, 255), -1)
        cv2.circle(img, (x2, y2), 4, (0, 0, 255), -1)

        cv2.imshow("test", img)
        cv2.waitKey(100)
    except FileNotFoundError:
        index = 0

    index += 1
