import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./log/webServer.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50), nullable=False),
    sqlalchemy.UniqueConstraint("name"),
    sqlalchemy.Column("time", sqlalchemy.String(22), nullable=False),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
