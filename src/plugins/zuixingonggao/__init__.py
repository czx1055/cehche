#from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, PrivateMessageEvent
from configobj import ConfigObj
import datetime
import pytz
from nonebot import on_command
from nonebot_plugin_apscheduler import scheduler
#import socket
from nonebot import require, on_command, get_bot
import requests
from nonebot.adapters.onebot.v11 import (GroupMessageEvent, Message,
                                         MessageSegment,Bot)
from nonebot import get_bots
from lxml import etree
from bs4 import BeautifulSoup

# 第一个定时器

import asyncio
from pyppeteer import launch
require("nonebot_plugin_apscheduler")

import nonebot







my_dict = {'唯我独尊': '1', '青梅煮酒': '2', '大唐万象': '3', '天鹅坪': '4', '破阵子': '5', '飞龙在天': '6', '斗转星移': '7', '龙争虎斗': '8', '长安城': '9',
           '蝶恋花': '10', '梦江南': '11', '剑胆琴心': '12', '幽月轮': '13', '绝代天骄': '14', '乾坤一掷': '15', '缘起稻香': '16', '梦回长安': '17', '天宝盛世': '18'}

matcher = on_command("test_overload")

tz = pytz.timezone('Asia/Shanghai')

# 设置访问时间为每周一、周三和周六晚上20.30.02
weekday = [0, 2, 5]  # 分别对应周一、周三和周六
time = datetime.time(20, 30)


async def is_group_muted(group_id: int) -> bool:
    bot = get_bot()
    group_info = await bot.get_group_info(group_id=group_id, no_cache=True)
    group_data = group_info['group_data']
    return group_data['is_mute_all']

@scheduler.scheduled_job("cron", second="*/30")
async def zuixingonggao():

    url = "https://jx3.xoyo.com/launcher/update/latest.html"
    response = requests.get(url)


    try:
        # 读取配置文件中的最新版本号
        cfg_path = "./test.cfg"
        config = ConfigObj(cfg_path, encoding='UTF-8')
        logo = config['gonggao']['id']

        # 找到当前HTML中的版本号
        doc = etree.HTML(response.text)
        data = doc.xpath('/html/body/div[1]/div[1]/text()[3]')
        version = data[0].split("：")[1].strip()
        #print(version)
        # 比较版本号大小
        

        if version == logo:
            print("公告未更新")
        elif version > logo:
            print("公告更新")
            config["gonggao"]["id"] = version
            config.write()
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.text)
            params = {'prompt': "帮我把下面的内容概述一下："+soup.text}
            url = "http://chat.dl-100.cn/api/chat-process"
            
            
            response = requests.get(url,params=params).json()
            xx = response['response'] 
            bot = get_bot()
            group_list = await bot.get_group_list()
            for group in group_list:

                    group_id = group["group_id"]
                    if is_group_muted(group_id) != True:
                        await bot.call_api("send_msg",group_id=group_id, message=xx)
                        
                    await asyncio.sleep(60.0)    


            

    except ( AttributeError) as e:
        print("读取配置文件或解析网页内容失败:", e)

