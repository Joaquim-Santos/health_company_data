from datetime import datetime
from dateutil.relativedelta import relativedelta
from marshmallow import Schema, fields, EXCLUDE, validate, post_load
from marshmallow.exceptions import ValidationError


# Definiu-se o filtro de idade como no mínimo 18, pois considerou-se que há apenas maiores de idade cadastrados.
class PatientsFiltersSchema(Schema):
    first_name = fields.Str(required=False, validate=[validate.Length(min=3, max=30)], allow_none=True)
    last_name = fields.Str(required=False, validate=[validate.Length(min=3, max=30)], allow_none=True)
    start_age = fields.Int(required=False, validate=[validate.Range(min=18)], allow_none=True)
    end_age = fields.Int(required=False, validate=[validate.Range(min=18)], allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, many, **kwargs):
        data_without_none = {key: value for key, value in data.items() if value is not None}

        try:
            if data_without_none['start_age'] > data_without_none['end_age']:
                raise ValidationError("Idade inicial não pode ser maior do que a final.")
        except KeyError:
            pass

        # Engloba quem ainda não completou a idade máxima no anoa atual.
        try:
            data_without_none['end_age'] += 1
        except KeyError:
            pass

        for key in ['start_age', 'end_age']:
            try:
                data_without_none[key] = datetime.now() - relativedelta(years=data_without_none[key])
                data_without_none[key] = data_without_none[key].replace(minute=0, hour=0, second=0, microsecond=0)
            except KeyError:
                continue

        return data_without_none
