from health_company_data_api import db
from health_company_data_api.common.abstract_model import AbstractModel


class PatientsModel(db.Model, AbstractModel):
    __tablename__ = 'patients'

    uuid = db.Column(db.String(256), nullable=False, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
