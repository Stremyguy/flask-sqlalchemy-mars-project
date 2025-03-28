from data.db_session import create_session, create_engine
from sqlalchemy.orm import Session
from data.category import Category
from sqlalchemy.dialects.postgresql import insert as pg_insert

def run_seeds() -> None:
    session = create_session()
    create_category(session)

def create_category(session: Session):
    # TODO написать создание категорий
    engine = create_engine()
    categories = ['Првая категория', 'Вторая категория', 'Третья категория']
    count = 1
    for i in categories:
        stmt = pg_insert(Category).values(id=count, name=i)
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],
            set_={'name': stmt.excluded.name}
        )

        conn = engine.connect()
        conn.execute(stmt)
        conn.commit()
        conn.close()
        
        session.commit()
        count += 1