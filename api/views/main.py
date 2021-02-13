from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware


from   route import router
from db_session import database_instance

app = FastAPI()

""""
origins = [
    #add the localhost
    "http://127.0.0.1:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.app.state.db = database_instance
    response = await call_next(request)
    return response

@app.on_event("startup")
async def startup():
    await database_instance.connect()
    app.state.db = database_instance


app.include_router(router)

