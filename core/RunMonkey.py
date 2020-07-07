# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import os
import unittest
from core.utils.Log import Log


class RunMonkey:
    def __init__(self, device):
        self.test_report_root = "../log/MonkeyLog"

        self.device = device

        if not os.path.exists(self.test_report_root):
            os.mkdir(self.test_report_root)

        self.test_report_path = os.path.join(self.test_report_root,
                                             self.device['model'].replace(':', '_').replace(' ', '') + '_' +
                                             self.device['serial'])

        if not os.path.exists(self.test_report_path):
            os.mkdir(self.test_report_path)

    def get_path(self):
        log_path: str = Log().get_log_path()
        report_path: str = self.test_report_path.replace('../log', '')
        return log_path + report_path

    def get_device(self):
        return self.device

    @staticmethod
    def run_cases(cases):
        runner = unittest.TextTestRunner()
        runner.run(cases)
