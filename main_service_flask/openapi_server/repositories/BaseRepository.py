from uuid import UUID

from flask import abort

# for import export
import io
import csv

from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete, or_, func

from openapi_server.config import normalize_skill_name
from openapi_server.database.init_database import Session
from openapi_server.database.tables import CandidateDB, candidate_skills, SkillDB, internship_skills, InternshipDB
from openapi_server.repositories.filter_sort import apply_filters, apply_sorting


class BaseRepository:
	def __init__(self, model, def_sort_by = "name"):
		self.model = model
		self.def_sort_by = def_sort_by

	def get_all(self, filters: dict = None, offset: int = 0, limit: int = 10, sort_by: str = None,
				sort_order: str = "asc"):
		# try:
			with Session() as db:
				query = db.query(self.model)
				query = apply_filters(query, filters)
				default_sort_by = "name" if self.model.__name__ == "CandidateDB" else "position"
				query = apply_sorting(query, sort_by or default_sort_by, sort_order)
				total_items = query.count()
				items = query.offset(offset).limit(limit).all()
				remaining_items = total_items - (offset + len(items))
				return {
					"pagination": {
						"total": total_items,
						"limit": limit,
						"offset": offset,
						"remaining": remaining_items
					},
					"data": [item.to_candidateWithId() if hasattr(item, 'to_candidateWithId')
							 else item.to_internshipsWithId()
							 for item in items]
				}
		# except SQLAlchemyError:
		#	 abort(500, description="Database error.")

	def get_by_id(self, item_id: str):
		item_uuid = self.validate_uuid(item_id)
		try:
			with Session() as db:
				item = db.query(self.model).filter(self.model.uuid == item_uuid).first()
				if item:
					return item.to_candidateWithId() if hasattr(item,'to_candidateWithId') else item.to_internshipsWithId()
				else:
					abort(404, description=f"{self.model.__name__} not found.")
		except SQLAlchemyError as e:
			abort(500, description="Database error.")

	def delete(self, item_id: str):
		item_uuid = self.validate_uuid(item_id)
		query = delete(self.model).where(self.model.uuid == item_uuid)
		with Session() as session:
			result = session.execute(query)
			session.commit()
		if result.rowcount > 0:
			return "Successful operation"
		abort(404)

	def add(self, data: dict):
		try:
			with Session() as db:
				if hasattr(self.model, 'email') and 'email' in data:
					existing_item = db.query(self.model).filter(self.model.email == data['email']).first()
					if existing_item:
						abort(400, description="Candidate with this email already exists.")

				skills = []
				if hasattr(self.model, 'skills') and 'skills' in data:
					skills = self.process_skills(db, data['skills'])
					data = data.copy()
					del data['skills']

				new_item = self.model(**data)

				# Привязка skills к объекту
				if hasattr(new_item, 'skills'):
					new_item.skills = skills

				db.add(new_item)
				db.commit()
				db.refresh(new_item)
				return new_item.to_candidateWithId() if hasattr(new_item, 'to_candidateWithId') else new_item.to_internshipsWithId(), 201
		except SQLAlchemyError as e:
			abort(500, description=f"Database error: {e}")

	def update(self, item_id: str, new_values: dict):
		item_uuid = self.validate_uuid(item_id)
		try:
			with Session() as session:
				item_to_update = session.query(self.model).filter(self.model.uuid == item_uuid).first()
				if not item_to_update:
					abort(404, description="Item not found.")

				if hasattr(self.model, 'skills') and 'skills' in new_values:
					skills = self.process_skills(session, new_values['skills'])
					item_to_update.skills = skills
					new_values = new_values.copy()
					del new_values['skills']

				for attr, value in new_values.items():
					setattr(item_to_update, attr, value)

				session.commit()
				session.refresh(item_to_update)

				return item_to_update.to_candidateWithId() if hasattr(item_to_update,
																	  'to_candidateWithId') else item_to_update.to_internshipsWithId()

		except SQLAlchemyError:
			abort(500, description="Database error.")

	def export_to_csv(self, filters: dict = None, offset: int = 0, limit: int = 10, sort_by: str = None,
				sort_order: str = "asc"):
		get_response = self.get_all(filters, limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order)
	
		data = get_response.get("data")
		if not data:
			abort(204, "Nothing to return")

		csv_file = 'response.csv'
		csv_columns = list(data[0].body.keys())
		csv_columns[csv_columns.index("employmentType")] = "employment_type"
		csv_columns[csv_columns.index("hoursPerWeek")] = "hours_per_week"
		csv_columns[csv_columns.index("pathToResume")] = "path_to_resume"
		
		with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			
			for item in data:
				item.body["employment_type"] = item.body["employmentType"]
				del(item.body["employmentType"])
				item.body["hours_per_week"] = item.body["hoursPerWeek"]
				del(item.body["hoursPerWeek"])
				item.body["path_to_resume"] = item.body["pathToResume"]
				del(item.body["pathToResume"])
				writer.writerow(item.body)

		with open(csv_file, 'rb') as csvfile:
			return csvfile.read()
	
	def import_from_csv(self, file):
		try:
			binary_string = file.read()

			file_like = io.StringIO(binary_string.decode('utf-8'))
			dict_reader = csv.DictReader(file_like)
			try:
				for column_name in dict_reader.fieldnames:
					getattr(self.model, column_name)
			except:
				abort(400, f"Provided file contains columns absent in database: {column_name}")
			for row in dict_reader:
				row["skills"] = row["skills"].split(', ')
				row["employment_type"] = row["employment_type"].split(', ')
				try:
					self.add(row)
				except HTTPException as e:
					print(f"Candidate with email: {e} was skipped")
			return "Импортирование завершенно успешно"
		except SQLAlchemyError as e:
			abort(500, f"Database error: {e}")
		except Exception as e:
			abort(500, f"Unhandled error: {e}")

	@staticmethod
	def validate_uuid(uuid_to_validate) -> UUID:
		try:
			return UUID(uuid_to_validate)
		except ValueError:
			abort(400, description="Invalid UUID format.")

	@staticmethod
	def process_skills(session, skill_names: list[str]) -> list:
		"""Обрабатывает список скиллов: нормализует, проверяет наличие в БД, создает новые при необходимости."""
		skills = []

		for raw_name in skill_names:
			normalized_name = normalize_skill_name(raw_name)
			skill = session.query(SkillDB).filter_by(name=normalized_name).first()
			if not skill:
				skill = SkillDB(name=normalized_name)
				session.add(skill)
				session.flush()
			skills.append(skill)

		return skills