import cv2
# import argparse
import numpy as np
import freenect


def get_coor(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'row= ', y, '     col= ', x
        d = rawdepth[y, x]
        print 'rawdepth = ', d
        coord = y, x, d
        f.write(str(coord))

# function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array2 = array.astype(np.uint8)
    return array

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#                help="name of the output image")
#args = vars(ap.parse_args())

f = open('coordinates_2down.txt', 'a')

cv2.namedWindow('img')
cv2.setMouseCallback('img', get_coor)
# image = cv2.imread(args["image"])
# image = cv2.imread('./input/hsv_depth_image_5.png')

while (1):
        #get a frame from depth sensor
    rawdepth = get_depth()
    depth = np.zeros((480,640), dtype=np.int16)
#    print 'depth shape = ' + str(depth.shape)
#    print 'depth dtype = ' + str(depth.dtype)
    for i in range(480):
      for j in range(640):
        depth[i, j] = (rawdepth[i,j]*255)/2047
    depth = cv2.convertScaleAbs(depth)
    cv2.imshow('img', depth)
    k = cv2.waitKey()
    if k == 27:
        break
cv2.destroyAllWindows()
f.write('\n')
f.close()