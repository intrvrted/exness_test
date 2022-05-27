import os
from time import strftime as getTime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import generate_latest, Counter

counter = Counter('http_requests_total', 'HTTP requests', ['method', 'endpoint'])

enableDb = os.getenv("SQLITE", 'False').lower() in ('true', '1', 't')

if enableDb:
    import db_support as db
else:
    import logging
    fileName = getTime('webServer_%Y-%m-%d.log')
    logging.basicConfig(filename = f"log/{fileName}",
                        encoding = 'utf-8',
                        level = logging.INFO,
                        format = '%(message)s: %(asctime)s',
                        datefmt = '%H:%M:%S - %d.%m.%Y',
                        force = True)


class User(BaseModel):
    name: str


app = FastAPI()


@app.get("/hello")
async def hello():
    counter.labels('GET', '/hello').inc()
    return {"Hello Page"}

@app.get("/user")
async def getUser(name: str):
    counter.labels('GET', '/user').inc()
    if enableDb:
        try:
            query = db.users.select().with_only_columns([db.users.c.name, db.users.c.time]).where(db.users.c.name == f'{name}')
            return await db.database.fetch_all(query)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"{e}")
    if enableDb == False:
        return {"GET /user: Enable DB support by setting SQLITE env variable to True"}

@app.post("/user", status_code=204)
async def postUser(user: User):
    counter.labels('POST', '/user').inc()
    if enableDb == False:
        logging.info(user.name)
    if enableDb:
        try:
            userTime = getTime('%H:%M:%S - %d.%m.%Y')
            query = db.users.insert().values(name = user.name, time = userTime)
            last_record_id = await db.database.execute(query)
            return {"id": last_record_id, **user.dict()}
        except Exception as e:
            raise HTTPException(status_code = 409, detail = f"User {user.name} already exists. {e}")

@app.get("/metrics")
def requests_count():
    data = generate_latest(counter)
    return {data}
