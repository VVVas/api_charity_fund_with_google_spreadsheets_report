from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_charity_project_full_amount_more_invested_amount,
    check_charity_project_fully_invested,
    check_charity_project_invested_amounts,
    check_charity_project_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investment import close_obj, investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> list[CharityProjectDB]:
    """Получение всех проектов."""
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Создание проекта, только для администратора."""
    await check_charity_project_name_duplicate(charity_project.name, session)

    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )

    await investment(new_charity_project, Donation, session)

    return new_charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Удаление проекта, только для администратора."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    await check_charity_project_invested_amounts(
        charity_project
    )

    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Обновление проекта, только для администратора."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    await check_charity_project_fully_invested(
        charity_project,
    )

    if obj_in.name is not None:
        await check_charity_project_name_duplicate(
            obj_in.name, session
        )

    if obj_in.full_amount is not None:
        await check_charity_project_full_amount_more_invested_amount(
            charity_project, obj_in.full_amount
        )

    charity_project = await charity_project_crud.update(
        db_obj=charity_project, obj_in=obj_in, session=session
    )

    if obj_in.full_amount is not None:
        await close_obj(charity_project)
        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)

    return charity_project
