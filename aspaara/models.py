from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:////test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Talent(Base):
    __tablename__ = "talent"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    grade = Column(String, nullable=True)

    plannings = relationship("Planning", back_populates="talent")

    def __repr__(self):
        return f"Talend(id={self.id}, name={self.name}, fullname={self.grade})"


class JobManager(Base):
    __tablename__ = "job_manager"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)

    plannings = relationship("Planning", back_populates="job_manager")

    def __repr__(self):
        return f"JobManager(id={self.id}, name={self.name})"


class Client(Base):
    __tablename__ = "client"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)

    plannings = relationship("Planning", back_populates="client")

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name})"


class Planning(Base):
    __tablename__ = "planning"

    id = Column(Integer, primary_key=True, index=True)
    original_id = Column(String, unique=True, nullable=False)

    talent_id = Column(String, ForeignKey("talent.id"), index=True)
    talent = relationship("Talent", back_populates="plannings")

    client_id = Column(String, ForeignKey("client.id"), index=True)
    client = relationship("Client", back_populates="plannings")

    job_manager_id = Column(String, ForeignKey("job_manager.id"), index=True)
    job_manager = relationship("JobManager", back_populates="plannings")

    booking_grade = Column(String, nullable=True)

    operating_unit = Column(String, nullable=False)

    office_city = Column(String, nullable=True)
    office_postal_code = Column(String, nullable=False)

    total_hours = Column(Float, nullable=False)
    start_date = Column(DateTime, index=True, nullable=False)
    end_date = Column(DateTime, nullable=False)

    industry = Column(String, nullable=True)

    optional_skills = Column(JSON, nullable=True)
    required_skills = Column(JSON, nullable=True)

    is_unassigned = Column(Boolean, nullable=False)

# class Skill(Base):
#     __tablename__ = "skill"
#
#     id = Column(Integer, primary_key=True, index=True, sqlite_autoincrement=True)
#     name = Column(String, nullable=False)
#     category = Column(String, nullable=False)

# plannings_required_skills_table = Table(
#     "plannings_required_skills",
#     Base.metadata,
#     Column("planning_id", ForeignKey("planning.id"), primary_key=True),
#     Column("skill_id", ForeignKey("skill.id"), primary_key=True),
# )
