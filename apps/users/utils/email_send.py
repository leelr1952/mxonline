# coding:utf-8
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from mxonline.settings import EMAIL_FROM


def random_str(randomlength):
    str = ''
    chars = 'QqWwEeRrTtYyUuIiOoPpAaSsDdFfGgHhJjKkLlZzXxCcVvBbNnMm0123456789'
    length = len(chars)
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type = 'register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = u'慕学在线网注册激活链接'
        email_body = u'请点击以下链接1233321321321完成注册：http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass

    elif send_type == 'forget':
        email_title = u'慕学在线网注册重置密码'
        email_body = u'请点击以下链接1233321321321完成密码重置：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

    elif send_type == 'update':
        email_title = u'慕学在线网邮箱修改验证码'
        email_body = u'哈哈哈,你修改邮箱的验证码为：{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass