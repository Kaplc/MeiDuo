# 定义任务
from django.middleware.csrf import logger

from celery_tasks.sms.yuntongxun.CCP_REST_DEMO.SDK.ccp_sms import CCP
from .code import SETTING_CODE, SETTING_TIME
from ..main import celery_app


# 使用装饰器定义任务
@celery_app.task(name='celery_send_message_code')  # 定义name=send_message_code别名
def celery_send_message_code(mobile, sms_code):
    """
    异步发送短信验证码
    :param mobile: 要发送的手机号
    :param sms_code: 发送内容
    :return: 返回发送结果
    """

    send_res = ''

    try:
        send_res = CCP().send_template_sms(mobile, [sms_code, SETTING_TIME.SMS_CODE_REDIS_EXPIRES_YUNTONGXUN],
                                           SETTING_CODE.SMS_TEMPLATES)
    except Exception as error:
        logger.error(error)
    finally:
        return send_res
