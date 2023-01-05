# -*- coding: utf-8 -*-
import os
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips

def videoConcat(videos, out_vidio):
    """
    函數功能: 將videos內的視頻首尾相接，輸出name
    ex: videoConcat(["1.mp4", "2.mp4", "3.mp4"], "out.mp4")
    NOTE: 每個影片的畫面長寬需一致
    """
    finalclip = concatenate_videoclips([VideoFileClip(v) for v in videos])
    finalclip.write_videofile(out_vidio)

def myAudioclip(in_video, out_audio):
    """
    in_video: 檔名(mp4)
    out_audio: 檔名(mp3)
    ex: myAudioclip("1.mp4", "1.mp3")
    """
    # 函數功能: 在指定路徑下，截取in_video的聲音檔，輸出out_audio
    audio_clip = AudioFileClip(in_video)
    audio_clip.write_audiofile(out_audio)

def main():
    for file in os.listdir('./'):
        root, ext = os.path.splitext(file)
        print(root, ext)
        if ext=='.mp4':
            myAudioclip(file, f"{root}.mp3")

if __name__=='__main__':
    main()

