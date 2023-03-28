import ffmpeg
import string
import hmac
import hashlib
import base64
import random
#from tencentcloud.nlp.v20190408 import nlp_client, models
#from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
#from tencentcloud.common.profile.http_profile import HttpProfile
#from tencentcloud.common.profile.client_profile import ClientProfile
from nonebot.adapters.onebot.v11.permission import GROUP
#from tencentcloud.common import credential
import json
from pyppeteer import launch
import asyncio
from configobj import ConfigObj
from bs4 import BeautifulSoup
from nonebot.typing import T_State
from jinja2 import Template
import re
import time
from pathlib import Path
import os
import requests
from typing import Optional

from nonebot import Bot, get_driver, on_keyword

from nonebot.adapters.onebot.v11 import (GroupMessageEvent, Message,
                                         MessageSegment, Event,GroupRequestEvent)
from nonebot.params import CommandArg
from nonebot.plugin.on import on_command, on_message,on_regex,on_request,on_notice
from nonebot.rule import to_me
from .config import Config
from urllib.parse import quote
global_config = get_driver().config
config = Config.parse_obj(global_config)








day_tewo = on_message(priority=100, rule=to_me())


parent_dir = os.path.dirname(os.path.abspath(__file__))

@day_tewo.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    
    st = str(event.message)
    id = str(event.user_id)
    conversationId = None
    parentMessageId = None
    url="http://api.aipiaxi.cn/jqr/chatgpt?id="+id
   
    response = requests.get(url).json()
    code =response['code']
    if code == 200:

        conversationId: Optional[str] = response['data'][0]['conversationId']
        parentMessageId: Optional[str] = response['data'][0]['parentMessageId']
    encoded_str = st
    if conversationId is not None and parentMessageId is not None:
        # 处理 'conversationId' 和 'parentMessageId' 都存在的情况
        #data = {"conversationId": conversationId, "parentMessageId": parentMessageId}
        
        
        params = {'content': encoded_str}
        url = "http://app.aipiaxi.cn/get_responses"
        
        
        response = requests.get(url,params=params).json()
        xx = response['response'] 
            
        #conversationId = response['conversationId'] 
        #parentMessageId = response['parentMessageId']
            
        await bot.send(event=event, message=xx)
        url="http://api.aipiaxi.cn/jqr/chatgptxz?id="+id+"&conversationId="+encoded_str+"&parentMessageId="+xx
        response = requests.get(url).json()
        code =response['code']



    else:
        # 处理 'conversationId' 或 'parentMessageId' 不存在的情况
        
        params = {'content': encoded_str,"options": {}}
        url = "http://app.aipiaxi.cn/get_responses"
        
        response = requests.get(url,params=params).json()
        xx = response['response'] 
        await bot.send(event=event, message=xx)
        conversationId = response['conversationId'] 
        parentMessageId = response['parentMessageId']
        url="http://api.aipiaxi.cn/jqr/chatgptxz?id="+id+"&conversationId="+encoded_str+"&parentMessageId="+xx
        response = requests.get(url).json()
    
   




generate_page = on_command("余额查询",priority=1)


@generate_page.handle()
async def handle_generate_page(bot: Bot, event: GroupMessageEvent, state: T_State):
    # 获取图片链接
    
    url = 'http://chat.dl-100.cn/api/config'
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'http://chat.dl-100.cn',
        'Referer': 'http://chat.dl-100.cn/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'Hm_lvt_127767e3d675609c895c52e7b8dbbc4a=1679922450,1679922602,1679928835,1679980273; Hm_lpvt_127767e3d675609c895c52e7b8dbbc4a=1679984138'
    }
    data = '{}'

    response = requests.post(url, headers=headers, data=data, verify=False).json()['data']['balance']

    print(response)
    await bot.send(event=event, message="当前chatgpt余额："+response+"美元")


day_anins = on_command("日常",priority=98)

