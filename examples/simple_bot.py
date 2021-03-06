"""
simple bot with simple word
"""

import asyncio
import os
import sys

from faq_bot.channel.qna_maker_channel import (     # type: ignore
    QnaMakerChannelOptions, QnaMakerChannel
)
from faq_bot.bot import Bot     # type: ignore

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), 'src')))

KNOWLEDGE_BASE_TOKEN = os.getenv('QNA_KNOWLEDGE_BASE_TOKEN')
ENDPOINT = os.getenv('QNA_ENDPOINT')


async def run_bot():
    """
    run the sample bot
    """
    options = QnaMakerChannelOptions(
        knowledge_base_token=KNOWLEDGE_BASE_TOKEN,
        endpoint=ENDPOINT
    )
    channel = QnaMakerChannel(options=options)
    bot = Bot(channel)
    while True:
        print('请问您要问什么吗？')
        query = input('question >>')
        result = await bot.ask(query)
        print(result)


asyncio.run(run_bot())
