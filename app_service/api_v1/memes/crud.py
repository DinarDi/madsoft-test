from fastapi import (
    UploadFile,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import (
    select,
    Result,
)

from database import Meme
from .schemas import (
    MemeBase,
    MemeUpdate,
    MemeResponse,
)
from s3connect import s3connect


async def get_memes(
        session: AsyncSession,
        offset: int = 1,
        limit: int = 10,
):
    """
    Возвращает все мемы
    :param session: AsyncSession
    :param offset: int
    :param limit: int
    :return: list(Meme)
    """
    stmt = select(Meme).offset(offset).limit(limit)
    result: Result = await session.execute(stmt)
    memes = result.scalars().all()
    return list(memes)


async def get_meme(
        session: AsyncSession,
        pk: int,
):
    """
    Возвращает мем
    :param session: AsyncSession
    :param pk: id мема
    :return: Meme
    """
    stmt = select(Meme).where(Meme.id == pk)
    res: Result = await session.execute(stmt)
    meme = res.scalar_one()
    return meme


async def create_meme(
        session: AsyncSession,
        payload: MemeBase,
        file: UploadFile,
) -> Meme:
    """
    Добавить мем в бд
    :param session: AsyncSession
    :param payload: MemeBase
    :param file: UploadFile
    :return: Meme
    """
    data = payload.model_dump()
    meme: Meme = Meme(
        title=payload.title,
        description=payload.description
    )
    session.add(meme)

    res = await s3connect.create_file(
        data=data,
        file=file
    )
    if res.status_code == 500:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'error_message': 'Something went wrong'
            },
        )
    meme.img_url = res.json()['img_link']
    await session.commit()
    await session.refresh(meme)
    return meme


async def update_meme(
        session: AsyncSession,
        pk: int,
        payload: MemeUpdate | None,
        file: UploadFile | None
):
    stmt = select(Meme).where(Meme.id == pk)
    try:
        res: Result = await session.execute(stmt)
        meme = res.scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'error_message': 'Meme not found'
            }
        )
    if payload:
        for k, v in payload.model_dump().items():
            if v is not None:
                setattr(meme, k, v)

    data = MemeResponse.model_validate(meme).model_dump()
    if file:
        result = await s3connect.update_file(
            data=data,
            file=file
        )
        if result.status_code == 500:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    'error_message': 'Something went wrong'
                },
            )
        meme.img_url = result.json()['img_link']
    await session.commit()
    await session.refresh(meme)
    return meme


async def delete_meme(
        session: AsyncSession,
        meme_id: int
):
    stmt = select(Meme).where(Meme.id == meme_id)
    res: Result = await session.execute(stmt)
    meme = res.scalar_one()

    result = await s3connect.delete_file(
        meme=meme
    )
    if result.status_code == 500:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'error_message': 'Something went wrong'
            },
        )

    await session.delete(meme)
    await session.commit()