@day_anins.handle()
async def _(bot: Bot, event: GroupMessageEvent):
   

    t = time.gmtime()
    ricang = requests.get('http://app.aipiaxi.cn/ricang')
    if ricang.status_code == 200:
        tdmj = ricang.json()['tdmj']
        ggrw = ricang.json()['ggrw']
        mijing = ricang.json()['mijing']
        dazhan = ricang.json()['dazhan']
        zhenyin = ricang.json()['zhenyin']
        zhanchangshousheng = ricang.json()['zhanchangshousheng']

        await bot.send(event=event, message='今天是' + time.strftime("%Y-%m-%d", t) + '\n'  + dazhan + '\n' + '战场首胜：'+zhanchangshousheng + '\n' + '阵营日常：' + zhenyin+ '\n' + '团队秘境：' + tdmj+ '\n' + '公共任务：' + ggrw+ '\n' + '秘境任务：' + mijing )
    else:
       await bot.send(event=event, message="通知管理员更新推栏token")


    

    
    # dazhan = dz[0]
    # strinfo = re . compile('大战！')
    # zhanchang = dz[1]
    # strinfo1 = re . compile('战场-')
    # zhenyingricang = dz[2]
    # strinfo2 = re . compile('战！')
    # a = strinfo.sub('  ', dazhan)
    # b = strinfo1.sub('', zhanchang)
    # c = strinfo2.sub('', zhenyingricang)
    # await   day_anins.finish(Message( '今天是'+ time.strftime("%Y-%m-%d",t) + '\n' + '大战:' +a + '\n' + '战场首胜：'+b+ '\n' + '阵营日常：'+c)      + '\n' + '行侠·楚州：' + title + '\n' + '福源宠物：' + chongwu  + '\n' + '园宅会赛：' + zydi)

    #await bot.send(event=event, message='今天是' + time.strftime("%Y-%m-%d", t) + '\n' + '大战:' + a + '\n' + '战场首胜：'+b + '\n' + '阵营日常：' + c)










# @day_anins.handle()
# async def _(bot: Bot, event: GroupMessageEvent):
   

#     t = time.gmtime()
#     ricang = requests.get('https://cms.jx3box.com/api/cms/game/daily?date=' +
#                           time.strftime("%Y-%m-%d", t)).json()['data']

#     dz = []
#     for i in ricang:
#         dz.append(i['activity_name'])
#     dazhan = dz[0]
#     strinfo = re . compile('大战！')
#     zhanchang = dz[1]
#     strinfo1 = re . compile('战场-')
#     zhenyingricang = dz[2]
#     strinfo2 = re . compile('战！')
#     a = strinfo.sub('  ', dazhan)
#     b = strinfo1.sub('', zhanchang)
#     c = strinfo2.sub('', zhenyingricang)
#     # await   day_anins.finish(Message( '今天是'+ time.strftime("%Y-%m-%d",t) + '\n' + '大战:' +a + '\n' + '战场首胜：'+b+ '\n' + '阵营日常：'+c)      + '\n' + '行侠·楚州：' + title + '\n' + '福源宠物：' + chongwu  + '\n' + '园宅会赛：' + zydi)

#     await bot.send(event=event, message='今天是' + time.strftime("%Y-%m-%d", t) + '\n' + '大战:' + a + '\n' + '战场首胜：'+b + '\n' + '阵营日常：' + c)

my_dict = {'唯我独尊': '1', '青梅煮酒': '2', '大唐万象': '3', '天鹅坪': '4', '破阵子': '5', '飞龙在天': '6', '斗转星移': '7', '龙争虎斗': '8', '长安城': '9', '蝶恋花': '10',
           '梦江南': '11', '剑胆琴心': '12', '幽月轮': '13', '绝代天骄': '14', '乾坤一掷': '15', '缘起稻香': '16', '梦回长安': '17', '天宝盛世': '18', '唯满侠': '1', '双梦': '11', '横刀断浪': '19'}


day_cd = on_command('命令')


@day_cd.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await day_kf.finish(Message('https://www.aipiaxi.cn/index.php/2023/02/24/573/'))


day_cd = on_command('看美女')


@day_cd.handle()
async def _(bot: Bot, event: GroupMessageEvent):

    video_url = 'https://v.api.aa1.cn/api/api-dy-girl/index.php?aa1=json'
    video_url = requests.get(video_url).json()['mp4']
    video = MessageSegment.video('https:'+video_url)
    await bot.send(event=event, message=video)


qiyu = {'拜春擂': '113', '镜中琴音': '112', '追魂骨': '111', '红尘不渡': '110', '故岁辞': '109', '重洋客': '108', '子夜歌': '107', '千秋铸': '106', '枉叹恨': '105', '万灵当歌': '104', '幽海牧': '103', '鸠雀记': '102', '庆舞良宵': '101',
        '度人心': '99', '凌云梯': '98', '风雨意': '97', '念旧林': '96', '童蒙志': '95', '旧宴承欢': '94', '寻猫记': '93', '捉贼记': '92', '丹青记': '91', '流年如虹': '90', '一枝栖': '89', '侠行囧途': '88', '尘网中': '87',
        '白月皎': '86', '话玄虚': '85', '争铸吴钩': '83', '劝学记': '82', '瀛洲梦': '81', '莫贪杯': '80', }


