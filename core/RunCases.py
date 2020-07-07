# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import os

from core.report.HTMLTestReport import HTMLTestRunner
from core.utils.Log import Log


class RunCases:
    def __init__(self, device):
        self.test_report_root = '../TestReport'
        self.device = device

        if not os.path.exists(self.test_report_root):
            os.mkdir(self.test_report_root)

        # date_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
        # self.test_report_path = os.path.join(self.test_report_root, date_time+self.device['udid'].replace(':', '_'))
        self.test_report_path = os.path.join(self.test_report_root,
                                             self.device['model'].replace(':', '_').replace(' ', '') + '_' +
                                             self.device['serial'])

        if not os.path.exists(self.test_report_path):
            os.mkdir(self.test_report_path)

        self.file_name = os.path.join(self.test_report_path, 'TestReport.html')

    def get_path(self):
        log_path: str = Log().get_root_path()
        report_path: str = self.test_report_path.replace('..', '')
        return log_path + report_path

    def get_device(self):
        return self.device

    def run(self, cases):
        with open(self.file_name, 'wb') as file:
            runner = HTMLTestRunner(stream=file, title=self.device['model'] + '自动化测试报告', description='用例执行情况：')
            runner.run(cases)
            file.close()


# if __name__ == '__main__':
#     print(os.path.)
