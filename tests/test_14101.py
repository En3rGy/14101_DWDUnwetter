# coding: utf8
# import struct

import unittest
import time
import json
import datetime


################################
# get the code
with open('framework_helper.py', 'r') as f1, open('../src/14101_DWD Unwetter (14101).py', 'r') as f2:
    framework_code = f1.read()
    debug_code = f2.read()

exec (framework_code + debug_code)


################################
# unit tests
class UnitTests(unittest.TestCase):

    def setUp(self):
        print("\n###setUp")
        with open("credentials.txt") as f:
            self.cred = json.load(f)

        self.logic_module = DWDUnwetter_14101_14101(0)
        self.logic_module.on_init()

        # self.tst.debug_input_value[self.tst.PIN_I_S_PW] = self.cred["PIN_I_S_PW"]

    def test_get_data(self):
        print("### test_get_data")
        self.logic_module.debug_input_value[self.logic_module.PIN_I_SCITY] = "Lörrach"
        ret = self.logic_module.get_data()
        print(ret)
        self.assertNotEqual(ret, "")

    def test_read_json(self):
        print("### test_read_json")
        json_example = open("Warnungen_Gemeinden.json", 'r+')
        self.logic_module.read_json(json_example.read())
        self.assertTrue(self.logic_module.debug_output_value[self.logic_module.PIN_O_FLEVEL] == 5)

    def test_read_json2(self):
        print("### test_read_json")
        json_example = open("Warnungen_Gemeinden_2.json", 'r+')
        self.logic_module.read_json(json_example.read())
        self.assertTrue(self.logic_module.debug_output_value[self.logic_module.PIN_O_FSTART] == 1627758000)
        self.assertFalse(self.logic_module.debug_output_value[self.logic_module.PIN_O_BACTIVE])

    def test_read_json3(self):
        print("### test_read_json3")
        json_example = open("Warnungen_Gemeinden_3.json", 'r+')
        self.logic_module.read_json(json_example.read())
        print("Level: " + str(self.logic_module.debug_output_value[self.logic_module.PIN_O_FLEVEL]))
        self.assertTrue(self.logic_module.debug_output_value[self.logic_module.PIN_O_FLEVEL] == 3)

    def test_read_json4(self):
        print("### test_read_json4")
        json_example = open("Warnungen_Gemeinden_4.json", 'r+')
        self.logic_module.read_json(json_example.read())
        print("Level: " + str(self.logic_module.debug_output_value[self.logic_module.PIN_O_FLEVEL]))
        self.assertEqual(21, self.logic_module.debug_output_value[self.logic_module.PIN_O_FLEVEL])

    def test_read_json5(self):
        print("### test_read_json5")
        json_example = open("Warnungen_Gemeinden_5.json", 'r+')
        self.logic_module.read_json(json_example.read())
        print("Level: " + str(self.logic_module.debug_output_value[self.logic_module.PIN_O_FLEVEL]))
        self.assertEqual(4, self.logic_module.debug_output_value[self.logic_module.PIN_O_FLEVEL])

    def test_time_conversion(self):
        print("### test_time_conversion")
        ts = time.time()
        utc_offset = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts)).total_seconds()

        in_time = "2021-06-28T18:17:00Z"
        out_time = self.logic_module.conv_time(in_time) - utc_offset
        res = 1624897020
        self.assertEqual(res, out_time)

    if __name__ == '__main__':
        unittest.main()

