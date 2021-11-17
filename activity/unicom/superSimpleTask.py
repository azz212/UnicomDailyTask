# -*- coding: utf8 -*-
import requests
from random import randint
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient
import time

class SuperSimpleTask(UnicomClient):
    """
        签到页积分任务
    """

    def __init__(self, mobile, password):
        super(SuperSimpleTask, self).__init__(mobile, password)
        self.session.headers = requests.structures.CaseInsensitiveDict({
            "accept": "application/json, text/plain, */*",
            "origin": "https://img.client.10010.com",
            "user-agent": self.useragent,
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://img.client.10010.com/SigininApp/index.html",
            "x-requested-with": "com.sinovatech.unicom.ui"
        })
        self.toutiao = TouTiao(mobile)

    def listTaskInfo(self):
        '''
        签到看视频任务话费红包 add zhao 2021-11-16 在宾馆
        {"data":{"achieve":"1","allocation":"3","code":"0000","curTime":"2021-11-16 20:50:15","expireTime":"2021-11-16 22:50:14","prizeName":"签到看视频任务话费红包"},"msg":"ok!","status":"0000"}
        {"data":{"achieve":"0","allocation":"3","code":"0000","curTime":"2021-11-16 20:49:02","expireTime":"2021-11-16 20:49:02","prizeName":"签到看视频任务话费红包"},"msg":"ok!","status":"0000"}
        '''
        url='https://act.10010.com/SigninApp/multitask/listTaskInfo'
        data = {
        }


        resp = self.session.post(url=url)
        result = resp.json()
        print(json.dumps(result, indent=4, ensure_ascii=False))
        paramsList = result


        return paramsList

    def getPrize(self):
        '''
        {"status":"0000","msg":"ok!","data":{"id":null,"prizeCount":null,"returnStr":null,"equityValue":"+0.06元","state":"0","statusDesc":"领取成功","businessADType":"GET_DOTASK_PHONE","doubleIntegralNum":null,"tips":null,"picUrl":null,"leftBtn":{"btnName":null,"btnUrl":null,"btnBackGroundColor":null,"btnSubscript":null},"rightBtn":{"btnName":"赢戴尔电脑","btnUrl":"https://u.10010.cn/tbMJn","btnBackGroundColor":"","btnSubscript":""},"cishu":"0","channel":"taskTelephone"}}
        '''
        url='https://act.10010.com/SigninApp/prize/getPrize'
        title=''

        self.flushTime(randint(15, 20))
        options = {
            'arguments1': '',
            'arguments2': '',
            'codeId': 946276966,#?? codeId 是多少  946276966
            'channelName': 'android-签到看视频得话费红包-激励视频',
            'remark': '签到-兑换-做任务得话费',##%E7%AD%BE%E5%88%B0-%E5%85%91%E6%8D%A2-%E5%81%9A%E4%BB%BB%E5%8A%A1%E5%BE%97%E8%AF%9D%E8%B4%B9
            'ecs_token': self.session.cookies.get('ecs_token')
        }

        orderId = self.toutiao.reward(options)

        data = {
            "type": 'get',
            "channel": "taskTelephone",
            "orderId": orderId
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data

    def getTask(self, floorMark):
        url = 'https://act.10010.com/SigninApp/superSimpleTask/getTask'
        data = {
            'floorMark': floorMark  # superEasy bigRew
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        # print(json.dumps(data))
        return data['data']

    def doTask(self, item):
        print(item['title'])
        url = 'https://act.10010.com/SigninApp/simplyDotask/doTaskS'
        data = {
            'taskId': item['taskId']
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        print(url)
        return data['status']

    def accomplishDotaskOptions(self):
        url = 'https://act.10010.com/SigninApp/simplyDotask/accomplishDotask'
        _ = self.session.options(url=url, headers={
            'Content-Type': 'application/json'
        })

    def accomplishDotask(self, item, orderId=''):
        url = 'https://act.10010.com/SigninApp/simplyDotask/accomplishDotask'
        data = {
            "taskId": item['taskId'],
            "systemCode": "QDQD",
            "orderId": orderId
        }
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'application/json'
        })
        data = resp.json()
        print(json.dumps(data))

    def receiveBenefits(self):
        url = 'https://act.10010.com/SigninApp/floorData/receiveBenefits'
        resp = self.session.post(url=url)
        data = resp.json()
        print(json.dumps(data))

    def energy(self):
        url = 'https://act.10010.com/SigninApp/simplyDotask/energy'
        resp = self.session.post(url=url)
        data = resp.json()
        print(json.dumps(data))

    def recordLog(self, log):
        record = self.readCookie(f'{self.mobile}SuperSimpleTaskRecord')
        if not record:
            record = {}
        if len(record) > 30:
            k = list(record.keys())[0]
            record.pop(k)
        record[self.now_date] = log
        self.saveCookie(f'{self.mobile}SuperSimpleTaskRecord', record)

    def run(self):

        for item in self.getTask('superEasy'):
            # return
            #bug 如果视频时间未到，没有achieve 字段,则挑过次任务
            if 'achieve' not in item:
                continue

            print(json.dumps(item))
            # add 202111-16 加任务
            if item['title'] in [
                '去浏览积分商城', '兑换1次话费红包', '玩4次0元夺宝',
                '玩3次转盘赢好礼', '玩3次套牛赢好礼', '玩3次扔球赢好礼',
                '玩3次刮刮乐', '玩3次开心抓大奖', '看2次完整视频',
                '完成下载参与斗地主游戏', '完成下载参与捕鱼游戏','参与双十一摇大奖','完成右上角气泡区21个定时任务','完成右上角气泡区31个定时任务'
            ] and int(item['achieve']) != int(item['allocation']) and item['btn'] not in ['倒计时','']:#倒计时没有按钮文字
                print(item['title'])
                print(int(item['allocation']) - int(item['achieve']))
                for _ in range(int(item['allocation']) - int(item['achieve'])):
                    orderId = ''
                    self.accomplishDotaskOptions()
                    self.flushTime(1)
                    if item['title'] == '看2次完整视频':
                        self.flushTime(randint(15, 20))
                        options = {
                            'arguments1': '',
                            'arguments2': '',
                            'codeId': 946779474,
                            'channelName': 'android-签到超简单任务看视频-激励视频',
                            'remark': '简单任务-看视频得奖励',
                            'ecs_token': self.session.cookies.get('ecs_token')
                        }
                        orderId = self.toutiao.reward(options)
                    self.accomplishDotask(item, orderId)
                    item['achieve'] = int(item['achieve']) + 1
                    self.flushTime(randint(10, 15))
                # self.flushTime(randint(60, 65))
                # break
            if int(item['achieve']) == int(item['allocation']) and item['btn'] not in ['已完成', '倒计时']:
                # int(item['showStyle']) != 3:
                status = self.doTask(item)
                self.receiveBenefits()
                self.flushTime(randint(15, 20))
                if status != '0000':
                    self.getTask('superEasy')
                    self.doTask(item)
                #break
                time.sleep(5)

        for item in self.getTask('bigRew'):
            if int(item['achieve']) == int(item['allocation']) and item['btn'] != '已完成':  # int(item['showStyle']) != 3:
                self.doTask(item)
                self.flushTime(randint(5, 10))
        self.energy()

        self.flushTime(randint(3, 5))
        log = '[superEasy]\n'
        for item in self.getTask('superEasy'):
            log += f"{item['title']}:{item['btn']}---进度:{item['achieve']}/{item['allocation']}\n"
        log += '[bigRew]\n'
        for item in self.getTask('bigRew'):
            log += f"{item['title']}:{item['btn']}---进度:{item['achieve']}/{item['allocation']}\n"
        self.recordLog(log)

        #add 签到看视频任务话费红包
        tasks=self.listTaskInfo()
        # {"data":{"achieve":"1","allocation":"3","code":"0000","curTime":"2021-11-16 20:50:15","expireTime":"2021-11-16 22:50:14","prizeName":"签到看视频任务话费红包"},"msg":"ok!","status":"0000"}
        if tasks['status']=='0000':
            task=tasks['data']
            if task['achieve']<task['allocation']:
                print('当前完成{0}'.format(task['achieve']))
                if task['expireTime']<=task['curTime']:
                    print('可以继续完成任务')
                    result=self.getPrize()
                    if result['status']=='0000':
                        print('任务完成，获得{0}'.format(result['data']['equityValue']))

                else:
                    print('当前未到任务时间{0}'.format(task['expireTime']))
            else:
                print('所有任务已经完成')



if __name__ == '__main__':
    pass
