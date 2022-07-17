from marshmallow import Schema, fields, EXCLUDE, validate, post_load


class TransactionsFiltersSchema(Schema):
    from_amount = fields.Float(
        required=False, validate=[validate.Range(min=0)], allow_none=True
    )
    from_timestamp = fields.DateTime(
        required=False, format="%Y-%m-%d %H:%M:%S", allow_none=True
    )

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data, many, **kwargs):
        return {key: value for key, value in data.items() if value is not None}
