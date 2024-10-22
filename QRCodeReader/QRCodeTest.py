import unittest
import os
import numpy as np
from PIL import Image                           #python image library
import QRCodeReader.QRCodeReader as QR          #import QRCodeReader function

current_path = os.path.dirname(__file__)


# obtain the absolute path of current python file
def get_image_path(file_name):
    return os.path.join(current_path,"test_images",file_name)


test_image_twline_groupname_Eng_date = get_image_path("Colorfight.JPG")
test_image_groupname_with_space_Chinese_date = get_image_path("CS32.JPG")
test_name_of_pureQRCode = get_image_path("pure_qrcode.jpg")
test_name_date_5_23 = get_image_path("wx_5_23.jpeg")
#print(test_name)

class TestMethods(unittest.TestCase):

    #assertEqual(): check for an expected result -- assertEqual(a,b)
    #assertTrue() / assertFalse(): verify a condition
    #assertRaises(): to verify that a specific exceptions gets raised

    #passing -v option to test script will instruct unittest.main()
    #to enable higher value of verbosity

    #python -m unittest -v test_module

    # def setUp(self):
    #     #testing framework will automatically call for every single test we run
    #
    # def tearDown(self):
    #     .dispose()

    # @unittest.skip
    # @unittest.skipIf()
    # @unittest.skipUnless()
    # @unittest.expectedFailure() # mark the test as an expected failure.
    #                             # if the test fails when run, the test is not
    #                             # counted as failure

    #If setUp() succeeded, tearDown() will be run whether the test method succeeded or not

    test_image_twoline_groupname_EnglishDate = Image.open(test_image_twline_groupname_Eng_date)
    test_image_space_between_groupname_ChineseDate = Image.open(test_image_groupname_with_space_Chinese_date)
    test_image_pureQRCode = Image.open(test_name_of_pureQRCode)
    test_image_date_5_23 = Image.open(test_name_date_5_23)



    # test function for basic get_position
    def test_get_position_func(self):
        coordinate = np.zeros(8)    #decide shape
        reader = QR.QRCodeReader()
        result = reader.get_position(self.test_image_twoline_groupname_EnglishDate,coordinate)
        self.assertTrue(result)



    #test function for get group name
    #1. test get group name with pure code (result should be '')
    def test_get_purecode_group_name(self):
        reader = QR.QRCodeReader()
        text = reader.get_group_name(self.test_image_pureQRCode)
        # print(text)
        self.assertEqual(text,'')

    # #2. test function for get group name (with image of "CS32.JPG")
    # def test_get_group_name(self):
    #     reader = QR.QRCodeReader()
    #     text = reader.get_group_name(self.test_image_2)
    #     # print(text)
    #     self.assertEqual(text,'2018 Spring CS 32')
    #
    # #3. test function for get group name (with image of "Colorfight! UCSB AI Competition")
    # def test_get_two_line_group_name(self):
    #     reader = QR.QRCodeReader()
    #     text = reader.get_group_name(self.test_image)
    #     # print(text)
    #     self.assertEqual(text, 'Colorfight! UCSB AI Competition')




    #test function for get date
    #1. test function for with pure code
    def test_get_pureqrcode_date(self):
        reader = QR.QRCodeReader()
        date = reader.get_date(self.test_image_pureQRCode)
        self.assertEqual(date,None)

    #2. test function with "CS32.JPG"
    def test_get_date_Chinese_system(self):
        reader = QR.QRCodeReader()
        date = reader.get_date(self.test_image_space_between_groupname_ChineseDate)
        self.assertEqual(date, (5,4))

    def test_get_date_Chinese_system2(self):
        reader = QR.QRCodeReader()
        date = reader.get_date(self.test_image_date_5_23)
        self.assertEqual(date, (5,23))

    #3. test function with "Colorfight! UCSB AI Competition"
    def test_get_date_English_system(self):
        reader = QR.QRCodeReader()
        date = reader.get_date(self.test_image_twoline_groupname_EnglishDate)
        self.assertEqual(date, (5,9))


    # test function for add date function (date in tuple)
    def test_add_date_separated_by_slash(self):
        reader = QR.QRCodeReader()
        new_image = reader.generate_image(QR.QRCode(date = '5/9'))
        date = reader.get_date(new_image)
        self.assertEqual(date,(5,9))

    def test_add_date_separated_by_slash_2(self):
        reader = QR.QRCodeReader()
        new_image = reader.generate_image(QR.QRCode(date = '5/4'))
        date = reader.get_date(new_image)
        self.assertEqual(date,(5,4))



    # # test function for add group name function
    # #1. group name without space between
    # def test_add_group_name_without_space(self):
    #     reader = QR.QRCodeReader()
    #     new_image = reader.generate_image(QR.QRCode(name = 'Colorfight!'))
    #     name = reader.get_group_name(new_image)
    #     self.assertEqual(name,'Colorfight!')
    #
    # #2. group name with space between
    # def test_add_group_name_with_space(self):
    #     reader = QR.QRCodeReader()
    #     new_image = reader.generate_image(QR.QRCode(name = 'Colorfight! UCSB AI Competition'))
    #     name = reader.get_group_name(new_image)
    #     self.assertEqual(name,'Colorfight! UCSB AI Competition')

#(url,"https://weixin.qq.com/g/Adg2obWiOHYLufnG")


if __name__ == '__main__':
        unittest.main(verbosity=2)
