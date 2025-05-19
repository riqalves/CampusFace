from fastapi import FastAPI

from router.userRouter import user_router
from router.authRouter import auth_router
from router.hubRouter import hub_router

app = FastAPI()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API is up and running"}

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(hub_router, prefix="/hub", tags=["Hub"])








