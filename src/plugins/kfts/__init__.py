#from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot import on_command
from nonebot_plugin_apscheduler import scheduler
#import socket
from nonebot import require,get_bots,on_command
import requests

from nonebot import get_bots
require("nonebot_plugin_apscheduler")

my_dict = {'唯我独尊': '1', '青梅煮酒': '2', '大唐万象': '3', '天鹅坪': '4', '破阵子': '5', '飞龙在天': '6', '斗转星移': '7', '龙争虎斗': '8', '长安城': '9',
           '蝶恋花': '10', '梦江南': '11', '剑胆琴心': '12', '幽月轮': '13', '绝代天骄': '14', '乾坤一掷': '15', '缘起稻香': '16', '梦回长安': '17', '天宝盛世': '18'}

matcher = on_command("test_overload")


# def kftus(a, b):
#     sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sk.settimeout(1)
#     try:
#         sk.connect((a, 3724))
#         print(b)
#         dq = my_dict.get(b)
#         print(a+' OK '+dq)
#         q = '1'
#         kfzt = requests.get('http://api.aipiaxi.cn/jqr/kfjk',
#                             params={'id': dq}).json()['data'][0]['kf']
#         if q != kfzt:
#             print(a+' OK')
#             requests.get(url="http://api.aipiaxi.cn/jqr/kfxg",
#                          params={'kf': q, 'id': dq})
            
            
#             """ qun = 'http://api.aipiaxi.cn/jqr/qun?id='+bot.self_id
#             qun_dict = requests.get(qun).json()['data']
#             for zz in qun_dict:
#                  bot.call_api("send_group_msg",group_id=zz['qun'], message="开服了") """

    # except Exception:
    #     print(b+"NO")
    #     q = '2'
    #     kfzt = requests.get('http://api.aipiaxi.cn/jqr/kfjk',
    #                         params={'id': my_dict.get(b)}).json()['data'][0]['kf']
    #     if q != kfzt: 
    #         print(a+' OK')
    #         requests.get(url="http://api.aipiaxi.cn/jqr/kfxg",
    #                      params={'kf': q, 'id': my_dict.get(b)})
    #         return 2
    #         """ qun = 'http://api.aipiaxi.cn/jqr/qun?id='+bot.self_id
    #         qun_dict = requests.get(qun).json()['data']
    #         for zz in qun_dict:
    #             bot.send_group_msg(
    #                 *{'group_id': zz['qun'], 'message': b+'维护了'}) """

    # sk.close()



import os
import configparser

def DQ(b):
   dq = my_dict.get(b)
   kfzt = requests.get('http://api.aipiaxi.cn/jqr/kfjk',params={'id': dq}).json()['data'][0]['kf']
   return kfzt

from configobj import ConfigObj
cfg_path = "./test.cfg"
config = ConfigObj(cfg_path, encoding='UTF-8')



async def xigua(server:str):
   kf=DQ(server)
   
   kfzt=config['server'][server]
   if kfzt != kf:
      config['server'][server] = kf
      config.write()
      bot, = get_bots().values()
      
      """ qun = 'http://api.aipiaxi.cn/jqr/qun?id='+bot.self_id
      qun_dict = requests.get(qun).json()['data'] """
      
      qun = await bot.call_api("get_group_list",no_cache='false')

      """ await bot.call_api("send_msg",group_id=543911756, message=qun) """
      if kf == '1' : 
         for zz in qun:
            kfzt = requests.get('http://api.aipiaxi.cn/jqr/qunhao',params={'qun': zz['group_id'],'jqrqq': bot.self_id}).json()['data']
            kfdq=len(kfzt)
            
            if kfdq > 0:
               dq=kfzt[0]['server']
               if dq == server:
                await bot.call_api("send_msg",group_id=zz['group_id'], message=server+"开服了")
               
               

      elif  kf == '2':
         
         for zz in qun:
            kfzt = requests.get('http://api.aipiaxi.cn/jqr/qunhao',params={'qun': zz['group_id'],'jqrqq': bot.self_id}).json()['data']
            kfdq=len(kfzt)
            
            if kfdq > 0:
               dq=kfzt[0]['server']
               if dq == server:
                await bot.call_api("send_msg",group_id=zz['group_id'], message=server+"维护了")
               
               

@scheduler.scheduled_job("cron", second="*/3")
async def _():
   
   await xigua('唯我独尊')
   await xigua('青梅煮酒')
   await xigua('大唐万象')
   await xigua('大唐万象')
   await xigua('天鹅坪')
   await xigua('破阵子')
   await xigua('飞龙在天')
   await xigua('斗转星移')
   await xigua('龙争虎斗')
   await xigua('长安城')
   await xigua('蝶恋花')
   await xigua('梦江南')
   await xigua('剑胆琴心')
   await xigua('幽月轮')
   await xigua('剑胆琴心')
   await xigua('绝代天骄')
   await xigua('乾坤一掷')
   await xigua('缘起稻香')
   await xigua('梦回长安')
   await xigua('天宝盛世')
   
   
   
   """ kf=DQ('唯我独尊')
   
   kfzt=config['server']['唯我独尊']
   if kfzt != kf:
      config['server']['唯我独尊'] = kf
      config.write()
      bot, = get_bots().values()
      
      qun = 'http://api.aipiaxi.cn/jqr/qun?id='+bot.self_id
      qun_dict = requests.get(qun).json()['data']
      
      
      if kf == '1' : 
         for zz in qun_dict:
            if zz['server'] == '唯我独尊':
               await bot.call_api("send_msg",group_id=zz['qun'], message=zz['server']+"开服了")
               
               

      elif  kf == '2':
         
         for zz in qun_dict:
            if zz['server'] == '唯我独尊':
            
               await bot.call_api("send_msg",group_id=zz['qun'], message=zz['server']+"维护了")  """

                
         
    
   
   
   
   #key=config.options("config")
    


   
    
    
    



    
    

