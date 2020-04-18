import functools
from urllib import parse

from django.shortcuts import render, redirect

# Create your views here.
from Bas import settings
from app.ali_info import auth_token, user_info
from app.models import Userinfo

from app.wx_info import Wxlogin_info


def login_wx(request):
    # 微信开发者id
    appid = settings.AppID_wx
    # 作用域,网页应用目前仅填写snsapi_login
    scope = 'snsapi_login'
    # 回调地址，使用urlEncode对链接进行处理
    # redirect_uri = parse.urlencode(settings.REDIRECT_URI_wx)
    redirect_uri = settings.REDIRECT_URI_wx
    # 该参数可用于防止csrf攻击
    state = 'yanzhi'

    return render(request, 'login.html', {'appid': appid,
                                          'scope': scope,
                                          'redirect_uri': redirect_uri,
                                          'state': state})


def User_info_wx(request):
    """
    微信：

    :param request:
    :return:
    """
    user = Wxlogin_info()

    user_info = user.get_info()

    return render(request, 'user_info.html', locals())


def User_info_zfb(request):
    """
    支付宝：
    获取返回的数据并保存到数据库，重定向到用户中心
    :param request:
    :return:
    """
    # 获取auth_code
    auth_code = request.GET.get('auth_code')
    # code换access_token
    auth_tokens = auth_token(auth_code)
    # 获取用户信息
    user_info_zfbs = user_info(auth_tokens)
    userinfo_check = Userinfo.objects.filter(user_id=user_info_zfbs[0])
    if not userinfo_check:
        userinfo = Userinfo()
        userinfo.user_id = user_info_zfbs[0]
        userinfo.nike_name = user_info_zfbs[1]
        userinfo.gender = user_info_zfbs[2]
        userinfo.province = user_info_zfbs[3]
        userinfo.city = user_info_zfbs[4]
        userinfo.avatar = user_info_zfbs[5]
        userinfo.save()
    return redirect('/user/%s' % user_info_zfbs[0])





# 用户中心
def User(request, **kwargs):
    user_id = kwargs['user_id']
    userinfos = Userinfo.objects.filter(user_id=int(user_id))
    return render(request, 'user_info.html', {'userinfos': userinfos})

#
# def core(request):
#     #@functools.wraps()
#     return render(request,'core.html')


