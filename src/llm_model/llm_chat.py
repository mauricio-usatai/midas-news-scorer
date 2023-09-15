from abc import ABC, abstractmethod


class LLMChat(ABC):
    @abstractmethod
    def send_message_from_template(
        self,
        human_message_template: str,
        **template_args,
    ) -> str:
        """
        Sends a message to a LLM model as a human

        Args:
            human_message_template (str): A message template
            template_args: The values to be replaced on the template

        Returns:
            str: The response from the model
        """
        raise NotImplementedError