day_gl = on_command('攻略')


@day_gl.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    if not args is None:
        dq = str(args)
        qy = qiyu.get(dq)

        if not qy is None:

            browser = await launch()
            page = await browser.newPage()
            await page.goto('https://www.jx3box.com/adventure/'+qy)
            yazhengma = await page.waitForSelector('#c-article-part1')
            await yazhengma.screenshot({'path': 'gl.png', 'fullPage': True})
            await browser.close()
            with open("gl.png", "rb") as f:
                img = f.read()
            mes = MessageSegment.image(img)
            await bot.send(event=event, message=mes)


day_kf = on_command('开服')


@day_kf.handle()
async def _(bot: Bot, event: GroupMessageEvent):

    kfzt = requests.get('http://api.aipiaxi.cn/jqr/qunhao',
                        params={'qun': event.group_id, 'jqrqq': bot.self_id}).json()['data'][0]

    kfdq = kfzt['server']
    if kfdq == '':
        kfdq = '唯我独尊'

    dq = my_dict.get(kfdq)
    #kfzt = requests.get('http://api.aipiaxi.cn/jqr/kfjk',params={'id': dq}).json()['data'][0]['kf']
    kfzt = requests.get('http://api.aipiaxi.cn/jqr/kfjk',
                        params={'id': dq}).json()
    zt = kfzt['code']
    kfztt = kfzt['data'][0]['kf']
    sj = kfzt['data'][0]['time']
    sjj = kfzt['data'][0]['stime']

    if kfztt == '1':
        await day_kf.finish(Message(kfdq+'在'+sj+'开服的'))
    elif kfztt == '2':
        await day_kf.finish(Message(kfdq+'在'+sj+'维护的'))




def Bddq(qqq, jqrqq):
    kfzt = requests.get('http://api.aipiaxi.cn/jqr/qunhao',
                        params={'qun': qqq, 'jqrqq': jqrqq}).json()
    code = kfzt['code']
    kfdq = kfzt['data'][0]['server']
    if code == 200:
        return kfdq
    else:
        kfdq = '唯我独尊'
        return kfdq


def dd373(qqq, ww, jqrqq, dq):
    if ww == '':
        dm = ddcode.get(dq)
    else:
        dm = ddcode.get(ww)

    req = requests.get(url="https://www.dd373.com/s-8v8pc2-" +
                       dm+"-0-0-0-cwmaee-0-0-0-0-0-0-0-0-0.html", headers=headers)
    req.encoding = "utf-8"
    html = req.text

    soup = BeautifulSoup(req.text, features="html.parser")
    company_item = soup.find("p", class_="font12 colorFF5")
    dd = company_item.text.strip()
    return 'dd373:'+dd


def UU898(qqq, ww, jqrqq, dq):
    if ww == '':
        dm = uucode.get(dq)
    else:
        dm = uucode.get(ww)

    req = requests.get(
        url="http://www.uu898.com/newTrade-150-c-3-"+dm, headers=headers)
    req.encoding = "utf-8"
    html = req.text

    soup = BeautifulSoup(req.text, features="html.parser")
    company_item = soup.find("h6", title="每一元人民币对应的物品数量。").find("span")
    zp = company_item
    dd = zp.text.strip()

    return 'uu898:' + dd


def xsj(qqq, ww, jqrqq, dq):
    if ww == '':
        dm = wbcode.get(dq)
    else:
        dm = wbcode.get(ww)

    kfzt = requests.get('https://api-wanbaolou.xoyo.com/api/buyer/goods/list?'+dm +
                        '&sort%5Bsingle_count_price%5D=0&game=jx3&page=1&size=1').json()['data']['list'][0]
    ZJ = str(kfzt['single_count_price'])
    return "万宝楼:1元="+ZJ+"金"


def w173(qqq, ww, jqrqq, dq):
    if ww == '':
        dm = w1733.get(Bddq(qqq, jqrqq))
    else:
        dm = w1733.get(ww)

    req = requests.get(url=dm, headers=headers)
    req.encoding = "gb2312"
    html = req.text

    soup = BeautifulSoup(req.text, features="html.parser")
    company_item = soup.find("ul", class_="pdlist_unitprice")
    zp = company_item.find("li").find("b")
    dd = str(zp.text.strip())
    """ strinfo = re . compile('.00')
    a = strinfo.sub('',dd) """

    return "5173:"+dd + "金"


