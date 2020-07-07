# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""


class ReportPath:
    @classmethod
    def set_path(cls, ps):
        cls.path = ps

    def get_path(self):
        return self.path
