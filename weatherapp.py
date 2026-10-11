from fastapi import FastAPI, Form, Request  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
import requests  # pyright: ignore[reportMissingModuleSource]
from mysql.connector import Connect # pyright: ignore[reportMissingImports]
from sqlalchemy import Column,String,Integer,Time ,Float,create_engine # pyright: ignore[reportMissingImports]
from sqlalchemy.ext.declarative import declarative_base # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import sessionmaker # pyright: ignore[reportMissingImports]
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
url="mysql+mysqlconnector://root:Pavani%40123@localhost:3306/Weather"
engine=create_engine(url)
LocalSession=sessionmaker(bind=engine,autoflush=False)
Base=declarative_base()
templates=Jinja2Templates(directory="templates")
class WeatherData(Base):
    __tablename__='Weather Data'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    name=Column(String(50),nullable=False)
    region=Column(String(30))
    country=Column(String(30))
    Time=Column(Time)
    Temperature_in_Celsius= Column(Float)
    Temperature_in_Fahrenheit=Column(Float)
    Condition=Column(String(20))
    feelslike=Column(Float)
    chanceofrain=Column(Integer)
    CO=Column(Float)
    PM2_5=Column(Float)
    PM10=Column(Float)

Base.metadata.create_all(bind=engine)

app=FastAPI()
@app.post('/')
def get_weather(location:str=Form()):
    query_parameters={
        'key':'c1f2a7ec66754b43bb892051260910',
        'q':location,
        'aqi':'yes'
    }
    response=requests.get('https://api.weatherapi.com/v1/current.json',params=query_parameters)
    print("STATUS:",response.status_code)
    print("RESPONSE:",response.text)
    db=LocalSession()
    data=response.json()
    name=data["location"]["name"]
    region=data["location"]["region"]
    country=data["location"]["country"]
    Time=data["location"]["localtime"]
    Temperature_in_Celsius=data['current']['temp_c']
    Temperature_in_Fahrenheit=data['current']['temp_f']
    Condition=data["current"]["condition"]['text']
    feelslike=data["current"]['feelslike_c']
    chanceofrain=data["current"]["chance_of_rain"]
    CO=data["current"]["air_quality"]["co"]
    PM2_5=data["current"]["air_quality"]["pm2_5"]
    PM10=data["current"]["air_quality"]["pm10"]
    weather_data=WeatherData(name=name,region=region,country=country,Time=Time,Temperature_in_Celsius=Temperature_in_Celsius,Temperature_in_Fahrenheit=Temperature_in_Fahrenheit,Condition=Condition,feelslike=feelslike,chanceofrain=chanceofrain,CO=CO,PM2_5=PM2_5,PM10=PM10)
    db.add(weather_data)
    db.commit()
    db.close()
    return response.json()
@app.get('/showweather',response_class=HTMLResponse)
def showtables(req:Request):
    db=LocalSession()
    results= db.query(WeatherData).all()
    db.close()
    return templates.TemplateResponse(request=req,name="weather.html",
                                      context={
                                          "data":results
                                      })
