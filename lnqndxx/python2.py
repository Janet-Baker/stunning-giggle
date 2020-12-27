# -*- coding: utf8 -*-
import requests
import json

# 下方填写登录信息
head = {
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'http://websecond.lngqt.shechem.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'api.lngqt.shechem.cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x1700122c) NetType/WIFI Language/zh_CN',
    'Referer': 'http://websecond.lngqt.shechem.cn/study',
    'Accept-Language': 'zh-cn'
}
cookie = {'BDed_HeaderKey': 'C2YDAywMRQYDAWN4UBNiMS5Cfi9fJFByDHwIUDjQmNaBuN7W7fXQ7dE%3D'}
key = "SCT2724TH3hvvQpXvCU3xRO9fwbgspOk"


# 检查当前学习课程
def getnowlearn():
    global head
    global cookie
    url = 'http://api.lngqt.shechem.cn/webapi/learn/getnowlearn'
    res = requests.post(url, headers=head, cookies=cookie, data="token=")
    print res.text
    # 返回值是json，需要解码
    res_decoded = json.loads(str(res.text))
    print ("## 课程名为："),
    print res_decoded['data']['title']
    return res_decoded


# 上传学习记录
def addlearnlog(res_decoded):
    global head
    global cookie
    body = str("lid=" + res_decoded['data']['id'] + "&token=")
    # 开始签到
    url = 'http://api.lngqt.shechem.cn/webapi/learn/addlearnlog'
    result = requests.post(url, headers=head, cookies=cookie, data=body)
    result_decoded = json.loads(str(result.text))
    print result
    print "## 学习成功！##"
    # 以下是serverChan服务的发送内容。
    wechat(res_decoded)
    return result_decoded['errCode']


# 微信推送server酱
def wechat(res_decoded):
    global key
    url = str("https://sctapi.ftqq.com/" + key + ".send")
    kw = {
        'text': "青年大学习签到成功！",
        'desp': res_decoded['data']['title']
    }
    print requests.get(url, params=kw)
    return


# 主线引导与云函数入口
def main_handler(event, context):
    res_decoded = getnowlearn()
    if not res_decoded['data']['is_learn']:
        return addlearnlog(res_decoded)
    else:
        print "## 无学习任务！"
        return res_decoded['errCode']


# 本地入口
if __name__ == '__main__':
    main_handler(1, 2)
