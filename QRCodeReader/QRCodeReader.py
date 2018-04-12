#Fuheng Zhao 2018/4/05
import pyqrcode
from io import BytesIO
import base64
from pyzbar.pyzbar import decode
from PIL import Image
import os
import cv2
import numpy as np
import pytesseract
import argparse

class QRCode:
    def __init__(self, url = ''):
        self.url = url

class QRCodeReader:
    def __init__(self):
        pass

    '''
    Return a PIL image object for a specified URL

    args:
        url:
            a string for url to generate image
    return:
        a PIL image object
    '''
    def generate_image(self, url):
        qr_code = pyqrcode.create(url)
        # scale it up so it's clear
        base64_str = qr_code.png_as_base64_str(scale=6)
        im = Image.open(BytesIO(base64.b64decode(base64_str)))
        return im

    '''
    If any QRCode recognized, return a QRCode object, otherwise return None

    args:
        image:
            A PIL object
    return:
        A QRCode object
    '''
    def get_qrcode_data(self, image):
        d = decode(image)
        if len(d) == 0:
            return None
        qrcode = QRCode(url = d[0].data.decode('utf-8'))

        return qrcode

    def get_text(self, image_path):
        im = Image.open(image_path)
        test=decode(im)
        position=test[0].rect
        #print(test[0].rect)
        position=str(position)

        coordinate=np.zeros(8)
        count=0
        for i in range(len(position)):
            if position[i] == '=':
                coordinate[count]=i+1
                count=count+1
            elif position[i]==')':
                coordinate[count]=i-1
            elif position[i] == ',':
                coordinate[count]=i-1
                count=count+1
        #print(coordinate)
        left=int(position[int(coordinate[0]):int(coordinate[1])+1])
        top=int(position[int(coordinate[2]):int(coordinate[3])+1])
        width=int(position[int(coordinate[4]):int(coordinate[5])+1])
        height=int(position[int(coordinate[6]):int(coordinate[7])+1])

        im = Image.open(image_path)
        rec=(left+width/6,top-width/2,left+width,top)
        c_im=im.crop(rec)
        c_im.show()
        text=pytesseract.image_to_string(c_im,lang='chi_sim')
        #print(text)
        return text

'''
Simple test code can he bere
'''
if __name__ == '__main__':
    reader = QRCodeReader()
    im = reader.generate_image("abc")
    assert(reader.get_qrcode_data(im).url == "abc")
    print("test passed")
