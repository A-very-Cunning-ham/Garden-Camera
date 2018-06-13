# Avery Cunningham
# Drive upload adapted from API example code found at:
# https://developers.google.com/drive/api/v3

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import picamera
import numpy as np

from signal import pause
import time
import sys

def upload(filePath): # This function accepts a file path of a saved image and uploads it to a Google Drive folder
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    FILES = (
        (filePath, None),
    )

    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    for filename, mimeType in FILES:
        metadata = {'name': filename,
    		'parents': ['1-Z-1APw7TthagDC8phmmzNYKXxw_hCtb']}
        if mimeType:
            metadata['mimeType'] = mimeType
        res = DRIVE.files().create(body=metadata, media_body=filename).execute()
        if res:
            print('Uploaded "%s" (%s)' % (filename, res['mimeType']))

def main(): # This function captures a NIR image and uploads it processed as a NDVI or raw to Google Drive using upload ()
    arg = sys.argv[1] # Determine command line arguemnts used while running this command. 

    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        #camera.awb_mode = 'off'
        #camera.awb_gains = ((1.2),(1))
        time.sleep(2)
        output = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')

    red = 0
    nir = 2

    output32 = output.astype(np.float32)

    a = (output32[:, :, nir] - output32[:, :, red])
    b = (output32[:, :, red] + output32[:, :, nir])

    ndvi = np.divide(a, b, out=np.zeros_like(a), where=b!=0)

    del a, b

    if(arg == "NDVI"):
        plt.figure(1)
        plt.imshow(ndvi, cmap = "nipy_spectral", vmin = -1, vmax = 1)
        plt.colorbar()
        save = '/home/pi/Desktop/pics/NDVI.%s.png' % (time.strftime("%Y%m%d-%H%M%S"))
        plt.savefig(save)
        plt.close()
        print("Saved NDVI")
        upload(save)
    elif(arg == "NIR"):
        plt.figure(2)
        plt.imshow(output)
        save = '/home/pi/Desktop/pics/NIR.%s.png' % (time.strftime("%Y%m%d-%H%M%S"))
        plt.savefig(save)
        plt.close()
        print("Saved RGB")
        upload(save)

if __name__== "__main__":
  main()