ddcode = {"蝶恋花": 'km917s-52fsse', "龙争虎斗": 'km917s-ch7w22', "长安城": 'km917s-m10vqg', "幽月轮": 'hswdmk-jvtg2x',
          "斗转星移": 'hswdmk-ackn6g', "剑胆琴心": 'hswdmk-7vfvfx', "乾坤一掷": 'hswdmk-jwr9j74', "唯我独尊": 'hswdmk-td3he5',
          "梦江南": 'hswdmk-kqkv28', "绝代天骄": 'h56n27-36eh2k', "天鹅坪": 'fgd20g-1h23hp', "破阵子": 'fgd20g-kjkanv',
          "飞龙在天": 'n11r40-0kbk65', "青梅煮酒": 'sc86kv-g85njj', "凌雪藏锋": 'sc86kv-mb5h4n', "风月同天": 'sc86kv-5whegb',
          "止戈为武": '7kr689-5njgjc', "百无禁忌": 'p0fq8c-mh8vjt', "横刀断浪": 'hswdmk-jhdewb'}

uucode = {"蝶恋花": '1315-s30493', "龙争虎斗": '1315-s6883', "长安城": '1315-s8920', "幽月轮": '1319-s9588',
          "斗转星移": '1319-s8966', "剑胆琴心": '1319-s18064', "乾坤一掷": '1319-s8967', "唯我独尊": '1319-s6897',
          "梦江南": '1319-s8963', "绝代天骄": '1650-s11110', "天鹅坪": '2695-s30199', "破阵子": '2695-s30198',
          "飞龙在天": '2696-s30216', "青梅煮酒": '3428-s39907', "凌雪藏锋": '3428-s42664', "风月同天": '3428-s43251',
          "止戈为武": '2821-s30270', "百无禁忌": '2820-s30269', "横刀断浪": '1319-s53509'}


wbcode = {"蝶恋花": 'zone_id=z01&server_id=gate0126', "龙争虎斗": 'zone_id=z01&server_id=gate0115', "长安城": 'zone_id=z01&server_id=gate0101', "幽月轮": 'zone_id=z05&server_id=gate0519',
          "斗转星移": 'zone_id=z05&server_id=gate0515', "剑胆琴心": 'zone_id=z05&server_id=gate0524', "乾坤一掷": 'zone_id=z05&server_id=gate0514', "唯我独尊": 'zone_id=z05&server_id=gate0505',
          "梦江南": 'zone_id=z05&server_id=gate0502', "绝代天骄": 'zone_id=z08&server_id=gate0807', "天鹅坪": 'zone_id=z21&server_id=gate2107', "破阵子": 'zone_id=z21&server_id=gate2106',
          "飞龙在天": 'zone_id=z22&server_id=gate2204', "青梅煮酒": 'zone_id=z24&server_id=gate2402', "凌雪藏锋": 'zone_id=z24&server_id=gate2407', "风月同天": 'zone_id=z24&server_id=gate2409',
          "止戈为武": 'zone_id=z29&server_id=gate2901', "百无禁忌": 'zone_id=z31&server_id=gate3101', "横刀断浪": 'zone_id=z05&server_id=gate0533'}

