from typing import BinaryIO

from miniopy_async import Minio

from core import media_settings


class S3Config:
    def __init__(
            self,
            endpoint: str,
            access_key: str,
            secret_key: str,
            bucket: str,
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
            cert_check=False
        )
        self.bucket = bucket

    async def upload_file(
            self,
            file_name: str,
            file: BinaryIO
    ) -> str:
        """
        Метод для загрузки файла
        :param file_name: Имя файла
        :param file: Файл для отправки
        :return: url
        """
        await self.client.put_object(
            bucket_name=self.bucket,
            object_name=file_name,
            data=file,
            length=-1,
            part_size=100 * 1024 * 1024,
        )
        return f'localhost:9000/{self.bucket}/{file_name}'

    async def update_file(
            self,
            old_file_name: str,
            file_name: str,
            file: BinaryIO
    ):
        """
        Метод для обновления файла
        :param old_file_name: Старое имя файла
        :param file_name: Новой имя файла
        :param file: Новый файл для отправки
        :return: Новый url
        """
        await self.client.remove_object(
            bucket_name=self.bucket,
            object_name=old_file_name,
        )

        url = await self.upload_file(
            file_name=file_name,
            file=file
        )
        return url

    async def delete_file(
            self,
            file_name: str
    ):
        """
        Метод для удаления файла
        :param file_name: Имя файла
        """
        await self.client.remove_object(
            bucket_name=self.bucket,
            object_name=file_name
        )


minio_handler = S3Config(
    endpoint=media_settings.ENDPOINT,
    access_key=media_settings.MINIO_SERVER_ACCESS_KEY,
    secret_key=media_settings.MINIO_SERVER_SECRET_KEY,
    bucket=media_settings.BUCKET,
)
