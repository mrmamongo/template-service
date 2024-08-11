from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import func

metadata_obj = MetaData()

users_table = Table(
    'users',
    metadata_obj,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('google_id', String, nullable=False),
    schema='template_schema',
)
