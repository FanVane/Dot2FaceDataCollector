# 标注瞳孔的

import numpy as np
import cv2
import matplotlib.pyplot as plt # plt 用于显示图片
import math
import cv2
import numpy as np
import dlib
import time
import math
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("F:\EGY\eye\YDY\shape_predictor_68_face_landmarks.dat")
POINTS_NUM_LANDMARK = 68
def _largest_face(dets):
    if len(dets) == 1:
        return 0
    face_areas = [(det.right() - det.left()) * (det.bottom() - det.top()) for det in dets]
    largest_area = face_areas[0]
    largest_index = 0
    for index in range(1, len(dets)):
        if face_areas[index] > largest_area:
            largest_index = index
            largest_area = face_areas[index]
    print("largest_face index is {} in {} faces".format(largest_index, len(dets)))
    return largest_index
# 从dlib的检测结果抽取姿态估计需要的点坐标
def get_image_points_from_landmark_shape(landmark_shape):
    if landmark_shape.num_parts != POINTS_NUM_LANDMARK:
        print("ERROR:landmark_shape.num_parts-{}".format(landmark_shape.num_parts))
        return -1, None
    # 2D image points. If you change the image, you need to change vector
    image_points = [
        (landmark_shape.part(36).x, landmark_shape.part(36).y),
        (landmark_shape.part(37).x, landmark_shape.part(37).y),
        (landmark_shape.part(38).x, landmark_shape.part(38).y),
        (landmark_shape.part(39).x, landmark_shape.part(39).y),
        (landmark_shape.part(40).x, landmark_shape.part(40).y),
        (landmark_shape.part(41).x, landmark_shape.part(41).y),
        (landmark_shape.part(42).x, landmark_shape.part(42).y),
        (landmark_shape.part(43).x, landmark_shape.part(43).y),
        (landmark_shape.part(44).x, landmark_shape.part(44).y),
        (landmark_shape.part(45).x, landmark_shape.part(45).y),
        (landmark_shape.part(46).x, landmark_shape.part(46).y),
        (landmark_shape.part(47).x, landmark_shape.part(47).y)
    ]
    return 0, image_points
im = cv2.imread(r'F:\EGY\eye\YDY\212121.jpg')
size = im.shape
if size[0] > 700:
    h = size[0] / 2
    w = size[1] / 2
    im = cv2.resize(im, (int(w), int(h)), interpolation=cv2.INTER_CUBIC)
dets = detector(im, 0)
largest_index = _largest_face(dets)
face_rectangle = dets[largest_index]
cv2.rectangle(im, (face_rectangle.left(),face_rectangle.top()), (face_rectangle.right(),face_rectangle.bottom()), (0, 255, 0), 1)
landmark_shape = predictor(im, face_rectangle)
image_points=get_image_points_from_landmark_shape(landmark_shape)
# 画出12个点
# point_size = 1
# point_color = (0, 0, 255) # BGR
# thickness = 1 # 可以为 0 、4、8
# for i in range(12):
#     cv2.circle(im, image_points[1][i], point_size, point_color, thickness)
#左眼
temp=np.array([image_points[1][0],image_points[1][1],image_points[1][2],image_points[1][3],image_points[1][4],image_points[1][5]])
rect = cv2.minAreaRect(temp)
box = cv2.boxPoints(rect) # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
box = np.int0(box)
print([box])#上左 上右
mean_p1=math.ceil((max(box[:,1])-min(box[:,1]))/2)
mean_p0=math.ceil((max(box[:,0])-min(box[:,0]))/2)
shang=(min(box[:,1])-mean_p1)
xia=(max(box[:,1])+mean_p1)
zuo=(min(box[:,0])-mean_p0)
you=(max(box[:,0])+mean_p0)
roi = im[shang:xia,zuo:you]
boxx = np.array([(zuo,shang),(you,shang),(you,xia),(zuo,xia)])
print(boxx)
# 画出来
cv2.imshow("roi",roi)
# cv2.drawContours(im, [boxx], 0, (255, 0, 0), 1)



img_BGR = roi
img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)
img_GRAY = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2GRAY)
#print(img_GRAY.shape)
#print(img_RGB.shape)
img= cv2.cvtColor(img_RGB, cv2.COLOR_RGB2GRAY)


height = img.shape[0]
weight = img.shape[1]
k=math.sqrt(height*weight/100/300)
k2=math.sqrt(k)
print(k,k2)



#边缘检测
v1 = cv2.Canny(img, 100/k2, 200/k2)


#灰度求值

#重新引出
v2 = cv2.cvtColor(img_RGB, cv2.COLOR_RGB2GRAY)#

#膨胀
v2_5=cv2.erode(v2,None,iterations=math.ceil(max(2*k,3)))

#灰度平均
v2_8=cv2.equalizeHist(v2_5)

#二值化
a,v3=cv2.threshold(v2_8,30,255,cv2.THRESH_BINARY)


# v1 = cv2.Canny(v3, 100, 200)
# v3=v2
# ret = np.hstack((img,v1))
# plt.imshow(ret, cmap="gray")


