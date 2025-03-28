import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None
__engine = None

def global_init() -> None:
    global __factory
    
    if __factory:
        return

    conn_str = f"postgresql://postgres:postgres@127.0.0.1:5432/mars-egor"
    print(f"Подключение к базе данных по адресу {conn_str}")

    global __engine
    __engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=__engine)

    from . import __all_models
    
    SqlAlchemyBase.metadata.create_all(__engine)


def create_session() -> Session:
    global __factory
    return __factory()

def create_engine() -> Session:
    global __engine
    return __engine
