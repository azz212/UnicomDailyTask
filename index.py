# -*- coding: utf8 -*-

from threading import Thread
from activity.unicom.dailySign import SigninApp
from activity.unicom.integralTask import IntegralTask
from activity.unicom.watchAddFlow import WatchAddFlow
from activity.unicom.superSimpleTask import SuperSimpleTask
from activity.unicom.unicomTurnCard import TurnCard
from activity.unicom.unicomTurnTable import TurnTable
from activity.unicom.unicomZhuaWaWa import ZhuaWaWa
from activity.unicom.sheggMachine import SheggMachine
from activity.unicom.blindBox import BlindBox
from activity.unicom.unicomSignerTask import SignerTask
from activity.unicom.zhuanjifenWeiBo import ZJFWeiBo
from activity.unicom.qiandao11 import QianDao11
from activity.unicom.wotree import Wotree

from activity.woread.luckdraw import LuckDraw
from activity.woread.openbook import OpenBook
from activity.woread.readluchdraw import ReadLuchDraw
from activity.woread.thanksgiving import ThanksGiving
from activity.woread.prizedetail import Prize
from activity.wolearn.zsmh import ZSMHAct
from activity.wolearn.xxdgg import XxdggAct
from activity.wolearn.wabao import WzsbzAct
from activity.wolearn.wmms2 import BxwmAct
from activity.wolearn.stdt5 import Stdthd
from activity.womail.dailyTask import DailySign
from activity.womail.scratchable import Scratchable
from activity.womail.puzzle2 import Puzzle2
from activity.push.pushlog import PushLog
import json
import time
account_json = json.load(open('utils\\account.json'))
    #print(account_json)
account=[]
for key in account_json.keys():
    # print(key)
    # print(account_json[key])
    account.append((key, account_json[key]))
def Template(cls):
    # 联通手机号 服务密码 配置 (支持多账号)
    ts = []

    global  account

    for mobile, password in account:
        ts.append(Thread(target=cls(mobile, password).run))
    for t in ts:
        t.start()
    for t in ts:
        t.join()


def WXTemplate(cls):
    # 微信沃邮箱 mobile openId配置 (支持多账号)
    ts = []
    for item in [
        # {
        #     "mobile": "xxx",
        #     "openId": "xxx"
        # },
        # {
        #     "mobile": "xxx",
        #     "openId": "xxx"
        # },
    ]:
        ts.append(Thread(target=cls(**item).run))
    for t in ts:
        t.start()
    for t in ts:
        t.join()


def PushTemplate():
    # 消息推送 (读取数据存储服务记录的日志进行推送)
    # utils/config.py 推送配置
    # 填写参与活动任务的账号
    # 不需要推送 可以不填
    global account

    PushLog(account).run()


def main_handler(event=None, context=None):
    """
        腾讯云函数每15分钟执行一次
    """

    now_time = int(time.strftime(
        '%H%M',
        time.localtime(time.time() + 8 * 60 * 60 + time.timezone)
    ))
    DEBUG = False


    now_time=16000
    nowdebug=True

    # 沃阅读活动 取消阅读任务
    woyuedu=False

    if (now_time in range(600, 800) or DEBUG) and woyuedu :  # 7次
        Template(LuckDraw)
        Template(OpenBook)
        pass
    if (now_time in range(600, 730) or DEBUG) and woyuedu:  # 5次
        Template(ThanksGiving)
        pass
    if (now_time in range(800, 830) or DEBUG) and woyuedu:  # 1次
        Template(ReadLuchDraw)
        pass
    if (now_time in range(830, 900) or DEBUG) and woyuedu:  # 自动领取奖品
        Template(Prize)
        pass

    # 沃学习活动
    woxuexi=False
    if (now_time in range(900, 1100) or DEBUG) and woxuexi:
        Template(ZSMHAct)  # 7
        Template(XxdggAct)  # 8
        Template(WzsbzAct)  # 6
        Template(BxwmAct)  # 5
    if (now_time in range(900, 930) or DEBUG) and woxuexi:
        Template(Stdthd)

    # 沃邮箱活动
    woyouxiang=False
    if (now_time in range(1000, 1010) or now_time in range(1300, 1310) or DEBUG) and woyouxiang:
        WXTemplate(DailySign)
        WXTemplate(Puzzle2)
        WXTemplate(Scratchable)

    # ----------------------------------------------------------------
    # 使用华为云函数工作流 (腾讯云函数、阿里函数计算 ip在获取积分接口被限制)
    # 联通每日签到
    if now_time in range(800, 830) or now_time in range(1130, 1200) or now_time in range(1530, 1600) or DEBUG:
        Template(SigninApp)


    # 联通签到页看视频领流量
    if now_time in range(800, 900) or DEBUG:
        #Template(WatchAddFlow)
        pass

    # 赚积分外卖购物任务---这个非法
    waimai=True
    if (now_time in range(900, 930) or DEBUG) and waimai:
        Template(SignerTask)
        #Template(ZJFWeiBo)
        Template(QianDao11)

    # 联通签到页积分任务
    if now_time in range(800, 1600) or DEBUG :
        Template(SuperSimpleTask)

    # 联通积分翻倍任务
    if now_time in range(800, 1000) or DEBUG:
        Template(IntegralTask)

    # 联通签到页转盘抽卡任务
    if now_time in range(900, 1100) or DEBUG:
        Template(SheggMachine)
        Template(BlindBox)
        Template(TurnCard)
        Template(TurnTable)
        Template(ZhuaWaWa)
    # 联通沃之树

    if now_time in range(900, 1100) or DEBUG or  nowdebug:
        Template(Wotree)

    # 消息推送
    if now_time in range(1130, 1140) or now_time in range(1530, 1540) or DEBUG:
        PushTemplate()

if __name__ == '__main__':
    PushTemplate()


    main_handler("","")