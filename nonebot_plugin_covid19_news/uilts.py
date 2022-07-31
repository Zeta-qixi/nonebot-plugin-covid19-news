from nonebot import get_driver
from pathlib import Path
from nonebot.log import logger
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from typing import Union, List
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11.event import  MessageEvent


SEND_IMAGE = False
FONT_PATH =  Path("data/fonts")
FONT_PATH.mkdir(parents=True, exist_ok=True)
FONT_SIZE = 13


try:
    type_ = get_driver().config.covid19_message_type
    if type_ in ['image', 'Image']:

        FONT = ImageFont.truetype(font= str((FONT_PATH/'MSYH.TTC').resolve()), size = FONT_SIZE)
        SEND_IMAGE = True
        logger.info('将以 Image形式发送合并消息')
except:
    logger.info('将以 Text形式发送合并消息')

# 合并消息
async def send_forward_msg_group(
        bot: Bot,
        group_id: int,
        message: List,
):

    if isinstance(message, str):
        message = [message]

    def to_json(msg):
        return {"type": "node", "data": {"name": "疫情信息", "uin": bot.self_id, "content": msg}}
    await bot.call_api(
        "send_group_forward_msg", group_id=group_id, messages=[to_json(msg) for msg in message]
    )

# 转图片消息
def text2image(text:Union[str, List]) -> Message:
    L, H = 20, 0
    
    res = []
    
    for t in text.splitlines():
      
        res_ = [t[L*i:L*i+L] for i in range(len(t)//L+1)]
        H  += (len(res_))
        res.append("\n".join(res_).strip())

    img = Image.new("RGB",(L * (FONT_SIZE+1), H * (FONT_SIZE+5)+10), color =(255,255,255))
    
    draw = ImageDraw.Draw(img)

    draw.text((5,5), '\n'.join(res), font=FONT, fill='black')

    output = BytesIO()
    img.save(output, format="png")
    return MessageSegment.image(output)



async def send_msg(
        bot: Bot,
        event: Union[MessageEvent, int],
        message: Union[str, Message, List],
):

    if event.message_type == 'group':
        if not isinstance(message, list):
            message = [message]
        if SEND_IMAGE:
            message = [text2image(msg) for msg in message]
        await send_forward_msg_group(bot, event.group_id, message)
    else:
        await bot.send(event=event, message=message)
