import json
from urllib.parse import unquote
from utils.common import Common
from utils.message import getMessage


class PushLog(Common):

    def __init__(self, accounts, _=None):
        super(PushLog, self).__init__()
        self.accounts = accounts
        self.message = ''

    def run(self):
        for account in self.accounts:
            account = unquote(account[0])
            self.mobile = account[0]
            for record in [
                'SigninAppRecord', 'SuperSimpleTaskRecord',
                'WatchAddFlowRecord', 'WoReadRecord',
                'WoLearnRecord', 'WoMailRecord'
            ]:
                if self.mobile.isdigit() and record == 'WoMailRecord':
                    continue
                if not self.mobile.isdigit() and record != 'WoMailRecord':
                    continue
                self.message += f'{self.mobile}{record}[{self.now_date}]'.center(64, '-') + '\n'
                msg = self.readCookie(f'{self.mobile}{record}')
                if not msg:
                    msg = "未获取到日志"
                if isinstance(msg, dict):
                    msg = msg.get(self.now_date, '未获取到日志')
                    if not isinstance(msg, str):
                        msg = json.dumps(msg, indent=4, ensure_ascii=False)
                self.message += msg + '\n'
        if self.accounts:
            getMessage(self.message).run()


if __name__ == '__main__':
    pass
