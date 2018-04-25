import unittest
import os

from PIL import Image

import QRCodeReader.QRCodeReader as QR

img_folder = os.path.dirname(__file__)

def get_img_path(filename):
    return os.path.join(img_folder, "test_images", filename)

class QRCodeRead(unittest.TestCase):

    def test_pure(self):
        im = Image.open(get_img_path("pure_qrcode.jpg"))
        reader = QR.QRCodeReader()
        data = reader.get_qrcode_data(im)
        url = data.url
        self.assertEqual(url, "https://weixin.qq.com/g/A10Tsm5HwB87ITpB")

class QRCodeBasic(unittest.TestCase):

    def test_read_and_write(self):
        reader = QR.QRCodeReader()
        im = reader.generate_image(QR.QRCode(url = "abc"))
        url = reader.get_qrcode_data(im).url
        self.assertEqual(url, "abc");

if __name__ == '__main__':
    unittest.main(verbosity = 2)
