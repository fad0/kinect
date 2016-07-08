#import the necessary modules
import freenect
import cv2
import numpy as np
 
#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array2 = array.astype(np.uint8)
    return array
 
#if __name__ == "__main__":
while 1:
    #get a frame from depth sensor
    depth = get_depth()
#    depth = np.load('depth_array_4.npy')
#    print 'depth shape = ' + str(depth.shape)
#    print 'depth dtype = ' + str(depth.dtype)
    for i in range(480):
      for j in range(640):
        depth[i,j] = (depth[i,j]*255)/2047
    depth = cv2.convertScaleAbs(depth)
    cv2.imshow('Depth image',depth)
#    while(1):
#        coords = raw_input('Input x y: ')
#        print coords[0]
#        if cv2.waitKey():
#            break
    # quit program when 'esc' key is pressed
#    k = cv2.waitKey(1000) & 0xFF
    k = cv2.waitKey()
    if k == 27:
        break
cv2.destroyAllWindows()
# I am adding comments to see if things are tracked
