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

from typing import Union, Any, List, Union
from dataclasses import dataclass

from faq_bot.channel import Channel, ChannelOptions


@dataclass
class SentenceBertChannelOptions(ChannelOptions):
    """options for sentence-bert"""
    model: str = 'bert-base-chinese'


class SentenceBertChannel(Channel):
    def __init__(self, options: SentenceBertChannelOptions):
        self.options = options
        self.model = SentenceTransformer(self.options.model)

    def encode(self, sentences: Union[List[str], str]) -> List[ndarray]:
        """encode the sentences, and return the sentences embedding"""
        embeddings = self.model.encode(sentences=sentences)
        return embeddings

    def train(self):
        """train the model with default params"""
        word_embedding_model = models.Transformer(self.options.model)
        # Apply mean pooling to get one fixed sized sentence vector
        pooling_model = models.Pooling(
            word_embedding_model.get_word_embedding_dimension(),
            pooling_mode_mean_tokens=True,
            pooling_mode_cls_token=False,
            pooling_mode_max_tokens=False
        )

        model = SentenceTransformer(
            modules=[word_embedding_model, pooling_model])

    def _read_dataset(self) -> SentencesDataset:
        """read the dataset to sentence"""

    async def ask(self, query: Union[str]) -> Any:
