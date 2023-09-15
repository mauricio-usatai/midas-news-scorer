from typing import Optional

from io import BytesIO, StringIO

import boto3
from botocore.exceptions import ClientError

from settings import Settings

from ..logger import logging
from .object_storage import ObjectStorage


settings = Settings()
logger = logging.getLogger(settings.LOGGER)


class S3ObjectStorage(ObjectStorage):
    def __init__(self):
        if settings.DEPLOY == "local":
            self._s3 = boto3.resource(
                "s3",
                endpoint_url="http://minio:9000",
                aws_access_key_id="miniodev",
                aws_secret_access_key="miniodev",
                verify=False,
            )
        else:
            self._s3 = boto3.resource(
                "s3",
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

    def put(self, path: str, bucket: str, body: StringIO) -> None:
        """
        Saves a buf into a remote bucket

        Args:
            path (str): The path of the opbject to be stored, including its name
            bucket (str): Bucket name
            body (StringIO): The buf to be saved
        """
        obj = self._s3.Object(settings.BUCKET, path)
        try:
            # Convert to bytes
            body.seek(0)
            body = BytesIO(body.read().encode("utf-8"))
            obj.put(Body=body)
        except ClientError as err:
            logger.error(err)

    def get(self, path: str, bucket: str) -> Optional[StringIO]:
        obj = self._s3.Object(settings.BUCKET, path)
        try:
            response = obj.get()
            byte_stream = response["Body"]
        except (ClientError, KeyError) as err:
            logger.error(err)
            return None

        return StringIO(byte_stream.read().decode("utf-8"))
