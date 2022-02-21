import smtplib
import requests
from html import escape
from email.mime.text import MIMEText


class Message:

    def __init__(self, subject, content, qq, pushplus, tg, ftqq):
        self.subject = subject
        self.content = content
        self.init_setattr(qq)
        self.init_setattr(pushplus)
        self.init_setattr(tg)
        self.init_setattr(ftqq)
        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
        })

    def init_setattr(self, kw: dict):
        for k in kw:
            self.__setattr__(k, kw[k])

    def init_content_to_html(self):
        template = ''
        for s in self.content.split('\n'):
            indent = s.count(' ')
            s = s.strip()
            template += f'<div style="margin-bottom: -10px;"><font size="1" face="黑体">{indent * "&nbsp; "}{s}</font></div>'
        return template

    def init_content_to_tg(self):
        """
            发送内容大小限制4096 分块发送
        """
        content_block = []
        b = []
        for i, t in enumerate(self.content, 1):
            b.append(t)
            if i % 4096 and i != len(self.content):
                continue
            content_block.append(''.join(b))
            b = []
        return content_block

    def qqemail(self):
        """
            QQ邮箱接收推送消息
            消息自己发给自己
        """
        msg = MIMEText(self.init_content_to_html(), 'html')  # 生成一个MIMEText对象
        msg['subject'] = self.subject  # 放入邮件主题
        msg['from'] = self.msg_from  # 放入发件人
        msg['to'] = self.msg_to  # 放入收件人
        try:
            # 通过ssl方式发送，服务器地址，端口
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            # 登录到邮箱
            s.login(self.msg_from, self.password)
            # 发送邮件 发送方 收件方 要发送的消息
            s.sendmail(self.msg_from, self.msg_to, msg.as_string())
            # 关闭会话
            s.quit()
        except smtplib.SMTPException as e:
            print(e)

    def pushplus(self):
        """
            utils/config.py 消息推送配置
            微信扫码登录 http://www.pushplus.plus/
            一对一推送 复制自己的token
            pushplus微信公众号接收推送消息
        """
        try:
            url = 'http://www.pushplus.plus/api/send'
            data = {
                "channel": "wechat",
                "content": self.init_content_to_html(),
                "template": "html",
                "title": self.subject,
                "token": self.token,
                "webhook": ""
            }
            resp = requests.post(url, json=data, headers={
                'Content-Type': 'application/json'
            })
            print(resp.json())
        except Exception as e:
            print(e)

    def tgbot(self):
        try:
            if (
                    not (self.chat_id.isdigit() or self.chat_id[0] == '-' and self.chat_id[1:].isdigit())
                    and self.chat_id[0] != '@'
            ):
                self.chat_id = "@" + self.chat_id
            if not self.tg_api:
                self.tg_api = "https://api.telegram.org"
            if self.tg_api.find('://') == -1:
                self.tg_api = "https://" + self.tg_api
            if self.tg_api[-1] == '/':
                self.tg_api = self.tg_api[:-1]
            url = f'{self.tg_api}/bot{self.bot_token}/sendMessage'
            for block in self.init_content_to_tg():
                data = {
                    'chat_id': self.chat_id,
                    'text': escape(block),
                    'parse_mode': 'HTML'
                }
                resp = self.session.post(url=url, data=data)
                print(resp.json())
        except Exception as e:
            print(e)

    def ftqq(self):
        try:
            url = f'https://sctapi.ftqq.com/{self.sendkey}.send'
            data = {
                'title': self.subject,
                'desp': self.content.replace('\n', '\n\n'),
                'channel': self.channel,
                'openid': self.openid
            }
            resp = self.session.post(url=url, data=data)
            print(resp.json())
        except Exception as e:
            print(e)

    def run(self):
        try:
            from .sendNotify import send
            print(self.subject)
            print(self.content)
            send(self.subject, self.content.replace('\n', '\n\n'))
        except Exception as err:
            print(str(err))
            print("无推送文件")

        if self.token:
            self.pushplus()
        if self.msg_from and self.password and self.msg_to:
            self.qqemail()
        if self.bot_token and self.chat_id:
            self.tgbot()
        if self.sendkey:
            self.ftqq()


def getMessage(content):
    from utils.config import push_message_conf
    return Message('联通每日任务', content, **push_message_conf)


if __name__ == "__main__":
    pass
