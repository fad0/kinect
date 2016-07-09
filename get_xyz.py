import cv2
import numpy as np
import freenect


def get_coor(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'row= ', y, '     col= ', x
        d = rawdepth[y, x]
        print 'rawdepth = ', d
        coord = y, x, d
        f.write(str(coord))
        f.write('\n')


# function to get depth image from kinect
def get_depth():
    array, _ = freenect.sync_get_depth()
    return array


f = open('row_col_depth.txt', 'w')
cv2.namedWindow('img')
cv2.setMouseCallback('img', get_coor)
while 1:
    # get a frame from depth sensor
    rawdepth = get_depth()
    depth = np.zeros((480, 640), dtype=np.int16)
    for i in range(480):
        for j in range(640):
            depth[i, j] = (rawdepth[i, j]*255)/2047
    depth = cv2.convertScaleAbs(depth)
    cv2.imshow('img', depth)
    k = cv2.waitKey()
    if k == 27:
        break

cv2.destroyAllWindows()
f.close()
