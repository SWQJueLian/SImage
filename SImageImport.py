#!/usr/bin/python
# -*- coding: utf-8 -*-
# utf-8 中文编码

u'''
搜索 bmp 图像并导出，同时支持再次导入功能。

'''
import base64
import json
import pprint
import shutil
import sys

__author__ = 'GameXG'

IMG_OUT_DIR_PATH = 'img'

from glob import glob
import mmap
import struct
import os

def _import(fname = 'splash.mbn'):
    if not  os.path.isfile(fname):
        print (u'不存在文件 %s '%fname)
        return
    print(u'准备处理 %s ...'% fname)

    cDirPath = os.path.dirname(os.path.abspath(fname))

    imgOutDirPath = os.path.join("%s/%s"%(os.path.join(cDirPath,IMG_OUT_DIR_PATH),os.path.basename(fname)))

    if not os.path.isfile(os.path.join(imgOutDirPath,'info.json')):
        print(u'未找到导出记录，请先导出图片。')
        return

    with open(os.path.join(imgOutDirPath,'info.json'),'rb') as f:
        imgList = json.load(f,encoding='utf-8')

    with open(fname, "r+b") as fp:
        map = mmap.mmap(fp.fileno(), 0,access=mmap.ACCESS_WRITE)

        for img in imgList:
            imgPath = os.path.join(imgOutDirPath,img['fname'])

            # 检查图片尺寸
            if os.path.getsize(imgPath) != img['size']:
                print(u'图片大小不正确，处理终止。详细信息：\r\n预期大小：%s 字节\r\n实际大小：%s 字节\r\n图片路径：%s'%(
                    img['size'],os.path.getsize(imgPath),imgPath
                ))
                return

            # 检查镜像对应的位置是否图像
            map.seek(img['offset'])
            magic ,size = struct.unpack('<2sI',map.read(6))
            if magic != base64.decodestring(img['magic']) or size != img['size']:
                print(u'非预期的镜像，请重新到导出图像并修改！')
                return

            print(u'开始回写 %s ...'%imgPath)
            with open(imgPath,'rb') as imgfile:
                map.seek(img['offset'])
                shutil.copyfileobj(imgfile,map)
                map.flush()
            print(u'回写成功。')

    print(u'当前镜像处理完毕。\r\n')



if __name__ == '__main__':
    if len(sys.argv)>1:
        for fname in sys.argv[1:]:
            try:
                _import(fname)
            except Exception ,e:
                pprint.pprint(e)
    else:
            try:
                _import()
            except Exception ,e:
                pprint.pprint(e)
    raw_input()

