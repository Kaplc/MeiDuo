from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from .contents import *
from apps.users.models import User
import logging

logger = logging.getLogger('django')



