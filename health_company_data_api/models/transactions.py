from health_company_data_api import db
from health_company_data_api.common.abstract_model import AbstractModel


class TransactionsModel(db.Model, AbstractModel):
    __tablename__ = "transactions"

    uuid = db.Column(db.String(256), nullable=False, primary_key=True)
    patient_uuid = db.Column(db.String(256), db.ForeignKey("patients.uuid"))
    pharmacy_uuid = db.Column(
        db.String(256), db.ForeignKey("pharmacies.uuid"), nullable=False
    )
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
