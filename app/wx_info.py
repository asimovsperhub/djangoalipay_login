"""
一：微信官方登录页面
1。用户请求
https://open.weixin.qq.com/connect/qrconnect?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect

appid:''
scope: "snsapi_login"
redirect_url   :请使用urlEncode对链接进行处理
response_type: 'code'
2.用户授权后，回调地址带code和state


二：网站内集成微信登录二维码
1.引入js
http://res.wx.qq.com/connect/zh_CN/htmledition/js/wxLogin.js
2.实例js对象
var obj = new WxLogin({
 self_redirect:true,
 id:"login_container", #页面显示二维码的容器id
 appid: " ",
 scope: "snsapi_login",
 redirect_uri: "",
  state: "",
 style: "",
 href: ""
 });


三；code换access_token
请求页面：
https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code

appid ：' '
secret	：	应用密钥AppSecret，在微信开放平台提交应用审核通过后获得
code	：	第一二步回调地址返回的code
grant_type ： authorization_code


respone：
{
"access_token":"ACCESS_TOKEN",   接口调用凭证
"expires_in":7200,
"refresh_token":"REFRESH_TOKEN",  	access_token接口调用凭证超时时间， 单位（秒）
"openid":"OPENID",              授权用户唯一标识
"scope":"SCOPE",                用户授权的作用域(需求)，使用逗号（,）分隔
"unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"   当且仅当该网站应用已获得该用户的userinfo授权时，才会出现该字段
}


2.刷新access_token有效期

1. 若access_token已超时，那么进行refresh_token会获取一个新的access_token，新的超时时间；
2. 若access_token未超时，那么进行refresh_token不会改变access_token，但超时时间会刷新，相当于续期access_token。


https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN

appid:
grant_type:refresh_token
#refresh_token拥有较长的有效期（30天），当refresh_token失效的后，需要用户重新授权。
refresh_token:刷新上一步返回的refresh_token长效凭证时间



四：通过access_token调用用户信息snsapi_userinfo

http请求方式: GET
https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID

access_token ：调用凭证
openid		： 普通用户的标识，对当前开发者帐号唯一
lang		： 国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语，默认为zh-CN


respone:
{
"openid":"OPENID",
"nickname":"NICKNAME",
"sex":1,
"province":"PROVINCE",
"city":"CITY",
"country":"COUNTRY",
"headimgurl": "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
"privilege":[
"PRIVILEGE1",
"PRIVILEGE2"
],
"unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL" : 用户统一标识。针对一个微信开放平台帐号下的应用，同一用户的unionid是唯一的

}



沙箱环境入口


小程序有测试号系统沙盒环境：

测试号管理 | 微信公众平台

https://developers.weixin.qq.com/sandbox

公众号开发也有测试号沙盒环境

微信公众平台

https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login

"""


import requests

from Bas import settings


class Wxlogin_info():
    # 微信开发者id
    appid = settings.AppID_wx
    appsecret = settings.AppSecret_wx

    # code=''
    # state=''
    def get_info(self):
        # 1.获取code,和state
        try:
            #
            self.code = self.request.GET.get('code')
            self.state = self.request.GET.get('state')
        except Exception as  e:
            print("获取参数code,state错误", e)
        # 2.code换access_token

        try:
            # https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
            access_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
            params = {
                'appid': self.appid,
                'secret': self.appsecret,
                'code': self.code,
                'grant_type': 'authorization_code'
            }
            # 请求re_url,将返回的数据序列化
            res = requests.get(access_url, params=params).json()
            # 获取access_token
            #global access_token
            access_token = res['access_token']
            # 获取unionid。
            #global unionid
            unionid = res['unionid']
            #
            #global openid
            openid = res['openid']
            # 长效凭证
            #global refresh_token
            refresh_token = res['refresh_token']
        except Exception as e:
            print("获取参数access_token错误",e)

        # 3.刷新refresh_token长效凭证过期，通过access_token获取的refresh_token
        try:
            # https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN
            re_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'
            params = {
                'appid': self.appid,
                'grant_type': 'authorization_code',
                'refresh_token': refresh_token
            }
            # 请求re_url,将返回的数据序列化
            res = requests.get(re_url, params=params).json()
            # 获取新的长效凭证
            refresh_token_new = res['refresh_token']
        except Exception as e:
            print("获取参数错误refresh_token",e)
        # 4。获取用户信息
        try:
            # https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID
            user_info_url = 'https://api.weixin.qq.com/sns/userinfo'
            params = {
                'access_token': access_token,
                'openid': openid
            }
            res = requests.get(user_info_url, params=params).json()
            #global user_info
            user_info = []
            # 遍历dict中的所有value
            for value in res.values():
                # 将iso8859-1码转换成utf-8
                value = value.encode('iso8859-1').decode('utf-8')
                user_info.append(value)
        except Exception as e:
            print("获取用户信息失败",e)

        return unionid, user_info
