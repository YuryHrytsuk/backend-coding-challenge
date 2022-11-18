import json
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from sqlalchemy.orm import sessionmaker

from aspaara import models as m
from aspaara.models import Base

engine = create_engine("sqlite:////test.db", echo=True)
Session = sessionmaker(engine)


def convert_to_dt(s):
    if s:
        return datetime.strptime(s, '%m/%d/%Y %H:%M %p')

    return s


def main():
    with open("/data/planning.json") as f:
        data = json.loads(f.read())

    Base.metadata.create_all(engine)

    clients = []
    job_manages = []
    talents = []
    plannings = []

    for item in data:
        if item.get("clientId"):
            clients.append(dict(id=item["clientId"], name=item.get("clientName")))

        if item.get("jobManagerId"):
            job_manages.append(
                dict(id=item["jobManagerId"], name=item.get("jobManagerName"))
            )

        if item.get("talentId"):
            talents.append(
                dict(id=item["talentId"], name=item.get("talentName"), grade=item.get("talentGrade"))
            )

        plannings.append(dict(
            id=item.get("id"),
            original_id=item.get("originalId"),
            talent_id=item.get("talentId"),
            booking_grade=item.get("bookingGrade"),
            operating_unit=item.get("operatingUnit"),
            office_city=item.get("officeCity"),
            office_postal_code=item.get("officePostalCode"),
            job_manager_id=item.get("jobManagerId"),
            total_hours=item.get("totalHours"),
            start_date= convert_to_dt(item.get("startDate")),
            end_date=convert_to_dt(item.get("endDate")),
            client_id=item.get("clientId"),
            industry=item.get("industry"),
            is_unassigned=item.get("isUnassigned"),
            required_skills=item.get("requiredSkills"),
            optional_skills=item.get("optionalSkills"),
        ))

    with Session.begin() as session:

        stmt = sqlite_upsert(m.Client).values(clients)
        stmt = stmt.on_conflict_do_nothing(index_elements=[m.Client.id])
        session.execute(stmt)

        stmt = sqlite_upsert(m.Talent).values(talents)
        stmt = stmt.on_conflict_do_nothing(index_elements=[m.Talent.id])
        session.execute(stmt)

        stmt = sqlite_upsert(m.JobManager).values(job_manages)
        stmt = stmt.on_conflict_do_nothing(index_elements=[m.JobManager.id])
        session.execute(stmt)

        stmt = sqlite_upsert(m.Planning).values(plannings)
        stmt = stmt.on_conflict_do_nothing(index_elements=[m.Planning.id])
        session.execute(stmt)


if __name__ == "__main__":
    main()
