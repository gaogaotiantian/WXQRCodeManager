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
        self.assertIsNotNone(r.status_code)
        self.assertIsNotNone(r.text)

    def test_get_id0(self):
        r = requests.get(url + '/api/v1/qrcode?id=0')
        self.assertEqual(r.status_code, 404)

    def test_get_id_negative(self):
        r = requests.get(url + '/api/v1/qrcode?id=-1')
        self.assertEqual(r.status_code, 404)

    def test_get_invald_id(self):
        r = requests.get(url + '/api/v1/qrcode?id=stub')
        self.assertEqual(r.status_code, 400)

    def test_get_id_without_value(self):
        r = requests.get(url + '/api/v1/qrcode?id=')
        self.assertEqual(r.status_code, 400)

    def test_get_noId(self):
        r = requests.get(url + '/api/v1/qrcode')
        self.assertEqual(r.status_code, 400)

    def test_get_random_argument(self):
        r = requests.get(url + '/api/v1/qrcode?stub=stub')
        self.assertEqual(r.status_code, 400)

    def test_get_float(self):
        self.assertIsNotNone(requests.get(url + '/api/v1/qrcode?id=7.7').status_code)

    def test_get_id_space(self):
        r = requests.get(url + '/api/v1/qrcode?id= ')
        self.assertEqual(r.status_code, 400)


class qrcode_post(unittest.TestCase):
    def setUp(self):
        r = requests.get(url + '/')
        if r.status_code != 200:
            self.skipTest("Server Error, Could not get root page")

    def test_post_random_qr(self):
        files = {'img': open('images/test_qrcode.png','rb')}
        r = requests.post(url + '/api/v1/qrcode', files=files)
        self.assertEqual(r.status_code, 400)
        files['img'].close()

    def test_post_valid(self):
        files = {'img': open('images/myfile.jpg','rb')}
        r = requests.post(url + '/api/v1/qrcode', files=files)
        self.assertEqual(int(r.status_code/100), 2)
        files['img'].close()


class groups_get(unittest.TestCase):
    def setUp(self):
        r = requests.get(url + '/')
        if r.status_code != 200:
            self.skipTest("Server Error, Could not get root page")

    def test_search_empty(self):
        r = requests.get(url + '/api/v1/groups?keywords= ')
        self.assertEqual(r.status_code, 200)

    def test_search_no_arg(self):
        r = requests.get(url + '/api/v1/groups')
        self.assertEqual(r.status_code, 200)

    def test_search_invalid_arg(self):
        r = requests.get(url + '/api/v1/groups?keywords=')
        self.assertEqual(r.status_code, 200)

    def test_search_ucsb(self):
        r = requests.get(url + '/api/v1/groups?keywords=ucsb')
        self.assertEqual(r.status_code, 200)
        for i in r.json()['results']:
            tags = [x.lower() for x in i['tags']]
            self.assertIn('ucsb',tags)
        print()
        for i in r.json()['results']:
            self.qrget_search_result(str(i['id']))

    def test_search_cs(self):
        r = requests.get(url + '/api/v1/groups?keywords=cs')
        self.assertEqual(r.status_code, 200)
        for i in r.json()['results']:
            tags = [x.lower() for x in i['tags']]
            self.assertIn('cs', tags)
        print()
        for i in r.json()['results']:
            self.qrget_search_result(str(i['id']))

    def qrget_search_result(self,id):
        r = requests.get(url + '/api/v1/qrcode?id=' + id)
        self.assertEqual(r.status_code, 200)
        print("id" + id + " passed")


class groups_post(unittest.TestCase):
    def setUp(self):
        r = requests.get(url + '/')
        if r.status_code != 200:
            self.skipTest("Server Error, Could not get root page")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_url', type=str, nargs=1, help="Server URL to request. Usage: python3 ServerVal.py "
                                                             "http://127.0.0.1:5000")
    parser.add_argument('test_code', type=str, nargs='?', default='all')
    args = parser.parse_args()
    url = args.input_url[0]
    test_code = args.test_code
    url_dct = {"remote": "https://wxqrcodemanager.herokuapp.com"}
    if url in url_dct:
        url = url_dct[url]
    else:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
    try:
        r = requests.get(url + '/')
    except:
        print("Connection Error, Please check if server is running and check url address")
    else:
        if not test_code in ["qr_get","qr_post","groups_get","groups_post","all"]:
            print("Please enter correct test code, include: qr_get, qr_post, groups_get, groups_post")
            exit(0)
        elif test_code == "qr_get":
            suite = unittest.TestLoader().loadTestsFromTestCase(qrcode_get)
        elif test_code == "qr_post":
            suite = unittest.TestLoader().loadTestsFromTestCase(qrcode_post)
        elif test_code == "groups_get":
            suite = unittest.TestLoader().loadTestsFromTestCase(groups_get)
        elif test_code == "groups_post":
            suite = unittest.TestLoader().loadTestsFromTestCase(groups_post)
        else:
            unittest.main(verbosity=2, argv=['first-arg-is-ignored'], exit=False)
            exit(1)
        # ignore the first arg because parser, verbosity set to 2 for more test info, change to 1 for less
        unittest.TextTestRunner(verbosity=2).run(suite)
