#!/usr/bin/env python
# coding=utf-8
"""
本文件的作用：对 coin_market_cap 使用 scrapy contract 的方式进行单元测试
使用：
>> python coin_market_cap_UnitTest.py -v
"""

import os
import sys
import unittest
import subprocess

class Testcoin_market_cap(unittest.TestCase):
    """
    对 coin_market_cap 使用 scrapy contract 的方式进行单元测试
    """

    @classmethod
    def setUpClass(self):
        print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("对 time_series/coin_market_cap 的功能模块进行测试...")
        print("-------------------------------------------------------------")

    @classmethod
    def tearDownClass(self):
        print("-------------------------------------------------------------")
        print("对 time_series/coin_market_cap 的功能模块进行测试完成")
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

    def test_coin_market_cap_scrapy_contracts(self):
        '''在 time_series/coin_market_cap 目录下运行 scrapy check ...'''

        current_dir_path = os.path.abspath(os.path.dirname(__file__))
        target_dir_path = os.path.abspath(os.path.join(current_dir_path, 'coin_market_cap/'))
        os.chdir(target_dir_path)
        result = subprocess.run(['scrapy', 'check'], stdout=subprocess.PIPE)
        os.chdir(current_dir_path)
        # if result.returncode==1 there is some kind of errors
        self.assertEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
