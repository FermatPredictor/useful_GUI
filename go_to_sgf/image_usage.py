# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
from collections import Counter

def img_to_arr(img, board_sz=19):
    """
    輸入一張圖片，回傳numpy array表示格子是黑或白或空格。
    (除非棋盤死亡線都被棋子遮擋可能失敗，不然應該判斷的出)
    """
    
    def check_color(x,y, grid_sz):
        """
        給定棋格座標與棋格大小，偵測黑棋回傳1、白棋-1、空格 0
        """
        dx, dy = grid_sz
        pat = gray_img[y-dy//2:y+dy//2, x-dx//2:x+dx//2]
        flat = [1 if e<45 else (-1 if e>220 else 0) for e in pat.flatten()]
        cnt = Counter(flat)
        if cnt[1]>dx*dy//4:
            return 1
        if cnt[-1]>dx*dy//4:
            return -1
        return 0
        
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('debug_gray.png', gray_img)

    grid_line = 31 # 圍棋棋盤的格線顏色(如果是其它軟體的棋盤，此值需重設)
    grid_y = [i for i in range(len(image)) if sum(n==grid_line for n in gray_img[i,:])>35]
    grid_x = [i for i in range(len(image)) if sum(n==grid_line for n in gray_img[:,i])>35]

    """
    根據棋盤左上、右下角推算出來的x,y格線座標
    """
    grid_x = [int(n) for n in np.linspace(min(grid_x), max(grid_x), num=board_sz)]
    grid_y = [int(n) for n in np.linspace(min(grid_y), max(grid_y), num=board_sz)]
    grid_sz = (grid_x[1]-grid_x[0], grid_y[1]-grid_y[0])
    print(f"偵測到棋盤方格大小{grid_sz}")
    
    arr = np.zeros(shape=(board_sz, board_sz))
    for i, x in enumerate(grid_x):
        for j, y in enumerate(grid_y):
            #print(i,j, check_color(x,y, grid_sz))
            color = check_color(x,y, grid_sz)
            if color==1:
                # 偵測黑棋
                arr[j][i] = 1 
                cv2.circle(img,(x,y),grid_sz[0]//4,(0,0,255),-1)
            elif color==-1:
                # 偵測白棋
                arr[j][i] = -1
                cv2.circle(img,(x,y),grid_sz[0]//4,(0,255,0),-1)
    cv2.imwrite('debug.png', img)
    return arr

def to_sgf(np_arr):
    """
    給定np_arr，將其轉換為圍棋的sgf檔
    """
    def parse(pos):
        return f"[{chr(ord('a')+pos[0])}{chr(ord('a')+pos[1])}]"
    
    ab = [] # 黑棋座標
    aw = [] # 白棋座標
    n = len(np_arr)
    for i in range(n):
        for j in range(n):
            if np_arr[i][j]==1:
                ab.append(parse((j,i)))
            elif np_arr[i][j]==-1:
                aw.append(parse((j,i)))
    res = f"(;CA[big5]SZ[19]AB{''.join(ab)}AW{''.join(aw)})"
    with open('go.sgf', 'w') as f:
        f.write(res)
    

if __name__ == '__main__':
    start = time.time()
    image = cv2.imread('go.png')
    arr = img_to_arr(image)
    to_sgf(arr)
    print(f"產生sgf時間: {time.time()-start}秒")
    #cv2.imshow('Result', image)
    #cv2.waitKey(0)