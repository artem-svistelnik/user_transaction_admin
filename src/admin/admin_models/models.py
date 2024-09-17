from sqladmin import ModelView
from models import User, Transaction


class UserAdmin(ModelView, model=User):
    can_create = False
    column_list = [User.id, User.username]
    form_columns = [User.id, User.username]
    column_labels = {"id": "ID", "username": "Username"}
    form_widget_args = {"id": {"readonly": True}}


class TransactionAdmin(ModelView, model=Transaction):
    can_create = False
    column_list = [
        Transaction.id,
        Transaction.user_id,
        Transaction.transaction_type,
        Transaction.amount,
        Transaction.created_at,
    ]
    form_columns = [
        Transaction.id,
        Transaction.transaction_type,
        Transaction.amount,
        Transaction.created_at,
    ]
    form_widget_args = {
        "id": {"readonly": True},
        "user_id": {"readonly": True},
        "created_at": {"readonly": True},
    }
