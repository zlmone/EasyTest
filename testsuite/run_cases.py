#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
# sys.path.append(os.path.split(os.path.split(os.path.abspath(''))[0])[0])
from core.CaseStrategy import CaseStrategy
from core.Drivers import Drivers
from core.report.Report import *

sys.path.append('..')

if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下
    now = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    # backup_report('./TestReport', './TestReport_History', now)

    cs = CaseStrategy()
    cases = cs.collect_cases(suite=False)
    Drivers().run(cases)

    # Generate zip_report file  压缩测试报告文件
    # zip_report()
