# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import wda
from core.ATXServer2 import ATXServer2
from core.utils.Loader import ReadConfig

wdaUrl = None
ios_devices = ATXServer2(ReadConfig().get_server_url()).present_ios_devices()
if ios_devices:
    wdaUrl = ios_devices[0]['source']['wdaUrl']

c = wda.Client(wdaUrl)
print(c.status())
print(c.healthcheck())

with c.session('com.genshuixue.student') as d:
    d(label=u"我的课程").click()
    d(label=u"返回").click()
