#Fuheng Zhao 2018/4/05
import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image
from pytesseract import*
class QRC:
    def gcode(word,name):
        q=pyqrcode.create(word)
        q.png(name,scale=6)

    
    def dcode(im):
        d=decode(Image.open(im))
        print(d)

    
    #def extract(a):
   #     im = Image.open(a)
  #      text=pytesseract.image_to_string(im,lang='chi_sim')
 #       print(txt)



