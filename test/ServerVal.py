import unittest
import requests
import argparse


class qrcode_get(unittest.TestCase):
    def setUp(self):
        r = requests.get(url + '/')
        if r.status_code != 200:
            self.skipTest("Server Error, Could not get root page")

    def test_get_id1(self):
        r = requests.get(url + '/api/v1/qrcode?id=1')
        assert r.status_code == 200
        assert r.text

    def test_get_id0(self):
        r = requests.get(url + '/api/v1/qrcode?id=0')
        assert r.status_code == 404

    def test_get_id_negative(self):
        r = requests.get(url + '/api/v1/qrcode?id=-1')
        assert r.status_code == 404

    def test_get_invald_id(self):
        r = requests.get(url + '/api/v1/qrcode?id=stub')
        assert r.status_code == 400

    def test_get_id_without_value(self):
        r = requests.get(url + '/api/v1/qrcode?id=')
        assert r.status_code == 400

    def test_get_noId(self):
        r = requests.get(url + '/api/v1/qrcode')
        assert r.status_code == 400

    def test_get_random_argument(self):
        r = requests.get(url + '/api/v1/qrcode?stub=stub')
        assert r.status_code == 400

    def test_get_float(self):
        assert requests.get(url + '/api/v1/qrcode?id=7.7').status_code

    def test_get_id_space(self):
        r = requests.get(url + '/api/v1/qrcode?id= ')
        assert r.status_code == 400


class qrcode_post(unittest.TestCase):
    def setUp(self):
        r = requests.get(url + '/')
        if r.status_code != 200:
            self.skipTest("Server Error, Could not get root page")


class groups_get(unittest.TestCase):
    def setUp(self):
        r = requests.get(url + '/')
        if r.status_code != 200:
            self.skipTest("Server Error, Could not get root page")


class groups_post(unittest.TestCase):
    def setUp(self):
        r = requests.get(url + '/')
        if r.status_code != 200:
            self.skipTest("Server Error, Could not get root page")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_url', type=str, nargs=1, help="Server URL to request. Usage: python3 ServerVal.py "
                                                             "http://127.0.0.1:5000")
    parser.add_argument('test_code', nargs='?', default='5', help="1-5, default 5. 1 for qr_get, 2 for qr_post, 3 for "
                                                                  "groups_get, 4 for groups_post, 5 for all test")
    args = parser.parse_args()
    url = args.input_url[0]
    test_code = int(args.test_code)
    try:
        r = requests.get(url + '/')
    except:
        print("Connection Error, Please check if server is running and check url address")
    else:
        if test_code < 1 or test_code > 5:
            print("Please enter test code from 1-5, -h for help")
            exit(0)
        elif test_code == 1:
            suite = unittest.TestLoader().loadTestsFromTestCase(qrcode_get)
        elif test_code == 2:
            suite = unittest.TestLoader().loadTestsFromTestCase(qrcode_post)
        elif test_code == 3:
            suite = unittest.TestLoader().loadTestsFromTestCase(groups_get)
        elif test_code == 4:
            suite = unittest.TestLoader().loadTestsFromTestCase(groups_post)
        else:
            unittest.main(verbosity=2, argv=['first-arg-is-ignored'], exit=False)
        # ignore the first arg because parser, verbosity set to 2 for more test info, change to 1 for less
        unittest.TextTestRunner(verbosity=2).run(suite)
