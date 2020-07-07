# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
from core.BasePage import BasePage
from page.tab_route import TabRoutes
from page.login import LoginPage
from page.my_courses import MyCoursesPage
from core.Decorator import *
import unittest

from core.utils.Loader import ReadConfig
from page import login

apk_path = ReadConfig().get_apk_path()
pkg_name = ReadConfig().get_pkg_name()


class LiveBackSteps(unittest.TestCase, BasePage):
    @classmethod
    # @setupclass
    def setUpClass(cls):
        cls.d.app_stop(pkg_name)

    # @testcase
    def test_liveback_stable(self):
        # self.d.app_uninstall(pkg_name)
        # self.install(apk_path)
        self.d.app_start(pkg_name)
        # self.set_fastinput_ime()
        time.sleep(5)
        TabRoutes().to_my_courses().course_item('直播回放稳定性专用').live_entry('看回放')