w1733 = {"蝶恋花": 'http://s.5173.com/jxqy-5ootfk-iw0yxb-x0bxtt-0-kb0ewi-0-0-0-a-a-a-a-a-0-0-0-0.shtml', "龙争虎斗": 'http://s.5173.com/jxqy-5ootfk-iw0yxb-24gxko-0-kb0ewi-0-0-0-a-a-a-a-a-0-0-0-0.shtml', "长安城": 'http://s.5173.com/jxqy-5ootfk-iw0yxb-hczhmz-0-kb0ewi-0-0-0-a-a-a-a-a-0-0-0-0.shtml', "幽月轮": 'http://s.5173.com/jxqy-5ootfk-1got2e-x0y4sd-0-kb0ewi-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml',
         "斗转星移": 'http://s.5173.com/jxqy-5ootfk-1got2e-vt0v0n-0-kb0ewi-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml', "剑胆琴心": 'http://s.5173.com/jxqy-5ootfk-1got2e-fynxvi-0-kb0ewi-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml', "乾坤一掷": 'http://s.5173.com/jxqy-5ootfk-1got2e-2nzyqv-0-kb0ewi-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml', "唯我独尊": 'http://s.5173.com/jxqy-5ootfk-1got2e-0ognud-0-kb0ewi-0-0-0-a-a-a-a-a-0-0-0-0.shtml',
         "梦江南": 'http://s.5173.com/jxqy-5ootfk-1got2e-ymz55j-0-kb0ewi-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml', "绝代天骄": 'http://s.5173.com/jxqy-5ootfk-2l3v3x-dog0bd-0-kb0ewi-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml', "天鹅坪": 'http://s.5173.com/jxqy-5ootfk-1bk5qc-jjvp1o-0-kb0ewi-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml', "破阵子": 'http://s.5173.com/jxqy-5ootfk-1bk5qc-lv10cn-0-kb0ewi-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml',
         "飞龙在天": 'http://s.5173.com/jxqy-5ootfk-lkbi21-p0m1dw-0-kb0ewi-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml', "青梅煮酒": 'http://s.5173.com/jxqy-5ootfk-a534501f7ba24eca9a50f171e31dbb85-o4z44f-0-0-0-0-0-a-a-a-a-a-0-itemprice_asc-0-0.shtml', "凌雪藏锋": 'http://s.5173.com/jxqy-5ootfk-a534501f7ba24eca9a50f171e31dbb85-1xfrss-0-kb0ewi-0-0-0-a-a-a-a-a-0-0-0-0.shtml', "风月同天": 'http://s.5173.com/jxqy-5ootfk-a534501f7ba24eca9a50f171e31dbb85-00z1lu-0-kb0ewi-0-0-0-a-a-a-a-a-0-0-0-0.shtml',
         "止戈为武": 'http://s.5173.com/jxqy-5ootfk-a534501f7ba24eca9a50f171e31dbb85-1xfrss-0-kb0ewi-0-0-0-a-a-a-a-a-0-0-0-0.shtml', "百无禁忌": 'http://s.5173.com/jxqy-5ootfk-a534501f7ba24eca9a50f171e31dbb85-1xfrss-0-kb0ewi-0-0-0-a-a-a-a-a-0-0-0-0.shtml', "横刀断浪": 'http://s.5173.com/jxqy-5ootfk-1got2e-ewczyq-0-kb0ewi-0-0-0-a-a-a-a-a-0-0-0-0.shtml'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

dqq = {'唯满侠': '唯我独尊', '唯我独尊': '唯我独尊', '青梅煮酒': '青梅煮酒', '双梦': '梦江南', '梦江南': '梦江南', '大唐万象': '大唐万象', '天鹅坪': '天鹅坪', '破阵子': '破阵子', '飞龙在天': '飞龙在天', '斗转星移': '斗转星移',
       '龙争虎斗': '龙争虎斗', '长安城': '长安城', '蝶恋花': '蝶恋花', '剑胆琴心': '剑胆琴心', '幽月轮': '幽月轮', '绝代天骄': '绝代天骄', '乾坤一掷': '乾坤一掷', '缘起稻香': '缘起稻香', '梦回长安': '梦回长安', '天宝盛世': '天宝盛世', '横刀断浪': '横刀断浪'}


day_jinjia = on_command('金价')


@day_jinjia.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):

    dq = str(args)

    if dq == '':
        dq = Bddq(event.group_id, bot.self_id)
    if dq == '':
        dq = '唯我独尊'
    dq = dqq.get(dq)
    dd = dd373(event.group_id, dq, bot.self_id, dq)
    uu = UU898(event.group_id, dq, bot.self_id, dq)
    wbl = xsj(event.group_id, dq, bot.self_id, dq)
    w1 = w173(event.group_id, dq, bot.self_id, dq)
    dd = dq+'\n'+dd+'\n'+uu + '\n'+wbl+'\n' + w1

    await bot.send(event=event, message=dd)

day_bangding = on_command('绑定')


@day_bangding.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    dqqq = {'唯满侠': '唯我独尊', '唯我独尊': '唯我独尊', '青梅煮酒': '青梅煮酒', '双梦': '梦江南', '梦江南': '梦江南', '大唐万象': '大唐万象', '天鹅坪': '天鹅坪', '破阵子': '破阵子', '飞龙在天': '飞龙在天', '斗转星移': '斗转星移',
            '龙争虎斗': '龙争虎斗', '长安城': '长安城', '蝶恋花': '蝶恋花', '剑胆琴心': '剑胆琴心', '幽月轮': '幽月轮', '绝代天骄': '绝代天骄', '乾坤一掷': '乾坤一掷', '缘起稻香': '缘起稻香', '梦回长安': '梦回长安', '天宝盛世': '天宝盛世', '横刀断浪': '横刀断浪'}
    dd = str(args)
    if dqqq.get(dd) == dd:

       

        kfztT = requests.get('http://api.aipiaxi.cn/jqr/dqxg',
                             params={'id': event.group_id, 'server': dd}).json()['code']
        if kfztT == 200:
            await bot.send(event=event, message=dd+"绑定成功")
        elif kfztT == 201:

            kfzt = requests.get('http://api.aipiaxi.cn/jqr/bddq', params={
                                'jqrqq': bot.self_id, 'qun': event.group_id, 'kf': '1', 'znlt': '1', 'sever': dd}).json()
            code = kfzt['code']
            if code == 200:
                await bot.send(event=event, message=dd+"绑定成功")
            else:
                await bot.send(event=event, message=dd+"绑定失败")

   


