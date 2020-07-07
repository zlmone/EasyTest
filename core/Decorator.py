# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import time

from functools import wraps
from core.BasePage import BasePage
from core.report.ReportPath import ReportPath
from core.utils.Log import Log
from page.login import LoginPage
import os
import imageio
import shutil

flag = 'IMAGE:'
log = Log()


def _screenshot(name):
    date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    screenshot = name + '-' + date_time + '.PNG'
    # path = ReportPath().get_path() + '/' + screenshot
    path = os.path.join(ReportPath().get_path(), screenshot)
    driver = BasePage().get_driver()
    driver.screenshot(path)
    return screenshot


def _screenshot_for_gif():
    tmp_path = os.path.join(ReportPath().get_path(), 'tmp')
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    tmpshot = str(round(time.time() * 1000)) + '.PNG'
    path = os.path.join(tmp_path, tmpshot)
    driver = BasePage().get_driver()
    driver.screenshot(path)
    return path


def _create_gif():
    """
    生成gif文件，原始图片仅支持png格式
    gif_name ： 字符串，所生成的 gif 文件名，带 .gif 后缀
    path :      需要合成为 gif 的图片所在路径
    duration :  gif 图像时间间隔
    """

    frames = []
    path = os.path.join(ReportPath().get_path(), 'tmp')
    if not os.path.exists(path):
        pass
    else:
        png_files = os.listdir(path)
        image_list = [os.path.join(path, f) for f in png_files]
        list.sort(image_list)
        for image_name in image_list:
            # 读取 png 图像文件
            frames.append(imageio.imread(image_name))
        # 保存为 gif
        gif_name = str(round(time.time() * 1000)) + '.gif'
        gif_path = os.path.join(ReportPath().get_path(), gif_name)
        imageio.mimsave(gif_path, frames, 'GIF', duration=0.6)
        shutil.rmtree(path)
        return gif_name


def checklogin(func):
    @wraps(func)
    def wrapper(*args):
        try:
            if LoginPage().check_need_login():
                LoginPage().input_phone(args[0]).input_password(args[1]).submit_login()
            func()
        except Exception as e:
            log.i(e)


def teststep(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('--> %s' % func.__qualname__)
            ret = func(*args, **kwargs)
            return ret
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'AssertionError', 'Error')
            raise AssertionError(e)
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'Exception', 'Error')
            raise Exception(e)
        # finally:
        #     _screenshot_for_gif()  # 截取gif生成用图

    return wrapper


def teststeps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('--> %s' % func.__qualname__)
            ret = func(*args, **kwargs)
            log.d('  <-- %s, %s', func.__qualname__, 'Success')
            return ret
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'AssertionError', 'Error')
            raise AssertionError(e)
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'Exception', 'Error')
            raise Exception(e)
        # finally:
        #     _screenshot_for_gif()  # 截取gif生成用图

    return wrapper


def testcase(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.d('--> %s', func.__qualname__)
            ret = func(*args, **kwargs)
            log.d('<-- %s, %s\n', func.__qualname__, 'Success')
            return ret
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'AssertionError', 'Fail')

            if flag in str(e):
                raise AssertionError(e)
            else:
                raise AssertionError(flag + _screenshot(func.__qualname__))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'Exception', 'Error')

            if flag in str(e):
                raise Exception(e)
            else:
                raise Exception(flag + _screenshot(func.__qualname__))
        # finally:
        #     log.i(flag + _create_gif())  # 生成gif 并删除tmp文件夹

    return wrapper


def _wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.d('--> %s', func.__qualname__)
            ret = func(*args, **kwargs)
            log.d('<-- %s, %s\n', func.__qualname__, 'Success')
            return ret
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'AssertionError', 'Fail')

            if flag in str(e):
                raise AssertionError(e)
            else:
                raise AssertionError(flag + _screenshot(func.__qualname__))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'Exception', 'Error')

            if flag in str(e):
                raise Exception(e)
            else:
                raise Exception(flag + _screenshot(func.__qualname__))

    return wrapper


def setup(func):
    return _wrapper(func)


def teardown(func):
    return _wrapper(func)


def setupclass(func):
    return _wrapper(func)


def teardownclass(func):
    return _wrapper(func)
