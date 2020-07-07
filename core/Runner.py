# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/7/2 11:03 上午
    @Description:  
"""
from core.Monkey import Maxim, NativeMonkey
from core.utils.Loader import ReadConfig

runner = ReadConfig().get_monkey_runner()


class MonkeyRunner:

    @staticmethod
    def runner():
        if runner == 'maxim':
            return Maxim()
        elif runner == 'native':
            return NativeMonkey()
