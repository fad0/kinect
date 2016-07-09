import freenect

degrees_tilt = input('Input tilt in degrees: ')
degrees_tilt = int(degrees_tilt)
ctx = freenect.init()
dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)

retval = freenect.set_tilt_degs(dev, degrees_tilt)
print retval
