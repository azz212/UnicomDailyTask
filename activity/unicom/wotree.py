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
        #url = 'https://m.client.10010.com/mactivity/task/toolList.htm'
        url='https://m.client.10010.com/mactivity/task/list.htm'
        data = {
            #'floorMark': floorMark  # superEasy bigRew
        }
        results= {
            "msg": "查询任务成功",
            "code": "0000",
            "data": {
                "taskListDTOS": [{
                    "detailPicture": "https://m1.img.10010.com/resources/7188192A31B5AE06E41B64DA6D65A9B0/20191230/png/20191230174245.png",
                    "isFinishTask": "0",
                    "propId": "20190712600000001",
                    "propImg": "https://m1.img.10010.com/resources/7188192A31B5AE06E41B64DA6D65A9B0/20191230/png/20191230174223.png",
                    "propNum": "1",
                    "sortContinent": "1",
                    "taskDetails": "1、连续浇水7天，可获得一瓶杀虫剂&2、中间如果任务中断，将重新累计&3、领取奖励后，可以开启新的一轮连续浇水7天任务",
                    "taskId": "0001",
                    "taskNum": "7",
                    "taskTitle": "连续浇水7天",
                    "wateringNumber": "7"
                }, {
                    "detailPicture": "https://m1.img.10010.com/resources/7188192A31B5AE06E41B64DA6D65A9B0/20191230/png/20191230174316.png",
                    "isFinishTask": "1",
                    "propId": "20190712600000002",
                    "propImg": "https://m1.img.10010.com/resources/7188192A31B5AE06E41B64DA6D65A9B0/20191230/png/20191230174329.png",
                    "propNum": "1",
                    "sortContinent": "2",
                    "taskDetails": "1、每周一0点至每周日24点为一个任务周期&2、每周仅能领取一瓶好友专用杀虫剂&3、若在一个任务周期内未完成任务，下个任务周期，任务将重新开始&4、仅限给好友浇水",
                    "taskId": "0002",
                    "taskNum": "30",
                    "taskTitle": "一周帮好友浇水30次",
                    "wateringNumber": "0"
                }, {
                    "detailPicture": "https://m1.img.10010.com/resources/7188192A31B5AE06E41B64DA6D65A9B0/20191230/png/20191230174358.png",
                    "isFinishTask": "1",
                    "propId": "2019092300000001",
                    "propImg": "https://m1.img.10010.com/resources/7188192A31B5AE06E41B64DA6D65A9B0/20191230/png/20191230174344.png",
                    "propNum": "1",
                    "sortContinent": "3",
                    "taskDetails": "1、此任务为不限时任务&2、帮好友杀虫每满50条即可领取一瓶强力杀虫剂&3、领取奖励后，可以开启新的一轮帮好友杀虫50条任务&4、仅限帮好友杀虫",
                    "taskId": "0003",
                    "taskNum": "50",
                    "taskTitle": "帮好友除虫50条",
                    "wateringNumber": "0"
                }, {
                    "detailPicture": "https://m1.img.10010.com/resources/7188192A31B5AE06E41B64DA6D65A9B0/20191230/png/20191230174415.png",
                    "isFinishTask": "1",
                    "propId": "20191121000000",
                    "propImg": "https://m1.img.10010.com/resources/7188192A31B5AE06E41B64DA6D65A9B0/20191230/png/20191230174426.png",
                    "propNum": "1",
                    "sortContinent": "4",
                    "taskDetails": "1、此任务为不限时任务&2、每加10个好友即可领取一瓶防虫剂&3、领取奖励后，可以开启新的一轮加10个好友任务&4、同一个好友不可重复添加",
                    "taskId": "0004",
                    "taskNum": "10",
                    "taskTitle": "加10个好友",
                    "wateringNumber": "0"
                }]
            }
        }
        resp = self.session.post(url=url, data=data)
        data = resp.json()
        print(json.dumps(data))
        return data['data']['taskList']

    def doTask(self, item):
        print(item['taskTitle'])
        url = 'https://m.client.10010.com/mactivity/task/watchPage.htm'
        data = {
            'taskId': item['taskId']
        }
        resp = self.session.get(url=url, params=data)
        resp = resp.json()
        print(url)
        print(json.dumps(resp))

        return resp

    def accomplishDotaskOptions(self):
        url = 'https://act.10010.com/SigninApp/simplyDotask/accomplishDotask'
        _ = self.session.options(url=url, headers={
            'Content-Type': 'application/json'
        })

    def accomplishDotask(self, item, orderId=''):
        url = 'https://m.client.10010.com/mactivity/arbordayJson/giveGrowChance.htm?videoId={0}'.format(orderId)
        data = {
        }
        resp = self.session.post(url=url, json=data, headers={
            'Content-Type': 'application/json'
        })
        data = resp.json()
        print(json.dumps(data))
        return data

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
    def videoreward(self):
        '''
        看视频浇水
        '''
        item=""

        orderId = ''
        self.accomplishDotaskOptions()
        self.flushTime(1)


        options = {
            'arguments1': '',
            'arguments2': '',
            'codeId': 946779474,
            'channelName': 'android-签到超简单任务看视频-激励视频',
            'remark': '简单任务-看视频得奖励',
            'ecs_token': self.session.cookies.get('ecs_token')
        }

        orderId = self.toutiao.reward(options)
        self.flushTime(randint(20, 25))

        data = self.accomplishDotask(item, orderId)
        if data['code']=='0009':# 当日已经赠送了机会了
            return

        try:
            takeFlow = self.session.post('https://m.client.10010.com/mactivity/arbordayJson/arbor/3/0/3/grow.htm',timeout=1)
            resp = takeFlow.json()
            print(takeFlow.json())

            print('增加{0},当前培养值{1}'.format(resp['data']['addedValue'], resp['data']['trainValue']))

        except Exception as e:
            print(e)

    # self.flushTime(randint(60, 65))
    # break

    # 获取沃之树首页，得到领流量的目标值
    def get_woTree_glowList(self):
        index = self.session.post('https://m.client.10010.com/mactivity/arbordayJson/index.htm')
        index.encoding = 'utf-8'
        res = index.json()
        output = res['data']['flowChangeList']
        output += res['data']['shareFlowChangeList']
        return output
    def get_task_finishelist(self):
        index = self.session.post('https://m.client.10010.com/mactivity/arbordayJson/index.htm')
        index.encoding = 'utf-8'
        res = index.json()
        output = res['data']['popList']

        return output
    def run(self):
        #视频浇水
        self.videoreward()

        # 领取4M流量*3
        for task in self.getTask(''):
            # return
            #bug 如果视频时间未到，没有achieve 字段,则挑过次任务
            if task['isFinishTask']=="0":
                print('任务已完成{0}'.format(task['taskTitle']))
                print(task)
            else:
                print('开始做任务')
                resp = self.doTask(task)
                if resp['code']=='0000':
                    print('OK')



        try:
            flowList = self.get_task_finishelist()
            for flow in flowList:
                # 这里会请求很长时间，发送即请求成功
                try:
                    takeFlow = self.session.post(
                        'https://m.client.10010.com/mactivity/arbordayJson/arbor/{0}/{1}/0/grow.htm'.format(flow['id'],flow['type']), timeout=1)
                    resp=takeFlow.json()
                    print(takeFlow.json())

                    print('增加{0},当前培养值{1}'.format(resp['data']['addedValue'],resp['data']['trainValue']))

                except Exception as e:
                    print(e)
            self.session.post('https://m.client.10010.com/mactivity/arbordayJson/getChanceByIndex.htm?index=0')
            url='https://m.client.10010.com/mactivity/task/0001/accept.htm?taskFlag=812707'#获得道具任务



        except Exception as e:

            print('浇水 ' + str(e))


if __name__ == '__main__':
    pass
