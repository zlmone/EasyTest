# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import os
import threading
import time

from core.ATXServer import ATXServer
from core.BasePage import BasePage
# from core.Devices import *    # for循环 check_alive  比较慢
from core.Devices_new import *  # 多进程 check_alive ，Mac下需要配置  `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`到环境变量
from core.utils.Log import Log
from core.utils.Loader import ReadConfig
from core.report.Report import create_statistics_report, backup_report
from core.report.ReportPath import ReportPath
from core.RunCases import RunCases
from core.RunMonkey import RunMonkey
from core.utils.DataProvider import generate_test_data
from core.utils.ChromeDriver import ChromeDriver
from core.Runner import MonkeyRunner
from core.Demons import Demons


def check_devices():
    # 根据method 获取android设备
    method = ReadConfig().get_method().strip()
    if method == 'SERVER':
        # get ATX-Server Online devices
        # devices = ATX_Server(ReadConfig().get_server_url()).online_devices()
        print('Get available online devices from ATX-Server...')
        devices = get_online_devices(ATXServer(ReadConfig().get_server_url()).online_devices())
        print('\nThere has %s online devices in ATX-Server' % len(devices))

    elif method == 'SERVER2':
        print('Get available online devices from atxserver2...')
        devices = atxserver2_online_devices(ATXServer2(ReadConfig().get_server_url()).present_android_devices())
        print('\nThere has %s online devices in atxserver2' % len(devices))

    elif method == 'UDID':
        print('Get available UDID devices %s from atxserver2...' % ReadConfig().get_server_udid())
        devices = atxserver2_online_devices(ATXServer2(ReadConfig().get_server_url()).present_udid_devices())
        print('\nThere has %s available udid devices in atxserver2' % len(devices))

    elif method == 'IP':
        # get  devices from resources devices list
        print('Get available IP devices %s from resources... ' % ReadConfig().get_devices_ip())
        devices = get_devices()
        print('\nThere has %s  devices alive in resources IP list' % len(devices))

    elif method == 'USB':
        # get  devices connected PC with USB
        print('Get available USB devices connected on PC... ')
        devices = get_connected_devices()
        print('\nThere has %s  USB devices alive ' % len(devices))

    else:
        raise Exception('Config.ini method illegal:method =%s' % method)

    return devices


class Drivers:
    @staticmethod
    def _run_cases(run, cases):
        log = Log()
        log.set_logger(run.get_device()['model'], os.path.join(run.get_path(), 'client.log'))
        log.i('udid: %s' % run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:
            # run cases
            base_page.set_fastinput_ime()
            base_page.d.shell('logcat -c')  # 清空logcat

            run.run(cases)

            # 将logcat文件上传到报告
            base_page.d.shell('logcat -d > /sdcard/logcat.log')
            time.sleep(1)
            base_page.d.pull('/sdcard/logcat.log', os.path.join(path.get_path(), 'logcat.log'))

            base_page.set_original_ime()
            base_page.identify()
            if ReadConfig().get_method().strip() in ["UDID", "SERVER2"]:
                log.i('release device %s ' % run.get_device()['serial'])
                ATXServer2(ReadConfig().get_server_url()).release_device(run.get_device()['serial'])
            else:
                pass
        except AssertionError as e:
            log.e('AssertionError, %s', e)

    @staticmethod
    def _run_monkey(run: RunMonkey, cases, cmd, actions, widget_black):
        print("开始调用 _run_maxim")
        log = Log()
        p = run.get_path()
        print(p)
        path = os.path.join(run.get_path(), 'client.log')
        print(path)
        log.set_logger(run.get_device()['model'], os.path.join(run.get_path(), 'client.log'))
        log.i('udid: %s', run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
            device_name = run.get_device()['ip']
        else:
            base_page.set_driver(run.get_device()['serial'])
            device_name = run.get_device()['serial']
        try:
            # run cases
            # 清空logcat
            base_page.d.shell('logcat -c')
            if cases:
                run.run_cases(cases)
            # 如果为局部稳定性，则开启守护线程 针对目标页面进行monkey测试
            if ReadConfig().get_monkey_is_single():
                Demons(device_name).run()
                t = threading.Thread(target=MonkeyRunner.runner().run_monkey,
                                     args=(cmd, actions, widget_black))
                t.start()
                t.join()
            else:
                MonkeyRunner.runner().run_monkey(cmd, actions, widget_black)

            base_page.d.shell('logcat -d > /sdcard/logcat.log')
            time.sleep(1)
            # 拉取monkey运行日志到本地
            base_page.d.pull('/sdcard/logcat.log', os.path.join(path.get_path(), 'logcat.log'))
            if ReadConfig().get_monkey_runner() == 'maxim':
                base_page.d.pull('/sdcard/monkeyerr.txt', os.path.join(path.get_path(), 'monkeyerr.txt'))
                base_page.d.pull('/sdcard/monkeyout.txt', os.path.join(path.get_path(), 'monkeyout.txt'))
            elif ReadConfig().get_monkey_runner() == 'native':
                base_page.d.pull('/sdcard/nativemonkeyerr.txt', os.path.join(path.get_path(), 'nativemonkeyerr.txt'))
                base_page.d.pull('/sdcard/nativemonkeyout.txt', os.path.join(path.get_path(), 'nativemonkeyout.txt'))

            base_page.set_original_ime()
            base_page.identify()
            if ReadConfig().get_method().strip() in ["UDID", "SERVER2"]:
                log.i('release device %s ' % run.get_device()['serial'])
                ATXServer2(ReadConfig().get_server_url()).release_device(run.get_device()['serial'])
            else:
                pass
        except AssertionError as e:
            log.e('AssertionError, %s', e)

    def run(self, cases):
        start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        devices = check_devices()
        if not devices:
            print('There is no device found,test over.')
            return

        # generate test data data.json 准备测试数据
        generate_test_data(devices)

        print('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        runs = []
        for i in range(len(devices)):
            runs.append(RunCases(devices[i]))
        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_cases,
                             args=(run, cases,))
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')
        ChromeDriver.kill()

        #  Generate statistics report  生成统计测试报告 将所有设备的报告在一个HTML中展示
        create_statistics_report(runs)
        # backup_report('./TestReport', './TestReport_History', start_time)

    def run_monkey(self, cases=None, cmd=None, actions=False, widget_black=False):
        start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        devices = check_devices()
        if not devices:
            print('There is no device found,test over.')
            return
        print('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(devices)
        runs = []
        for i in range(len(devices)):
            runs.append(RunMonkey(devices[i]))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_monkey,
                             args=(run, cases, cmd, actions, widget_black,))
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')
        # backup_report('./MaximReport', './MaximReport_History', start_time)


if __name__ == '__main__':
    command = MonkeyRunner.runner().command(package='com.genshuixue.student', runtime=1,
                                            throttle=300,
                                            options=' -v -v ')

    Drivers().run_monkey(cmd=command, actions=True, widget_black=False)
