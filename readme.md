# Arduino PI Weather API 
#### This page includes documentation for developing with the arduino weather station api 

Fetches All Weather Records
```http
GET /api/weather
```

Get the most recent weather forecasts
```http
GET /api/weather/recent
```

As of now there are only two arguments **begin** and **end**. These process the data only from the begin date to the **end** date.
```http
GET /api/weather?begin="2018-08-23 21:27:49"
GET /api/weather?end="2018-08-23 21:27:49"
GET /api/weather?begin="2018-08-22"&end="2018-08-24"
```
