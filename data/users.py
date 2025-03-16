import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"
    
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    position = sqlalchemy.Column(sqlalchemy.String)
    speciality = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    
    jobs = orm.relationship("Jobs", back_populates="leader")
    departments = orm.relationship("Departments", back_populates="user_chief")
    
    def set_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password: str) -> check_password_hash:
        return check_password_hash(self.hashed_password, password)
    
    def __repr__(self) -> str:
        return f"<Colonist> {self.id} {self.surname} {self.name}"

