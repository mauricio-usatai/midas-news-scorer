from typing import Optional
from abc import ABC, abstractmethod
from io import StringIO


class ObjectStorage(ABC):
    """
    Object storage "interface"
    """

    @abstractmethod
    def put(self, path: str, bucket: str, body: StringIO) -> None:
        """
        Puts an object in an remote object storage

        Args:
            path (str): The path of the object
            bucket (str): The name of the bucket
            body (StringIO): The file data
        """
        raise NotImplementedError

    def get(self, path: str, bucket: str) -> Optional[StringIO]:
        """
        Get an object from the remote object storage and
        return it as a readable stream

        Args:
            path (str): The path of the object
            bucket (str): The name of the bucket
        """
        raise NotImplementedError
