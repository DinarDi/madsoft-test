from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    UploadFile,
    File,
    Response,
)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    NoResultFound,
)

from api_v1.memes import crud as meme_crud
from database import db_manager
from .schemas import (
    ApiMemeListResponse,
    ApiMemeResponse,
    MemeResponse,
    MemeCreateRequest,
    ApiMemeCreateResponse,
    MemeUpdateRequest,
    ApiMemeUpdateResponse,
)


memes_router = APIRouter(
    tags=['Memes'],
)


@memes_router.get(
    '/',
    response_model=ApiMemeListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_memes(
        session: AsyncSession = Depends(db_manager.get_session),
        page: int = 1,
        limit: int = 10,
):
    try:
        offset = (page - 1) * limit
        memes = await meme_crud.get_memes(
            session=session,
            offset=offset,
            limit=limit
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'error_message': 'Something went wrong'
            }
        )
    response = [
        MemeResponse.model_validate(meme).model_dump() for meme in memes
    ]
    return JSONResponse(
        content={
            'page': page,
            'limit': limit,
            'data': response
        },
        status_code=status.HTTP_200_OK
    )


@memes_router.get(
    '/{meme_id}',
    response_model=ApiMemeResponse,
    status_code=status.HTTP_200_OK,
)
async def get_meme(
        meme_id: int,
        session: AsyncSession = Depends(db_manager.get_session),
):
    try:
        meme = await meme_crud.get_meme(
            session=session,
            pk=meme_id
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'error_message': 'Meme not found'
            }
        )

    response = MemeResponse.model_validate(meme).model_dump()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'data': response
        }
    )


@memes_router.post(
    '/',
    response_model=ApiMemeCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_meme(
        payload: MemeCreateRequest,
        file: UploadFile,
        session: AsyncSession = Depends(db_manager.get_session),
):
    try:
        meme = await meme_crud.create_meme(
            session=session,
            payload=payload,
            file=file
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                'error_message': 'Meme with this title already exists'
            }
        )

    meme_response = MemeResponse.model_validate(meme).model_dump()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'data': meme_response
        }
    )


@memes_router.put(
    '/{meme_id}',
    response_model=ApiMemeUpdateResponse,
    status_code=status.HTTP_200_OK,
)
async def update_meme(
        meme_id: int,
        payload: Annotated[MemeUpdateRequest, None] = None,
        file: Annotated[UploadFile, File] = File(None),
        session: AsyncSession = Depends(db_manager.get_session)
):
    try:
        meme = await meme_crud.update_meme(
            session=session,
            pk=meme_id,
            payload=payload,
            file=file
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                'error_message': 'Meme with this title already exists'
            }
        )

    response = MemeResponse.model_validate(meme).model_dump()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'data': response
        }
    )


@memes_router.delete(
    '/{meme_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_meme(
        meme_id: int,
        session: AsyncSession = Depends(db_manager.get_session),
):
    try:
        await meme_crud.delete_meme(
            session=session,
            meme_id=meme_id
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'error_message': 'Meme not found'
            }
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
