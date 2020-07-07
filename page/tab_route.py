# coding:utf-8
"""
    @Author:  guozhiwen
    @Date:  2020/7/2 2:02 下午
    @Description:  
"""

from core.Decorator import *
from page.online_courses import OnlineCoursesPage
from page.my_courses import MyCoursesPage


class TabRoutes(BasePage):
    def __init__(self):
        # 处理更新弹窗
        if self.d(resourceId='com.genshuixue.student:id/dialog_update_btn_close').exists:
            self.d(resourceId='com.genshuixue.student:id/dialog_update_btn_close').click()
        # 处理鼓励弹窗
        if self.d(resourceId='com.genshuixue.student:id/dialog_comment_app_btn_refuse').exists:
            self.d(resourceId='com.genshuixue.student:id/dialog_comment_app_btn_refuse').click()

    def to_online_courses(self):
        try:
            self.d(resourceId='com.genshuixue.student:id/student_activity_main_home_page_container').click_exists(1)
            print("跳转我的在线好课页面")
            return OnlineCoursesPage()
        except Exception:
            raise Exception('jump to online courses page error')

    def to_my_courses(self):
        try:
            self.d(resourceId='com.genshuixue.student:id/student_activity_main_my_course_container').click_exists(1)
            print("跳转我的课程页面")
            return MyCoursesPage()
        except Exception:
            raise Exception('jump to my courses page error')
