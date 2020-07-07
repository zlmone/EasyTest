# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""


from __future__ import absolute_import

import atexit
import os
import platform

import psutil as pt
import six
from selenium import webdriver

if six.PY3:
    import subprocess
else:
    import subprocess as subprocess


def get_pid_by_name(name):
    pids = pt.process_iter()
    pid_list = []
    for pid in pids:
        if pid.name() == name:
            pid_list.append(int(pid.pid))
    return pid_list


class ChromeDriver(object):
    def __init__(self, driver, port):
        self._d = driver
        self._port = port

    def _launch_webdriver(self):
        # print("start chromedriver instance")
        p = subprocess.Popen(['chromedriver', '--port=' + str(self._port)])

        try:
            p.wait(timeout=2.0)
            return False
        except subprocess.TimeoutExpired:
            return True

    def driver(self, device_ip=None, package=None, attach=True, activity=None, process=None):
        """
        Args: - package(string): default current running app - attach(bool): default true, Attach to an
        already-running app instead of launching the app with a clear data directory - activity(string): Name of the
        Activity hosting the WebView. - process(string): Process name of the Activity hosting the WebView (as given
        by ps). If not given, the process name is assumed to be the same as androidPackage.

        Returns:
            selenium driver
        """
        app = self._d.current_app()
        capabilities = {
            'chromeOptions': {
                'androidDeviceSerial': device_ip or self._d.serial,
                'androidPackage': package or app['package'],
                'androidUseRunningApp': attach,
                'androidProcess': process or app['package'],
                'androidActivity': activity or app['activity'],
            }
        }
        self._launch_webdriver()
        dr = webdriver.Remote('http://localhost:%d' % self._port, capabilities)

        # always quit driver when done
        atexit.register(dr.quit)
        return dr

    @staticmethod
    def kill():

        if platform.system() == 'Windows':
            # for windows
            pid = get_pid_by_name('chromedriver.exe')
            for i in pid:
                os.popen('taskkill /PID %d /F' % i)
        else:
            # # for mac
            pid = get_pid_by_name('chromedriver')
            for i in pid:
                os.popen('kill -9 %d' % i)

        print('All chromedriver pid killed')


if __name__ == '__main__':
    import uiautomator2 as u2

    d = u2.connect()
    dri = ChromeDriver(d, 3456).driver()
    # dr = webdriver.Chrome()
    dri.find_element_by_id('index-kw').send_keys('python')

    dri.find_element_by_id('index-bn').click()
    # elem = driver.find_element_by_link_text(u"index-kw")
    dri.quit()
    ChromeDriver.kill()
    print(platform.system())
