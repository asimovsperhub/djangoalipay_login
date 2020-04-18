# 私钥
import traceback

from Bas import settings

# 应用私钥
app_private_key_string = open("/Users/apple/PycharmProjects/untitled_bas/Bas/app_private_key_string.pem").read()

# 支付宝公钥
ali_public_key_string = open('/Users/apple/PycharmProjects/untitled_bas/Bas/ali_public_key.pem').read()

import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.constant.ParamConstants import *

# 日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')

# 实例化客户端
alipay_client_config = AlipayClientConfig()
alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
# appid
alipay_client_config.app_id = settings.APPID_zfb
# 应用私钥
alipay_client_config.app_private_key = app_private_key_string
# 支付宝公钥
alipay_client_config.alipay_public_key = ali_public_key_string
# 初始化DefaultAlipayClient
client = DefaultAlipayClient(alipay_client_config, logger)


# code换token
def auth_token(auth_code):
    """
    :param auth_code: 支付宝回调带的参数
    :return:
    """
    from alipay.aop.api.response.AlipaySystemOauthTokenResponse import AlipaySystemOauthTokenResponse
    from alipay.aop.api.request.AlipaySystemOauthTokenRequest import AlipaySystemOauthTokenRequest

    request = AlipaySystemOauthTokenRequest()

    request.code = auth_code

    request.grant_type = "authorization_code"

    # 执行API调用,即向支付宝发送请求
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc(), e)
    if not response_content:
        print("failed execute")
    else:
        response = AlipaySystemOauthTokenResponse()
        # 解析响应结果
        response.parse_response_content(response_content)
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            auth_token = response.access_token
            return auth_token
        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)


# 通过token获取user_info
def user_info(auth_token):
    """
    :param auth_token前端点击链接，操作完，支付宝会带参数(auth_code)返回到回调页面
    :return:
    """

    from alipay.aop.api.request.AlipayUserInfoShareRequest import AlipayUserInfoShareRequest
    from alipay.aop.api.response.AlipayUserInfoShareResponse import AlipayUserInfoShareResponse

    # 构造请求参数对象
    # # 接口alipay.user.info.share获取用户信息）
    request = AlipayUserInfoShareRequest()
    # 初始化一个空字典，用与保存参数
    udf_params = dict()
    # 添加auth_token到字典 中
    udf_params[P_AUTH_TOKEN] = auth_token
    # 将udf_params字典参数添加到请求request中,即此时request(biz_model,udf_params)
    request.udf_params = udf_params

    # 执行API调用
    try:
        # 执行接口请求()
        # global response_content
        response_content = client.execute(request)
        # user_info=response_content.get('user_id')
        # print(response_content)
    except Exception as e:
        print(traceback.format_exc())

    if not response_content:
        print("failed execute")
    else:
        response = AlipayUserInfoShareResponse()
        # 解析响应结果
        response.parse_response_content(response_content)
        # 响应成功的业务处理
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            return [response.user_id, response.nick_name, response.gender, response.province, response.city,
                    response.avatar]
        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)


# 创建订单
def Trade_Create(out_trade_no, total_amount, subject, buyer_id):
    """
    :param out_trade_no:
    :param total_amount:
    :param subject:
    :param buyer_id:
    :return:
    """

    from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
    from alipay.aop.api.request.AlipayTradeCreateRequest import AlipayTradeCreateRequest
    from alipay.aop.api.response.AlipayTradeCreateResponse import AlipayTradeCreateResponse

    # 构造请求参数对象

    # 创建实例化订单对象
    model = AlipayTradeCreateModel()
    # 订单号
    model.out_trade_no = out_trade_no
    # 总价价
    model.total_amount = total_amount
    # 商品名
    model.subject = subject
    # 买家id
    model.buyer_id = buyer_id
    request = AlipayTradeCreateRequest(biz_model=model)

    # 执行API调用
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc(), e)

    if not response_content:
        print("failed execute")
    else:
        # 解析响应结果
        response = AlipayTradeCreateResponse()
        response.parse_response_content(response_content)
        # 响应成功的业务处理
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            print("get response trade_no:" + response.trade_no)
        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)


# 支付接口
def Trade_PagePay(out_trade_no, total_amount, subject, buyer_id):
    """
    :param out_trade_no:
    :param total_amount:
    :param subject:
    :param buyer_id:
    :return:
    """
    from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
    from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
    from alipay.aop.api.response.AlipayTradePagePayResponse import AlipayTradePagePayResponse

    # 构造请求参数对象

    # 实例化参数Model对象
    model = AlipayTradePagePayModel()
    # 订单号(保证唯一性)
    model.out_trade_no = out_trade_no
    # 单价
    model.total_amount = total_amount
    # 商品名
    model.subject = subject
    # 买家id
    model.buyer_id = buyer_id
    request = AlipayTradePagePayRequest(biz_model=model)
    # 用户确认支付后，支付宝通过 get 请求 returnUrl（商户入参传入），返回同步返回参数
    request.return_url = ''
    # 交易成功后，支付宝通过 post 请求 notifyUrl（商户入参传入），返回异步通知参数
    request.notify_url = ''
    # 执行API调用
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc(), e)

    if not response_content:
        print("failed execute")
    else:
        # 解析响应结果
        response = AlipayTradePagePayResponse()
        response.parse_response_content(response_content)
        # 响应成功的业务处理
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            print("get response trade_no:" + response.trade_no)
        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)


# 订单查询
def Trade_Query(out_trade_no, trade_no):
    """
    :param out_trade_no:
    :param trade_no:
    :return:
    """
    from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
    from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
    from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse

    model = AlipayTradeQueryModel()
    # 商户订单号
    model.out_trade_no = out_trade_no
    # 支付宝交易号，和商户订单号不能同时为空
    model.trade_no = trade_no
    request = AlipayTradeQueryRequest(biz_model=model)
    # 执行API调用
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc(), e)
    if not response_content:
        print("failed execute")
    else:
        # 解析响应结果
        response = AlipayTradeQueryResponse()
        response.parse_response_content(response_content)
        # 响应成功的业务处理
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            print("get response trade_no:" + response.trade_no)
        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

# 退款


if __name__ == '__main__':
    # auth_token = auth_token(auth_code='7c9636e1394a4b8293d938e933d5SE29')
    # # 获取用户信息
    # user_infos = user_info(auth_token)
    # print(user_infos[0])
    # ['https://tfs.alipayobjects.com/images/partner/T1j7pDXkhcXXXXXXXX', '深圳市', 'm', 'w b', '广东省', None, None]
    pass
