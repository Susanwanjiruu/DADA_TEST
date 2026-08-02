from fastapi import FastAPI
from database import Base, engine
from app.routers import (
    registrations,
    avatars,
    games,
    game_progress,
    organisations,
    support_requests,
    admin_actions,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SHE++ API")

app.include_router(registrations.router)
app.include_router(avatars.router)
app.include_router(games.router)
app.include_router(game_progress.router)
app.include_router(organisations.router)
app.include_router(support_requests.router)
app.include_router(admin_actions.router)


@app.get("/")
def root():
    return {"message": "SHE++ API is running"}