from marshmallow import Schema, fields, EXCLUDE, validate, post_load


class PharmaciesFiltersSchema(Schema):
    name = fields.Str(
        required=False, validate=[validate.Length(min=3, max=50)], allow_none=True
    )
    city = fields.Str(
        required=False, validate=[validate.Length(min=3, max=50)], allow_none=True
    )

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, many, **kwargs):
        return {key: value for key, value in data.items() if value is not None}
