import numpy as np
import pandas as pd

from src import utils
from src.llm_model import ChatGPT35
from src.object_storage import S3ObjectStorage
from src.logger import logging
from settings import Settings


settings = Settings()
logger = logging.getLogger(settings.LOGGER)


def main():
    # Read from S3
    news_parsed_data = S3ObjectStorage().get(
        bucket=settings.BUCKET,
        path=f"news-feed-responses/{settings.RUN_ID}-articles.csv",
    )
    if not news_parsed_data:
        return

    articles_df = pd.read_csv(news_parsed_data)

    # get model response
    llm = ChatGPT35()
    chat_responses = []
    for index in range(len(articles_df)):
        news_content = articles_df.iloc[index]["parsedContent"]

        if pd.isna(news_content):
            chat_responses.append(np.nan)
            continue

        chat_response = llm.send_message_from_template(
            human_message_template=settings.NEWS_PROMPT_TEMPLATE,
            news_content=news_content,
        )

        chat_responses.append(chat_response["content"])

    articles_df["chatResponses"] = chat_responses

    # save to S3
    utils.save_object(
        object_storage=S3ObjectStorage(),
        key="gpt-responses.csv",
        obj=articles_df,
    )


if __name__ == "__main__":
    main()
