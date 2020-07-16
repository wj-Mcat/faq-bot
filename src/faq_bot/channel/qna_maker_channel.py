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

import json
import logging
import time
from dataclasses import dataclass
from typing import Union, Any

import httpx
from azure.cognitiveservices.knowledge.qnamaker.authoring import QnAMakerClient
from azure.cognitiveservices.knowledge.qnamaker.authoring.models import \
    CreateKbDTO, OperationStateType
from msrest.authentication import CognitiveServicesCredentials

from .channel import Channel, ChannelOptions

log = logging.getLogger(__name__)


@dataclass
class QnaMakerChannelOptions(ChannelOptions):
    authoring_key: str
    resource_name: str


class QnaMakerChannel(Channel):
    """
    connect the micorsoft Qna Maker service
    """

    async def ask_question(self, query: Union[str]) -> Any:
        pass

    def __init__(self, options: QnaMakerChannelOptions):
        super().__init__()
        self.options = options
        endpoint = f'https://wechatyqnachinese.azurewebsites.net/qnamaker/' \
              f'knowledgebases/{self.options.resource_name}/generateAnswer'

        self.client: QnAMakerClient = QnAMakerClient(
            endpoint=endpoint,
            credentials=CognitiveServicesCredentials(
                self.options.authoring_key
            )
        )

    @staticmethod
    def _monitor_operation(client: QnAMakerClient, operation):

        for i in range(20):
            if operation.operation_state in [OperationStateType.not_started,
                                             OperationStateType.running]:
                print("Waiting for operation: {} to complete.".format(
                    operation.operation_id))
                time.sleep(5)
                operation = client.operations.get_details(
                    operation_id=operation.operation_id)
            else:
                break
        if operation.operation_state != OperationStateType.succeeded:
            raise Exception("Operation {} failed to complete.".format(
                operation.operation_id))

        return operation

    def init_knowledge_base(self, knowledge: CreateKbDTO):
        """
        init the knowledge base

        eg:
            qna1 = QnADTO(
                answer="Yes, You can use our [REST APIs](https://docs.microsoft.com/rest/api/cognitiveservices/qnamaker/knowledgebase) to manage your knowledge base.",
                questions=["How do I manage my knowledgebase?"],
                metadata=[
                    MetadataDTO(name="Category", value="api"),
                    MetadataDTO(name="Language", value="REST"),
                ]
            )

            qna2 = QnADTO(
                answer="Yes, You can use our [Python SDK](https://pypi.org/project/azure-cognitiveservices-knowledge-qnamaker/) with the [Python Reference Docs](https://docs.microsoft.com/python/api/azure-cognitiveservices-knowledge-qnamaker/azure.cognitiveservices.knowledge.qnamaker?view=azure-python) to manage your knowledge base.",
                questions=["Can I program with Python?"],
                metadata=[
                    MetadataDTO(name="Category", value="api"),
                    MetadataDTO(name="Language", value="Python"),
                ]
            )

            urls = []
            files=[]

            create_kb_dto = CreateKbDTO(
                name="QnA Maker Python SDK Quickstart",
                qna_list=[
                    qna1,
                    qna2
                ],
                urls=urls,
                files=[],
                enable_hierarchical_extraction=True,
                default_answer_used_for_extraction="No answer found.",
                language="English"
            )

        """
        create_op = self.client.knowledgebase.create(
            create_kb_payload=knowledge
        )
        create_op_monitor = self._monitor_operation(
            client=self.client,
            operation=create_op
        )

        # Get knowledge base ID from resourceLocation HTTP header
        knowledge_base_ID = create_op_monitor.resource_location.replace(
            "/knowledgebases/", "")
        print("Created KB with ID: {}".format(knowledge_base_ID))
        return knowledge_base_ID

    async def generate_answer(self, query: Union[str]) -> Any:
        """
        this is the simple way to call the core interface
        send the query to Qna Maker and return the result
        """
        header = {
            'Authorization': f'EndpointKey {self.options.authoring_key}',
            'Content-Type': 'application/json'
        }
        url = f'https://wechatyqnachinese.azurewebsites.net/qnamaker/' \
              f'knowledgebases/{self.options.resource_name}/generateAnswer'

        async with httpx.AsyncClient(headers=header) as client:
            result = await client.post(
                url = url,
                json = {
                    'question': query
                }
            )
            return json.loads(result.text)

    def publish(self, knowledge_id: str):
        """publish the knowledge base"""
        log.info('publish the knowledge base')
        self.client.knowledgebase.publish(kb_id=knowledge_id)
