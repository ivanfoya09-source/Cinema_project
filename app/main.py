from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from app.routers import reservation

# Routers
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.genres import router as genres_router
from app.routers.movies import router as movies_router
from app.routers.halls import router as halls_router
from app.routers.movie_sessions import router as sessions_router
from app.routers.bookings import router as bookings_router
from app.routers.tickets import router as tickets_router
from app.routers.pages import router as pages_router
from app.routers import upload
from app.routers.admin import router as admin_router
from app.routers import payment


app = FastAPI(title="Cinema API",version="1.0.0",description="Cinema website built with FastAPI")

@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc: HTTPException):
    return RedirectResponse(
        url="/login",
        status_code=303,
    )

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

app.include_router(pages_router)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(genres_router)
app.include_router(movies_router)
app.include_router(halls_router)
app.include_router(sessions_router)
app.include_router(bookings_router)
app.include_router(tickets_router)
app.include_router(reservation.router)
app.include_router(upload.router)
app.include_router(admin_router)
app.include_router(payment.router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Cinema API is running"
    }