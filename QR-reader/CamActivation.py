import cv2
import pyzbar.pyzbar as pyzbar
from datetime import datetime

#width = 2592
#height = 1944


#camera.set(3,width)
#camera.set(4,height)

def decodeCam(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(gray)
    print('reading...', end='\r')
    for barcode in barcodes:
        barcodeData = barcode.data.decode()
        barcodeType = barcode.type
        print("["+str(datetime.now())+"] Type:{} | Data: {}".format(barcodeType, barcodeData))
        Check(barcodeData)
    return image

try:
 while True:
# Read current frame
  ret, frame = camera.read()
  im=decodeCam(frame)
except KeyboardInterrupt:
 print('interrupted!')
