"""
faq-bot  https://github.com/wj-Mcat/faq-bot

Authors:    Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright wj-Mcat

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from typing import Any
from faq_bot.channel import Channel     # type: ignore


# pylint: disable=too-few-public-methods
class Bot:
    """
    A bot policy to use different faq channel
    """
    def __init__(self, channel: Channel):
        """
        initialize the bot to complete the basic faq
        """
        self.channel = channel

    async def ask(self, query: str) -> Any:
        """
        the bot feed the query to the channel and get the result
        return back to faq bot
        """
        answer = await self.channel.ask(query)
        return answer
