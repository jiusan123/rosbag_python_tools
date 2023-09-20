import glob
import os
from PIL import Image
import numpy as np
#from ros import rosbag
#import roslib, rospy
#from cv_bridge import CvBridge


timestamp_path = 'timestamp.txt'
image_path = 'interlaken_00_b_images_rectified_left'
output_bag = 'out.bag'


def ReadTimestamp(timestamp_path):
    timestamps = []
    with open(timestamp_path, 'r') as file:
        lines = file.readlines()
    file.close()
    for line in lines:
        data = int(line.strip())
        timestamps.append(data)
    return timestamps

def ReadImage(image_path):
    images = []
    for imagePath in glob.glob(image_path + "\*.png"):
        images.append(imagePath)
    return images


def CreateBag(timestamps, images, output_bag):
    if not os.path.exists(output_bag):
        os.system(r'touch %s' % output_bag)
    # bag = rosbag.Bag(output_bag, 'w')
    for i in range(len(timestamps)):
        # stamp = rospy.rostime.Time.from_sec(float(timestamps[i]/1000000))
        image = Image.open((images[i]))
        cb = CvBridge()
        data = np.asarray(image)
        image_msg = cb.cv2_to_imgmsg(data)
        image_msg.header.stamp = stamp
        image_msg.header.frame_id = "camera"
        bag.write('camera/image', image_msg, stamp)
    bag.close()


timestamps = ReadTimestamp(timestamp_path)
images = ReadImage(image_path)
CreateBag(timestamps, images, output_bag)

