# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import os

import yaml


# configPath = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "../../resources/config.yaml")
# )


# 获取config.yaml中的各项配置

class ReadConfig:
    def __init__(self):
        self.cf = YamlUtil("../../resources/config.yaml").load_yaml()

    def get_method(self):
        value = self.cf.get("DEVICES").get('method')
        return value

    def get_server_url(self):
        value = self.cf.get("DEVICES").get("server")
        return value

    def get_server_token(self):
        value = self.cf.get("DEVICES").get("token")
        return value

    def get_server_udid(self):
        value = self.cf.get("DEVICES").get("udid")
        return value.split('|')

    def get_devices_ip(self):
        value = self.cf.get("DEVICES").get("IP")
        return value.split('|')

    def get_apk_url(self):
        value = self.cf.get("APP").get("apk_url")
        return value

    def get_apk_path(self):
        value = self.cf.get("APP").get("apk_path")
        return value

    def get_pkg_name(self):
        value = self.cf.get("APP").get("pkg_name")
        return value

    def get_testdata(self, name):
        value = self.cf.get("TESTDATA").get(name)
        return value.split('|')

    def get_monkey_runner(self):
        value = self.cf.get("Monkey").get("runner")
        return value

    def get_monkey_is_single(self):
        value = self.cf.get("Monkey").get("is_single")
        return value

    def get_monkey_schema(self):
        value = self.cf.get("Monkey").get("schema")
        return value

    def get_monkey_white_activity(self):
        value = self.cf.get("Monkey").get("white_activity")
        return value

    def get_monkey_main_activity(self):
        value = self.cf.get("Monkey").get("main_activity")
        return value

    def get_monkey_widget(self):
        value = self.cf.get("Monkey").get("widget")
        return value

    def get_monkey_internal(self):
        value = self.cf.get("Monkey").get("internal")
        return value

    def get_monkey_max_time(self):
        value = self.cf.get("Monkey").get("max_time")
        return value

    def get_monkey_events(self):
        value = self.cf.get("Monkey").get("events")
        return value


# 解析yaml文件，返回dict
class YamlUtil:

    def __init__(self, path):
        self._path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), path)
        )

    def load_yaml(self):
        x = ''
        try:
            with open(self._path) as f:
                x = yaml.safe_load(f)
        except Exception as e:
            print(e)
        finally:
            f.close()

        return x

    def dump_yaml(self, obj):
        try:
            with open(self._path, "w") as f:
                yaml.safe_dump(obj, f)
        except Exception as e:
            print(e)
        finally:
            f.close()


if __name__ == '__main__':
    print(ReadConfig().get_pkg_name())
    print(ReadConfig().get_testdata('user_name'))
    # print(ReadConfig().get_server_udid())
