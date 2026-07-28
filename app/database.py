from fastapi import FastAPI

import models
from database import Base, engine
from routers import registrations

Base.metadata.create_all(bind=engine)

app = FastAPI(title = 'DADASAFE API', version = "1.0" )

app.include_router(registrations.router)