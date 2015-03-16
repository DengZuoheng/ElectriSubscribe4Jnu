##暨大电费订阅##
###Intro###
- 这是一个暨大珠海校区, 订阅电费的项目, 当你的宿舍的电费余额低于一定限额时, 就会发邮件通知.
- 当然也希望做成微信和短信通知, 不过成本比较大, 而且一开始只是为了自己用, 所以邮件通知基本就够了.
- 抓取电费余额的代码在`./server/trigger/service.py`, 其他部分代码倒是没什么可看的.

###Require###
- Python2.7
- Django1.7
- [PyCurl](http://pycurl.sourceforge.net/)
- [PyQuery](https://github.com/gawel/pyquery/)

###Install###
- `./server`是一个django项目, 要实现新增订阅的话, 就需要运行这个django项目.
- 每日的查询是`./server/main.py`实现的, main.py会一直运行, 所以应该用nohup运行
- 代码中数据库使用的是mysql, 相关设置在`./server/server/settings.py` 可自行更改.
- 邮件发送使用的是我自己的邮箱, 相关代码在`./server/MailSender.py`,`./subscriber/models.py`,`./trigger/trigger.py`都有涉及, 可自行更改.

###TODO###
- 发送邮件测试(本地没法测试gmail, 墙, 你懂的
- 写一个简单版, 给自己专用, 就不用上数据库, django什么的了

###Lisence###
- 虽然lisence还没写, 不过你就当做是GPL吧