from langchain.schema import SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

from settings import Settings
from .llm_chat import LLMChat
from ..logger import logging


settings = Settings()
logger = logging.getLogger(settings.LOGGER)


class ChatGPT35(LLMChat):
    def __init__(self):
        self.context = settings.MODEL_CONTEXT
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
        )

    def send_message_from_template(
        self,
        human_message_template: str,
        **template_args,
    ) -> str:
        """
        Get answer from chatGPT model

        Args:
            human_message_template (str): A message template
            template_args: The values to be replaced on the template

        Returns:
            str: The response from the model
        """

        context = SystemMessage(content=self.context)
        message = HumanMessagePromptTemplate.from_template(
            template=human_message_template
        )
        chat_prompt = ChatPromptTemplate.from_messages(messages=[context, message])
        chat_prompt_with_values = chat_prompt.format_prompt(**template_args)

        response = self.llm(chat_prompt_with_values.to_messages())

        return response.content
