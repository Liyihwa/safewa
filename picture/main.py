from PIL import Image

import crypt
import logwa
import numpy as np
import exifread

def get_info(file_path):
    img=open(file_path,"rb")
    # img通过open函数打开
    tags=exifread.process_file(img)
    return tags


def get_exif(img):
    exif_data = {}
    if hasattr(img, 'getexif'):
        exif_data = img.getexif()

    return exif_data


# img是PIL的Image.open()得到的
def LSB_extract(img):
    pixels = np.array(img)
    lsb_info=(pixels&1)
    lsb_info=lsb_info.reshape(1,-1)

    return crypt.Bytes.from_string("".join(str(x) for x in list(lsb_info[:][0])))


#图片自动分析工具
def auto(filepath):
    file=crypt.Bytes.from_file(filepath)
    logwa.infof("不严格ascii: {}", (file.to_ascii_list("")))
    logwa.infof("exif以及其他信息: {}", get_info(filepath))
    logwa.infof("{::gx}", "Complete! ==============")

    return LSB_extract(Image.open(filepath))


if __name__ == '__main__':
    logwa.std_on(logwa.level_only_config())
    file=crypt.Bytes.from_file("E:\Desktop\stegano1.bmp")
    print("".join(file.to_ascii_list()))





