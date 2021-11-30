# -*- coding: utf8 -*-
import requests
from random import randint
from utils import jsonencode as json
from utils.toutiao_reward import TouTiao
from utils.unicomLogin import UnicomClient
import time

class Wotree(UnicomClient):
    """
        签到页积分任务
    """

    def __init__(self, mobile, password):
        super(Wotree, self).__init__(mobile, password)
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

    # 获取沃之树首页，得到领流量的目标值
    def get_woTree_glowList(self):
        index = self.session.post('https://m.client.10010.com/mactivity/arbordayJson/index.htm')
        index.encoding = 'utf-8'
        res = index.json()
        output = res['data']['flowChangeList']
        output += res['data']['shareFlowChangeList']
        return output

    def run(self):
        # 领取4M流量*3
        try:
            flowList = self.get_woTree_glowList()
            num = 1
            for flow in flowList:
                # 这里会请求很长时间，发送即请求成功
                flag = False
                try:
                    takeFlow = self.session.get(
                        'https://m.client.10010.com/mactivity/flowData/takeFlow.htm?flowId=' + flow['id'], timeout=1)
                except Exception as e:
                    flag = True
                    print('【沃之树-领流量新】: 4M流量 x' + str(num))
                # 等待1秒钟
                time.sleep(1)
                num = num + 1
                if flag:
                    continue
                takeFlow.encoding = 'utf-8'
                res1 = takeFlow.json()
                if res1['code'] == '0000':
                    print('【沃之树-领流量】: 4M流量 x' + str(num))
                else:
                    print('【沃之树-领流量】: 已领取过 x' + str(num))
                # 等待1秒钟
                time.sleep(1)
                num = num + 1
            self.session.post('https://m.client.10010.com/mactivity/arbordayJson/getChanceByIndex.htm?index=0')
            # 浇水
            grow = self.session.post('https://m.client.10010.com/mactivity/arbordayJson/arbor/3/0/3/grow.htm')
            grow.encoding = 'utf-8'
            res2 = grow.json()
            print('【沃之树-浇水】: 获得' + str(res2['data']['addedValue']) + '培养值')
            time.sleep(1)
        except Exception as e:

            print('【沃之树】: 错误，原因为: ' + str(e))

        self.flushTime(randint(3, 5))
        log = '[superEasy]\n'
        for item in self.getTask('superEasy'):
            log += f"{item['title']}:{item['btn']}---进度:{item['achieve']}/{item['allocation']}\n"
        log += '[bigRew]\n'
        for item in self.getTask('bigRew'):
            log += f"{item['title']}:{item['btn']}---进度:{item['achieve']}/{item['allocation']}\n"
        self.recordLog(log)




if __name__ == '__main__':
    pass
