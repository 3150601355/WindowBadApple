'''
先运行   1.video2img.py					解析badapple视频，分离出每一帧，存放在FRAMES_FOLDER文件夹下
再运行   2.img2window.py				解析上面的每一帧，并控制窗口的显示和隐藏，截图存放在OUTCOME_FOLDER文件夹下
最后运行 3.packScreenshots2Video.py		把OUTCOME_FOLDER文件夹下的几千张图片打包为新的视频

    
    作者  偶尔有点小迷糊   （这段不可以删哦）
	https://space.bilibili.com/39665558

'''

import math
import time
import os

import cv2
import numpy as np
from PIL import Image,ImageGrab
import win32gui,win32api,win32con

#########################################
# 上面这几个轮子一定要装好，不然无法运行
# 上面这几个轮子一定要装好，不然无法运行
# 上面这几个轮子一定要装好，不然无法运行
#########################################


##########################################################################
# 变量定义

DEBUG_MODE = False

FRAMES_FOLDER = "frames-40x30"
OUTCOME_FOLDER = "outcome-40x30"

FRAMES_COUNT = 6502 # FRAMES_FOLDER里面图片的数量，哪位有空改进一下自动获取，我就偷个懒:)

# 不含系统菜单（SYSTEM MENU）的窗口的最小宽度和高度（win10默认设置）
PW = 32
PH =30

# 生成窗口方阵的分辨率
ResX = 40
ResY = 30

# 物理显示器分辨率
DISPLAY_W = 1920
DISPLAY_H = 1080

# 生成图像的区域
if  DEBUG_MODE:
    SCREEN_W = 32
    SCREEN_H = 30

    VIDEO_OFFSET_X = 0
    VIDEO_OFFSET_Y = 0    
else:
    SCREEN_W = ResX * PW # 窗口方阵的宽度（每个窗口宽32像素，横向共40个窗口）
    SCREEN_H = ResY * PH # 30*30=900

    VIDEO_OFFSET_X = int( (DISPLAY_W - SCREEN_W) / 2 )  #挪一挪，放屏幕中间好看点
    VIDEO_OFFSET_Y = int( (DISPLAY_H - SCREEN_H) / 2 )  #    


# 窗口句柄矩阵
hWndArray = [  [0]*ResX  for row in range(ResY)] 

# 窗口可见性矩阵（缓存，提高效率用）
# 值=1为可见，0为不可见
visibleArray = [  [1]*ResX  for row in range(ResY) ]  

##########################################################################
# 函数定义

# 根据img中每个点的像素值，显示或隐藏对应位置的窗口
#       为提高效率使用了visibleArray[][]来记录每个窗口的可见性
def showImgByNotepad(img):
    img = img.convert('L')
    pixels = img.load()
    
    for w in range(img.width):
        for h in range(img.height):
            if pixels[w, h] > 100:
                # 认为是白色，显示对应位置的窗口
                if visibleArray[h][w] == 0:
                    win32gui.ShowWindow(hWndArray[h][w ], win32con.SW_SHOW)
                    visibleArray[h][w]  = 1
            else:
                # 认为是黑色，要把对应的窗口隐藏。
                if visibleArray[h][w] == 1:
                    win32gui.ShowWindow(hWndArray[h][w ], win32con.SW_HIDE)
                    visibleArray[h][w]  = 0    


# x,y 为用户坐标，和矩阵系数不相同，但有对应关系
# show就是隐藏对应的窗口，把桌面背景show出来
def showPixel(x, y):
    win32gui.ShowWindow(hWndArray[y][x ], win32con.SW_HIDE)


# 批量创建进程，并将进程主窗口句柄放在hWndArray[][]中
def createWindows():
    global hWndArray
    
    for x in range(ResX):
        for y in range(ResY):
                hWnd = createNotepad(x * ResX + y)
                hWndArray[y][x] = hWnd
                resizeAndMove(hWnd, x, y)#y


# 调整窗口大小和位置，让它们排队站好        
def resizeAndMove(hWnd, x, y):
    win32gui.MoveWindow(hWnd, x*PW - 8 + VIDEO_OFFSET_X, y*PH + VIDEO_OFFSET_Y, PW, PH, win32con.TRUE )# -8：位置微调


# 创建单个进程    
def createNotepad(index):
    # 创建单个进程 
    hInstance = win32api.ShellExecute(0, 'open', 'vbpad.exe', '', '', 1)

    # 创建速度不能太快，否则系统响应不及，就出错了
	# 当然这取决于你机器的配置，很好的配置可以把参数调小些
	# 我这个是9600K + 16G内存 + SSD
    if index < 1000:
        win32api.Sleep(100)
    else:
        win32api.Sleep(250)
        
    hWnd = win32gui.GetForegroundWindow()
    return hWnd


# 截图
# 参数是左上角和右下角坐标点的屏幕坐标
# 返回彩色cv2格式的图片。其实用灰度会比彩色图片快一些
def takeScreenshot(left, top, right, bottom):
    img = ImageGrab.grab(bbox=(left, top, right, bottom))
    img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
    return img

	
# 创建文件夹(如果不存在的话)
def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName) 
		
		
# 由bmp图像对窗口进行排列
def bmp2notepad():
    count = 0
    while(count <= FRAMES_COUNT):
        # 加载opencv处理后的图片
        img = Image.open(FRAMES_FOLDER + "/ba-" + str(count).zfill(4) + ".jpg")
        # 根据图片内容控制窗口矩阵的显示和隐藏
        showImgByNotepad(img)
        # 把窗口组成的图像截屏存储
        capImage = takeScreenshot(0, 0, DISPLAY_W, DISPLAY_H)
        cv2.imwrite(OUTCOME_FOLDER + "/ba-" + str(count).zfill(4) + ".jpg", capImage)

        # log
        print(time.asctime( time.localtime(time.time()) ), '\t\t', count, '/', FRAMES_COUNT, 'frames')
        count += 1


##########################################################################
# 程序入口

if __name__ == "__main__":
    # 创建文件夹
    mkdir(OUTCOME_FOLDER)
	
    # 创建多个窗口并初始化
    createWindows()

    # 由bmp图像对窗口进行排列
    bmp2notepad()
