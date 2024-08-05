import math
import numpy as np

def rotate_rectangle(left, top, width, height, angle):
    theta = math.radians(angle)  # 將角度轉換為弧度
    # 計算矩形中心點
    cx = left + width / 2
    cy = top + height / 2
    print("center: ", [cx, cy])
    
    # 計算矩形的四個頂點相對於中心點的坐標
    dx1, dy1 = -width / 2, -height / 2
    dx2, dy2 = width / 2, -height / 2
    dx3, dy3 = width / 2, height / 2
    dx4, dy4 = -width / 2, height / 2
    
    # 構建旋轉矩陣
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    print("R: ", R)
    T = np.array([[cx], [cy]])

    point1 = (np.dot(R, np.array([[dx1], [dy1]])) + T).tolist()
    point2 = (np.dot(R, np.array([[dx2], [dy2]])) + T).tolist()
    point3 = (np.dot(R, np.array([[dx3], [dy3]])) + T).tolist()
    point4 = (np.dot(R, np.array([[dx4], [dy4]])) + T).tolist()

    print(point1[0][0], point1[1][0])
    # 將四個頂點坐標轉換成列表形式並返回
    rotated_rectangle = [
                        [point1[0][0], point1[1][0]],
                        [point2[0][0], point2[1][0]],
                        [point3[0][0], point3[1][0]],
                        [point4[0][0], point4[1][0]]
                        ]
    
    return rotated_rectangle


# 以左上角坐標為 (2, 4)，寬度為 12，高度為 10 的矩形為例，將其逆時針旋轉 45 度
left = 2
top = 4
width = 12
height = 10
angle = 90

rotated_rectangle = rotate_rectangle(left, top, width, height, angle)
print("Rotated Rectangle Points:", rotated_rectangle)
