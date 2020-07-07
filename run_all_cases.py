# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import sys

from core.CaseStrategy import CaseStrategy
from core.Drivers import Drivers
from core.report.Report import *

sys.path.append('.')

if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下
    now = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    # backup_report('./TestReport', './TestReport_History', now)

    cs = CaseStrategy()
    cases = cs.collect_cases(suite=True)
    Drivers().run(cases)

    # Generate zip_report file  压缩测试报告文件
    # zip_report()
