from types import resolve_bases
from typing import Any, List, Union, Dict
from pg_db import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, Security
from schemas import user, car, token
from sqlalchemy.orm import Session
import crud
import models
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import Auth
import uvicorn


auth_handler = Auth()
security = HTTPBearer()

def get_db():
    print("getting db")
    db = SessionLocal()
    print("finished getting db")

    try:
        yield db
    finally:
        print("closing db")

        db.close()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redocs",
    title="Core API",
    description="New Framework of Python",
    version="2.0",
    openapi_url="/api/v1/openapi.json",
)

@app.post("/signup", response_model=user.UserCreated)
async def register_user(user_details: user.UserSignup , db: Session = Depends(get_db)):
    print("signing up db")
    
    db_user = crud.get_user_by_username(db = db, username = user_details.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db = db, user=user_details)

def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> models.User:
    token = credentials.credentials
    username = auth_handler.decode_token(token)
    if not (username):
        return 'Not Authorized'
    user = crud.get_user_by_username(db = db, username = username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/login")
async def login_user(user_details: user.UserLogin , db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db = db, username = user_details.username)
    if (user is None):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if (not auth_handler.verify_password(user_details.password, user.password)):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return crud.login(user_details)

@app.post('/refresh_token', response_model= token.LoginToken)
def refresh_token(refresh_token : token.RefreshToken):
    new_tokens = auth_handler.refresh_token(refresh_token.refresh_token)
    return new_tokens

@app.get('/cars/', response_model = List[car.CarList])
def get_cars(db: Session = Depends(get_db),
             current_user: models.User= Depends(get_current_user),
             
            ):
    cars = crud.get_cars_by_user(db = db, user_id = current_user.id)
    return cars

@app.get('/cars/{id}', response_model = car.CarList)
def get_cars(
        id : int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
        ):

    car = crud.get_car_by_id(db = db, user_id = current_user.id,
            car_id = id)
    if not car:
        raise HTTPException(status_code=404, detail="No Car with given ID")
    return car


@app.post('/cars/add', response_model = car.CarCreate)
def add_car(car_details : car.CarCreate, db: Session = Depends(get_db),
             current_user: models.User= Depends(get_current_user),
            ):
    car = crud.create_user_car(db = db, car_details = car_details,
                     user_id = current_user.id)
    return car

@app.delete('/cars/{id}', response_model = car.CarList)
def delete_car(
        id : int,
        db: Session = Depends(get_db),
        current_user: models.User= Depends(get_current_user),
        ):
    car = crud.delete_car_by_id(db = db, user_id = current_user.id,
            car_id = id)
    if not car:
        raise HTTPException(status_code=404, detail="No Car with given ID")
    return car

@app.put('/cars/{id}', response_model = car.CarList)
def update_car(
        id : int,
        car_details: Union[car.UpdateCar, Dict[str, Any]],
        db: Session = Depends(get_db),
        current_user: models.User= Depends(get_current_user),
        ):
    car = crud.update_user_car(db = db, user_id = current_user.id,
            car_id = id, car_details = car_details)
    if not car:
        raise HTTPException(status_code=404, detail="No Car with given ID")
    return car


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)