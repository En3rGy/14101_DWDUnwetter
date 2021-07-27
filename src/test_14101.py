# coding: UTF-8

import unittest
import datetime

##########################################################
import json
import urllib
import urllib2
import ssl
import urlparse
import time
import calendar
import threading


#########################################################

class hsl20_4:
    LOGGING_NONE = 0

    def __init__(self):
        pass

    class BaseModule:
        debug_output_value = {}
        debug_set_remanent = {}
        debug_input_value = {}

        def __init__(self, a, b):
            pass

        def _get_framework(self):
            f = hsl20_4.Framework()
            return f

        def _get_logger(self, a, b):
            return 0

        def _get_remanent(self, key):
            return 0

        def _set_remanent(self, key, val):
            self.debug_set_remanent = val

        def _set_output_value(self, pin, value):
            self.debug_output_value[int(pin)] = value
            print "# Out: " + str(value) + " @ pin " + str(pin)

        def _get_input_value(self, pin):
            if pin in self.debug_input_value:
                return self.debug_input_value[pin]
            else:
                return 0

    class Framework:
        def __init__(self):
            pass

        def _run_in_context_thread(self, a):
            pass

        def create_debug_section(self):
            d = hsl20_4.DebugHelper()
            return d

        def resolve_dns(self, a):
            if a == 'maps.dwd.de':
                return "141.38.3.18"
            else:
                return "127.0.0.1"

    class DebugHelper:
        def __init__(self):
            pass

        def set_value(self, cap, text):
            print("DEBUG value\t'" + str(cap) + "': " + str(text))

        def add_message(self, msg):
            print("Debug Msg\t" + str(msg))

        def add_exception(self, msg):
            print("EXCEPTION Msg\t" + str(msg))


