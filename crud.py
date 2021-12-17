from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update
from schemas.user import UserLogin, UserSignup
from schemas.car import CarCreate, UpdateCar
from models import User, Car
import datetime, uuid
from auth import Auth
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, Union

auth_handler = Auth()
security = HTTPBearer()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserSignup):
    hashed_password = auth_handler.encode_password(user.password)
    new_date = str(datetime.datetime.now())

    db_user = User(
        username = user.username,
        password = hashed_password,
        name = user.name,
        created_at = new_date,
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login(user_details: UserLogin):
    access_token = auth_handler.encode_token(user_details.username)
    refresh_token = auth_handler.encode_refresh_token(user_details.username)
    return {'access_token': access_token, 'refresh_token': refresh_token}

def create_user_car(db: Session, car_details: CarCreate, user_id: int):
    new_date = str(datetime.datetime.now())
    db_item = Car(
        name = car_details.name,
        model_name = car_details.model_name,
        created_at = new_date,
        year_released = car_details.year_released,
        user_id = user_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_cars_by_user(db: Session, user_id: int):
    cars = db.query(Car).filter(Car.user_id == user_id).all()
    return cars

def get_car_by_id(db: Session, user_id: int, car_id: int):
    cars = db.query(Car).filter(
        Car.user_id == user_id
        ).filter(Car.id == car_id).first()
    return cars

def delete_car_by_id(db: Session, user_id: int, car_id: int):
    car = db.query(Car).filter(
        Car.user_id == user_id
        ).filter(Car.id == car_id).first()
    if car:
        db.delete(car)
        db.commit()
    return car

def update_user_car(db: Session, car_details: Union[UpdateCar, Dict[str, Any]],
                     user_id: int, car_id : int):
    car = db.query(Car).filter(
        Car.user_id == user_id
        ).filter(Car.id == car_id).first()
    if not car:
        return car
    car_data = jsonable_encoder(car)
    if isinstance(car_details, dict):
        update_data = car_details
    else:
        update_data = car_details.dict(exclude_unset=True)
    for field in car_data:
        if field in update_data:
            setattr(car, field, update_data[field])
    db.add(car)
    db.commit()
    db.refresh(car)
    return car