import json
import os
import sqlite3
import unittest
from unittest.mock import MagicMock, patch
from urllib import request

from data.gdc1a import Gdc1aPipeline

class Test_gdc1a(unittest.TestCase):
    def setUp(self):
        self.classUnderTest = Gdc1aPipeline()

    def test_system_pipeline(self):
        #arrange
        #act
        total, path = self.classUnderTest.runPipeline()
        #assert
        self.assertTrue(os.path.exists(path))
        con = sqlite3.connect(path)
        cursor = con.execute('select count(*) from cases')
        actual_total = cursor.fetchone()[0]
        self.assertEqual(total, actual_total, "The number of cases in the database {} is not the downloaded sample number {}".format(actual_total, total))
        con.close()

    @patch('urllib.request.urlopen')
    @patch('urllib.request.Request')
    def test_component_request_post(self, mock_urlopen, mock_request):
        #arrange
        expected_json = "{name='test', weather='sunny'}"
        expected_json_encoded = expected_json.encode("UTF-8")
        mock_urlopen.return_value = MagicMock()
        mock_urlopen.reason.return_value = 'OK'
        mock_urlopen.return_value.__enter__.return_value.reason = 'OK'
        mock_urlopen.read.return_value = expected_json_encoded
        mock_urlopen.return_value.__enter__.return_value.read.return_value = expected_json_encoded
        mock_request.return_value = ""
        request.Request = mock_request
        request.urlopen = mock_urlopen
        #act
        jsonResponse = self.classUnderTest.requestPost(url="testurl", data={"query": "", 'variables': ""})
        #assert
        self.assertEqual(jsonResponse, json.dumps(expected_json, indent=2))

        