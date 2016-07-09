# *********************************************#
# check_path_fast.py                           #
# Author: FAD0                                 #
# Date  : 20160709                             #
# *********************************************#

# import the necessary modules
import freenect
import cv2
import numpy as np


# import sys


# function to get RGB image from kinect
def get_video():
    array, _ = freenect.sync_get_video()
    array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    return array


# function to get depth image from kinect
def get_depth():
    array, _ = freenect.sync_get_depth()
    #    array = array.astype(np.uint8)
    return array


# Read in the calibrator file
# Rows represent distance from kinect
# disparity (floor disparity) is actual output of kinect depth sensor
# left and right columns represent the width of 16 inches
# Row, disparity, left column, right column
# Rows are measured at from 2 to 10 feet in 1 foot increments
inputs = np.zeros((9, 4), dtype=np.int16)
my_file = open("./input/calibrator.csv", "r")
next(my_file)
j = 0
for line in my_file:
    l = [i.strip() for i in line.split(',')]
    l = map(int, l)
    inputs[j, ] = np.asarray(l, dtype=np.int16)
    j += 1
my_file.close()

# Disparity variance for any given distance
dis_variance = 15

# Image size in pixel row and column
rows = 480
columns = 640
center = columns / 2

# 16" Box half width in pixels at 2 and 10 feet
half_width_near = (inputs[0, 3] - inputs[0, 2]) / 2
half_width_far = (inputs[8, 3] - inputs[8, 2]) / 2
half_width_4 = (inputs[2, 3] - inputs[2, 2]) / 2
half_width_6 = (inputs[4, 3] - inputs[4, 2]) / 2

# Line endpoints for left and right side that represents a 16" corridor
left_near = center - half_width_near
left_far = center - half_width_far
left_4 = center - half_width_4
left_6 = center - half_width_6
right_near = center + half_width_near
right_far = center + half_width_far
right_4 = center + half_width_4
right_6 = center + half_width_6
row_near = inputs[0, 0]
row_far = inputs[8, 0]
row_4 = inputs[2, 0]
row_6 = inputs[4, 0]

# calculate left and right column as a function of row
# assume linear -> y = mx + b
# column = m(row) + b, m = (y2-y1)/(x2-x1), b = y - mx
m_left = 1.0 * (left_near - left_far) / (inputs[0, 0] - inputs[8, 0])
b_left = left_near - m_left * inputs[0, 0]
print 'm_left = ', m_left
print 'b_left = ', b_left
m_right = 1.0 * (right_near - right_far) / (inputs[0, 0] - inputs[8, 0])
b_right = right_near - m_right * inputs[0, 0]
print 'm_right = ', m_right
print 'b_right = ', b_right

# Calculate Disparity as function of row
# assume linear -> y = mx + b
m_dis = 1.0 * (inputs[0, 1] - inputs[1, 1]) / (inputs[0, 0] - inputs[1, 0])
b_dis = inputs[0, 1] - m_dis * inputs[0, 0]

print 'm_dis = ', m_dis
print 'b_dis = ', b_dis

# sys.exit()

depth = np.zeros([480, 640])
while 1:
    # get a frame from depth sensor
    rawdepth = get_depth()
    #    print 'rawdepth shape = ' + str(rawdepth.shape)
    #    print 'rawdepth dtype = ' + str(rawdepth.dtype)
    for i in range(row_6, 480):
        for j in range(left_near, right_near):
            col_left = int(m_left * i + b_left)
            col_right = int(m_right * i + b_right)
            if j in range(col_left, col_right):
                floor_dis = int(m_dis * i + b_dis) - dis_variance
                if rawdepth[i, j] < floor_dis:
                    depth[i, j] = 0
                else:
                    depth[i, j] = 2047
            else:
                depth[i, j] = rawdepth[i, j]
        else:
            depth[i, j] = rawdepth[i, j]

    depth = cv2.convertScaleAbs(depth)

    ######################################################################
    #   Add the scaled boundary markers

    # Draw a diagonal bounding lines
    cv2.line(depth, (left_near, row_near), (left_far, row_far), (0, 0, 0), 2)

    cv2.line(depth, (right_near, row_near), (right_far, row_far), (0, 0, 0), 2)

    # Draw distance markers
    # 2 feet
    cv2.line(depth, (left_near, row_near), (right_near, row_near), (0, 0, 0), 2)
    cv2.line(depth, (left_4, row_4), (right_4, row_4), (0, 0, 0), 2)
    cv2.line(depth, (left_6, row_6), (right_6, row_6), (0, 0, 0), 2)

    # Add text to right most distance markers
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(depth, "2'", (center, row_near - 5), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(depth, "4'", (center, row_4 - 5), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(depth, "6'", (center, row_6 - 5), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    cv2.imshow('Depth image', depth)
    # quit program when 'esc' key is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
