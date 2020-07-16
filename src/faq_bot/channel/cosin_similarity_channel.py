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

import logging
from typing import Any, List, Union, Optional
from dataclasses import dataclass

from torch import nn, Tensor

from faq_bot.channel import Channel, ChannelOptions

log = logging.getLogger(__name__)

VECTOR_MAP = {
    'word2vec': './data/word2vec.zh.vec',
    'fasttext': './data/fasttext.zh.vec'
}

UNKNOWN_TOKEN = '<unknown_token>'
UNKNOWN_TOKEN_INDEX = 0

@dataclass
class CosinSimilarityChannelOptions(ChannelOptions):
    vector_type: str = 'word2vec'


class CosinSimilarityChannel(Channel):
    """
    Cosin Similarity with simple word-vector
    """

    async def ask_question(self, query: Union[str]) -> Any:
        pass

    def __init__(self, options: Optional[CosinSimilarityChannelOptions] = None):
        """load the vector according types"""
        if not options:
            options = CosinSimilarityChannelOptions()

        if options.vector_type not in VECTOR_MAP:
            raise Exception(f'vector type <{options.vector_type}> '
                            f'is not supported')
        self.options = options
        self.embedding = nn.Embedding()

    def _load_vocabulary(self) -> dict:
        """load vocabulary according to """
        index = 1
        word2idx = {}
        with open(VECTOR_MAP[self.options.vector_type], 'r+', encoding='utf-8') as f:
            for line in f:
                splits = line.split(' ')
                word2idx[splits[0]] = Tensor(splits[1:])



        return word2idx



