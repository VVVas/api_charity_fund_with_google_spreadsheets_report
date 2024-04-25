from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)

router = APIRouter()


@router.get(
    '/',
    response_model=str,
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
) -> str:
    """Формирование отчёта и получение ссылки на него."""
    charity_projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    charity_projects_quantity = len(charity_projects)
    spreadsheetid = await spreadsheets_create(charity_projects_quantity,
                                              wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    charity_projects,
                                    wrapper_services)
    return f'https://docs.google.com/spreadsheets/d/{spreadsheetid}'
