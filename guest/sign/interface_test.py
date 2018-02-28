#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" a test module """

__author__ = 'YF'

import requests
import unittest


class GetEventListTest(unittest.TestCase):
    "查询发布会接口测试"

    def setUp(self):
        self.url = "http://127.0.0.1:8000/api/get_event_list/"

    def test_get_event_null(self):
        "发布会ID为NULL的情况"
        r = requests.get(self.url, params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], "parameter error")


if __name__ == '__main__':
    unittest.main()