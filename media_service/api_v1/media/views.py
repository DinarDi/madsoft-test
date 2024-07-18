from fastapi import (
    APIRouter,
    UploadFile,
    File,
    status,
    HTTPException,
    Response,
)
from fastapi.responses import JSONResponse
from miniopy_async.error import S3Error

from s3_settings import minio_handler


media_router = APIRouter(
    tags=['Media'],
)


@media_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def upload_image(file: UploadFile = File()):
    try:
        link_to_file = await minio_handler.upload_file(
            file_name=file.filename,
            file=file.file,
        )
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'error_message': 'Error in s3 service'
            }
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'img_link': link_to_file
        },
    )


@media_router.put(
    '/{img_name}',
    status_code=status.HTTP_200_OK,
)
async def update_img(
        img_name: str,
        file: UploadFile = File(),
):
    try:
        link_to_file = await minio_handler.update_file(
            old_file_name=img_name,
            file_name=file.filename,
            file=file.file
        )
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'error_message': 'Error in s3 service'
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'img_link': link_to_file
        }
    )


@media_router.delete(
    '/{file_name}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_img(
        file_name: str
):
    try:
        await minio_handler.delete_file(
            file_name=file_name
        )
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'error_message': 'Error in s3 service'
            }
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
