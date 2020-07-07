# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
# from core.BasePage import BasePage
# from core.maxim_monkey import maxim
from core.Decorator import *


class OnlineCoursesPage(BasePage):

    def wait_page(self):
        try:
            if self.d(text='在线好课').wait(timeout=15):
                pass
            else:
                raise Exception('Not in HomePage')
        except Exception:
            raise Exception('Not in HomePage')


if __name__ == '__main__':
    from core.utils.Log import Log
