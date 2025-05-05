from sqlmodel import create_engine, SQLModel

engine = create_engine('sqlite:///./library.db',echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)