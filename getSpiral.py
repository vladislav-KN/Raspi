from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

from RPi import GPIO 
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
 
hostname = 'vendingsys.azurewebsites.net'
idVending = '5'

# получение списка спиралей с товарами
def GetListSpirals(idOrder):
    r = requests.get("https://" + hostname + "/Order/Scan/" + idOrder +"/" + idVending, verify=False)
    # обработка запроса
    return r.json()

# загорается светодиод
def RotateMotor(motorNum):
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(motorNum, GPIO.OUT) 

    GPIO.output(motorNum, True) 
    sleep(5) 
    GPIO.output(motorNum, False) 
    GPIO.cleanup()
    sleep(5)

# изменение информации о заказе
def ChangeOrder(idOrder):
    r = requests.get("https://" + hostname + "/Order/ChangeOrder/" + idOrder, verify=False) 
    # обработка запроса


# open screen of the vending
options = Options()
options.binary_location = "/usr/lib/chromium-browser/chromium-browser"    #chrome binary location specified here
options.add_argument("--start-maximized") #open Browser in maximized mode
options.add_argument("--no-sandbox") #bypass OS security model
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path='/usr/bin/chromedriver')
driver.get('https://' + hostname + '/VendingWindow/' + idVending)
time.sleep(30)

# Scan QR-code
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv", help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())
#vs = VideoStream(src=0).start()  #Uncomment this if you are using Webcam
vs = VideoStream(usePiCamera=True).start() # For Pi Camera
time.sleep(2.0)
csv = open(args["output"], "w")
found = set()
 
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        
        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
        if barcodeData not in found:            
            # получаем номер спирали
            numSpirals = GetListSpirals(barcodeData)
            for numSpiral in numSpirals:
                print("{} ({})".format("NumSpiral", numSpiral))
                # item is in vending
                if(numSpiral > 0):
                    
                    if(numSpiral > 0):
                    
                        # загорается светодиод - выдача товара
                        RotateMotor(23)
                        time.sleep(15)
                    
                        # write in log
                        csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))
                        csv.flush()
                        found.add(barcodeData)
                else:
                    print("Ошибка: Заказ не найден/Спираль с заказанным товаром не найдена/Заказ уже получен")
            
            # изменяем информацию о заказе в бд
            ChangeOrder(barcodeData)
            # show context ads
            driverAds = webdriver.Chrome(options=options, executable_path='/usr/bin/chromedriver')
            driverAds.get('https://' + hostname + '/VendingWindowThanks/' + idVending + '/' + barcodeData)
            time.sleep(30)
            driverAds.quit()
            # refresh vendscreen
            driver.refresh()
        
        text = "{} ({})".format(barcodeData, barcodeType)
        print (text)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
 
        
    cv2.imshow("Barcode Reader", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the `s` key is pressed, break from the loop
    if key == ord("s"):
        break
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()