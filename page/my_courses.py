# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/7/2 2:00 下午
    @Description: 我的课程页
"""
from core.Decorator import *
from page.login import LoginPage


class MyCoursesPage(BasePage):

    def __init__(self):
        if LoginPage().check_need_login():
            print("检测到未登录，开始执行登录>>>>>")
            LoginPage().input_phone("18820200001").input_password("qwer1234").submit_login()
            print("登录成功，执行后续逻辑")
        print("用户已登录，执行后续逻辑")

    def course_item(self, course_name):
        if self.find_element_by_swipe_up(self.d(text=course_name), max_swipe=10).exists:
            self.d(text=course_name).click()
        # 处理 联系老师 弹窗
        self.d(resourceId="com.genshuixue.student:id/student_dialog_fragment_class_group_close").click_exists()
        return self

    def live_entry(self, course_type):
        if self.find_element_by_swipe_up(self.d(text=course_type), max_swipe=10).exists:
            self.d(text=course_type).click()
        return self
