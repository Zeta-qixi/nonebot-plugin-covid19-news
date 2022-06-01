from ast import alias
from .data_load import DataLoader
from nonebot import on_regex, on_command, get_bot, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot import require, logger
from .tools import NewsData

DL = DataLoader('data.json')
NewsBot = NewsData()

        
'''

 指令:
 # help
 # follow   
 # unfollow
 # city_news
 # city_poi_list

'''
__help__ = """---疫情信息 指令列表---
关注疫情 + 城市 （关注疫情 深圳）
取消关注疫情 + 城市
城市 + 疫情 （深圳疫情）
城市 + 疫情政策 （深圳疫情政策）
城市 + 风险地区  （深圳风险地区） 
"""
help = on_command(".help")
@help.handle()
async def _(bot: Bot, event: MessageEvent):
    await help.finish(message = __help__)

follow = on_command("关注疫情", priority=5, block=True)
@follow.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State(), city: Message=CommandArg()):
    city = city.extract_plain_text()    
    if "group" in event.get_event_name():    
        gid = str(event.group_id)
    else:
        gid = str(event.user_id)

    if NewsBot.data.get(city) and city not in FOCUS[gid]:
        FOCUS[gid].append(city)
        DL.save()
        await follow.finish(message=f"已添加{city}疫情推送")
    else:
        await follow.finish(message=f"添加失败")


unfollow = on_command("取消关注疫情", priority=5, block=True, aliases={"取消疫情", "取消推送疫情"})
@unfollow.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State(), city: Message=CommandArg()):
    city = city.extract_plain_text()

    if "group" in event.get_event_name(): 
        gid = str(event.group_id)
    else:
        gid = str(event.user_id)

    if NewsBot.data.get(city) and city in FOCUS[gid]:
        FOCUS[gid].remove(city)
        DL.save()
        await unfollow.finish(message=f"已取消{city}疫情推送")
    else:
        await unfollow.finish(message=f"取消失败")



city_news = on_regex(r'^(.{0,6})(疫情.{0,4})', block=True, priority=10)
@city_news.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State()):
    city_name, kw = state['_matched_groups']

    city = NewsBot.data.get(city_name)

    if kw in ['疫情政策', '疫情']:
        if city:
            if kw == '疫情政策':
                await city_news.finish(message=city.policy)
            else:
                await city_news.finish(message=f"{NewsBot.time}\n{city.main_info}")
        else:
            await city_news.finish(message="查询的城市不存在或存在别名")


city_poi_list = on_regex(r'^(.{0,6})(风险地区)', block=True, priority=10)
@city_poi_list.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State()):
    city_name, _ = state['_matched_groups']
    city = NewsBot.data.get(city_name)
    if city:
        await city_poi_list.finish(message=city.poi_list)

'''

 定时更新 & 定时推送

'''

FOCUS = DL.data


scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron',  minute='*/30', second='0', misfire_grace_time=60)
async def update():

    if NewsBot.update_data():
        logger.info(f"[疫情数据更新]{NewsBot.time}")
        city_list = []
        for gid in FOCUS.keys():
            for c in FOCUS.get(gid):
                city = NewsBot.data.get(c)
                city_list.append(city)
                logger.info(city)
                # 判定是否为更新后信息
                if city.isUpdated is True:
                    # send group or private
                    
                    try:
                        await get_bot().send_group_msg(group_id = int(gid), message= '关注城市疫情变化\n' + city.main_info)
                    except Exception as e:
                        await get_bot().send_private_msg(user_id= int(gid), message= '关注城市疫情变化\n' + city.main_info)
                
        for city in city_list:
            city.isUpdated = False


try:
    if (getattr(get_driver().config, 'covid19', None)):
        convid_config = get_driver().config.covid19
        if convid_config.get('notice') in ['true', "True"]:
            async def notice():
                res = []
                filter_city = convid_config.get('filter',[]) + ['香港', '台湾', '中国']
                for _, city in list(NewsBot.data.items()):
                    if city.all_add >= convid_config.get('red-line', 500): 
                        if city.name not in filter_city:
                            res.append(f"{city.main_info}")
                
                if res:
                    message = NewsBot.time + '\n' + '\n\n'.join(res)

                    group_list = convid_config.get('group')

                    if group_list == 'all':
                        group = await get_bot().get_group_list()
                        group_list = [ g['group_id'] for g in group ]

                    for gid in group_list:
                        await get_bot().send_group_msg(group_id=gid, message=message)

            scheduler.add_job(notice, "cron", hour="11",minute="5" ,id="covid19_notice")
except Exception as e:
    logger.info(f"config设置有误: {e}")          