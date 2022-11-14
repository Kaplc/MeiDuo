# -*- coding:utf-8 -*-

from celery_tasks.sms.yuntongxun.CCP_REST_DEMO.SDK.CCPRestSDK import REST

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8aaf0708842397dd01846bb99c1f17f9'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = 'da899db136824904a929ac6ee28f883d'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8aaf0708842397dd01846bc1f9311805'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'app.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = '8883'

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'


# 云通讯官方提供的发送短信代码实例
# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id
def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(_serverIP, _serverPort, _softVersion)
    rest.setAccount(_accountSid, _accountToken)
    rest.setAppId(_appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    print(result)
    for k, v in result.items():

        if k == 'templateSMS':
            for k, s in v.items():
                print('%s:%s' % (k, s))
        else:
            print('%s:%s' % (k, v))


# 封装成单例节省资源
class CCP(object):
    """发送短信的单例类"""

    # __new__在__init__前调用
    # cls表示类表示创建出来的实例, self才是实例
    def __new__(cls, *args, **kwargs):
        """判断是否存在类属性_instance, _instance是类CCP唯一对象"""

        # hasattr(对象名, 属性): 判断对象有无该属性
        if not hasattr(CCP, "_instance"):
            # 为该类设置_instance属性
            # super()使用cls的mro顺序(CCP, object)的CCP的父类, 就是object的__new__方法
            # 为对象分配内存空间和返回对象的引用给cls._instance(对象的地址类似)
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)

            # 初始化sendTemplateSMS函数,
            # rest属性绑定到单例cls._instance中实现一起销毁和生成
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)
        return cls._instance

    # 在单例封装发送短信方法
    def send_template_sms(self, to, datas, temp_id):
        """

        :param to: 注册手机号
        :param datas: 数据内容['验证码', 过期时间)
        :param temp_id: 模板id
        :return: 结果
        """

        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        if result.get("statusCode") == "000000":
            # 返回0，表示发送短信成功
            return 0
        else:
            # 返回-1，表示发送失败
            return -1



if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1
    sendTemplateSMS('18475754696', ['123456', 5], 1)
