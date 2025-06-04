from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.userRouter import user_router
from router.hubRouter import hub_router
from router.requestRouter import request_router
from router.faceRouter import face_router
from router.imageRouter import image_router
from router.authRouter import auth_router

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:5173",
    "https://campus-face.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)









@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API is up and running"}

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(hub_router, prefix="/hub", tags=["Hub"])
app.include_router(image_router, prefix="/image", tags=["Image"])
app.include_router(face_router, prefix="/face", tags=["Face"])
app.include_router(request_router, prefix="/request", tags=["Request"])








