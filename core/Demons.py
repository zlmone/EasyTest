# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:  
"""
import os
import subprocess
import time
import threading

from core.BasePage import BasePage
from core.utils.Log import Log
from core.utils.Loader import ReadConfig

log = Log()
schema = ReadConfig().get_monkey_schema()
main_activity = ReadConfig().get_monkey_main_activity()
widget = ReadConfig().get_monkey_widget()
white_activity = ReadConfig().get_monkey_white_activity()
internal = ReadConfig().get_monkey_internal()
max_time = ReadConfig().get_monkey_max_time()
start_time = int(time.time())


class Demons(BasePage):
    def __init__(self, device):
        self._device = device
        if self.d is None:
            self.set_driver(device)
        log.set_logger(device, "demons_{0}.log".format(device))

    def run(self):
        t1 = threading.Thread(target=self.demons, args=())
        t1.start()
        # t1.join()

    def demons(self):
        print('开始调用 demons')
        try:
            while True:
                current_activity = self.get_current_activity()
                if self.injuge(current_activity, white_activity):
                    log.i("**********设备 {0} 停留当前页面**********".format(self._device))
                else:
                    log.i(">>>>>>>>>>>>>>>>设备 {0} 正在拉回指定页面>>>>>>>>>>>>>>".format(self._device))
                    if widget is not None:
                        self.demons_widget()
                    elif schema is not None:
                        self.demons_schema()
                    elif main_activity is not None:
                        self.demons_activity()
                time.sleep(internal)
                if (int(time.time()) - start_time - 5) > max_time:
                    break

        except Exception as e:
            log.i("回到指定页面异常：%s" % e)
        print('调用 demons 结束')

    def get_current_activity(self) -> str:
        try:
            activity = subprocess.Popen(
                "adb -s %s shell dumpsys activity activities|grep mResumedActivity| awk '{print $4}'" % self._device,
                stdout=subprocess.PIPE,
                shell=True).stdout.read().decode()
            log.i("设备 {0} 获取当前页面为: {1}".format(self._device, activity))
            return activity.strip()
        except Exception as e:
            log.e(e)

    def demons_activity(self):
        log.i("设备 {0} 正在通过Activity跳转：{1}".format(self._device, main_activity))
        try:
            os.popen("adb -s {0} shell am start -n {1}".format(self._device, main_activity))
        except Exception as e:
            log.e("Activity跳转异常：%s" % e)

    def demons_schema(self):
        log.i("设备 {0} 正在通过Schema跳转：{1}".format(self._device, schema))
        try:
            os.popen("adb -s {0} shell am start -d {1}".format(self._device, schema))
        except Exception as e:
            log.e("Schema跳转异常：%s" % e)

    def demons_widget(self):
        log.i("设备 {0} 正在通过widget跳转：{1}".format(self._device, widget))
        try:
            self.d(text=widget).click()
        except Exception as e:
            log.e("widget跳转异常：%s" % e)

    def injuge(self, curent_activity: str, activity: list) -> bool:
        if len(activity) > 0:
            if activity.__contains__(curent_activity):
                log.i("设备 {0} 命中白名单".format(self._device))
                return True
            else:
                log.i("设备 {0} 未命中白名单".format(self._device))
                return False
        else:
            log.e("whiteActivity 未配置")


if __name__ == '__main__':
    demons = Demons("1e7af099")
    demons.get_current_activity()
    demons.demons()
