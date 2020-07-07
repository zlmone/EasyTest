# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import subprocess

from core.Decorator import *
from core.utils.Loader import ReadConfig

from core.utils.Log import Log

log = Log()
maxin_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../resources/maxim/")
)
monkeylog_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../log/MonkeyLog/")
)

monkey_event: dict = ReadConfig().get_monkey_events()


def get_options():
    options = ''
    for k, v in monkey_event.items():
        options += ' --{0} {1} '.format(k, v)
    return options


class NativeMonkey(BasePage):

    @classmethod
    def command(cls, package, seed=123456, runtime: int = 30, throttle: int = 300, options=None, off_line=True):
        """
        monkey命令封装
        :param package:被测app的包名
        :param seed:伪随机数生成器的种子值。如果您使用相同的种子值重新运行 Monkey，它将会生成相同的事件序列
        :param runtime: 运行时间 minutes分钟
        :param throttle: 在事件之间插入固定的时间（毫秒）延迟
        :param options: 其他参数及用法同原始Monkey
        :param off_line: 是否脱机运行 默认Ture
        :return: shell命令
        """

        package = ' -p ' + package
        seed = ' -s ' + str(seed)
        # event_count = str(int(runtime / throttle * 60000))
        event_count = str(int(runtime * 1846))
        throttle = ' --throttle ' + str(throttle)

        if options:
            options = ' ' + options
        else:
            options = ''

        off_line_cmd = ' >/sdcard/nativemonkeyout.txt 2>/sdcard/nativemonkeyerr.txt &'
        if off_line:
            monkey_shell = (
                ''.join([' "monkey', package, seed, throttle, get_options(), options, event_count, off_line_cmd, '"']))
        else:
            monkey_shell = (
                ''.join([' "monkey', package, seed, throttle, get_options(), options, event_count, '"']))

        return monkey_shell

    @classmethod
    def run_monkey(cls, *args):
        """
        清理旧的配置文件并运行monkey，等待运行时间后pull log文件到电脑
        monkey_shell: shell命令
        """
        print("run_monkey启动")
        log.i('MONKEY_SHELL:%s' % args[0])
        cls.clear_env()
        # throttle = int(args[0].split('throttle ')[1].split(' ')[0])
        event_count = int(args[0].split(' ')[-4].strip())
        log.i('starting run monkey')
        log.i('It will be take about %s minutes,please be patient ...........................' % str(
            int(event_count / 1846)))
        print(args[0])
        # 设置全屏
        log.i('set app full screen mode')
        cls.set_full_screen()
        subprocess.Popen("adb -s {0} shell {1}".format(cls.device_name, args[0]), stdout=subprocess.PIPE,
                         shell=True)
        time.sleep(int(event_count / 30))
        # 取消全屏
        log.i('cancel app full screen mode')
        cls.cancel_full_screen()
        log.i('monkey run end>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    @classmethod
    def clear_env(cls):
        log.i('Clearing monkey env')
        print(cls.d)
        cls.d.shell('rm -r /sdcard/nativemonkeyerr.txt')
        cls.d.shell('rm -r /sdcard/nativemonkeyout.txt')
        log.i('Clear monkey env success')


class Maxim(BasePage):
    # d = None

    @classmethod
    def command(cls, package, runtime, mode=None, whitelist=False, blacklist=False, throttle=None, options=None,
                off_line=True):
        """
        monkey命令封装
        :param package:被测app的包名
        :param runtime: 运行时间 minutes分钟
        :param mode: 运行模式
            uiautomatormix(混合模式,70%控件解析随机点击，其余30%按原Monkey事件概率分布)、
            pct-uiautomatormix n ：可自定义混合模式中控件解析事件概率 n=1-100
            uiautomatordfs：DFS深度遍历算法（优化版）（注 Android5不支持dfs）(u2和dsf冲突 无法使用）
            uiautomatortroy：TROY模式（支持特殊事件、黑控件等） 配置 max.xpath.selector troy控件选择子来定制自有的控件选择优先级
            None: 默认原生 monkey
        :param whitelist: activity白名单  需要将awl.strings 配置正确
        :param blacklist: activity黑名单  需要将awl.strings 配置正确
        :param throttle: 在事件之间插入固定的时间（毫秒）延迟
        :param options: 其他参数及用法同原始Monkey
        :param off_line: 是否脱机运行 默认Ture
        :return: shell命令
        """
        classpath = 'CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin ' \
                    'tv.panda.test.monkey.Monkey '
        package = ' -p ' + package
        runtime = ' --running-minutes ' + str(runtime)
        if mode:
            mode = ' --' + mode
        else:
            mode = ''
        if throttle:
            throttle = ' --throttle ' + str(throttle)
        else:
            throttle = ''
        if options:
            options = ' ' + options
        else:
            options = ''
        if whitelist:
            whitelist = ' --act-whitelist-file /sdcard/awl.strings'
        else:
            whitelist = ''
        if blacklist:
            blacklist = ' --act-blacklist-file /sdcard/awl.strings'
        else:
            blacklist = ''

        off_line_cmd = ' >/sdcard/monkeyout.txt 2>/sdcard/monkeyerr.txt &'
        if off_line:
            monkey_shell = (
                ''.join(['"', classpath, package, runtime, mode, whitelist, blacklist, throttle, get_options(), options,
                         off_line_cmd,
                         '"']))
        else:
            monkey_shell = (
                ''.join(['"', classpath, package, runtime, mode, whitelist, blacklist, throttle, get_options(), options,
                         '"']))

        return monkey_shell

    #  maxim 文件夹说明：
    # awl.strings：存放activity白名单
    # max.xpath.actions：特殊事件序列
    # max.xpath.selector：TROY模式（支持特殊事件、黑控件等） 配置 max.xpath.selector troy控件选择子来定制自有的控件选择优先级
    # max.widget.black：黑控件 黑区域屏蔽
    # max.strings 随机输入字符，内容可自定义配置

    @classmethod
    def run_monkey(cls, *args):
        """
        清理旧的配置文件并运行monkey，等待运行时间后pull log文件到电脑
        monkey_shell: shell命令 uiautomatortroy 时 max.xpath.selector文件需要配置正确
        actions: 特殊事件序列 max.xpath.actions文件需要配置正确
        widget_black: 黑控件 黑区域屏蔽 max.widget.black文件需要配置正确
        """
        print(cls.d)
        print("run_monkey启动")
        log.i('MONKEY_SHELL:%s' % args[0])
        cls.clear_env()
        cls.push_jar()
        if args[0].find('awl.strings') != -1:
            cls.push_white_list()
        if args[0].find('uiautomatortroy') != -1:
            cls.push_selector()
        if args[1]:
            cls.push_actions()
        if args[2]:
            cls.push_widget_black()
        cls.set_AdbIME()
        runtime = args[0].split('running-minutes ')[1].split(' ')[0]
        log.i('starting run monkey')
        log.i('It will be take about %s minutes,please be patient ...........................' % runtime)
        # restore uiautomator server
        cls.d.service('uiautomator').stop()
        time.sleep(2)
        print(args[0])
        cls.set_full_screen()
        subprocess.Popen("adb -s {0} shell {1}".format(cls.device_name, args[0]), stdout=subprocess.PIPE,
                         shell=True)
        time.sleep(int(runtime) * 60 + 3)
        cls.cancel_full_screen()
        log.i('monkey run end>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # restore uiautomator server
        cls.d.service('uiautomator').start()

    @classmethod
    def push_jar(cls):
        cls.d.push(os.path.join(maxin_path, 'monkey.jar'), '/sdcard/')
        cls.d.push(os.path.join(maxin_path, 'framework.jar'), '/sdcard/')
        log.i('push jar file--->monkey.jar framework.jar')

    @classmethod
    def push_white_list(cls):
        cls.d.push(os.path.join(maxin_path, 'awl.strings'), '/sdcard/')
        log.i('push white_list file---> awl.strings ')

    @classmethod
    def push_actions(cls):
        cls.d.push(os.path.join(maxin_path, 'max.xpath.actions'), '/sdcard/')
        log.i('push actions file---> max.xpath.actions ')

    @classmethod
    def push_selector(cls):
        cls.d.push(os.path.join(maxin_path, 'max.xpath.selector'), '/sdcard/')
        log.i('push selector file---> max.xpath.selector ')

    @classmethod
    def push_widget_black(cls):
        cls.d.push('./maxim/max.widget.black', '/sdcard/')
        log.i('push widget_black file---> max.widget.black ')

    @classmethod
    def push_string(cls):
        cls.d.push(os.path.join(maxin_path, 'max.strings'), '/sdcard/')
        log.i('push string file---> max.strings ')

    @classmethod
    def clear_env(cls):
        log.i('Clearing monkey env')
        print(cls.d)
        cls.d.shell('rm -r /sdcard/monkeyerr.txt')
        cls.d.shell('rm -r /sdcard/monkeyout.txt')
        cls.d.shell('rm -r /sdcard/max.widget.black')
        cls.d.shell('rm -r /sdcard/max.xpath.selector')
        cls.d.shell('rm -r /sdcard/max.xpath.actions')
        cls.d.shell('rm -r /sdcard/awl.strings')
        cls.d.shell('rm -r /sdcard/monkey.jar')
        cls.d.shell('rm -r /sdcard/framework.jar')
        cls.d.shell('rm -r /sdcard/max.strings')
        cls.d.shell('rm -r /sdcard/monkeyerr.txt')
        cls.d.shell('rm -r /sdcard/monkeyout.txt')
        log.i('Clear monkey env success')

    @classmethod
    def set_AdbIME(cls):
        log.i('setting AdbIME as default')
        ime = cls.d.shell('ime list -s').output
        if 'adbkeyboard' in ime:
            cls.d.shell('ime set com.android.adbkeyboard/.AdbIME')
        else:
            cls.install(os.path.join(maxin_path, 'ADBKeyBoard.apk'))
            cls.d.shell('ime enable com.android.adbkeyboard/.AdbIME')
            cls.d.shell('ime set com.android.adbkeyboard/.AdbIME')
            log.i('install adbkeyboard and set as default')
        cls.push_string()


if __name__ == '__main__':
    # log.set_logger('e36fde82', 'demo.log')
    # monkey = NativeMonkey()
    # monkey.set_driver('e36fde82')
    # print(monkey.device_info)
    # command = monkey.command(package='com.genshuixue.student', runtime=3, throttle=100,
    #                          options=' -v -v --pct-syskeys 0 ', off_line=True)
    # monkey.run_monkey(command)
    # ime = maxim.d.shell('ime list -s').output
    # print('adbkeyboard' in ime)
    # maxim.clear_env()
    # m = NativeMonkey()
    # d = {'cmd': 5}
    # m.run_monkey(cmd=5)

    print(get_options())
