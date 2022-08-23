"""
可通过腾讯云短信服务，来进行短信发送
1. 注册账号
2. 开通服务（认证等）
3. API/SDK方式
  api，接口 处理签名
  sdk，安装模块
"""


def send_sms(mobile, message) -> bool:
    """ 模拟发送消息请求 """
    print(f"手机号：{mobile}")
    print(f"验证码：{message}")
    if mobile and message:
        return True
    return False
