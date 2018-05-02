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
    def __init__(self, url = '', name = '',date=''):
        self.url = url
        self.name = name
        self.date = date
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
        date = qrcode_data.date
        qr_code = pyqrcode.create(url)
        base64_str = qr_code.png_as_base64_str(scale=10)
        im = Image.open(BytesIO(base64.b64decode(base64_str)))
        im=im.resize((760,760))
        #760, 760 deafult for the qrcode in wechat
        img_w, img_h = im.size
        result=Image.new(mode="RGB",size=(1000,1300),color=(255,255,255))
        #1000x1300 is the default size for wechar qrcode 
        bg_w, bg_h = result.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        result.paste(im,offset)
        if(name!=''):
            result = self.add_groupname(result, name)
        if(date!=''):
            result = self.add_date(result, date)
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
        return result

    def generate_image_base64(self, qrcode_data, thumbnail = False):
        if thumbnail == True:
            url = qrcode_data.url
            name = qrcode_data.name
            date = qrcode_data.date
            qr_code = pyqrcode.create(url)
            base64_str = qr_code.png_as_base64_str(scale=2)

            return base64_str

        else:
            img = self.generate_image(qrcode_data)
            buf = BytesIO()
            img.save(buf, format='PNG')
        
            return base64.b64encode(buf.getvalue()).decode('utf-8')

    def helper_position(self,image,coordinate):
        test = decode(image)
        if len(test) == 0:
            return False
        #get length height etc. for the qrcode image 
        position=test[0].rect
        position=str(position)

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
        return True

    def get_position(self,image,coordinate):
        temp=self.helper_position(image,coordinate)
        if temp == False:
            return None
        test = decode(image)
        position=test[0].rect
        position=str(position)

        left=int(position[int(coordinate[0]):int(coordinate[1])+1])
        top=int(position[int(coordinate[2]):int(coordinate[3])+1])
        width=int(position[int(coordinate[4]):int(coordinate[5])+1])
        height=int(position[int(coordinate[6]):int(coordinate[7])+1])
        arr=[left,top,width,height]
        return arr
        
    def add_groupname(self, image, word):
        img_w, img_h = image.size
        coordinate=np.zeros(8)
        arr=self.get_position(image,coordinate)
        if arr == None:
            return None
        left=arr[0]
        top=arr[1]
        width=arr[2]
        height=arr[3]
        image=image.convert('RGB')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.dirname(os.path.realpath(__file__)) + "/wqy-zenhei.ttc", 50)

        w,h=draw.textsize(word,font=font)
        #put word in center
        x=left+width/2-w/2
        y=(top-h)/2
        draw.text((x,y),word,(0,0,0),font=font)
        return image

    def add_date(self, image, date):
        img_w, img_h = image.size
        coordinate=np.zeros(8)
        arr=self.get_position(image,coordinate)
        if arr == None:
            return None
        left=arr[0]
        top=arr[1]
        width=arr[2]
        height=arr[3]

        image=image.convert('RGB')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.dirname(os.path.realpath(__file__)) + "/wqy-zenhei.ttc", 35)

        w,h=draw.textsize(date,font=font)
        #center
        x=left+width/2-w/2
        y=img_h-(img_h-top-height)/2
        draw.text((x,y),date,(0,0,0),font=font)
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
        img_w, img_h = image.size
        coordinate=np.zeros(8)
        arr=self.get_position(image,coordinate)
        if arr == None:
            return None
        left=arr[0]
        top=arr[1]
        width=arr[2]
        height=arr[3]

        im = image
        rec=(left+0.05*width,0,left+width,top)
        c_im=im.crop(rec)
        #c_im.show()
        text=pytesseract.image_to_string(c_im,lang='chi_sim')
        return text

    def get_date(self, image_o):
        #image = Image.open(image)
        image=image_o.convert('L')
        bw = np.asarray(image).copy()
        bw[bw < 180] = 0    # Black
        bw[bw >= 180] = 255 # White
        image=Image.fromarray(bw)

        mg_w, img_h = image.size
        coordinate=np.zeros(8)
        arr=self.get_position(image,coordinate)
        if arr == None:
            return None
        left=arr[0]
        top=arr[1]
        width=arr[2]
        height=arr[3]


        im = image
        rec=(left,top+11*height/10,left+width,img_h)
        c_im=im.crop(rec)
        #c_im.show()
        text=pytesseract.image_to_string(c_im,lang='chi_sim')
        return text

'''
Simple test code can he bere
'''
if __name__ == '__main__':
    reader = QRCodeReader()
    im = reader.generate_image(QRCode(url = "abc"))
    image=reader.add_groupname(im,"ABC")
    image=reader.add_date(image,"1/2/2018")

    assert(reader.get_qrcode_data(im).url == "abc")
    print("test passed")
    text=reader.get_group_name(image)
    print(text)
    assert(text=="ABC")
    print("add_groupname passed")
    text=reader.get_date(image)
    print(text)
    assert(text=="1/2/2018")
    print("add_date passed")
