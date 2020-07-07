# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/6/19 12:11 下午
    @Description: 登录页
"""
from core.Decorator import *
from core.BasePage import BasePage


class LoginPage(BasePage):

    def check_need_login(self):
        if self.d(text='登录/注册').exists or self.d(text='手机登录').exists:
            self.d(text='登录/注册').click_exists(3)
            self.d(text='手机登录').click_exists(3)
            return True
        else:
            return False

    def input_phone(self, phone):
        if self.d(resourceId="com.genshuixue.student:id/student_fragment_input_edit_phone").wait(timeout=3):
            print('输入手机号:%s ,并点击下一步' % phone)
            self.d(resourceId="com.genshuixue.student:id/student_fragment_input_edit_phone") \
                .set_text(phone)
            self.d(resourceId="com.genshuixue.student:id/student_fragment_input_next").click()
        return self

    def input_password(self, passwd):
        self.d.implicitly_wait(3)
        if self.d(resourceId="com.genshuixue.student:id/student_fragment_input_edit_password").wait(timeout=3):
            print('输入密码:%s' % passwd)
            self.d(resourceId="com.genshuixue.student:id/student_fragment_input_edit_password") \
                .set_text(passwd)
            # 通过keycode事件收起软键盘，避免遮挡其他控件
            self.d.press("back")
        return self

    def submit_login(self):
        print('点击登录按钮')
        self.d(resourceId="com.genshuixue.student:id/student_fragment_input_password_login").click_exists()
        return self


def login(phone, passwd):
    LoginPage().input_phone(phone).input_password(passwd).submit_login()