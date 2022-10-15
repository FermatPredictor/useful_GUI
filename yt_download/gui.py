# -*- coding: utf-8 -*-
import tkinter as tk
import time
import threading
import random
from pytube_usage import str_to_ytlink, download_list

class MyFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, background="red")
        self.l1 = tk.Label(self, text="輸入網址:", relief='solid', borderwidth=1)
        self.l1.pack(expand=True, fill=tk.BOTH, padx=1, pady=1)

        self.t1 = tk.Text(self, width=5)
        self.t1.pack(expand=True, fill=tk.BOTH)

        self.b1 = tk.Button(self, text="下載YT", command=self.analyse)
        self.b1.pack(expand=True, fill=tk.BOTH, pady=10)

        # self.result = tk.Label(self, text="點擊上面分析")
        # self.result.pack(expand=True, fill=tk.BOTH)

    def analyse(self):
        def work():
            self.b1["state"] = tk.DISABLED
            time.sleep(1)
            text = self.t1.get("1.0", "end")
            
            path = r'.\music'
            yt_list = str_to_ytlink(text)
            download_list(yt_list, path, True)
            
            self.b1["state"] = tk.ACTIVE
        thread = threading.Thread(target=work)
        thread.start()

if __name__=='__main__':
    window = tk.Tk()
    window.geometry("500x500+200+200")
    
    f1 = MyFrame(window)
    f1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20, pady=20)
    
    window.mainloop()