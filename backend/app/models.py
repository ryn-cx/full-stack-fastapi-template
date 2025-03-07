from app.items.models import SQLModel as ItemSQLModel
from app.users.models import SQLModel as UserSQLModel

target_metadata = [UserSQLModel.metadata, ItemSQLModel.metadata]
