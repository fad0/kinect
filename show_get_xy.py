import cv2
import argparse
import numpy as np


def get_coor(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'x= ', x, '     y= ', y
        coord = x, y
        f.write(str(coord))


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="name of the output image")
args = vars(ap.parse_args())

f = open('coordinates_2down.txt', 'a')

cv2.namedWindow('img')
cv2.setMouseCallback('img', get_coor)
image = cv2.imread(args["image"])
#image = cv2.imread('./input/hsv_depth_image_5.png')

while (1):
    cv2.imshow('img', image)
    k = cv2.waitKey()
    if k == 27:
        break
cv2.destroyAllWindows()
f.write('\n')
f.close()