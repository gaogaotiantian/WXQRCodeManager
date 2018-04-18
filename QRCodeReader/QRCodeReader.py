#Fuheng Zhao 2018/4/05
import pyqrcode
from io import BytesIO
import base64
from .pyzbar.pyzbar import decode
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import numpy as np
import pytesseract

def set_tesseract_path(path):
    pytesseract.pytesseract.tesseract_cmd = path

class QRCode:
    def __init__(self, url = '', name = ''):
        self.url = url
        self.name = name

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
    def generate_image(self, qrcode_data):
        url = qrcode_data.url
        name = qrcode_data.name
        qr_code = pyqrcode.create(url)
        # scale it up so it's clear
        base64_str = qr_code.png_as_base64_str(scale=10)
        im = Image.open(BytesIO(base64.b64decode(base64_str)))
        self.add_text(im, name)
        '''
        im=im.convert('RGBA')
        data=im.getdata()
        newData=[]
        for item in data:
            if item[0] == 255 and item[1]==255 and item[2]==255:
                newData.append((255,255,255,0))
            else:
                newData.append(item)
        im.putdata(newData)
        '''
        return im


    def add_text(self, image, word):
        test = decode(image)
        if len(test) == 0:
            return None
        #get length height etc. for the qrcode image 
        position=test[0].rect
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
        left=int(position[int(coordinate[0]):int(coordinate[1])+1])
        top=int(position[int(coordinate[2]):int(coordinate[3])+1])
        width=int(position[int(coordinate[4]):int(coordinate[5])+1])
        height=int(position[int(coordinate[6]):int(coordinate[7])+1])

        image=image.convert('RGB')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.dirname(os.path.realpath(__file__)) + "/wqy-zenhei.ttc", 35)
        x=left+width/10
        y=top-width/5
        #print(x,y)
        draw.text((x,y),word,(0,0,0),font=font)
        #image.save("test.png")
        return image

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
        name = self.get_group_name(image)
        qrcode = QRCode(url = d[0].data.decode('utf-8'), name = name)

        return qrcode
    '''
    def remove_gray(img,lower_val,upper_val):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_bound = np.array([0,0,lower_val])
        upper_bound = np.array([255,255,upper_val])
        mask = cv2.inRange(gray, lower_bound, upper_bound)
        return cv2.bitwise_and(gray, gray, mask = mask)
    

        return d[0].rect
        '''
    def get_group_name(self, image):
        #image = Image.open(image)
        
        test=decode(image)
        if len(test)==0:
            return None
        position=test[0].rect

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

        left=int(position[int(coordinate[0]):int(coordinate[1])+1])
        top=int(position[int(coordinate[2]):int(coordinate[3])+1])
        width=int(position[int(coordinate[4]):int(coordinate[5])+1])
        height=int(position[int(coordinate[6]):int(coordinate[7])+1])

        im = image
        rec=(left+width/10,top-width/3,left+width,top)
        c_im=im.crop(rec)
        text=pytesseract.image_to_string(c_im,lang='chi_sim')
        return text

'''
Simple test code can he bere
'''
if __name__ == '__main__':
    reader = QRCodeReader()
    im = reader.generate_image(QRCode(url = "abc", name = "name"))
    image=reader.add_text(im,"ABC")

    assert(reader.get_qrcode_data(im).url == "abc")
    print("test passed")
    text=reader.get_group_name(image)
    print(text)
    assert(text=="ABC")
    print("add_text passed")



