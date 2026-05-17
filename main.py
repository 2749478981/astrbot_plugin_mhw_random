import os
import random
import subprocess
from astrbot.api import logger
from astrbot.api.event import filter
from astrbot.api.star import Context, Star
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
from astrbot.core.star.filter.event_message_type import EventMessageType

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mhw_random.py")

TRIGGERS = ["怪猎随机", "随机怪猎"]


class MhwRandomPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AiocqhttpMessageEvent):
        msg = event.message_str.strip()
        if msg not in TRIGGERS:
            return

        output_path = f"/root/data/temp/mhw_{event.get_sender_id()}_{random.randint(0,9999)}.png"
        try:
            result = subprocess.run(
                ["/root/.local/share/uv/tools/astrbot/bin/python3", SCRIPT, output_path],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode != 0 or not os.path.exists(output_path):
                logger.error(f"MHW随机失败: {result.stderr}")
                yield event.plain_result("呜…纱雾的签筒卡住了，再试一次吧~")
                return

            yield event.image_result(output_path)

        except Exception as e:
            logger.error(f"MHW随机异常: {e}")
            yield event.plain_result("诶嘿…出了点小问题，再来一次嘛~")
