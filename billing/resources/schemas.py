from marshmallow import Schema, fields, INCLUDE, ValidationError


def is_positive(n):
    if n < 0:
        raise ValidationError("Value must be greater than 0.")


class CreateAccountSchema(Schema):
    balance = fields.Decimal(
        required=False,
        allow_none=False,
        missing=0,
        validate=is_positive,
        description="Начальный баланс"
    )

    class Meta:
        strict = True
        unknown = INCLUDE


class AddMoneySchema(Schema):
    user_id = fields.Integer(
        required=True,
        allow_none=False,
        description="ID пользователя"
    )
    amount = fields.Decimal(
        required=True,
        allow_none=False,
        validate=is_positive,
        description="Сумма"
    )

    class Meta:
        strict = True
        unknown = INCLUDE


class TransferSchema(Schema):
    source_user_id = fields.Integer(
        required=True,
        allow_none=False,
        description="ID пользователя отправителя"
    )
    target_user_id = fields.Integer(
        required=True,
        allow_none=False,
        description="ID пользователя получателя"
    )
    amount = fields.Decimal(
        required=True,
        allow_none=False,
        validate=is_positive,
        description="Сумма"
    )

    class Meta:
        strict = True
        unknown = INCLUDE
