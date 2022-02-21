# -*- coding: utf8 -*-
import time
import json
import execjs
import requests
from random import choices
from utils.common import Common
from utils.config import BASE_DIR,account_json
from utils.toutiao_sdk import getSign


class UnicomClient(Common):

    def __init__(self, mobile, password):
        super(UnicomClient, self).__init__()
        self.mobile = mobile
        self.password = password
        self.version = "android@8.0805"
        infos = account_json.get(self.mobile, '') or self.getDeviceId
        # 设备ID(通常是获取手机的imei) 联通判断是否登录多台设备 不能多台设备同时登录 填写常用的设备ID
        self.deviceId=infos['IMEI']
        self.useragent = "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 SE Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36; unicom{version:%s,desmobile:%s};devicetype{deviceBrand:Xiaomi,deviceModel:MI 8 SE};{yw_code:}" % (
            self.version,
            self.mobile,
        )

        self.session = requests.Session()
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "okhttp/4.4.0"
        })
        self.global_config = self.readCookie(self.mobile + "WoGame")
        if not isinstance(self.global_config, dict) or not self.global_config.get('cookie', '')\
                or 'cookie' not in self.global_config or 'd_deviceCode'  not in self.global_config['cookie']:
            self.login()
        else:

            self.deviceId = self.global_config['cookie']['d_deviceCode']
            self.session.cookies.update(self.global_config['cookie'])
        if not (self.session.cookies.get('jwt', False) and self.session.cookies.get('ecs_token', False)):
            raise Exception('[UnicomClient]未登录状态')
        self.last_login_time = time.strftime(
            "%Y-%m-%d",
            time.localtime(
                int(self.global_config['online']['reqtime']) / 1000
            )
        )

    def onLineConf(self, item):
        return {
            "reqtime": str(self.timestamp),
            "provinceChanel": "general",
            "appId": self.getAppId(),
            "netWay": "4G",
            "deviceModel": "MI 8 SE",
            "step": "dingshi",
            "deviceCode": self.deviceId,
            "version": self.version,
            "deviceId": self.deviceId,
            "deviceBrand": "Xiaomi",
            "token_online": item['token_online']
        }

    def getAppId(self):
        with open(BASE_DIR + '/utils/appId.json', 'r', encoding='utf8') as fp:
            appIds = json.loads(fp.read())  # type: dict
        if not appIds.get(self.mobile, False):
            raise Exception('[UnicomClient]获取appId失败')
        return appIds.get(self.mobile)

    def JSEncrypt(self, message):
        with open(BASE_DIR + '/utils/unicom.js', 'r', encoding='utf8') as fp:
            js = fp.read()
        ctx = execjs.compile(js)
        result = ctx.call('RSAEncrypt', message)
        return result

    def checklogin(self):
        url = 'https://m.client.10010.com/mobileService/checklogin.htm'
        resp = self.session.get(url=url)
        result = resp.json()
        print(result)
        return result.get('islogin', False)

    def login(self):
        self.session.cookies.clear_session_cookies()
        for k in self.session.cookies.get_dict():
            self.session.cookies.pop(k)
        url = 'https://m.client.10010.com/mobileService/login.htm'
        data = {
            "simCount": "1",
            "yw_code": "",
            "deviceOS": "android8.1.0",
            "mobile": self.JSEncrypt(self.mobile),
            "netWay": "4G",
            "deviceCode": self.deviceId,
            "isRemberPwd": "true",
            "version": self.version,
            "deviceId": self.deviceId,
            "password": self.JSEncrypt(self.password),
            "keyVersion": "",
            "pip": "10." + '.'.join([str(v) for v in choices(range(1, 255), k=3)]),
            "provinceChanel": "general",
            "appId": self.getAppId(),
            "deviceModel": "MI 8 SE",
            "deviceBrand": "Xiaomi",
            "timestamp": time.strftime('%Y%m%d%H%M%S', time.localtime(self.timestamp / 1000))
        }
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        result = resp.json()
        if result.get('token_online', False):
            self.global_config = {
                'online': {
                    "token_online": result['token_online'],
                    "reqtime": str(self.timestamp)
                },
                'cookie': self.session.cookies.get_dict()
            }
            self.saveCookie(self.mobile + "WoGame", self.global_config)
        else:
            print(resp.text)

    def onLine(self):
        self.session.cookies.clear_session_cookies()
        for k in self.session.cookies.get_dict():
            self.session.cookies.pop(k)
        url = 'https://m.client.10010.com/mobileService/onLine.htm'
        data = self.onLineConf(self.global_config['online'])
        resp = self.session.post(url=url, data=data)
        resp.encoding = 'utf8'
        result = resp.json()
        if result.get('token_online', False):
            self.global_config = {
                'online': {
                    "token_online": result['token_online'],
                    "reqtime": str(self.timestamp)
                },
                'cookie': self.session.cookies.get_dict()
            }
            self.saveCookie(self.mobile + "WoGame", self.global_config)
        else:
            print(resp.text)

    def taskcallbackquery(self, acId, taskId, accountChannel=""):
        """
            androidCodeId: c,
            iosCodeId: i,
            acId: a,
            taskId: n,
            remark: r,
            channel: "GGPD",
            channelName: o,
            rewards: !0,
            unWantedToast: !1,
            unWantedToast2: !1,
            accountChannel: "517050707",
            accountUserName: "5170507071",
            accountPassword: "123456",
            accountToken: "638d17ae37a648e9a786bb973d1c4c7b",
        """
        url = 'https://m.client.10010.com/taskcallback/taskfilter/query'
        data = {
            "arguments1": acId,  # "AC20200728150217",
            "arguments2": "GGPD",
            "arguments3": taskId,  # "96945964804e42299634340cd2650451",
            "arguments4": str(self.timestamp),
            "arguments6": accountChannel,
            "version": self.version,
            "netWay": "4G",
        }
        data["sign"] = getSign(data)
        resp = self.session.post(url=url, data=data, headers={
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'okhttp/4.4.0'
        })
        resp.encoding = 'utf8'
        result = resp.json()
        print(result)
        # if result['code'] == '9996':
        #     self.onLine()
        #     return
        if result['code'] == '0000' and not int(result.get('timeflag')) and int(result.get('givePercentage', 0)) != 100:
            # int(result.get('achieve')) != int(result.get('allocation')):
            return True
        return False

    def taskcallbackdotasks(
            self, acId, taskId,
            orderId, remark, accountChannel="",
            accountUserName="", accountPassword="", accountToken=""
    ):
        url = 'https://m.client.10010.com/taskcallback/taskfilter/dotasks'
        data = {
            "arguments1": acId,
            "arguments2": "GGPD",
            "arguments3": taskId,
            "arguments4": str(self.timestamp),
            "arguments6": accountChannel,
            "arguments7": accountUserName,
            "arguments8": accountPassword,
            "arguments9": accountToken,
            "orderId": orderId,
            "netWay": "4G",
            "remark": remark,  # "游戏视频任务积分",
            "version": self.version
        }
        data["sign"] = getSign(data)
        resp = self.session.post(url=url, data=data, headers={
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'okhttp/4.4.0'
        })
        resp.encoding = 'utf8'
        result = resp.json()
        print(result)

    def run(self):
        self.onLine()


if __name__ == '__main__':
    pass
