#Fuheng Zhao 2018/4/05
import pyqrcode
from io import BytesIO
import base64
from pyzbar.pyzbar import decode
from PIL import Image
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

'''
Simple test code can he bere
'''
if __name__ == '__main__':
    reader = QRCodeReader()
    im = reader.generate_image("abc")
    assert(reader.get_qrcode_data(im).url == "abc")
    print("test passed")
