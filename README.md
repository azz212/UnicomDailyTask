# UnicomDailyTask
联通日常任务 服务器定时执行（建议间隔2-3小时运行一次，视频每隔2个小时可再次完成）
+ 需搭建数据存储服务接口 [pythonanywhere仓库](https://github.com/rhming/pythonanywhere)
+ 沃阅读活动（不建议运行）
+ 沃学习活动（不建议运行）
+ 沃邮箱活动（不建议运行）
+ 联通日常任务
+ 联通签到页积分任务
+ 联通积分翻倍任务
+ 看视频得花费（新增）
+ 奥运签到积分（注意使用）

### 部分配置文件说明
```
|-- index.py  # 联通账号配置 微信沃邮箱账号配置
`-- utils
    |-- address.json  # 沃阅读自动领取奖品配置(配置收货地址)
    |-- appId.json  # 联通appId配置
    |-- config.py  # 数据存储服务接口配置 消息推送配置 常用设备ID配置(不能同时多台设备登录)
```
+ config.py文件
> `data_storage_server_url` pythonanywhere搭建的接口(替换成自己搭建的域名)
--- ---
> ![image](https://user-images.githubusercontent.com/49028484/133171069-60857c48-8277-4b57-8972-847c5aec1cd5.png)
--- ---
> ![image](https://user-images.githubusercontent.com/49028484/133170462-293d2800-172c-47c5-b5c5-21d0f0c98c2c.png)
--- ---
> `username` `password` pythonanywhere Web中开启的安全保护授权用户密码(没开启可以留空)
--- ---
> ![image](https://user-images.githubusercontent.com/49028484/133170503-f8ec2681-e7db-4de7-9246-142a541397dd.png)


