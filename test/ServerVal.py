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
        assert r.json()["err_msg"] == "Cannot find the id in database"
        assert r.status_code == 404

    def test_get_id10000(self):
        r = requests.get(url + '/api/v1/qrcode?id=10000')
        assert r.json()["err_msg"] == "Cannot find the id in database"
        assert r.status_code == 404

    def test_get_invald_id(self):
        r = requests.get(url + '/api/v1/qrcode?id=stub')
        assert r.json()["err_msg"] == "You need to input a valid id"
        assert r.status_code == 400

    def test_get_id_without_value(self):
        r = requests.get(url + '/api/v1/qrcode?id=')
        assert r.json()["err_msg"] == "You need to input a valid id"
        assert r.status_code == 400

    def test_get_noId(self):
        r = requests.get(url + '/api/v1/qrcode')
        assert r.json()["err_msg"] == "You need to input a valid id"
        assert r.status_code == 400

    def test_get_random_argument(self):
        r = requests.get(url + '/api/v1/qrcode?stub=stub')
        assert r.json()["err_msg"] == "You need to input a valid id"
        assert r.status_code == 400


class qrcode_post(unittest.TestCase):

    def setUp(self):
        r = requests.get(url + '/')
        if r.status_code != 200:
            self.skipTest("Server Error, Could not get root page")


class groups(unittest.TestCase):

    def setUp(self):
        r = requests.get(url + '/')
        if r.status_code != 200:
            self.skipTest("Server Error, Could not get root page")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter Server URL')
    parser.add_argument('input_url', type=str, nargs=1, help='Server URL to request')
    args = parser.parse_args()
    url = args.input_url[0]
    try:
        r = requests.get(url + '/')
    except:
        print("Connection Error, Please check if server is running and check url address")
    else:
        # ignore the first arg because parser, verbosity set to 2 for more test info, change to 1 for less
        unittest.main(verbosity=2,argv=['first-arg-is-ignored'], exit=False)
