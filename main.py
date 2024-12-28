from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from meeting.presentation import MeetingPresentation
from member.presentation import MemberPresentation
from payment.presentation import PaymentPresentation
from pydantic import BaseModel
from user.presentation import UserPresentation

app = FastAPI()


origins = ["https://nbbang.life"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization"],
    expose_headers=["Location"],
)


@app.get("/", status_code=200)
def haelth_check():
    return "haelth_check"


class LogData(BaseModel):
    data: str


@app.post("/api/log", status_code=201)
def print_log(log_data: LogData):
    print(log_data)


app.include_router(UserPresentation.router)
app.include_router(MeetingPresentation.router)
app.include_router(MemberPresentation.router)
app.include_router(PaymentPresentation.router)
