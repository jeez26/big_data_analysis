import multiprocessing
import random
import string

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

import ssl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_random_string(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


@app.get("/server/data")
async def get_server_data(request: Request):
    print(request.headers)
    return {"message": "Server data!"}


@app.get("/server/data/{item_id}")
async def get_server_data(request: Request, item_id):
    print(item_id)
    return {"message": f'Data for {item_id=} is {get_random_string(16)}'}


@app.on_event("startup")
async def startup_event():
    ssl._create_default_https_context = ssl._create_unverified_context
    process_name = multiprocessing.current_process().name
    print(f'Process {process_name} started')
    print("Server started")
    print(f'Open Swagger - https://localhost:8000/docs')


@app.on_event("shutdown")
async def shutdown_event():
    print("Server shutting down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
        ssl_keyfile='./certificates/localhost.key',
        ssl_certfile='./certificates/localhost.crt',
    )
