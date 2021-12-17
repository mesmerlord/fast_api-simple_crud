from pydantic import BaseModel, Field

class CarList(BaseModel):
    id : str = Field(..., example=12) 
    name : str = Field(..., example="TeslaMyEsla")
    model_name : str = Field(..., example="Toyota")
    created_at : str = Field(..., example="2021-12-17 09:41:44.212699")
    year_released : str = Field(..., example="2021")
    # user_id : str
    class Config:
        orm_mode = True

class CarCreate(BaseModel):
    name : str = Field(..., example="NoKia")
    model_name : str = Field(..., example="Kia")
    year_released : str = Field(..., example="2021")
    class Config:
        orm_mode = True

class UpdateCar(BaseModel):
    # Optional for partial updates
    name : str = None 
    model_name : str = None 
    year_released : str = None 