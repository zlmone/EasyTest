# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
"""
for循环 check_alive
"""

import re
import subprocess

import uiautomator2 as u2

from core.ATXServer import ATXServer
from core.utils.Loader import ReadConfig


def get_devices():
    """
    get the devices from Pubilc/resources.ini devices list
    return alive devices
    """
    devices_ip = ReadConfig().get_devices_ip()
    print('Connect devices from resources devices IP list %s' % devices_ip)
    devices_list = []
    for i in devices_ip:
        try:
            device = u2.connect(i)
            # device.reset_uiautomator()
            if device.agent_alive:
                device.healthcheck()
                if device.alive:
                    dict_tmp = device.device_info
                    dict_tmp['ip'] = i
                    devices_list.append(dict_tmp)
            else:
                print('The IP %s device is not alive,please checkout!' % i)
        except Exception as e:
            print('Raise ERROR %s\nThe IP %s device is not alive,please checkout!' % (e, i))
    return devices_list


def get_online_devices():
    """
    get the devices from ATX-Server
    return alive devices
    """
    devices = ATXServer(ReadConfig().get_server_url()).online_devices()
    # print('Connect devices from resources devices IP list %s' % devices_ip)
    devices_list = []
    if devices:
        for i in devices:
            try:
                device = u2.connect(i['ip'])
                if device.agent_alive:
                    device.healthcheck()
                    if device.alive:
                        devices_list.append(i)
                else:
                    print('The device %s  is not alive,please checkout!' % i['udid'])
            except Exception as e:
                print('Raise ERROR %s\nThe IP %s device is not alive,please checkout!' % (e, i['udid']))
        return devices_list
    else:
        raise Exception('ATX-Server has no online device!!! ')


def get_connected_devices():
    """
    get the devices USB connected on PC
    return alive devices
    """
    output = subprocess.check_output(['adb', 'devices'])
    pattern = re.compile(
        r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    matches = pattern.findall(output.decode())
    valid_serials = [m[0] for m in matches if m[1] == 'device']

    if valid_serials:
        print('The devices connected on PC: %s' % valid_serials)
        devices_list = []
        for i in valid_serials:
            try:
                device = u2.connect(i)
                if device.agent_alive:
                    device.healthcheck()
                    if device.alive:
                        dict_tmp = device.device_info
                        devices_list.append(dict_tmp)
                else:
                    print('The serial %s device is not alive,please checkout!' % i)
            except Exception as e:
                print('Raise ERROR %s\nThe serial %s device is not alive,please checkout!' % (e, i))
        return devices_list
    if len(valid_serials) == 0:
        print("No available android devices detected.")
        return []


if __name__ == '__main__':
    print(get_connected_devices())