circles1 = cv2.HoughCircles(v1, cv2.HOUGH_GRADIENT, 1, math.ceil(k), param1=100, param2=10, minRadius=math.ceil(min(height,weight)/10 ), maxRadius=math.ceil(max(height,weight)*20))
img_sp=v1.shape
print(img_sp)
circles = circles1[0, :, :]  # 提取为二维
circles = np.uint16(np.around(circles))  # 四舍五入，取整
best_y=0
best_x=0
best_r=0
best_va=100000
t=1
for i in circles[:]:
    # print('圆心坐标:\t', i[0], i[1],i[2])
    i0 = i[0].astype(np.int16)
    i1 = i[1].astype(np.int16)
    i2 = i[2].astype(np.int16)
    i2=math.ceil(i2)


    y_lb=max(i1-i2,1)
    y_ub=min(i1+i2+1,img_sp[0]+1)
    x_lb=max(i0-i2,1)
    x_ub=min(i0+i2+1,img_sp[1]+1)


    cec=v3[y_lb:y_ub,x_lb:x_ub]


    cec_mean = np.mean(cec)-math.sqrt(min((i2/min(height,weight))*255,255)*255)/2
    # cec_mean = np.mean(cec)

    if cec_mean < best_va:
        best_va= cec_mean
        best_y = i[1]
        best_x = i[0]
        best_r = i[2]

best_x=best_x+zuo
best_y=best_y+shang
cv2.circle(im, (best_x, best_y), 2, (255, 0, 0), 1)  # 画圆心
#右眼
temp=np.array([image_points[1][6],image_points[1][7],image_points[1][8],image_points[1][9],image_points[1][10],image_points[1][11]])
rect = cv2.minAreaRect(temp)
box = cv2.boxPoints(rect) # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
box = np.int0(box)
mean_p1=math.ceil((max(box[:,1])-min(box[:,1]))/2)
mean_p0=math.ceil((max(box[:,0])-min(box[:,0]))/2)
shang=(min(box[:,1])-mean_p1)
xia=(max(box[:,1])+mean_p1)
zuo=(min(box[:,0])-mean_p0)
you=(max(box[:,0])+mean_p0)
roi = im[shang:xia,zuo:you]
cv2.imwrite(r'C:\Users\MSI\Desktop\out1.jpg',roi)
boxx = np.array([(zuo,shang),(you,shang),(you,xia),(zuo,xia)])
# 画出来
# cv2.drawContours(im, [boxx], 0, (255, 0, 0), 1)
img_BGR = roi
img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)
img_GRAY = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2GRAY)
#print(img_GRAY.shape)
#print(img_RGB.shape)
img= cv2.cvtColor(img_RGB, cv2.COLOR_RGB2GRAY)


height = img.shape[0]
weight = img.shape[1]
k=math.sqrt(height*weight/100/300)
k2=math.sqrt(k)
print(k,k2)



#边缘检测
v1 = cv2.Canny(img, 100/k2, 200/k2)


#灰度求值

#重新引出
v2 = cv2.cvtColor(img_RGB, cv2.COLOR_RGB2GRAY)#

#膨胀
v2_5=cv2.erode(v2,None,iterations=math.ceil(max(2*k,3)))

#灰度平均
v2_8=cv2.equalizeHist(v2_5)

#二值化
a,v3=cv2.threshold(v2_8,30,255,cv2.THRESH_BINARY)


# v1 = cv2.Canny(v3, 100, 200)
# v3=v2
# ret = np.hstack((img,v1))
# plt.imshow(ret, cmap="gray")


circles1 = cv2.HoughCircles(v1, cv2.HOUGH_GRADIENT, 1, math.ceil(k), param1=100, param2=10, minRadius=math.ceil(min(height,weight)/10 ), maxRadius=math.ceil(max(height,weight)*20))
img_sp=v1.shape
print(img_sp)
circles = circles1[0, :, :]  # 提取为二维
circles = np.uint16(np.around(circles))  # 四舍五入，取整
best_y=0
best_x=0
best_r=0
best_va=100000
t=1
for i in circles[:]:
    # print('圆心坐标:\t', i[0], i[1],i[2])
    i0 = i[0].astype(np.int16)
    i1 = i[1].astype(np.int16)
    i2 = i[2].astype(np.int16)
    i2=math.ceil(i2)


    y_lb=max(i1-i2,1)
    y_ub=min(i1+i2+1,img_sp[0]+1)
    x_lb=max(i0-i2,1)
    x_ub=min(i0+i2+1,img_sp[1]+1)


    cec=v3[y_lb:y_ub,x_lb:x_ub]


    cec_mean = np.mean(cec)-math.sqrt(min((i2/min(height,weight))*255,255)*255)
    # cec_mean = np.mean(cec)

    if cec_mean < best_va:
        best_va= cec_mean
        best_y = i[1]
        best_x = i[0]
        best_r = i[2]
best_x=best_x+zuo
best_y=best_y+shang
cv2.circle(im, (best_x, best_y), 2, (255, 0, 0), 1)  # 画圆心

# plt.imshow(ret, cmap="gray")
cv2.imshow("Output", im)
# # 监听键盘上任何按键，如有案件即退出并关闭窗口
cv2.waitKey(0)
im.release()
cv2.destroyAllWindows()

