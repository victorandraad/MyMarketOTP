from fastapi import FastAPI
from app.endpoints import login, users, posts, verify_user

app = FastAPI()

app.include_router(login.router)
app.include_router(users.router)
app.include_router(verify_user.router)
app.include_router(posts.router, prefix='/post')