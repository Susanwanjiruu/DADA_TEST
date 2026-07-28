from fastapi import FastAPI

import models
from database import Base, engine
from routers import products

Base.metadata.create_all(bind=engine)

app = FastAPI(title = 'DADASAFE API', version = "1.0" )

app.include_router(products.router)