#########################################################

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class DWDUnwetter_14101_14101(hsl20_4.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_4.BaseModule.__init__(self, homeserver_context, "hsl20_3_dwd")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_4.LOGGING_NONE,())
        self.PIN_I_UDATE_RATE=1
        self.PIN_I_SCITY=2
        self.PIN_O_SHEADLINE=1
        self.PIN_O_FLEVEL=2
        self.PIN_O_SDESCR=3
        self.PIN_O_SINSTR=4
        self.PIN_O_FSTART=5
        self.PIN_O_FSTOP=6
        self.PIN_O_SALLWRNSTR=7
        self.PIN_O_SLV1STR=8
        self.PIN_O_SLV2STR=9
        self.PIN_O_SLV3STR=10
        self.PIN_O_SLV4STR=11
        self.PIN_O_SPREWRNSTR=12
        self.PIN_O_SHEATWRNSTR=13
        self.PIN_O_SUVWRNSTR=14
        self.PIN_O_BACTIVE=15
        self.PIN_O_BERROR=16
        self.PIN_O_SJSON=17

    ########################################################################################################
    #### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
    ###################################################################################################!!!##

    # Warnungen vor extremem Unwetter (Stufe 4) - lila
    # Unwetterwarnungen (Stufe 3) -> rot
    # Warnungen vor markantem Wetter (Stufe 2) -> orange
    # Wetterwarnungen (Stufe 1) -> gelb
    # Vorabinformation Unwetter -> rot gestreift
    # Hitzewarnung (extrem) -> dunkles flieder -> LEvel +20
    # Hitzewarnung -> helles flieder -> Level +20
    # UV - Warnung -> rosa -> Level 20
    # Keine Warnungen -> ---


    severity = {"Vorwarnung": 1, "-": 2, "Moderate": 3, "Severe": 4, "Extreme": 5}

    def set_output_value_sbc(self, pin, val):
        if pin in self.g_out_sbc:
            if self.g_out_sbc[pin] == val:
                print ("# SBC: " + str(val) + " @ pin " + str(pin) + ", data not send!")
                return

        self._set_output_value(pin, val)
        self.g_out_sbc[pin] = val

    def get_data(self):
        url_parsed = urlparse.urlparse("https://maps.dwd.de/geoserver/dwd/wfs")
        # Use Framework to resolve the host ip adress.
        host_ip = self.FRAMEWORK.resolve_dns(url_parsed.hostname)
        # Append port if provided.
        netloc = host_ip
        if url_parsed.port is not None:
            netloc += ':%s' % url_parsed.port
        # Build URL with the host replaced by the resolved ip address.
        url_resolved = urlparse.urlunparse((url_parsed[0], netloc) + url_parsed[2:])
        # Build a SSL Context to disable certificate verification.
        response_data = ""
        city = self._get_input_value(self.PIN_I_SCITY)
        try:
            # Build a http request and overwrite host header with the original hostname.
            new_data = {'service': 'WFS',
                        'request': 'GetFeature',
                        'typeName': 'dwd:Warnungen_Gemeinden',
                        'srsName': 'EPSG:4326',
                        'outputFormat': 'application/json',
                        'cql_filter': "AREADESC='" + str(city) + "'"}

            enc_data = urllib.urlencode(new_data)
            url_resolved = url_resolved + "/?" + enc_data
            ctx = ssl._create_unverified_context()

            request = urllib2.Request(url_resolved, headers={'Host': url_parsed.hostname})
            response = urllib2.urlopen(request, context=ctx)
            response_data = response.read()

        except Exception as e:
            self.set_output_value_sbc(self.PIN_O_BERROR, True)
            self.DEBUG.add_message("14101 " + str(city) + ": " + str(e) + " for '" + url_resolved + "'")

        return response_data

    def conv_time(self, str_time):
        tz_time = time.strptime(str_time, "%Y-%m-%dT%H:%M:%SZ")  # 2021-06-28T18:17:00Z
        unix_time = calendar.timegm(tz_time)
        return unix_time

    def read_json(self, json_data):
        data = json.loads(json_data)
        self.set_output_value_sbc(self.PIN_O_SJSON, json_data)
        features_cnt = 0
        if "totalFeatures" in data:
            features_cnt = data["totalFeatures"]
            self.DEBUG.set_value("Features for " + str(self._get_input_value(self.PIN_I_SCITY)), features_cnt)
            if features_cnt == 0:
                self.DEBUG.add_message("14101 " + str(self._get_input_value(self.PIN_I_SCITY)) + ": No warn data available.")
                self.reset_outputs()
                return

        else:
            self.valid_data = False
            self.DEBUG.add_message("14101 " + str(self._get_input_value(self.PIN_I_SCITY)) + ": Could not receive warn data.")
            return

        if "features" in data:
            features_data = data["features"]
            all_warnings = self.get_all_warnings(features_data)
            self.set_output_value_sbc(self.PIN_O_SALLWRNSTR, all_warnings)

            # find worst warning
            worst_data = {}
            max_level = 0
            for i in range(0, features_cnt):
                try:
                    feature_data = features_data[i]["properties"]
                    severity = feature_data["SEVERITY"]
                    level = 0
                    if severity in self.severity:
                        level = self.severity[severity]
                    else:
                        level = -100
                    if feature_data["URGENCY"] == "Future":
                        level = 1
                    if level > max_level:
                        max_level = level
                        worst_data = feature_data

                    worst_data["LEVEL"] = level

                finally:
                    pass

            # event = worst_data["EVENT"]
            headline = worst_data["HEADLINE"]
            descr = worst_data["DESCRIPTION"]
            instruction = worst_data["INSTRUCTION"]
            start_time = worst_data["EFFECTIVE"]
            start_time = self.conv_time(start_time)
            stop_time = worst_data["EXPIRES"]
            stop_time = self.conv_time(stop_time)

            # resp_type = worst_data["RESPONSETYPE"]
            # urgency = worst_data["URGENCY"]
            # severity = worst_data["SEVERITY"]
            # certainty = worst_data["CERTAINTY"]
            level = worst_data["LEVEL"]

            # determine if warn window is active
            warning_active = self.is_warning_active(start_time, stop_time)
            if self.warning_active != warning_active:
                self.set_output_value_sbc(self.PIN_O_BACTIVE, warning_active)
                self.warning_active = warning_active

            self.set_output_value_sbc(self.PIN_O_SHEADLINE, headline.encode("ascii", "xmlcharrefreplace"))
            self.set_output_value_sbc(self.PIN_O_SDESCR, descr.encode("ascii", "xmlcharrefreplace"))
            self.set_output_value_sbc(self.PIN_O_SINSTR, instruction.encode("ascii", "xmlcharrefreplace"))
            self.set_output_value_sbc(self.PIN_O_FSTART, start_time)
            self.set_output_value_sbc(self.PIN_O_FSTOP, stop_time)
            self.set_output_value_sbc(self.PIN_O_FLEVEL, level)
            self.set_output_value_sbc(self.PIN_O_BERROR, False)
            self.set_output_value_sbc(self.PIN_O_SALLWRNSTR, all_warnings.encode("ascii", "xmlcharrefreplace"))
            self.set_output_value_sbc(self.PIN_O_BACTIVE, warning_active)

            self.set_output_value_sbc(self.PIN_O_SHEATWRNSTR, "")
            self.set_output_value_sbc(self.PIN_O_SLV1STR, "")
            self.set_output_value_sbc(self.PIN_O_SLV2STR, "")
            self.set_output_value_sbc(self.PIN_O_SLV3STR, "")
            self.set_output_value_sbc(self.PIN_O_SLV4STR, "")
            self.set_output_value_sbc(self.PIN_O_SPREWRNSTR, "")
            self.set_output_value_sbc(self.PIN_O_SUVWRNSTR, "")

            if level == 1:
                self.set_output_value_sbc(self.PIN_O_SPREWRNSTR, all_warnings.encode("ascii", "xmlcharrefreplace"))
            elif level == 2:
                self.set_output_value_sbc(self.PIN_O_SLV1STR, all_warnings.encode("ascii", "xmlcharrefreplace"))
            elif level == 3:
                self.set_output_value_sbc(self.PIN_O_SLV2STR, all_warnings.encode("ascii", "xmlcharrefreplace"))
            elif level == 4:
                self.set_output_value_sbc(self.PIN_O_SLV3STR, all_warnings.encode("ascii", "xmlcharrefreplace"))
            elif level == 5:
                self.set_output_value_sbc(self.PIN_O_SLV4STR, all_warnings.encode("ascii", "xmlcharrefreplace"))
            elif level > 20:
                self.set_output_value_sbc(self.PIN_O_SHEATWRNSTR, all_warnings.encode("ascii", "xmlcharrefreplace"))
            elif level == 20:
                self.set_output_value_sbc(self.PIN_O_SUVWRNSTR, all_warnings.encode("ascii", "xmlcharrefreplace"))

            self.valid_data = True

        else:
            self.valid_data = False


    def get_val(self, json_data, key):
        val = ""
        if key in json_data:
            val = json_data[key]
        return val

    def get_all_warnings(self, features_data):
        msg = ""
        for i in range(0, len(features_data)):
            feature_data = features_data[i]["properties"]
            msg += self.get_val(feature_data, "EVENT")
            if i < len(features_data) - 1:
                msg += ", "

        return msg

    # determine if warn window is active
    # time is provided as us but function demands s
    # "start":1578765600 000,"end":1578823200 000
    def is_warning_active(self, start, end):
        current_time = time.localtime()
        end_time = time.localtime(end / 1000)
        start_time = time.localtime(start / 1000)
        return (current_time > start_time) and (current_time < end_time)

    def reset_outputs(self):
        self.DEBUG.add_message("14101 " + str(self._get_input_value(self.PIN_I_SCITY)) + ": Delete warn data.")
        self.valid_data = False
        self.set_output_value_sbc(self.PIN_O_SHEADLINE, "")
        self.set_output_value_sbc(self.PIN_O_SDESCR, "")
        self.set_output_value_sbc(self.PIN_O_SINSTR, "")
        self.set_output_value_sbc(self.PIN_O_FSTART, 0)
        self.set_output_value_sbc(self.PIN_O_FSTOP, 0)
        self.set_output_value_sbc(self.PIN_O_FLEVEL, 0)
        self.set_output_value_sbc(self.PIN_O_BACTIVE, False)
        self.set_output_value_sbc(self.PIN_O_BERROR, False)
        self.set_output_value_sbc(self.PIN_O_SHEATWRNSTR, "")
        self.set_output_value_sbc(self.PIN_O_SLV1STR, "")
        self.set_output_value_sbc(self.PIN_O_SLV2STR, "")
        self.set_output_value_sbc(self.PIN_O_SLV3STR, "")
        self.set_output_value_sbc(self.PIN_O_SLV4STR, "")
        self.set_output_value_sbc(self.PIN_O_SPREWRNSTR, "")
        self.set_output_value_sbc(self.PIN_O_SUVWRNSTR, "")
        self.set_output_value_sbc(self.PIN_O_SALLWRNSTR, "")

    def update(self):
        interval = self._get_input_value(self.PIN_I_UDATE_RATE)
        if interval <= 0:
            return

        try:
            self.DEBUG.add_message("14101 " + str(self._get_input_value(self.PIN_I_SCITY)) + ": Requesting DWD data.")
            data = self.get_data()
            self.read_json(data)
        finally:
            threading.Timer(interval, self.update).start()

    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()
        self.g_out_sbc = {}
        self.valid_data = False
        self.warning_active = False

        self.update()

    def on_input_value(self, index, value):
        city = str(self._get_input_value(self.PIN_I_SCITY))

        # get json date if triggered
        if (index == self.PIN_I_UDATE_RATE) and value > 0:
            self.update()

################################################################################


class TestSequenceFunctions(unittest.TestCase):
    tst = DWDUnwetter_14101_14101(0)

    def setUp(self):
        print("\n###setUp")
        with open("credentials.txt") as f:
            self.cred = json.load(f)

        self.tst = DWDUnwetter_14101_14101(0)
        self.tst.on_init()

        # self.tst.debug_input_value[self.tst.PIN_I_S_PW] = self.cred["PIN_I_S_PW"]

    def test_get_data(self):
        print("### test_get_data")
        self.tst.debug_input_value[self.tst.PIN_I_SCITY] = "Stuttgart"
        ret = self.tst.get_data()
        print(ret)
        self.assertNotEqual(ret, "")

    def test_read_json(self):
        print("### test_read_json")
        json_example = open("Warnungen_Gemeinden.json", 'r+')
        self.tst.read_json(json_example.read())
        self.assertTrue(True)

    def test_time_conversion(self):
        print("### test_time_conversion")
        ts = time.time()
        utc_offset = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts)).total_seconds()

        in_time = "2021-06-28T18:17:00Z"
        out_time = self.tst.conv_time(in_time) - utc_offset
        res = 1624897020
        self.assertEqual(res, out_time)

if __name__ == '__main__':
    unittest.main()
