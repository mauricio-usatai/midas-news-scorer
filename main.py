from typing import Union
import re

import numpy as np
import pandas as pd

from src import utils
from src.llm_model import ChatGPT35
from src.object_storage import S3ObjectStorage
from src.logger import logging
from settings import Settings


settings = Settings()
logger = logging.getLogger(settings.LOGGER)


def get_score(text: str) -> Union[str, float]:
    """
    Extracts a score from a model response
    """
    score = np.nan
    try:
        score_string = text.split("\n")[-1]
        score_candidate = int(re.findall(r"[-]?\d+", score_string)[0])
        if score_candidate <= 10 and score_candidate >= 0:
            score = score_candidate
    except (ValueError, IndexError) as err:
        logger.error(err)

    return score


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
    scores = []
    chat_responses = []
    for index in range(len(articles_df)):
        news_content = articles_df.iloc[index]["parsedContent"]

        if pd.isna(news_content):

            scores.append(np.nan)
            chat_responses.append(np.nan)
            continue

        chat_response = llm.send_message_from_template(
            human_message_template=settings.NEWS_PROMPT_TEMPLATE,
            news_content=news_content,
        )

        # Get score from model response
        chat_response = chat_response["content"]

        scores.append(get_score(chat_response))
        chat_responses.append(chat_response)

    articles_df["scores"] = scores
    articles_df["chatResponses"] = chat_responses

    # save to S3
    utils.save_object(
        object_storage=S3ObjectStorage(),
        key="gpt-responses.csv",
        obj=articles_df,
    )


if __name__ == "__main__":
    main()
