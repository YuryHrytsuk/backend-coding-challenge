from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from aspaara import crud
from aspaara.models import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/plannings")
def get_plannings(
    skip: int = 0,
    limit: int = 100,
    sort: crud.Sort = crud.Sort.ASC,
    filter_office_postal_code: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if limit > 1000:
        raise HTTPException(status_code=403, detail="'limit' must be <= 1000")

    import logging
    logging.warning(sort)

    plannings = crud.get_plannings(
        db,
        skip=skip,
        limit=limit,
        sort=sort,
        filter_office_postal_code=filter_office_postal_code,
    )
    return [
        {**p.__dict__, "talent": p.talent, "client": p.client, "job_manager": p.job_manager}
        for p in plannings
    ]
