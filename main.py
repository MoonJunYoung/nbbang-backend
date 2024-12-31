import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from meeting.presentation import MeetingPresentation
from member.presentation import MemberPresentation
from payment.presentation import PaymentPresentation
from user.presentation import UserPresentation

app = FastAPI()


# origins = ["https://nbbang.life"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
#     allow_headers=["Authorization"],
#     expose_headers=["Location"],
# )


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/", status_code=200)
def haelth_check():
    return True


app.include_router(UserPresentation.router)
app.include_router(MeetingPresentation.router)
app.include_router(MemberPresentation.router)
app.include_router(PaymentPresentation.router)


if __name__ == "__main__":
    if os.environ.get("SERVICE_ENV") == "dev":
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000)
