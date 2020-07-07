# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description:
"""
import logging
import os


class Log:
    @classmethod
    def set_logger(cls, udid, path: str):
        logger = logging.getLogger('GSX')
        logger.setLevel(logging.DEBUG)
        if not path.startswith('/'):
            path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../log/{0}".format(path))
            )
        fh = logging.FileHandler(path, encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s'
                                      + ' - %s' % udid
                                      + ' - %(levelname)s'
                                      + ' - %(message)s')

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        cls.logger = logger

    def d(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def i(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)
        # print(msg, *args, **kwargs)

    def w(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def c(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def e(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    @staticmethod
    def get_log_path():
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../log")
        )

    @staticmethod
    def get_root_path():
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../")
        )


if __name__ == '__main__':
    print(os.path.abspath(
        os.path.join(os.path.dirname(__file__), "client.log")))