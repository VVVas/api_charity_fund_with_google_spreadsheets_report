from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationBase, DonationDB, DonationDBAdmin
from app.services.investment import investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBAdmin],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> list[DonationDBAdmin]:
    """Получение всех пожертвований, только для администратора."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDB,
)
async def create_donation(
    donation: DonationBase,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> DonationDB:
    """Создание пожертвования."""
    new_donation = await donation_crud.create(
        donation, session, user
    )

    await investment(new_donation, CharityProject, session)

    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> list[DonationDB]:
    """Получение своих пожертвований пользователем."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