cfg_path = "./config.cfg"
config = ConfigObj(cfg_path, encoding='UTF-8')

""" config['j3sp']={}

config['j3sp']['logo'] = '17681277366' #账号
config['j3sp']['paswprd'] = 'czx1055'   #密码 """

logo = config['j3sp']['logo']
paswprd = config['j3sp']['paswprd']
secret_id = config['tx']['secret_id']
secret_key = config['tx']['secret_key']


def SP(dq):

    token = config['j3sp']['token']

    headers = {

        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": "https://www.j3sp.com/api.html",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "cookie": "PHPSESSID=e7q76e7u52puv5s9hfg1b69jc8; spc_token="+token+"; spc_uid=1779",
        "accept": "application/json, text/javascript, */*; q=0.01",

    }
    url = "https://www.j3sp.com/api/sand/?serverName="+dq+"&is_history=1&shadow=1"

    res = requests.get(url, headers=headers).json()
    if res['code'] == 1:
        sandImage = res['data']['sand_data']['sandImage']

        print(sandImage)
        return sandImage
    elif res['code'] == 401:
        DLurl = "https://www.j3sp.com/api/user/login?account="+logo+"&password="+paswprd

        dlres = requests.get(DLurl).json()
        dlrescode = dlres['code']
        token = dlres['data']['userinfo']['token']
        if dlrescode == 1:

            config['j3sp']['token'] = token
            config.write()
        sandImage = res['data']['sand_data']['sandImage']

        print(sandImage)
        return sandImage

    else:
        return '1'
Regex = {
    "交易行": r"(^交易行 [\u4e00-\u9fa5]+$)|(^交易行 [\u4e00-\u9fa5]+ [\u4e00-\u9fa5]+$)",
    "物价": r"(^物价 [\u4e00-\u9fa5]+$)",
    "物品": r"(^物品 [\u4e00-\u9fa5]+$)",
    "沙盘": r"(^沙盘$)|(^沙盘 [\u4e00-\u9fa5]+$)",
}

day_sp = on_regex(pattern=Regex['沙盘'], permission=GROUP, priority=5, block=True)


@day_sp.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    text_list = event.get_plaintext().split(" ")
    
    wp: Optional[str] = text_list[1].strip()
    #await bot.send(event=event, message=wp)    
    dq = str(wp)
    if dq == None:
       dq = Bddq(event.group_id, bot.self_id)
    TP = SP(dq)
    if TP != '1':
        mes = MessageSegment.image(TP)

        await bot.send(event=event, message=mes)
    else:
        await bot.send(event=event, message='沙盘获取失败请重试')
    

async def main(dd):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://app.aipiaxi.cn/wj.html?key='+dd)
    await page.screenshot({'path': 'example.png', 'fullPage': True})
    await browser.close()
























day_sp = on_regex(pattern=Regex['物价'], permission=GROUP, priority=5, block=True)


@day_sp.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    text_list = event.get_plaintext().split(" ")
    if len(text_list) == 2:
        #dq = str(args)
        wp: Optional[str] = text_list[1].strip()

        # dq=Bddq(event.group_id,bot.self_id)
        ricang = requests.post('https://www.j3price.top:8088/black-api/api/outward/search',
                            params={'step': 0, 'page': 1, 'size': 20, 'name': wp}).json()['data']['list']
        # print(ricang[0]['id'])

        if len(ricang) > 0:
            # await asyncio.get_event_loop().run_until_complete(main(dq))
            browser = await launch()
            page = await browser.newPage()
            #width, height = await page.evaluate('() => [document.documentElement.clientWidth, document.documentElement.clientHeight]')
            #await page.setViewport({'width': width, 'height': height})
            await page.setViewport({'width': 1420, 'height': 1980})
            await page.goto('http://app.aipiaxi.cn:6398/wj?key='+wp)
            await page.screenshot({'path': 'example.png', 'fullPage': True})
            await browser.close()
            with open("example.png", "rb") as f:
                img = f.read()
            mes = MessageSegment.image(img)
            await bot.send(event=event, message=mes)
        else:
            await bot.send(event=event, message="名字错误或不存在或没有数据")


































