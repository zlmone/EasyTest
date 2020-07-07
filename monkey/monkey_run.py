# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""

from core.Drivers import Drivers
from core.Runner import MonkeyRunner
import unittest
from monkey import liveback_steps

if __name__ == '__main__':
    cases = unittest.TestSuite()

    cases.addTest(liveback_steps.LiveBackSteps('test_liveback_stable'))
    command = MonkeyRunner.runner().command(package='com.genshuixue.student', runtime=3,
                                            throttle=100,
                                            options=' --ignore-crashes --ignore-timeouts -v -v ')

    Drivers().run_monkey(cases=cases, cmd=command)
