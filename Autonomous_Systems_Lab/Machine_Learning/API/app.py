from sre_parse import State
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sklearn.tree import DecisionTreeClassifier
from sklearn.impute import SimpleImputer
import pandas as pd
from pydantic import BaseModel

# Creating FastAPI instance
app = FastAPI()

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# define custom OpenAPI schema


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Truck Platooning API",
        version="1.0.2",
        description="This is the OpenAPI schema of our truck platooning API. Thisb API is used to predict the number of trucks required to complete a given task.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# creating class to define the request body
# and the type hints of each attribute


class request_body(BaseModel):
    TruckName: str
    Distance_Covered: int
    Match_of_Route: int
    Fuel_Consumption: int
    Body_Characteristics: int
    Equipment_Sensors: int
    Efficiency: int
    TruckName2: str
    Distance_Covered2: int
    Match_of_Route2: int
    Fuel_Consumption2: int
    Body_Characteristics2: int
    Equipment_Sensors2: int
    Efficiency2: int
    TruckName3: str
    Distance_Covered3: int
    Match_of_Route3: int
    Fuel_Consumption3: int
    Body_Characteristics3: int
    Equipment_Sensors3: int
    Efficiency3: int


# Loading Dataset
truckData = pd.read_csv("truckData.csv")

df = pd.DataFrame(truckData)

# Header
names = ['Distance_Covered', 'Match_of_Route', 'Fuel_Consumption',
         'Body_Characteristics', 'Equipment_Sensors', 'Efficiency', 'Rating']

X, Y = df.iloc[:, :-1], df.iloc[:, [-1]]

# Creating and Fitting our Model
clf = DecisionTreeClassifier()
clf.fit(X, Y)

# Creating an Endpoint to receive the data
# to make prediction on.


@app.post('/predict')
def predict(data: request_body):

    # Making the data in a form suitable for prediction
    test_data = [[
        data.Distance_Covered,
        data.Match_of_Route,
        data.Fuel_Consumption,
        data.Body_Characteristics,
        data.Equipment_Sensors,
        data.Efficiency
    ]]
    test_data2 = [[
        data.Distance_Covered2,
        data.Match_of_Route2,
        data.Fuel_Consumption2,
        data.Body_Characteristics2,
        data.Equipment_Sensors2,
        data.Efficiency2
    ]]
    test_data3 = [[
        data.Distance_Covered3,
        data.Match_of_Route3,
        data.Fuel_Consumption3,
        data.Body_Characteristics3,
        data.Equipment_Sensors3,
        data.Efficiency3
    ]]

    # Making the prediction
    result1 = clf.predict(test_data)[0]
    result2 = clf.predict(test_data2)[0]
    result3 = clf.predict(test_data3)[0]

    # Map the prediction to the rating
    rating1 = 0
    rating2 = 0
    rating3 = 0

    if result1 == 'Highest':
        rating1 = 4
    elif result1 == 'High':
        rating1 = 3
    elif result1 == 'low':
        rating1 = 2
    elif result1 == 'lowest':
        rating1 = 1
    else:
        rating1 = 0

    if result2 == 'Highest':
        rating2 = 4
    elif result2 == 'High':
        rating2 = 3
    elif result2 == 'low':
        rating2 = 2
    elif result2 == 'lowest':
        rating2 = 1
    else:
        rating2 = 0

    if result3 == 'Highest':
        rating3 = 4
    elif result3 == 'High':
        rating3 = 3
    elif result3 == 'low':
        rating3 = 2
    elif result3 == 'lowest':
        rating3 = 1
    else:
        rating3 = 0

    # Return the max rating
    if (rating1 >= rating2) and (rating1 >= rating3):
        return data.TruckName + ' ' + ':' + ' ' + result1
    elif (rating2 >= rating1) and (rating2 > rating3):
        return data.TruckName2 + ' ' + ':' + ' ' + result2
    elif (rating3 >= rating1) and (rating3 >= rating2):
        return data.TruckName3 + ' ' + ':' + ' ' + result3
    else:
        return data.TruckName + ' '+ ':' + ' ' + result1


app.openapi = custom_openapi
