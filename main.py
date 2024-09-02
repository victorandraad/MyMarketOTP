from fastapi import FastAPI, Request
from app.endpoints import login, users, posts, verify_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para o domínio correto em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=r"app/resources/views")

app.include_router(login.router)
app.include_router(users.router)
app.include_router(verify_user.router)
app.include_router(posts.router, prefix='/post')

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})