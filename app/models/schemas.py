from sqlmodel import Field, Session, SQLModel, create_engine, text

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

engine = create_engine("sqlite:///database.db", echo=True)
session = Session(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", age=50)
    hero_2 = Hero(name="Spider", secret_name="Peter Parker", age=25)
    hero_3 = Hero(name="Wolverine", secret_name="Logan", age=100)

    with session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()
        session.close()

def read_heroes():
    with session:
        satement = session.exec(text('SELECT * from hero'))
        for hero in satement:
            print(hero)
        session.commit()
       
def delete_heroes():
    with session:
        satement = session.exec(text('DELETE from hero'))
        print(f"Deleted {satement.rowcount} heroes")
        session.commit()
session.close()

# create_db_and_tables()
# create_heroes()
# read_heroes()
# delete_heroes()