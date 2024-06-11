import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import os
import numpy as np
import math

#Bu bölümde gerekli kütüphaneler içe aktarılıyor ve
#folder değişkeni ile verilerin kaydedileceği klasör belirleniyor.
#Eğer klasör yoksa, os.makedirs(folder) ile oluşturuluyor.
folder = "data/A"
if not os.path.exists(folder):
    os.makedirs(folder)


#Bu fonksiyon, verilen sınırlayıcı kutunun koordinatlarını
#YOLO formatına dönüştürür.
#bbox (x, y, w, h) olarak verilen sınırlayıcı kutuyu,
#görüntü boyutlarına göre normalize edilmiş
#(center_x, center_y, width, height) formatına çevirir.
def convert_to_yolo_format(bbox, img_width, img_height):
    x, y, w, h = bbox
    center_x = (x + w / 2) / img_width
    center_y = (y + h / 2) / img_height
    width = w / img_width
    height = h / img_height
    return (center_x, center_y, width, height)


#cv2.VideoCapture(0) ile kameradan görüntü alınır.
#HandDetector(maxHands=1) ile el tespiti için bir HandDetector nesnesi oluşturulur.
#offset, imgSize, counter ve offset_burak değişkenleri tanımlanır.
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
offset = 20
imgSize = 300
counter = 0
offset_burak=30

#Bu döngüde sürekli olarak kamera görüntüsü alınır (cap.read()).
#detector.findHands(img, draw=False) ile eller tespit edilir ve eğer el varsa,
#hand['bbox'] ile elin sınırlayıcı kutusu (x, y, w, h) alınır.
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=False)  
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        #cv2.rectangle(img, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 0), 2)
        #print(x, y, w, h)

        #imgWhite ile beyaz bir görüntü oluşturulur.
        #imgCrop ile elin bulunduğu bölge kırpılır.
        #Elin boyut oranına göre (aspectRatio) kırpılan görüntü yeniden boyutlandırılır (imgResize) ve
        #imgWhite içine ortalanarak yerleştirilir.
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        imgCropShape = imgCrop.shape
        aspectRatio = h / w
        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize

        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    #cv2.imshow ile orijinal görüntü ekranda gösterilir.
    #cv2.waitKey(1) ile klavyeden bir tuşa basılması beklenir.
    #Eğer s tuşuna basılırsa, görüntü bir dosyaya kaydedilir (cv2.imwrite).
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        timestamp = time.time()
        img_path = f'{folder}/Image_{timestamp}.jpg'
        txt_path = f'{folder}/Image_{timestamp}.txt'
        cv2.imwrite(img_path, img)

        #Görüntünün boyutları alınır (img.shape).
        #Sınırlayıcı kutu YOLO formatına dönüştürülür (convert_to_yolo_format).
        #YOLO formatındaki koordinatlar bir dosyaya yazılır (txt_path).
        #Kaydedilen görüntü ve koordinatlar konsola yazdırılır.
        img_height, img_width, _ = img.shape
        yolo_coords = convert_to_yolo_format((x-25, y-10, w+offset_burak, h+offset_burak), img_width, img_height)
        with open(txt_path, 'w') as f:
            f.write(f"0 {yolo_coords[0]} {yolo_coords[1]} {yolo_coords[2]} {yolo_coords[3]}\n")

        print(f"Image saved: {img_path}")
        print(f"Coordinates saved: {txt_path}")
        print(counter)
