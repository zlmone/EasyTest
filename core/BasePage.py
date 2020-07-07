# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import os
import subprocess
import threading
import time
import uiautomator2 as u2
from uiautomator2 import UiObjectNotFoundError
from multiprocessing import Process
import re
from core.utils.ChromeDriver import ChromeDriver
from core.utils.Ports import Ports
from core.report.ReportPath import ReportPath
from core.utils.DataProvider import get_apk_info


# u2.DEBUG = True

class BasePage(object):
    d = None
    device_name = ''

    @classmethod
    def set_driver(cls, dri):
        cls.d = u2.connect(dri)
        cls.device_info = cls.d.device_info
        cls.device_name = cls.d.device_info['serial']

    def get_driver(self):
        return self.d

    @classmethod
    def install(cls, apk_path):
        t1 = threading.Thread(target=cls.local_install, args=(cls.device_name, apk_path))
        t2 = threading.Thread(target=cls.install_check, args=())
        t1.start()
        t2.start()
        t1.join()

    @classmethod
    def install_check(cls):
        print("调用install_check")
        time.sleep(2)
        brand = cls.d.device_info['brand']
        if brand == 'vivo':
            if cls.d(resourceId='com.bbk.account:id/edit_Text').exists:
                cls.d(resourceId='com.bbk.account:id/edit_Text').set_text('qwerty123')
                cls.d(resourceId='android:id/button1').click_exists(3)
        elif brand == 'oppo':
            pass
        elif brand == 'xiaomi':
            pass
        elif brand == 'huawei':
            pass
        else:
            pass
        # cls.watch_device()
        num = 0
        keyword = ['继续安装', '允许安装', '安装', '完成']
        while num < 3:
            for key in keyword:
                # cls.d.xpath.when(i).click()
                cls.d(text=key).click_exists(2)
            time.sleep(2)
            num += 1
        print("调用install_check 完成")
        return cls

    @staticmethod
    def local_install(device_name, apk_path):
        """
        安装本地apk 覆盖安装，不需要usb链
        """
        print("调用 local_install")
        # packagename = get_apk_info(apk_path)['package']
        # device_name = cls.d.device_info['serial']
        # file_name = os.path.basename(apk_path)
        # dst = '/data/local/tmp/' + file_name
        # print('start to install %s' % file_name)
        # cls.d.push(apk_path, dst)
        # print('start install %s' % dst)
        # cls.protect()
        # r = cls.d.shell(['pm', 'install', '-r', dst], stream=True)
        # i = r.text.strip()
        # print(time.strftime('%H:%M:%S'), i)
        # # self.unwatch_device()
        # packages = list(map(lambda p: p.split(':')[1], cls.d.shell('pm list packages').output.splitlines()))
        # if packagename in packages:
        #     cls.d.shell(['rm', dst])
        # else:
        #     raise Exception('%s 安装失败' % apk_path)
        P = subprocess.Popen("adb -s {0} install {1}".format(device_name, apk_path), stdout=subprocess.PIPE, shell=True)
        data = P.stdout.read()
        if "Success" in str(data):
            print('Installing apk: {0} for device: {1} Success'.format(apk_path, device_name))
        if "Failure" in str(data):
            print('Installing apk: {0} for device: {1} Failure'.format(apk_path, device_name))

        print("调用 local_install 完成")

    @classmethod
    def unlock_device(cls):
        """unlock.apk install and launch"""
        pkgs = re.findall('package:([^\s]+)', cls.d.shell(['pm', 'list', 'packages', '-3'])[0])
        if 'io.appium.unlock' in pkgs:
            cls.d.app_start('io.appium.unlock')
            cls.d.shell('input keyevent 3')
        else:
            #  appium unlock.apk 下载安装
            print('installing io.appium.unlock')
            cls.d.app_install('https://raw.githubusercontent.com/pengchenglin/ATX-GT/master/apk/unlock.apk')
            cls.d.app_start('io.appium.unlock')
            cls.d.shell('input keyevent 3')

    @classmethod
    def back(cls):
        """
        点击返回
        页面没有加载完的时候，会出现返回失败的情况，使用前确认页面加载完成
        """
        time.sleep(1)
        cls.d.press('back')
        time.sleep(1)

    @classmethod
    def identify(cls):
        cls.d.open_identify()

    def set_chromedriver(self, device_ip=None, package=None, activity=None, process=None):
        driver = ChromeDriver(self.d, Ports().get_ports(1)[0]). \
            driver(device_ip=device_ip, package=package, attach=True, activity=activity, process=process)
        return driver

    def watch_device(self, keyword, internal=1):
        """
        如果存在元素则自动点击
         keyword="yes|允许|好的|跳过" internal 循环查找 1次
        """
        num = 0
        while num < internal:
            for key in keyword.split("|"):
                # cls.d.xpath.when(i).click()
                self.d(text=key).click_exists(2)
            time.sleep(2)
            num += 1

    @classmethod
    def unwatch_device(cls):
        """关闭watcher """
        cls.d.xpath.watch_clear()
        cls.d.xpath.watch_stop()
        time.sleep(2)

    @classmethod
    def get_toast_message(cls):
        message = cls.d.toast.get_message(3, 3)
        cls.d.toast.reset()
        return message

    @classmethod
    def set_fastinput_ime(cls):
        cls.d.set_fastinput_ime(True)

    @classmethod
    def set_original_ime(cls):
        cls.d.set_fastinput_ime(False)

    @classmethod
    def screenshot(cls):
        """截图并打印特定格式的输出，保证用例显示截图"""
        date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        screenshot_name = 'Manual_' + date_time + '.PNG'
        path = os.path.join(ReportPath().get_path(), screenshot_name)
        cls.d.screenshot(path)
        print('IMAGE:' + screenshot_name)

    @staticmethod
    def find_message(elements, text):
        """查找元素列表中是否存在 text"""
        count = elements.count
        while count > 0:
            count = count - 1
            message = elements[count].info['text']
            if text in message:
                return True
            elif count == 0:
                return False
        else:
            return False

    def _get_window_size(self):
        window = self.d.window_size()
        x = window[0]
        y = window[1]
        return x, y

    @staticmethod
    def _get_element_size(element):
        # rect = element.info['visibleBounds']
        rect = element.info['bounds']
        # print(rect)
        x_center = (rect['left'] + rect['right']) / 2
        y_center = (rect['bottom'] + rect['top']) / 2
        x_left = rect['left']
        y_up = rect['top']
        x_right = rect['right']
        y_down = rect['bottom']

        return x_left, y_up, x_center, y_center, x_right, y_down

    def _swipe(self, fromX, fromY, toX, toY, steps):
        self.d.swipe(fromX, fromY, toX, toY, steps)

    def swipe_up(self, element=None, steps=0.2):
        """
        swipe up
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element)
            fromX = x_center
            fromY = y_center
            toX = x_center
            toY = y_up
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = 0.5 * y
            toX = 0.5 * x
            toY = 0.25 * y

        self._swipe(fromX, fromY, toX, toY, steps)

    def swipe_down(self, element=None, steps=0.2):
        """
        swipe down
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element)

            fromX = x_center
            fromY = y_center
            toX = x_center
            toY = y_down
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = 0.5 * y
            toX = 0.5 * x
            toY = 0.75 * y

        self._swipe(fromX, fromY, toX, toY, steps)

    def swipe_left(self, element=None, steps=0.2):
        """
        swipe left
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element)
            fromX = x_center
            fromY = y_center
            toX = x_left
            toY = y_center
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = 0.5 * y
            toX = 0.25 * x
            toY = 0.5 * y
        self._swipe(fromX, fromY, toX, toY, steps)

    def swipe_right(self, element=None, steps=0.2):
        """
        swipe right
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element)
            fromX = x_center
            fromY = y_center
            toX = x_right
            toY = y_center
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = 0.5 * y
            toX = 0.75 * x
            toY = 0.5 * y
        self._swipe(fromX, fromY, toX, toY, steps)

    def _find_element_by_swipe(self, direction, value, element=None, steps=0.2, max_swipe=6):
        """
        :param direction: swip direction exp: right left up down
        :param value: The value of the UI element location strategy. exp: d(text='Logina')
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: UI element
        """
        times = max_swipe
        for i in range(times):
            try:
                if value.exists:
                    return value
                else:
                    raise UiObjectNotFoundError
            except UiObjectNotFoundError:
                if direction == 'up':
                    self.swipe_up(element=element, steps=steps)
                elif direction == 'down':
                    self.swipe_down(element=element, steps=steps)
                elif direction == 'left':
                    self.swipe_left(element=element, steps=steps)
                elif direction == 'right':
                    self.swipe_right(element=element, steps=steps)
                if i == times - 1:
                    raise UiObjectNotFoundError

    def find_element_by_swipe_up(self, value, element=None, steps=0.2, max_swipe=6):
        return self._find_element_by_swipe('up', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_down(self, value, element=None, steps=0.2, max_swipe=6):
        return self._find_element_by_swipe('down', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_left(self, value, element=None, steps=0.2, max_swipe=6):
        return self._find_element_by_swipe('left', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_right(self, value, element=None, steps=0.2, max_swipe=6):
        return self._find_element_by_swipe('right', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    @classmethod
    def set_full_screen(cls):
        print("设置App运行环境为全屏模式")
        cls.d.shell('settings put global policy_control immersive.full=*')

    @classmethod
    def cancel_full_screen(cls):
        print("取消全屏模式")
        cls.d.shell('settings put global policy_control null')


if __name__ == '__main__':
    maxin_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../resources/maxim/ADBKeyBoard.apk")
    )
    page = BasePage()
    page.set_driver("e36fde82")
    # page.find_element_by_swipe_up(page.d(text='直播回放稳定性专用'))
    # page.d(resourceId="com.android.filemanager:id/udisk_size").click()
    # page.install_check()
    # page.watch_device("//*[@text='继续安装']|//*[@text='安装']")
    # page.d(text="继续安装").click()
    # page.watch_device("继续安装|安装")
    # page.install(maxin_path)
    page.d.press("back")
