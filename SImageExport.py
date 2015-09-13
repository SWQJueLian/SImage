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
import sys
import os

__author__ = 'GameXG'

IMG_OUT_DIR_PATH = 'img'

ABS_DIR = sys.argv[1]#sys.path[0]+os.path.sep+'splash.mbn'

import mmap
import struct

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
    print(u'当前镜像搜索完毕。\r\n')

if __name__ == '__main__':
    print(README)
    try:
        export(ABS_DIR)
    except Exception ,e:
        pprint.pprint(e)
    print("input anykey to exit....")
    raw_input()



