import json
from io import StringIO

import pandas as pd

from settings import Settings
from .object_storage import ObjectStorage


settings = Settings()


def save_object(object_storage: ObjectStorage, key: str, obj: object) -> None:
    buffer = StringIO()
    if key[-3:] == "csv" and isinstance(obj, pd.DataFrame):
        obj.to_csv(buffer)
    elif key[-4:] == "json" and isinstance(obj, dict):
        json.dump(obj, buffer)
    else:
        raise ValueError(
            "Could not determine file type when saving object to remote storage"
        )
    object_storage.put(
        path=f"char-responses/{settings.RUN_ID}-{key}",
        bucket=settings.BUCKET,
        body=buffer,
    )
