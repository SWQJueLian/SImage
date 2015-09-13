#!/usr/bin/python
# -*- coding: utf-8 -*-
# utf-8 中文编码

u'''
搜索 bmp 图像并导出，同时支持再次导入功能。

'''

README = u'''              中兴天机(S291)开机画面(第一屏)导入、导出工具

    SImageExport 可以将刷机包内 splash.mbn 文件内保存的BMP位图导出，修改后使用配套的 SImageImport 即可重新导入到 splash.mbn 文件内达到修改开机动画的目的。

    目前 splash.mbn 内有标准开机第一屏图片及FTM模式开机图片，CM版本刷机包还有电量不足开机画面。

    具体使用方式：

        1.解压你手机当前使用的刷机包，找到 splash.mbn 文件。

        注意：一定是手机当前使用的刷机包！！！
        不同版本的 splash.mbn 都有可能不一致，刷机成砖！！

        2.将 splash.mbn 文件拖到 SImageExport 文件图标上面。

        3.SImageExport 会读取 splash.mbn 内的图片，并保存到img目录。

        4.按自己的喜好修改导出的图片。

        注意：请不要修改图片格式、大小、位深等信息，否则极有可能刷机后变砖！！

        5.将 splash.mbn文件拖到 SImageImport文件图标上面，将图片导入 mbn镜像。

        6.通过 fastboot flash splash splash.mbn 将镜像刷回手机。

    只针对 ZTE S291 splash.mbn 做过有限测试
    因硬件和系统差异，刷机有风险，请务必细心操作，所有风险自行承担

    https://github.com/SWQJueLian/SImage

    Modifed By JueLian,Based on GameXG

    fix windows can not work
'''

import base64
import json
import pprint
import shutil
import sys
import os

__author__ = 'GameXG'

IMG_OUT_DIR_PATH = 'img'

ABS_DIR = sys.argv[1]#sys.path[0]+os.path.sep+'splash.mbn'

from glob import glob
import mmap
import struct

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
    print(README)
    try:
        _import(ABS_DIR)
    except Exception ,e:
        pprint.pprint(e)
    print("input anykey to exit....")
    raw_input()


