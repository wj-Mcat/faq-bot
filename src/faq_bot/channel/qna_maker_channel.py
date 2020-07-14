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

from typing import Union, Any
from dataclasses import dataclass
import json
import httpx

from .channel import Channel, ChannelOptions


@dataclass
class QnaMakerChannelOptions(ChannelOptions):
    knowledge_base_token: str
    endpoint: str


class QnaMakerChannel(Channel):
    """
    connect the micorsoft Qna Maker service
    """
    def __init__(self, options: QnaMakerChannelOptions):
        super().__init__()
        self.options = options

    async def ask(self, query: Union[str]) -> Any:
        """
        send the query to Qna Maker and return the result
        """
        header = {
            'Authorization': f'EndpointKey {self.options.endpoint}',
            'Content-Type': 'application/json'
        }
        url = f'https://wechatyqnachinese.azurewebsites.net/qnamaker/knowledgebases/{self.options.knowledge_base_token}/generateAnswer'

        async with httpx.AsyncClient(headers=header) as client:
            result = await client.post(
                url = url,
                json = {
                    'question': query
                }
            )
            return json.loads(result.text)
        