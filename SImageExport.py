#!/usr/bin/python
# -*- coding: utf-8 -*-
# utf-8 中文编码

u'''
搜索 bmp 图像并导出，同时支持再次导入功能。

'''
import base64
import json
import pprint
import sys

__author__ = 'GameXG'

IMG_OUT_DIR_PATH = 'img'

import mmap
import struct
import os

def export(fname = 'splash.mbn'):

    if not  os.path.isfile(fname):
        print (u'不存在文件 %s '%fname)
        return
    print (u'打开镜像文件：%s'%fname)

    cDirPath = os.path.dirname(os.path.abspath(fname))

    imgOutDirPath = os.path.join("%s/%s"%(os.path.join(cDirPath,IMG_OUT_DIR_PATH),os.path.basename(fname)))
    print(imgOutDirPath)

    with open(fname, "rb") as fp:
        map = mmap.mmap(fp.fileno(), 0,access=mmap.ACCESS_READ)

        if not os.path.exists(imgOutDirPath):
            os.makedirs(imgOutDirPath)

        imgList = []

        offset = -1
        while True:
            offset = map.find('BM',offset + 1)

            if offset<0:
                break

            map.seek(offset)

            magic ,size = struct.unpack('<2sI',map.read(6))
            if offset+size > map.size():
                print (u'找到错误尺寸的图片 %s ，大小 %s ，超过镜像大小，跳过。'%(offset,size))
                break
            img = {
                'magic':base64.encodestring(magic),
                'offset':offset,
                'size':size,
                'fname':"%s.bmp"%(offset)
            }

            imgFilePath = os.path.join(imgOutDirPath,img['fname'])

            print (u'找到图片 %s ，大小 %s 字节。\r\n保存到：%s'%(img['offset'],img['size'],imgFilePath))

            with open(imgFilePath,'wb') as imageFile :
                map.seek(offset)
                imageFile.write(map.read(img['size']))
                imageFile.flush()


            imgList.append(img)
    with open(os.path.join(imgOutDirPath,'info.json'),'wb') as f:
        json.dump(imgList,f,encoding='utf-8',ensure_ascii = False)
        f.flush()
    print(u'当前搜索完毕。\r\n')

if __name__ == '__main__':
    if len(sys.argv)>1:
        for fname in sys.argv[1:]:
            try:
                export(fname)
            except Exception ,e:
                pprint.pprint(e)
    else:
            try:
                export()
            except Exception ,e:
                pprint.pprint(e)
    raw_input()


