from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid

from sqlalchemy.orm import relationship

from openapi_server.database.init_database import Base, engine

from openapi_server.models import Candidate, CandidateWithId, InternshipWithId

class SkillDB(Base):
    __tablename__ = 'skills'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)

candidate_skills = Table(
    'candidate_skills',
    Base.metadata,
    Column('candidate_uuid', UUID(as_uuid=True), ForeignKey('candidates.uuid'), primary_key=True),
    Column('skill_uuid', UUID(as_uuid=True), ForeignKey('skills.uuid'), primary_key=True)
)

internship_skills = Table(
    'internship_skills',
    Base.metadata,
    Column('internship_uuid', UUID(as_uuid=True), ForeignKey('internships.uuid'), primary_key=True),
    Column('skill_uuid', UUID(as_uuid=True), ForeignKey('skills.uuid'), primary_key=True)
)

class CandidateDB(Base):
    __tablename__ = 'candidates'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(15), nullable=True)
    position = Column(String(100), nullable=True)
    education = Column(String(100), nullable=True)
    experience = Column(String(100), nullable=True)
    hours_per_week = Column(Integer, nullable=True)
    employment_type = Column(ARRAY(String), nullable=True)
    links = Column(String(100), nullable=True)
    path_to_resume = Column(String(100), nullable=True)  # ! this should be path_to_resume, might need to change variable name

    skills = relationship("SkillDB", secondary=candidate_skills, backref="candidates")

    def to_dict(self):
        employment_type_str = ', '.join(self.employment_type) if self.employment_type else ''
        skills_str = ', '.join([skill.name for skill in self.skills]) if self.skills else ''

        return {
            "uuid": str(self.uuid),
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "position": self.position,
            "education": self.education,
            "skills": skills_str,
            "experience": self.experience,
            "hoursPerWeek": self.hours_per_week,
            "employmentType": employment_type_str,
            "links": self.links,
            "pathToResume": self.path_to_resume
        }

    def to_candidateWithId(self) -> CandidateWithId:
        body = self.to_dict()
        del body["uuid"]
        return CandidateWithId(self.uuid, body)


class InternshipDB(Base):
    __tablename__ = 'internships'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    position = Column(String(100), nullable=True)
    education = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    hours_per_week = Column(Integer, nullable=True)
    employment_type = Column(ARRAY(String), nullable=True)
    description = Column(String(100), nullable=True)
    status = Column(String(100), nullable=True)

    skills = relationship("SkillDB", secondary=internship_skills, backref="internships")

    def to_dict(self):
        employment_type_str = ', '.join(self.employment_type) if self.employment_type else ''
        skills_str = ', '.join([skill.name for skill in self.skills]) if self.skills else ''
        return {
            "uuid": str(self.uuid),
            "position": self.position,
            "education": self.education,
            "skills": skills_str,
            "department": self.department,
            "hoursPerWeek": self.hours_per_week,
            "employmentType": employment_type_str,
            "description": self.description,
            "status": self.status,
        }

    def to_internshipsWithId(self) -> InternshipWithId:
        body = self.to_dict()
        del body["uuid"]
        return InternshipWithId(self.uuid, body)


# class CandidateDB(Base):
#     __tablename__ = 'candidates_test'
#
#     uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String(100), nullable=True)
#     email = Column(String(100), nullable=True)
#     phone = Column(String(10), nullable=True)
#     position = Column(String(100), nullable=True)
#     education = Column(String(100), nullable=True)
#     skills = Column(String(300), nullable=True)
#     experience = Column(String(100), nullable=True)
#     hours_per_week = Column(Integer, nullable=True)
#     employment_type = Column(String(10), nullable=True)
#     links = Column(String(100), nullable=True)
#     path_to_resume = Column(String(100), nullable=True)
#
#     def to_dict(self):
#         return {
#             "uuid": str(self.uuid),
#             "name": self.name,
#             "email": self.email,
#             "phone": self.phone,
#             "position": self.position,
#             "education": self.education,
#             "skills": self.skills,
#             "experience": self.experience,
#             "hoursPerWeek": self.hours_per_week,
#             "employmentType": self.employment_type,
#             "links": self.links,
#             "pathToResume": self.path_to_resume
#         }
#
#     def to_candidateWithId(self) -> CandidateWithId:
#         body = self.to_dict()
#         del body["uuid"]
#         return CandidateWithId(self.uuid, body)
#
#
# class InternshipDB(Base):
#     __tablename__ = 'internships_test'
#
#     uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     position = Column(String(100), nullable=True)
#     education = Column(String(100), nullable=True)
#     skills = Column(String(300), nullable=True)
#     department = Column(String(100), nullable=True)
#     hours_per_week = Column(Integer, nullable=True)
#     employment_type = Column(String(10), nullable=True)
#     description = Column(String(100), nullable=True)
#     status = Column(String(100), nullable=True)
#
#     def to_dict(self):
#         return {
#             "uuid": str(self.uuid),
#             "position": self.position,
#             "education": self.education,
#             "skills": self.skills,
#             "department": self.department,
#             "hoursPerWeek": self.hours_per_week,
#             "employmentType": self.employment_type,
#             "description": self.description,
#             "status": self.status,
#         }
#
#     def to_internshipsWithId(self) -> InternshipWithId:
#         body = self.to_dict()
#         del body["uuid"]
#         return InternshipWithId(self.uuid, body)

