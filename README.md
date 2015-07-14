# SImage
image 搜索工具，目前只打算支持 ZTE s291 开机画面 splash.mbn 搜索BMP格式图片并替换。

##中兴天机(S291)开机画面(第一屏)导入、导出工具

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

    http://www.chenwang.net
    https://github.com/GameXG/SImage