jiaoyihang_query = on_regex(pattern=Regex['交易行'], permission=GROUP, priority=5, block=True)
@jiaoyihang_query.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    text_list = event.get_plaintext().split(" ")
    if len(text_list) == 2:
        get_server = text_list[0]
        wp: Optional[str] = text_list[1].strip()
        dq: Optional[str] = Bddq(event.group_id, bot.self_id)
        #dq = Bddq(event.group_id, bot.self_id)
        zpo = requests.get('https://helper.jx3box.com/api/item/search',
                        params={'page': 1, 'keyword': wp}).json()['data']['data']
        # print(ricang[0]['id'])

        code = zpo[0]['id']
        print(code)

        jyh = requests.get('https://next2.jx3box.com/api/item-price/'+code +
                        '/detail', params={'server': dq, 'limit': 20}).json()['data']['prices'] 

        for aasd in zpo:
            code = str(aasd['id'])

            jyh = requests.get('https://next2.jx3box.com/api/item-price/'+code +
                            '/detail', params={'server': dq, 'limit': 20}).json()['data']['prices']
            if not jyh is None:
                jyhid = code
                imgg = str(aasd['IconID'])
                name = str(aasd['Name'])

        if not jyhid is None:

                # await asyncio.get_event_loop().run_until_complete(main(dq))
                browser = await launch()
                page = await browser.newPage()
                # await page.setViewport({'width': 1220, 'height': 1580})
                await page.goto('http://app.aipiaxi.cn:6398/jyhh?key=' + jyhid + '&dq=' + dq + '&img=' + imgg + '&name=' + name)
                await page.screenshot({'path': 'jyh.png', 'fullPage': True})
                await browser.close()
                with open("jyh.png", "rb") as f:
                    img = f.read()
                mes = MessageSegment.image(img)
                await bot.send(event=event, message=mes)
        else:
                await bot.send(event=event, message="查不到就是没有数据咯")


    else:
        #get_server = text_list[1]   
        wp = text_list[2].strip()
        dq = text_list[1].strip()
        zpo = requests.get('https://helper.jx3box.com/api/item/search',
                        params={'page': 1, 'keyword': wp}).json()['data']['data']
        # print(ricang[0]['id'])

        code = zpo[0]['id']
        print(code)

        jyh = requests.get('https://next2.jx3box.com/api/item-price/'+code +
                        '/detail', params={'server': dq, 'limit': 20}).json()['data']['prices'] 

        for aasd in zpo:
            code = str(aasd['id'])

            jyh = requests.get('https://next2.jx3box.com/api/item-price/'+code +
                            '/detail', params={'server': dq, 'limit': 20}).json()['data']['prices']
            if not jyh is None:
                jyhid = code
                imgg = str(aasd['IconID'])
                name = str(aasd['Name'])

        if not jyhid is None:

                # await asyncio.get_event_loop().run_until_complete(main(dq))
                browser = await launch()
                page = await browser.newPage()
                # await page.setViewport({'width': 1220, 'height': 1580})
                await page.goto('http://app.aipiaxi.cn:6398/jyhh?key=' + jyhid + '&dq=' + dq + '&img=' + imgg + '&name=' + name)
                await page.screenshot({'path': 'jyh.png', 'fullPage': True})
                await browser.close()
                with open("jyh.png", "rb") as f:
                    img = f.read()
                mes = MessageSegment.image(img)
                await bot.send(event=event, message=mes)
        else:
                await bot.send(event=event, message="查不到就是没有数据咯")
















day_sp = on_command('奇遇')


@day_sp.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    wp = str(args)
    dq = Bddq(event.group_id, bot.self_id)
    # await asyncio.get_event_loop().run_until_complete(main(dq))
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1220, 'height': 1580})
    await page.goto('http://app.aipiaxi.cn:6398/qy?key=' + wp + '&dq=' + dq)
    await page.screenshot({'path': 'qy.png', 'fullPage': True})
    await browser.close()
    with open("qy.png", "rb") as f:
        img = f.read()
    mes = MessageSegment.image(img)
    """ qun = await bot.call_api("get_group_list",no_cache='false')
    print(qun)
    
    await bot.call_api("send_msg",group_id=543911756, message=qun[0]['group_id']) """
    await bot.send(event=event, message=mes)


