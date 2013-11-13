#!/usr/bin/env python
#-*-coding:utf-8-*-
import redis
import json
import requests


def send(subject, text, to):
    return requests.post(
        "https://api.mailgun.net/v2/mail-internal.wandoujia.com/messages",
        auth=("api", "key-5br6rwrim18qcnavw7vfxrud2d9sg5r2"),
        data={"from": "喂豌豆 <feedme@samples.mailgun.org>",
              "to": to,
              "subject": subject,
              "text": text})


def job():
    c = redis.Redis(host='127.0.0.1', port=6379, db=8)
    keys = c.keys("dinner:cname:*@gmail.com")
    for key in keys:
        to = key.split(":")[-1]
        text = "hi!\n很冒昧的给您发这封邮件,我是豌豆荚的一名工程师,我写了喂豌豆http://fan.wandoulabs.com 这个订餐网站.偶然从后台发现您登陆喂豌豆使用的邮箱,相信您一定对我们的公司很感兴趣,而且充满了好奇心以及超越常人的技能(从您使用gmail登录就能看出来!)..\n\n那么就请海涵我通过这邮件勾搭一下你吧:)\n\n您肯定已经了解到我们的晚餐福利啦,除此之外,我们还有进口的空气净化器,高大上的办公环境,以及丰富的三餐和无限的水果饮料,更重要的是,你可以和我这样有趣的工程师一起工作,可以是喂豌豆这类的小工具,也可以是影响数千万用户的视频搜索,总之我们的公司是一个极客范硅谷范创新范十足的创业公司!\n\n还等什么呢,马上把简历发到我邮箱吧,相信咱们这种招聘方式一定是史无前例的,如果您真的来到了豌豆荚,那更是一段佳话啦,一个点餐网站带来的工作机会,说的就是你哦.\n\n期待着能和你在豌豆荚共进晚餐!\n\nP.S.\n 不要直接回复邮件哦,我的邮箱是zhida@wandoujia.com ,给我发简历吧!! 我会尽责的给你内推的哦,职位信息在这: http://wandoujia.com/join \n\nHacker 刘志达@豌豆荚 敬上"
        subject = "来豌豆荚吃晚饭吧!"
        print to
        #send(subject, text, to)

if __name__ == "__main__":
    job()
