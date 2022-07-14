from health_company_data_api import db
from health_company_data_api.common.abstract_model import AbstractModel


class UsersModel(db.Model, AbstractModel):
    __tablename__ = 'users'

    uuid = db.Column(db.String(256), nullable=False, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)
