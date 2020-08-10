'''
先运行   1.video2img.py					解析badapple视频，分离出每一帧，存放在FRAMES_FOLDER文件夹下
再运行   2.img2window.py				解析上面的每一帧，并控制窗口的显示和隐藏，截图存放在OUTCOME_FOLDER文件夹下
最后运行 3.packScreenshots2Video.py		把OUTCOME_FOLDER文件夹下的几千张图片打包为新的视频

    
    作者  偶尔有点小迷糊   （这段不可以删哦）
	https://space.bilibili.com/39665558

'''

import time
import os

import cv2
import numpy as np

#########################################
# 上面这几个轮子一定要装好，不然无法运行
# 上面这几个轮子一定要装好，不然无法运行
# 上面这几个轮子一定要装好，不然无法运行
#########################################


##########################################################################
# 变量定义

BAD_APPLE_VIDEO_PATH = './ba-source.mp4' #badapple源视频路径，没错你需要自己准备视频，我这只有代码哦

RESIZED_W = 40			# 每一帧图像要缩放为40x30分辨率
RESIZED_H = 30

FRAMES_FOLDER = 'frames-40x30'	# 把每一帧图像放在这个文件夹下

##########################################################################
# 函数定义

# 创建文件夹(如果不存在的话)
def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName) 
    
# 读入视频filename，提取每一帧，保存为jpg格式的图片(bmp处理速度快但占空间多，我试过，30多GB) 
def getVideoFrames(filename):
    cap = cv2.VideoCapture(filename)
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break;

        # 转为灰度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 调整大小
        resized = cv2.resize(gray, (RESIZED_W, RESIZED_H) )
        # 保存图片
        cv2.imwrite(FRAMES_FOLDER + "/ba-" + str(count).zfill(4) + ".jpg", resized)
		
        # log
        print(count, 'frames')		
        count += 1

    cap.release()

    
##########################################################################
# 入口

if __name__ == "__main__":
    # 创建文件夹
    mkdir(FRAMES_FOLDER)
    
    # 由源视频得到每一帧图片文件
    getVideoFrames(BAD_APPLE_VIDEO_PATH)

