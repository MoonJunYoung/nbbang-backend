import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum

from meeting.presentation import MeetingPresentation
from member.presentation import MemberPresentation
from payment.presentation import PaymentPresentation
from user.presentation import UserPresentation

load_dotenv()
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.options("/{rest_of_path:path}")
async def preflight(rest_of_path: str, request: Request):
    return JSONResponse(
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Expose-Headers": "*",
        }
    )


@app.get("/", status_code=200)
def haelth_check():
    return True


app.include_router(UserPresentation.router)
app.include_router(MeetingPresentation.router)
app.include_router(MemberPresentation.router)
app.include_router(PaymentPresentation.router)

SERVICE_ENV = os.environ.get("SERVICE_ENV")

handler = Mangum(app)

if __name__ == "__main__" and SERVICE_ENV == "dev":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
