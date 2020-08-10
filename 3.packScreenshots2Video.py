'''
先运行   1.video2img.py					解析badapple视频，分离出每一帧，存放在FRAMES_FOLDER文件夹下
再运行   2.img2window.py				解析上面的每一帧，并控制窗口的显示和隐藏，截图存放在OUTCOME_FOLDER文件夹下
最后运行 3.packScreenshots2Video.py		把OUTCOME_FOLDER文件夹下的几千张图片打包为新的视频

做第三步前，要装ffmpeg啊啊啊啊！
    
    作者  偶尔有点小迷糊   （这段不可以删哦）
	https://space.bilibili.com/39665558

'''

import os
import cv2
import numpy as np

#########################################
# 上面这几个轮子一定要装好，不然无法运行
# 上面这几个轮子一定要装好，不然无法运行
# 上面这几个轮子一定要装好，不然无法运行
#########################################

# 生成视频的分辨率
WIDTH = 1920
HEIGHT = 1080
        
#图片来源
OUTCOME_FOLDER = 'outcome-40x30'
filelist = os.listdir(OUTCOME_FOLDER)

#视频帧数
fps = 29.97


#生成视频的文件名
output_file = "ba-window.mp4"


# 创建文件夹(如果不存在的话)
def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
		


##########################################################################
# 入口

if __name__ == "__main__":		
    mkdir(OUTCOME_FOLDER)

    size = (WIDTH, HEIGHT) 
	
    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)

    count = 0
    for item in filelist:
        if item.endswith('.jpg'): 
        #找到路径中所有后缀名为.png的文件，可以更换为.jpg或其它
            item = OUTCOME_FOLDER + '/' +  item
            img = cv2.imread(item)
            video.write(img)
            print(count)
            count += 1

    video.release()
    cv2.destroyAllWindows()
