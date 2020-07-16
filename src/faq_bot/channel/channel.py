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
from abc import ABCMeta
from typing import Union, Any, List, Generator, Tuple
from dataclasses import dataclass


@dataclass
class ChannelOptions:
    pass


class Channel(metaclass=ABCMeta):
    """
    ask the question through different channels, eg: your custom channel,

    microsoft Qna Maker channel,  tencent sentence similarty restful api
    """
    async def ask_question(self, query: Union[str]) -> Any:
        """
        ask the question from channel
        """
        raise NotImplementedError

    @staticmethod
    def _load_all_questions() -> Generator[Tuple[str, str]]:
        """load all question sentence"""
        with open('./data/question.txt', 'r', encoding='utf-8') as f:
            for line in f:
                sentence_split = line.split(' ')
                if len(sentence_split) != 2:
                    raise Exception('sentence file format is invalid')
                yield sentence_split[0], sentence_split[1]

    @staticmethod
    def _load_all_answers() -> Generator[Tuple[str, str]]:
        """load all answer sentence"""
        with open('./data/answer.txt', 'r', encoding='utf-8') as f:
            for line in f:
                sentence_split = line.split(' ')
                if len(sentence_split) != 2:
                    raise Exception('sentence file format is invalid')
                yield sentence_split[0], sentence_split[1]
