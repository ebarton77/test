#!/usr/bin/env python3
import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import boto3
import requests

app = FastAPI()


# Model data you are expecting.
# Set defaults, data types, etc.
class Item(BaseModel):
    description: Optional[str] = None


@app.get("/")  # zone apex
def read_root():
    return {"Hello": "wonderful DS3002 professor and TA", "Check": "My README file for how to use my API or type /docs to check out my endpoints"}


@app.get("/disney")
def get_temp():
    LAT="28.5383"
    LON="-81.3792"
    KEY="6e3313543740951245a1a23b5a7d2491"
    units="Fahrenheit"
    url="https://api.openweathermap.org/data/2.5/weather?lat=" +LAT+"&lon=" + LON+"&appid=" + KEY
    response=requests.get(url)
    current=response.json()['main']['temp']
    current= round((int(current) *1.8 )- 459.67,2)
    feels = response.json()['main']['feels_like']
    feels=round((int(feels) *1.8 )- 459.67,2)
    description=response.json()['weather'][0]['description']
    return {"Current Disney Temp": current, "Feels Like": feels, "Units": units, "Description": description}

@app.get("/cville")
def get_temp():
    LAT="38.0293"
    LON="-78.4767"
    KEY="6e3313543740951245a1a23b5a7d2491"
    units="Fahrenheit"
    url="https://api.openweathermap.org/data/2.5/weather?lat=" +LAT+"&lon=" + LON+"&appid=" + KEY
    response=requests.get(url)
    current=response.json()['main']['temp']
    current= round((int(current) *1.8 )- 459.67,2)
    feels = response.json()['main']['feels_like']
    feels=round((int(feels) *1.8 )- 459.67,2)
    description=response.json()['weather'][0]['description']
    return {"Current C-ville Temp": current, "Feels Like": feels, "Units": units, "Description": description}

@app.get("/weather/{zip_code}")
def get_temp2(zip_code:int, country_code:str,units:str,lang:str, max_min_temp: bool):
    API_KEY="6e3313543740951245a1a23b5a7d2491"
    url="https://api.openweathermap.org/data/2.5/weather?zip=" +str(zip_code)+","+ str(country_code)+ "&appid=" + API_KEY +"&units=" +str(units)+ "&lang=" +str(lang)
    valid_units=["imperial", "standard", "metric"]
    valid_lang=[ "af","al", "ar","az","bg", "ca", "cz", "da", "de", "el", "en", "eu", "fa", "fi","fr", "gl", "he", "hi", "hr",
                 "hu", "id", "it", "ja", "kr", "la", "lt", "mk", "no", "nl", "pl", "pt", "pt_br", "ro", "ru", "sv", "sk", "sl",
                 "sp", "sr", "th", "tr", "ua", "uk", "vi", "zh_cn", "zh_tw", "zu"]
    if (len(country_code)>2):
        raise HTTPException(status_code=500, detail="Need to input a valid country code using two letters. A list of appropriate codes can be found in the country_codes.txt file")
    if (zip_code<10000):
        raise HTTPException(status_code=500, detail="Need to input a valid integer for the zip code")
    if (units not in valid_units):
        raise HTTPException(status_code=500, detail="You need to input a valid unit. The options are: standard, metric or imperial")
    if (lang not in valid_lang):
        raise HTTPException(status_code=500, detail="You need to input a valid language code. A list of appropriate codes can be found in the language_codes.txt")
    if (max_min_temp !=True) and (max_min_temp != False):
        raise HTTPException(status_code=500, detail="You need to input a boolean value of either true or false")
    response=requests.get(url)
    current=response.json()['main']['temp']
    feels = response.json()['main']['feels_like']
    description = response.json()['weather'][0]['description']
    max_temp=response.json()['main']['temp_max']
    min_temp=response.json()['main']['temp_min']
    if max_min_temp== True:
        return {"Current Temp in the " + str(zip_code) + " zip code": current, "Feels like": feels,
                "Description": description, "Maximum Temp":max_temp, "Minimum Temp":min_temp}
    return {"Current Temp in the "+str(zip_code) +" zip code": current, "Feels like": feels, "Description":description}
