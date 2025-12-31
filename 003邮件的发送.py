from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL


def send_email(sender_qq, pwd, sender, receiver, mail_content, mail_title):
    """
    Q: 如何利用Python使用QQ邮箱发送邮件
    A: 使用邮箱的IMAP/SMTP服务，利用Python的email模块进行邮件发送
    """
    host_server = 'smtp.qq.com'
    smtp = SMTP_SSL(host_server)  # SSL登录smtp服务器
    smtp.set_debuglevel(1)        # 参数值1开启调试模式，参数值0关闭
    smtp.ehlo(host_server)        # 启动用户认证
    smtp.login(sender_qq, pwd)    # 用户登录

    msg = MIMEText(mail_content, "plain", 'utf-8')   # 构造邮件内容
    msg["Subject"] = Header(mail_title, 'utf-8')     # 邮件标题
    msg["From"] = sender    # 发送者
    msg["To"] = receiver    # 收件者

    smtp.sendmail(sender, receiver, msg.as_string())  # 发送邮件
    smtp.quit()


if __name__ == "__main__":
    try:
        send_email('qq号', '授权码', '本人@qq.com', '收件@qq.com', '邮件内容', '标题')
    except BaseException as e:
        print(e)
