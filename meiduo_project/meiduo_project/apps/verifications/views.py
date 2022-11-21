import random

from django import http
# Create your views here.
from django.template.base import logger
from django.views import View
from django_redis import get_redis_connection
from celery_tasks.sms.tasks import celery_send_message_code
from .libs.captcha.captcha import captcha
# noinspection PyUnresolvedReferences
from meiduo_project.utils.response_code import RETCODE
# noinspection PyUnresolvedReferences
from meiduo_project.utils.parameter import SETTING_CODE, SETTING_TIME


class SMSCodeView(View):
    """发送短信验证码"""

    def get(self, request, mobile_cli, image_code, uuid):
        """
        接收get请求
        :param uuid: uuid
        :param image_code: 图形验证码
        :param mobile_cli: 注册手机号码
        :param request: 请求对象
        :return: json
        """
        # 接收参数
        mobile = mobile_cli
        image_code_cli = image_code
        uuid_cli = uuid
        # 校验参数
        if not all([mobile, image_code_cli, uuid]):
            return http.JsonResponse({"code": RETCODE.NECESSARYPARAMERR, "errmsg": "缺少参数"})
        # 获取图形验证码
        redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            # 图形验证码不存在或过期
            return http.JsonResponse({"code": RETCODE.IMAGECODEERR, "errmsg": "图形验证码过期"})
        # bytes转字符串解码
        image_code_server = image_code_server.decode()
        # 对比图形验证码
        if not (image_code_server.lower() == image_code_cli.lower()):
            return http.JsonResponse({
                "code": RETCODE.IMAGECODEERR,
                "errmsg": "图形验证码错误"
            })
        # 删除图形验证码
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            # 自定义输出日志
            logger.error(e)
        # 判断发送倒计时是否结束
        send_flag = redis_conn.get('sms_send_flag_%s' % mobile)
        if not (send_flag is None):  # 频繁发送
            return http.JsonResponse({
                "code": RETCODE.THROTTLINGERR,
                "errmsg": "请求过于频繁"
            })
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 建立redis通道
        pl = redis_conn.pipeline()

        pl.setex('sms_%s' % mobile, SETTING_TIME.SMS_CODE_REDIS_EXPIRES_REDIS, sms_code)  # 保存短信验证码
        pl.setex('sms_send_flag_%s' % mobile, SETTING_TIME.SMS_CODE_REDIS_EXPIRES_FLAG,
                 SETTING_CODE.SMS_FLAG_SEND)  # 保存已经发送的标识
        # 执行通道
        pl.execute()

        # 发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, SETTING_TIME.SMS_CODE_REDIS_EXPIRES_YUNTONGXUN],
        #                         SETTING_CODE.SMS_TEMPLATES)
        # 调用celery异步发送短信验证码, 不能忘记delay()
        celery_send_message_code.delay(mobile, sms_code)

        # 响应结果
        response = {
            "code": "%s" % RETCODE.OK,
            "errmsg": "发送成功",
            "sms_code": sms_code,
        }

        return http.JsonResponse(response)


class ImageCode(View):
    """生成图形验证码"""

    def get(self, request, uuid):
        """
        接收get
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
