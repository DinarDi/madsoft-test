import httpx
from fastapi import UploadFile

from core import settings
from api_v1.memes.schemas import (
    MemeCreateRequest,
    MemeResponse,
)
from database import Meme


class S3Connect:
    async def create_file(
            self,
            data: MemeCreateRequest,
            file: UploadFile,
    ):
        async with httpx.AsyncClient(trust_env=True) as client:
            res = await client.post(
                f'{settings.MEDIA_URL}/api/v1/media/',
                files={
                    'file': (data.get('title') + file.filename, file.file)
                }
            )
        return res

    async def update_file(
            self,
            data: MemeResponse,
            file: UploadFile,
    ):
        async with httpx.AsyncClient(trust_env=True) as client:
            res = await client.put(
                f'{settings.MEDIA_URL}/api/v1/media/{data.get('img_url').split('/')[-1]}',
                files={
                    'file': (data.get('title') + file.filename, file.file)
                }
            )
        return res

    async def delete_file(
            self,
            meme: Meme,
    ):
        async with httpx.AsyncClient(trust_env=True) as client:
            res = await client.delete(
                f'{settings.MEDIA_URL}/api/v1/media/{meme.img_url.split('/')[-1]}'
            )
        return res


s3connect = S3Connect()
