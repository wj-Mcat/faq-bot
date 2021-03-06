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
from typing import Union, Optional


class Token:
    """
    work token representation, keeping tack of the token's metadata,

    which will save the ner, pos, slot, and so on ...
    """
    def __init__(self, text: str, ner: Optional[str] = None, 
                 pos: Optional[str] = None):
        self.text = text
        self.ner: Optional[str] = ner
        self.pos: Optional[str] = pos
