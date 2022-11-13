import random

from django import http

# Create your views here.
from django.template.base import logger
from django.views import View
from django_redis import get_redis_connection

from .libs.captcha.captcha import captcha
from settings.response_code import RETCODE
from settings.code import SETTING_CODE, SETTING_TIME
from .libs.yuntongxun.CCP_REST_DEMO.SDK.ccp_sms import CCP


class SMSCodeView(View):
    """发送短信验证码"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 注册手机号码
        :return: json
        """
        # 接收参数
        # 从表单获取imag_code
        image_code_cli = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 校验参数
        if not all([image_code_cli, uuid]):
            return http.JsonResponse({"code": RETCODE.NECESSARYPARAMERR, "errmsg": "缺少参数"})
        # 图形验证码储存到redis
        # 链接redis
        conn_redis = get_redis_connection('verify_code')
        # 提取图形验证码
        image_code_sever = conn_redis.get('img_%s' % uuid)
        if image_code_sever is None:
            # 图形验证码不存在或过期
            return http.JsonResponse({"code": RETCODE.IMAGECODEERR, "errmsg": "图形验证码过期"})
        # 删除图形验证码
        try:
            conn_redis.delete('img_%s' % uuid)
        except Exception as e:
            # 自定义输出日志
            logger.error(e)
        # 对比图形验证码
        # bytes转字符串
        image_code_sever = image_code_sever.decode()
        if image_code_sever != image_code_cli:
            return http.JsonResponse({"code": RETCODE.IMAGECODEERR, "errmsg": "图形验证码错误"})
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 保存短信验证码
        conn_redis.setex('sms_%s' % mobile, SETTING_TIME.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 发送短信验证码
        CCP().send_template_sms(mobile, [sms_code, SETTING_TIME.SMS_CODE_REDIS_EXPIRES], SETTING_CODE.SMS_TEMPLATES)
        # 响应结果
        response = {
            "code": "%s" % RETCODE.OK,
            "errmsg": "发送成功",
        }

        return http.JsonResponse(response)


class CheckImageCode(View):
    """校验图形验证码"""

    def det(self, request, image_code_cli, uuid):
        """

        :param request: 请求对象
        :param image_code_cli: 客户端填写的图形验证码
        :param uuid: uuid
        :return: json
        """
        # 校验参数
        if not all([image_code_cli, uuid]):
            return http.JsonResponse({"code": RETCODE.NECESSARYPARAMERR, "errmsg": "缺少参数"})

        # 获取图形验证码
        redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get('img_%s' % uuid)

        # 对比图形验证码
        if not (image_code_server == image_code_cli):
            return http.JsonResponse({
                "code": RETCODE.IMAGECODEERR,
                "errmsg": "图形验证码错误"
            })



class ImageCode(View):
    """生成图形验证码"""

    def get(self, request, uuid):
        """

        :param uuid: 用户和验证码图片绑定唯一标识
        :param request:
        :return: image/jpg
        """

        # 生成图形验证码
        text, image = captcha.generate_captcha()

        # 保存图形验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, SETTING_TIME.IMAGE_CODE_REDIS_EXPIRES, text)

        # 响应图形验证码
        return http.HttpResponse(image, content_type='image/age')
