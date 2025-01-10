DA
https://chatgpt.com/c/6780fb75-e9f0-8012-b8ac-7475ce8e975b

 html javasript autokauppa sivu joka toimii live server, 

adminille kirjatumine ja admin voi muokata autoja edit.html ja admin voi siis lisätä/poistaa/muokata autoja. kun admin kirjatuu login.html se pääsee panel.html tiedostoon ja siellä on linkit add.html(voi lisätä autoja), edit.html(valikko josta voi valita muokattavan auton),  admincarinfo.html eli adminin autolistaan jossa on lista myytävistä autoisat ja on muokkaus nappi jossa aukeaa id:n perusteella edit.html.

index.html on valikko josta voi avata autolistan eli cars.html tiedoston ja index sivulla on haku kenttä josta voi hakea autoja ja rajata tietojen perusteella. carinfo.html tiedostoon avautuu id perusteella auton tiedot
, autojen tiedot ovat .json tiedotossa: 
tässä yhden auton tiedot 
{ 
    "cars": [
{
    "id": 1,
    "status"": "" (sale, inaccessible, sold, coming)
    "make": "Toyota",
    "model": "Corolla",
    "exact_model": "E210 GR Corolla"
    "year": 2020,
    "price": 17900,
    "mileage": 35000,
    "condition": "Good",
    "color": "Silver",
    "engine": {
      "type": "1.8L 4-Cylinder",
      "horsepower": 132,
      "fuel_type": "Gasoline"
    },
    "transmission": "Automatic",
    "features": [
      "Air Conditioning",
      "Navigation System",
      "Rearview Camera",
      "Bluetooth",
      "Apple CarPlay",
      "Lane Departure Warning",
      "Keyless Entry",
      "Cruise Control"
    ],
    "safety_features": [
      "ABS Brakes",
      "Traction Control",
      "Side-Impact Airbags",
      "Blind Spot Monitoring",
      "Parking Sensors"
    ],
    "service_history": [
      {
        "date": "2023-05-10",
        "description": "Oil Change and Tire Rotation",
        "service_center": "Toyota Service Center"
      },
      {
        "date": "2022-11-15",
        "description": "Brake Pad Replacement",
        "service_center": "Toyota Service Center"
      }
    ],
    "ownership_history": [
      {
        "owner": 1,
        "purchase_date": "2020-06-01",
        "sale_date": "2023-04-15",
        "reason_for_sale": "Upgraded to a new model"
      }
    ],
    "warranty": {
      "duration": "5 years",
      "coverage": "Basic Warranty",
      "remaining_years": 2
    },
    "location": {
      "dealership": "Car Dealership ABC",
      "address": "Street Address 123, 00100 Helsinki",
      "contact": "+358 123 456 789"
    },
    "image": "https://www.example.com/images/toyota_corolla_2020.jpg"
  }
]
}