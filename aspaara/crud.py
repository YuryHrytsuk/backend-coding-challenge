from enum import Enum
from typing import Optional

from sqlalchemy.orm import Session

from aspaara import models


class Sort(Enum):
    ASC = "asc"
    DESC = "desc"


def get_planning_by_id(db: Session, planning_id: int):
    return db.query(models.Planning).filter(models.Planning.id == planning_id).first()


def get_plannings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    sort: Sort = Sort.ASC,
    filter_office_postal_code: Optional[str] = None,
):
    query = db.query(models.Planning)

    if sort is Sort.ASC:  # Sorting
        query = query.order_by(models.Planning.start_date.asc())
    else:
        query = query.order_by(models.Planning.start_date.desc())

    if filter_office_postal_code is not None:  # Filtering
        query = query.filter(models.Planning.office_postal_code == filter_office_postal_code)

    query = query.offset(skip).limit(limit)  # Pagination

    return query.all()
