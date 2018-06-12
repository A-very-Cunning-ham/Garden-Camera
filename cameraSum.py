# Avery Cunningham
# NDVI Image Processing

import picamera
import numpy as np

from signal import pause
from time import sleep
import sys

def main():
	with picamera.PiCamera() as camera: # Capture the infrared picture to a numpy array
		camera.resolution = (320, 240)
		#camera.awb_mode = 'off'
		#camera.awb_gains = ((1.2),(1))
		sleep(2)
		output = np.empty((240, 320, 3), dtype=np.uint8)
		camera.capture(output, 'rgb')
		
	red = 0
	nir = 2
	
	output32 = output.astype(np.float32) # convert output to float32
	

	# NDVI = nir-red / nir+red

	a = (output32[:, :, nir] - output32[:, :, red]) # calculate numerator
	b = (output32[:, :, red] + output32[:, :, nir]) # calculate denominator
	
	ndvi = np.divide(a, b, out=np.zeros_like(a), where=b!=0) # divide, avoiding div by zero
	
	sum = np.sum(ndvi)+((320*240)/2) # calcualte ammount of healthy vegetation in scene
	sum = sum/(320*240)*100
	sum = round(sum, 2)
	sys.stdout.write("%s" % sum) # log output to stdout
	
if __name__== "__main__":
    main()