# 'clip':{'x':0,'y':0,'width': 1440,'height':1440}

day_sp = on_command('更新')


@day_sp.handle()
async def _(bot: Bot, event: GroupMessageEvent,):

    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://jx3.xoyo.com/launcher/update/latest.html')
    await page.screenshot({'path': 'gx.png', 'fullPage': True})
    await browser.close()
    with open("gx.png", "rb") as f:
        img = f.read()
    mes = MessageSegment.image(img)
    await bot.send(event=event, message=mes)




def qqq(qqq, jqrqq):
    kfzt = requests.get('http://api.aipiaxi.cn/jqr/qunhao',
                        params={'qun': qqq, 'jqrqq': jqrqq}).json()
    code = kfzt['code']
    if code == 200:
        kfdq = kfzt['data'][0]['znlt']
        return kfdq
    else:

        return '3'


#官方的权限验证、以及调用接口的参数
def test_2_offical(P):
    endpoint = "tts.tencentcloudapi.com"
    data = {
        'Action': 'TextToVoice',
        'Text': P,
        # 'session'+str(random.randint(1,10000)),   # 随机
        'SessionId': 'session_chang',
        'ModelType': '1',
        'Volume': '1',
        'Speed': '0',
        'ProjectId': '0',
        'VoiceType': '101015',
        'PrimaryLanguage': '1',
        'SampleRate': '16000',
        'Codec': 'mp3',
        # 下面是其他必选公共参数
        'Region': 'ap-beijing',
        'Nonce': random.randint(1, 100000),
        'SecretId': secret_id,
        'Timestamp': int(time.time()),
        'Version': '2019-08-23',
    }
    s = get_string_to_sign("GET", endpoint, data)
    data["Signature"] = sign_str(secret_key, s, hashlib.sha1)
    # print(data["Signature"])
    # 此处会实际调用，成功后可能产生计费
    resp = requests.get("https://" + endpoint, params=data)
    # 输出一下拼出来的参数
    # print(resp.url)
    # 输出一下返回
    # print(resp.json())
    # 保存返回的音频数据

    save_audio_file(resp.json())
    """ ST=resp.json()['Response']['Audio']
    return ST """


# def tx(st):
#     cred = credential.Credential(secret_id, secret_key)

#     httpProfile = HttpProfile()
#     httpProfile.endpoint = "nlp.tencentcloudapi.com"

#     clientProfile = ClientProfile()
#     clientProfile.httpProfile = httpProfile

#     client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

#     req = models.ChatBotRequest()

#     params = {
#         "Query": st
#     }
#     req.from_json_string(json.dumps(params))

#     resp = client.ChatBot(req)
#     if resp.Confidence >= 1:
#         return resp.Reply
#     else:
#         return '3'







def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    return s + query_str


def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)


# 保存成文件
def save_audio_file(rsp_dic):
    # 传回的音频, 是base64, 也就是一种用64个字符来表示任意二进制数据的方法（8bit）
    audio_txt = rsp_dic["Response"]["Audio"]
    file_path = "test_tts.mp3"
    base64_to_file(audio_txt, file_path)


def base64_to_file(base64_txt, file_path):
    audio_b_data = base64.b64decode(base64_txt)
    audio_file = open(file_path, 'wb')
    audio_file.write(audio_b_data)
    audio_file.close()
    # print("saved:"+file_path)


day_sppD = on_command('说', rule=to_me())


@day_sppD.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    sst = str(args)
    test_2_offical(sst)
    with open("test_tts.mp3", "rb") as f:
        au = f.read()

    zq = MessageSegment.record(au)
    await bot.send(event=event, message=zq)


day_sppD = on_command('开启聊天')


@day_sppD.handle()
async def _(bot: Bot, event: GroupMessageEvent):

    kfzt = requests.get('http://api.aipiaxi.cn/jqr/znlt',
                        params={'id': event.group_id, 'znlt': '1'}).json()
    code = kfzt['code']
    if code == 200:
        await bot.send(event=event, message='开启成功')
    else:
        await bot.send(event=event, message='关闭失败')
day_sppD = on_command('关闭聊天')


@day_sppD.handle()
async def _(bot: Bot, event: GroupMessageEvent):

    kfzt = requests.get('http://api.aipiaxi.cn/jqr/znlt',
                        params={'id': event.group_id, 'znlt': '2'}).json()
    code = kfzt['code']
    if code == 200:
        await bot.send(event=event, message='关闭成功')
    else:
        await bot.send(event=event, message='关闭失败')


