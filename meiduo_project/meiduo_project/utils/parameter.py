class SETTING_TIME:
    # 过期时间
    IMAGE_CODE_REDIS_EXPIRES = 180  # 图片验证码过期时间
    SMS_CODE_REDIS_EXPIRES_YUNTONGXUN = 5  # 云通信短信验证码过期时间(分钟)
    SMS_CODE_REDIS_EXPIRES_REDIS = 300  # redis短信验证码保存时间
    SMS_CODE_REDIS_EXPIRES_FLAG = 60  # redis保存send_flag的时间
    COOKIE_USERNAME_EXPIRES = 3600 * 24 * 3  # username的cookie过期时间


class SETTING_CODE:
    SMS_TEMPLATES = 1  # 短信验证码模板号码
    SMS_FLAG_SEND = 1  # 短信验证码已发送标识


class PAGE:
    USER_CENTER_ORDERS_PAGE = 5
