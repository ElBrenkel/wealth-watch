from datetime import datetime
from marshmallow import Schema, fields, post_load
from src.data_objects.transaction_type import TransactionType
from src.data_objects.routine import Routine, RoutineSchema


class Transaction:
    def __init__(
        self,
        description: str,
        amount: float,
        transaction_type: TransactionType,
        transaction_date=datetime.utcnow(),
        routine: Routine | None = None,
    ):
        self.description = description
        self.amount = amount
        self.transaction_date = transaction_date
        self.transaction_type = transaction_type
        self.routine = routine

    def to_json(self):
        return {
            "amount": self.amount,
            "description": self.description,
            "transaction_type": self.transaction_type.name,
            "transaction_date": datetime.strftime(self.transaction_date, "%Y-%m-%d"),
            "routine": None if not self.routine else self.routine.to_json(),
        }


class TransactionSchema(Schema):
    description = fields.Str()
    amount = fields.Number()
    transaction_date = fields.Str(required=False)
    transaction_type = fields.Enum(TransactionType)
    routine = fields.Nested(RoutineSchema, required=False)

    @post_load
    def make_transaction(self, transaction, **kwargs):
        if transaction["transaction_date"]:
            transaction["transaction_date"] = datetime.strptime(
                transaction["transaction_date"], "%Y-%m-%d"
            )
        return Transaction(**transaction)


# x = {
#     "description": "shalomiesss",
#     "amount": 354.5,
#     "transaction_date": "2024-08-19",
#     "transaction_type": "SPENDING",
# }

# sh = TransactionSchema().load(x)
# g = 1
