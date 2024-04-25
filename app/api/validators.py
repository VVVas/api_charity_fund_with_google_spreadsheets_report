from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка существования проекта с таким же именем."""
    charity_project_id = (
        await charity_project_crud.get_charity_project_id_by_name(
            charity_project_name, session
        )
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка существования проекта по его id."""
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден',
        )
    return charity_project


async def check_charity_project_invested_amounts(
        charity_project: CharityProject,
) -> None:
    """Проверка существования инвестированных средств в проект."""
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства',
        )


async def check_charity_project_full_amount_more_invested_amount(
        charity_project: CharityProject,
        charity_project_full_amount,
) -> None:
    """Проверка, что новая целевая суммы проекта не меньше собранной."""
    if charity_project_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Сумма не может быть меньше собранных средств',
        )


async def check_charity_project_fully_invested(
        charity_project: CharityProject,
) -> None:
    """Проверка проекта на закрытие."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект закрыт',
        )
