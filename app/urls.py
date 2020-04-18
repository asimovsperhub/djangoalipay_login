from django.conf.urls import url
from django.urls import path, re_path

from app import views

urlpatterns = [
    path('login/', views.login_wx, name='login'),
    # 回调路由，获取返回数据
    url('^user_info_zfb', views.User_info_zfb, name='User_info_zfb'),
    url('^user_info_wx', views.User_info_wx, name='User_info_wx'),
    # 用户信息显示
    # path('user/<int:user_id>',views.User,name='User')
    # #
    # re_path
    path('core/',views.core)
]
