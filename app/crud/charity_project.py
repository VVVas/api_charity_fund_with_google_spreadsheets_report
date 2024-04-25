from datetime import datetime
from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[list[str, str, datetime, datetime]]:
        charity_projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    CharityProject.description,
                    CharityProject.create_date,
                    CharityProject.close_date
                ]
            ).where(
                CharityProject.fully_invested
            ).order_by(
                extract('year', CharityProject.close_date) -
                extract('year', CharityProject.create_date),
                extract('month', CharityProject.close_date) -
                extract('month', CharityProject.create_date),
                extract('day', CharityProject.close_date) -
                extract('day', CharityProject.create_date)
            )
        )
        charity_projects = charity_projects.all()
        return charity_projects


charity_project_crud = CRUDCharityProject(CharityProject)
