import base64
import datetime
import json
import os
import time

import PyRSS2Gen
import requests
from bs4 import BeautifulSoup


def name2id(name):
    url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword=' + name
    res = requests.get(url)
    soup = json.loads(res.text)
    return soup.get('data').get('result')[0].get('mid')


def id2videos(id):
    url = "https://api.bilibili.com/x/space/arc/search?mid=" + str(
        id) + "&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp"
    res = requests.get(url)
    videos = json.loads(res.text).get("data").get("list").get("vlist")
    return videos


def video2pic(video):
    url = 'https:' + video.get('pic')
    return url

# def video2pic(video):
#     url = video.get('pic')[2:]
#     res = requests.get(url)
#     ls_f = base64.b64encode(BytesIO(res.content).read())
#     imgdata = base64.b64decode(ls_f)
#     return imgdata

def video2title(video):
    return video.get('title')


def video2bvid(video):
    return video.get('bvid')


def video2author(video):
    return video.get('author')


def video2time(video):
    timeArray = time.localtime(video.get("created"))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    lll = datetime.datetime.strptime(otherStyleTime, "%Y-%m-%d %H:%M:%S")
    mmm = lll.astimezone(tz=datetime.timezone.utc)
    return mmm


def video2link(video):
    return 'https://www.bilibili.com/video/' + video2bvid(video)


def video2des(video):
    str1 = '<p>' + video.get('description') + '</p>'
    str2 = '<p>' + '<img src="' + video2pic(video) + '" >' + '</p>'
    str3 = '<a href="' + video2link(video) + '">原文链接</a>'
    return str3 + str2 + str1

def cmp(x):
    return 0 - x.get('created')

def videos2rss(videos):
    items = []
    videos = sorted(videos, key=cmp)
    videos = videos[:100]
    for video in videos:
        item = PyRSS2Gen.RSSItem(
            title=video2title(video),
            description=video2des(video),
            link=video2link(video),
            author=video2author(video),
            comments=video2pic(video),
            guid=video2bvid(video),
            pubDate=video2time(video)
        )
        items.append(item)
    rss = PyRSS2Gen.RSS2(
        title='bilibili',
        link='https://gitee.com/shuifengche/rss/raw/master/bili.xml',
        description='bilibili',
        lastBuildDate=datetime.datetime.utcnow(),
        items=items
    )
    rss.write_xml(open('bilibili.xml', 'w'), encoding='utf-8')

# upName = ["李好帅", "马督工", "山高县", "没啥用科技", "暴走大事件", "半佛仙人", "暴躁的仙人"]
# for name in upName:
#     print("\"" + name + "\": " + name2id(name) + ",")

def isProgramInTitle(title,programs):
    for program in programs:
        if program in title:
            return True

if __name__ == '__main__':
    upName = ["李好帅", "何同学", "巫托邦", "CodeSheep", "正月点灯笼", "马督工", "凸山高县凸", "没啥用科技", "暴走大事件", "半佛仙人", "暴躁的仙人", "小王Albert"]
    list = []
    for name in upName:
        id = name2id(name)
        videos = id2videos(id)
        list += videos
    up = ["观视频工作室", "观察者网", "吃素的狮子"]
    programData = {
        "观视频工作室": ["山高县"],
        "观察者网": ["消化一下", "亚洲特快", "施老胡诌"],
        "吃素的狮子": ["梗百科"]
    }
    for name in up:
        id = name2id(name)
        mvideos = id2videos(id)
        videos = []
        for video in mvideos:
            programs = programData[name]
            title = video2title(video)
            if isProgramInTitle(title, programs):
                videos += [video]
        list += videos
    videos2rss(list)
