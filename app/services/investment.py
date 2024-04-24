from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import aware_utcnow
from app.models import CharityProject, Donation


async def close_obj(
        obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """Закрытие проекта или пожертвования."""
    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = aware_utcnow()
    return obj


async def calc_investment(
    new_obj: Union[CharityProject, Donation],
    open_obj: Union[CharityProject, Donation],
) -> list[Union[CharityProject, Donation], Union[CharityProject, Donation]]:
    """Распределение средств между проектом и пожертвованием."""
    to_close_new_obj = new_obj.full_amount - new_obj.invested_amount
    to_close_open_obj = open_obj.full_amount - open_obj.invested_amount

    if to_close_new_obj <= to_close_open_obj:
        open_obj.invested_amount += to_close_new_obj
        new_obj.invested_amount += to_close_new_obj

    else:
        open_obj.invested_amount += to_close_open_obj
        new_obj.invested_amount += to_close_open_obj

    return new_obj, open_obj


async def investment(
    new_obj: Union[CharityProject, Donation],
    open_obj_model: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """Перебор открытых объектов и их закрытие при распределениие средств."""
    open_objs = await session.execute(
        select(open_obj_model).where(open_obj_model.fully_invested == False) # noqa
    )
    open_objs = open_objs.scalars().all()

    for open_obj in open_objs:
        new_obj, open_obj = await calc_investment(new_obj, open_obj)

        if open_obj.invested_amount == open_obj.full_amount:
            open_obj = await close_obj(open_obj)
        session.add(open_obj)

        if new_obj.invested_amount == new_obj.full_amount:
            new_obj = await close_obj(new_obj)
            break

    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)
