from PIL import Image
import glob


def ResizeImage(image_path, save_path, img_size):
    images = []
    width = int(img_size[0])
    height = int(img_size[1])
    for i in range(len(glob.glob(image_path + "/*.png"))):
        imagePath = image_path + "/" + str(i).rjust(6, "0") + ".png"
        img = Image.open(imagePath)
        type = img.format
        new_img = img.resize((width, height), Image.Resampling.LANCZOS)
        # 第二个参数：
        # Image.NEAREST ：低质量
        # Image.BILINEAR：双线性
        # Image.BICUBIC ：三次样条插值
        # Image.ANTIALIAS：高质量
        newImagePath = save_path + "/" + str(i).rjust(6, "0") + ".png"
        new_img.save(newImagePath, type)


image_path = 'interlaken_00_b_images_rectified_left'
save_path = 'interlaken_00_b_images_rectified_left/new'
img_size = [640, 480]
ResizeImage(image_path, save_path, img_size)
