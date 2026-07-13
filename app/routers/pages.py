from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.core.dependencies import (
    get_current_admin,
    get_current_user,
)
from app.services.movie_service import MovieService
from app.services.movie_session_service import MovieSessionService
from app.services.genre_service import GenreService
from app.services.hall_service import HallService
from app.services.booking_service import BookingService

router = APIRouter(tags=["Pages"])

templates = Jinja2Templates(directory="app/templates")


def require_login(request: Request, db: Session):
    try:
        return get_current_user(request, db)
    except HTTPException:
        return None


@router.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    db: Session = Depends(get_db),
):

    current_user = require_login(request, db)

    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    movies = MovieService(db).get_all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "movies": movies,
            "user": current_user,
        },
    )


@router.get("/movies", response_class=HTMLResponse)
def movies(
    request: Request,
    page: int = 1,
    db: Session =Depends(get_db),
):

    current_user = require_login(request, db)

    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    limit = 6
    skip = (page - 1) * limit

    service = MovieService(db)

    movies = service.get_all(skip=skip, limit=limit)
    total_movies = service.count()

    total_pages = (total_movies + limit - 1) // limit

    return templates.TemplateResponse(
        "movies.html",
        {
            "request": request,
            "movies": movies,
            "page": page,
            "total_pages": total_pages,
            "user": current_user,
        },
    )


@router.get("/movie/{movie_id}", response_class=HTMLResponse)
def movie_detail(
    movie_id: int,
    request: Request,
    db: Session = Depends(get_db),
):

    current_user = require_login(request, db)

    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    movie = MovieService(db).get_by_id(movie_id)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Фільм не знайдено",
        )

    sessions = MovieSessionService(db).get_by_movie(movie_id)

    return templates.TemplateResponse(
        "movie_detail.html",
        {
            "request": request,
            "movie": movie,
            "sessions": sessions,
            "user": current_user,
        },
    )


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
        },
    )


@router.get("/register", response_class=HTMLResponse)
def register(request: Request):

    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
        },
    )


@router.get("/booking/{session_id}", response_class=HTMLResponse)
def booking(
    session_id: int,
    request: Request,
    db: Session = Depends(get_db),
):

    current_user = require_login(request, db)

    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    session = MovieSessionService(db).get_by_id(session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Сеанс не знайдено",
        )

    return templates.TemplateResponse(
        "booking.html",
        {
            "request": request,
            "session": session,
            "user": current_user,
        },
    )


@router.get("/payment/{booking_id}", response_class=HTMLResponse)
def payment(
    booking_id: int,
    request: Request,
    db: Session = Depends(get_db),
):

    current_user = require_login(request, db)

    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    booking = BookingService(db).get_booking(booking_id)

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Бронювання не знайдено",
        )

    return templates.TemplateResponse(
        "payment.html",
        {
            "request": request,
            "booking": booking,
            "user": current_user,
        },
    )


@router.get("/profile", response_class=HTMLResponse)
def profile(
    request: Request,
    db: Session = Depends(get_db),
):

    current_user = require_login(request, db)

    if current_user is None:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": current_user,
            "tickets": current_user.tickets,
        },
    )


@router.get("/admin", response_class=HTMLResponse)
def admin(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):

    movies = MovieService(db).get_all()
    genres = GenreService(db).get_all()
    halls = HallService(db).get_all()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "movies": movies,
            "genres": genres,
            "halls": halls,
            "user": current_user,
        },
    )