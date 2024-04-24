from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base
from app.core.utils import aware_utcnow


class ProjectDonationBase(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=aware_utcnow)
    close_date = Column(DateTime)
