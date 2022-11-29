# -*- coding: utf-8 -*-
import os
import re
from pytube import YouTube
from pytube import Playlist
import time

"""
當前版本: https://pypi.org/project/pytube/
pytube 12.1.0
"""

def download_list(yt_list, path = './', audio_only=False):
    """
    函數功能: 
    yt_list: list of YouTube
    path: 下載影片路徑，未指定則載至當前資料夾
    audio_only: 是否僅下載聲音檔
    """
    if not os.path.isdir(path):  #防呆: 如果資料夾不存在就建立
        os.mkdir(path)
    for i, yt in enumerate(yt_list):
        try:
            print(f"{i}. {yt.title}")  #顯示標題
            yt_fi = yt.streams.filter()
            loader = yt_fi.get_highest_resolution() if not audio_only else yt_fi.get_audio_only()
            ext = 'mp4' if not audio_only else 'mp3'
            name = re.sub('[:/|]','',yt.title) # 去除特殊字元
            loader.download(output_path=path, filename=f'{name}.{ext}')
        except Exception as e:
            print(f'第{i}個影片下載失敗: {e}')
        time.sleep(2) # 避免連續發太多request給線上

def url_to_ytlink(url):
    """
    將yt網址轉換為可下載的yt清單
    (sample: https://www.youtube.com/watch?v=mdSXKdnLX9I&list=PLMYdDQxtZ9cHn98uzc5V9JdaKcmrkuRSC&index=1)
    """
    return [y for y in Playlist(url).videos]

def txt_to_ytlink(file):
    """
    將檔案中的yt網址(以換行符號分隔)轉換為可下載的yt清單
    """
    with open(file) as file:
        urls = file.readlines()
    return [YouTube(line) for line in urls]

def str_to_ytlink(s):
    """
    將字串(以換行符號分隔)轉換為可下載的yt清單
    """
    urls = s.split('\n')
    return [YouTube(line) for line in urls if line]

        
if __name__ == "__main__":
    path = r'.\music'
    yt_list = txt_to_ytlink('video.txt')
    download_list(yt_list, path, True)