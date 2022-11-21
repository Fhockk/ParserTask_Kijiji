## About
- This application was created as a result of a final test task
- The purpose of the application is to collect all ads from the site

## Technical Requirements
- Code must be asynchronous and stable: aiohttp, asyncio
- There shouldn't be duplicated records
- App must scrape info as quickly as possible: rabbitmq

## First:
```shell
git clone https://github.com/Fhockk/ParserTask_Kijiji.git
```

## How to run this with Docker?
- Make sure you have docker installed and runninng on your machine
- Open the terminal to the docker-compose path and hit the following command -

```shell
docker-compose up --build
```

Some waiting.. And then open browser, go to [localhost](https://localhost)

Endpoint which allow you to get information with filtering data by [sort_by_price](https://localhost/sort_by_price)

Endpoint which allow you to get information with filtering data by [sort_by_date](https://localhost/sort_by_date)

All points from The Unit and Overview sections (API receive parameter name and
value True or False: [sort_by_hydro_and heat](https://localhost/sort/?hydro=True&heat=False) (for example)
