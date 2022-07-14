from health_company_data_api import db
from health_company_data_api.common.abstract_model import AbstractModel


class PharmaciesModel(db.Model, AbstractModel):
    __tablename__ = 'pharmacies'

    uuid = db.Column(db.String(256), nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
