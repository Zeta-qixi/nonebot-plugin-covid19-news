
import os
from nonebot import on_regex
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import  MessageEvent
from nonebot.typing import T_State
from nonebot import require, logger

from .tools import NewsData
NewsBot = NewsData()

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='*/3', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def update():
    if NewsBot.update_data():
        logger.info(f"[疫情数据更新]{NewsBot.time}")

city_news = on_regex(r'^(.{0,6})(疫情.{0,4})', block=True)
# city_policy = on_regex('(.*)(疫情政策)', block=True)

@city_news.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    city_name, kw = state['_matched_groups']

    city = NewsBot.data.get(city_name)
    if city:
        if kw == '疫情政策':
            await city_news.finish(message=city.policy)
        elif kw == '疫情':
            await city_news.finish(message=f"{NewsBot.time}\n{city.main_info}")
    else:
        await city_news.finish(message="查询的城市不存在或存在别名")

