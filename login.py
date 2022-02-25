# -*- coding: utf8 -*-

from threading import Thread
from activity.unicom.dailySign import SigninApp
from utils.unicomLogin import UnicomClient

import json
import time
import requests
from utils.config import account_json,account
class LoginAgain(UnicomClient):
    """
        签到页积分任务
    """

    def __init__(self, mobile, password):
        super(LoginAgain, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "accept": "application/json, text/plain, */*",
            "origin": "https://img.client.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://img.client.10010.com/SigininApp/index.html",
            "x-requested-with": "com.sinovatech.unicom.ui"
        })
        self.login()

def Template(cls):
    # 联通手机号 服务密码 配置 (支持多账号)
    ts = []
    for key in account_json.keys():
        ts.append(Thread(target=cls(key, account_json[key]['password']).run))
    for t in ts:
        t.start()
    for t in ts:
        t.join()


def main_handler(event=None, context=None):
    """
        腾讯云函数每15分钟执行一次
    """

    # ----------------------------------------------------------------
    # 使用华为云函数工作流 (腾讯云函数、阿里函数计算 ip在获取积分接口被限制)
    # 联通每日签到
    Template(LoginAgain)

if __name__ == '__main__':

    main_handler("","")