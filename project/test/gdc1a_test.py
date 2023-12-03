import os
import sqlite3
import unittest

from data.gdc1a import runPipeline

class Test_gdc1a(unittest.TestCase):
    def setUp(self):
        test = 1

    def test_pipeline(self):
        #arrange
        #act
        total, path = runPipeline()
        #assert
        self.assertTrue(os.path.exists(path))
        con = sqlite3.connect(path)
        cursor = con.execute('select count(*) from cases')
        actual_total = cursor.fetchone()[0]
        self.assertEqual(total, actual_total, "The number of cases in the database {} is not the downloaded sample number {}".format(actual_total, total))
        con.close()