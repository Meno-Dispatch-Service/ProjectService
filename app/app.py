from fastapi import FastAPI
from services.project.router import project_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Meno Disptach Project Service API V1")


app.include_router(project_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
