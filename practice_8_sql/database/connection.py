from sqlmodel import SQLModel, Session, create_engine

database_file = "planner.db"
database_url = f"sqlite:///{database_file}"

engine = create_engine(
    database_url,
    echo=True,
    connect_args={"check_same_thread": False}
)


def conn():
    from models.events import Event
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
