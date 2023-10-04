import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import argparse
import sys
import os
# matplotlib inline

def arg_parse(argv):
    parser = argparse.ArgumentParser(description="VVC CU Partition Visualization")
    parser.add_argument(
        "-seq",
        "--seq",
        default="BasketBallPass",
        help="which seq you want to run",
        required = True,
    )
    parser.add_argument(
        "-QP",
        "--QP",
        default="QP32",
        help="which QP you want to run",
    )
    parser.add_argument(
        "-skip",
        "--skip",
        default=16,
        type = int,
        help="How many frame you set to skip ",
    )
    parser.add_argument(
        "-num",
        "--num",
        default=1,
        type = int,
        help="How many frame you want to implement ",
    )
    parser.add_argument(
        "--save", type=bool, default=True, help="Save result,default: True"
    )
    args = parser.parse_args(argv)
    return args

def frame_processing(filename,idx = 0,skip = 1):
    idx+=skip
    if idx<10:
        idx = "00"+str(idx)
    elif(idx>=10 and idx<100):
        idx = "0"+str(idx)
    else:
        idx = str(idx)
    img = cv2.imread('/workspace/SSD/'+filename+"/im"+idx+".png",cv2.IMREAD_GRAYSCALE)
    img = np.asarray(img)
    return img

def frame_padding(frame,CTU_size = 128):
    width , height = frame.shape[1],frame.shape[0]
    # print(width,height)
    width_CTU_nums = math.ceil(width/128)
    height_CTU_nums = math.ceil(height/128)
    # print(width_CTU_nums,width_CTU_nums)
    pad_frame = np.zeros((height_CTU_nums*128,width_CTU_nums*128))
    # print(pad_frame.shape)
    for x in range(height):
        for y in range(width):
            pad_frame[x][y] = frame[x][y]
    return pad_frame

def frame_partition(test_seq,unit , img , QP = "QP" , currframe = 0,save = False,idx = 1):
    frame_width , frame_height = img.shape[1],img.shape[0]
    CTU_NUM = math.ceil(frame_width/128) * math.ceil(frame_height/128)
    frame_partition = np.zeros((frame_height,frame_width))
    begin = currframe * CTU_NUM
    for i in range(begin,CTU_NUM+begin):
        f = open(test_seq+'/frame'+str(idx+1)+'/'+unit+'_%d.txt'%(i+1), "r")
        for line in f:
            row = line.split(" ")
            startx , starty , height , width = int(row[0]) , int(row[1]) , int(row[2]) , int(row[3])
            if startx == 0 and starty==0 and height == 0 and width == 0:
                continue
            cv2.rectangle(img,(startx,starty),(startx+width,starty+height),(255,0,0),1,cv2.LINE_AA)
    if(save):
        if idx<10:
            idx = "00"+str(idx)
        elif(idx>=10 and idx<100):
            idx = "0"+str(idx)
        else:
            idx = str(idx)
        temp_dir = test_seq+'/_result'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        cv2.imwrite(temp_dir+'/'+unit+idx+".png",img)
    plt.show()
def main(argv):
    args = arg_parse(argv)
    # seq_name = "BasketBallPass"
    # QP = "QP32"
    # Frame_Skip = 16
    # Frame_Implement = 2
    # Save_result = True
    for i in range(args.num):
        img = frame_processing(args.seq,i,args.skip)
        print("input image size :",img.shape)
        img_padding = frame_padding(img)
        frame_partition(args.seq,"CTU",img,args.QP,currframe = 0,save = args.save,idx = i)
        
if __name__ == "__main__":
    main(sys.argv[1:])   
    

