import collections
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from tkinter import *
from tkinter.filedialog import askdirectory
Cache_dir = None
Out_dir =  None
def selectPath_in():
    global Cache_dir
    path_in_ = askdirectory()
    path_in.set(path_in_)
    Cache_dir = path_in_

def selectPath_out():
    global Out_dir
    path_out_ = askdirectory()
    path_out.set(path_out_)
    Out_dir = path_out_

"""
:音乐解码下载函数
:
:功能：从指定目录下载缓存文件，并下载解密后的MP3文件到 指定 目录下
:参数: Cache_dir   缓存文件的路径
"""
def Download_Music(Cache_dir):
    for root,dirs,files in os.walk(Cache_dir):
        for f in files:
            if f[-2:] == 'uc':
                with open(Cache_dir+"/"+f,'rb') as f1:
                    bate = bytearray(f1.read())
                    #通过缓存名称获取音乐id
                    music_id = f[:f.index('-')]
                    #通过网易云音乐的api结合音乐id获取音乐名称
                    r = requests.get('http://music.163.com/api/song/detail/?id='+music_id+'&ids=%5B'+music_id+'%5D',
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'})
                    music_name = r.text[18:r.text.index(',')]
                    for i,b in enumerate(bate):
                        bate[i] = b^0xa3
                    with open(Out_dir+'//'+music_name[1:-1]+".mp3",'wb') as f2:
                        f2.write(bate)

def start():
    Download_Music(Cache_dir)


root = Tk()
root.title("网易云音乐转码工具")
root.geometry()
path_in = StringVar()
path_out = StringVar()

Label(root,text = "缓存文件路径:").grid(row = 0, column = 0)
Entry(root, textvariable = path_in).grid(row = 0, column = 1)
Button(root, text = "路径选择", command = selectPath_in).grid(row = 0, column = 2)

Label(root,text = "音乐输出路径:").grid(row = 1, column = 0)
Entry(root, textvariable = path_out).grid(row = 1, column = 1)
Button(root, text = "路径选择", command = selectPath_out).grid(row = 1, column = 2)

Button(root,text = "开始转换",command = start).grid(row = 2, column = 1)

root.mainloop()


